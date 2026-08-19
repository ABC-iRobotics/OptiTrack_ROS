import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, TwistStamped
from std_srvs.srv import Trigger
import time
from scipy.spatial.transform import Rotation as R

class G1ServoTeleop(Node):

    is_servo_started = False

    def __init__(self):
        super().__init__('g1_servo_teleop')


        # INPUT FROM OPTITRACK
        self.subscription = self.create_subscription(
            PoseStamped,
            '/vrpn/Szog/pose', 
            self.vrpn_callback,
            10)
            
        # OUTPUT TO MOVEIT SERVO
        self.servo_pub = self.create_publisher(
            TwistStamped, 
            '/servo_node/delta_twist_cmds', 
            10)
        
        self.start_servo = self.create_client(
            Trigger,
            '/servo_node/start_servo',
        )

        starter_available = self.start_servo.wait_for_service(15)
        if not starter_available:
            self.get_logger().error('Servo node not found. Cannot start teleoperating.')
            exit()

        self.get_logger().info('Servo node started. Teleoperation is now available.')
            
        # VARIABLES TO MEASURE VELOCITY
        self.last_pose = None
        self.last_time = None
        
        self.get_logger().info("Relatív (Twist) Követés Indul! Mozgasd a Rigid Body-t.")

    def vrpn_callback(self, msg):
        if not self.is_servo_started:
            self.start_servo.call_async(Trigger.Request())
            self.is_servo_started = True
        
        current_time = time.time()
        
        # 1. SAVING THE FIRST DATA
        if self.last_pose is None:
            self.last_pose = msg.pose
            self.last_time = current_time
            self.get_logger().info("Bázis megvan, indulhat a mozgás!")
            return
        
            
        # MEASURING ELAPSED TIME (DELTA T)
        dt = current_time - self.last_time
        
        # SAFETY (IF 2 DATA IS COMING TOO FAST, WE DON'T WANT TO DIVIDE WITH ZERO)
        if dt < 0.005: 
            return
            
        # 2. MEASURING LINEAR VELOCITY
        vx = (msg.pose.position.x - self.last_pose.position.x) / dt
        vy = (msg.pose.position.y - self.last_pose.position.y) / dt
        vz = (msg.pose.position.z - self.last_pose.position.z) / dt
        
        # 3. MEASURING ANGULAR VELOCITY WITH SCIPY
        # KVATERNION DATA
        q_curr = [msg.pose.orientation.x, msg.pose.orientation.y, msg.pose.orientation.z, msg.pose.orientation.w]
        q_prev = [self.last_pose.orientation.x, self.last_pose.orientation.y, self.last_pose.orientation.z, self.last_pose.orientation.w]
        
        # CREATING SCIPY ROTATION OBJECT
        r_curr = R.from_quat(q_curr)
        r_prev = R.from_quat(q_prev)
        
        # RELATIVE DIFFERENCE BETWEEN THE 2 ROTATION
        r_diff = r_curr * r_prev.inv()
        
        # AXIS OF ROTATION AND ANGLE OF ROTATION IN (ANGULAR VELOCITY IN RAD/S)
        rot_vec = r_diff.as_rotvec() 
        
        wx = rot_vec[0] / dt
        wy = rot_vec[1] / dt
        wz = rot_vec[2] / dt
        
        # 4. COMMAND TO SERVO
        twist_msg = TwistStamped()
        twist_msg.header.stamp = self.get_clock().now().to_msg()
        twist_msg.header.frame_id = "pelvis" # A parancsot a robot testéhez (pelvis) viszonyítjuk
        
        # SCALING
        scale_linear = 1.0
        scale_angular = 1.0
        
        twist_msg.twist.linear.x = vx * scale_linear
        twist_msg.twist.linear.y = vy * scale_linear
        twist_msg.twist.linear.z = vz * scale_linear
        
        twist_msg.twist.angular.x = wx * scale_angular
        twist_msg.twist.angular.y = wy * scale_angular
        twist_msg.twist.angular.z = wz * scale_angular
        
        self.servo_pub.publish(twist_msg)
        
        # STATUS UPDATE
        self.last_pose = msg.pose
        self.last_time = current_time

def main(args=None):
    rclpy.init(args=args)
    node = G1ServoTeleop()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()