import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import math

def euler_from_quaternion(x, y, z, w):
    # (Ugyanaz az átalakító, mint eddig)
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = math.atan2(t0, t1)
    
    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = math.asin(t2)
    
    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = math.atan2(t3, t4)
    
    return roll_x, pitch_y, yaw_z

class G1DirectTeleop(Node):
    def __init__(self):
        super().__init__('g1_direct_teleop')
        
        # Létrehozunk egy Publisher-t a robot vezérlőjéhez!
        self.publisher_ = self.create_publisher(
            JointTrajectory, 
            '/right_control/joint_trajectory', 
            10)
            
        # Feliratkozunk a Motive adataira
        self.subscription = self.create_subscription(
            PoseStamped,
            '/vrpn/Szog/pose', 
            self.pose_callback,
            10)
            
        # Nagyon fontos: Itt meg kell adni a vezérelni kívánt jointok PONTOS nevét!
        # (Ezeket a robot dokumentációjából vagy RVizből lehet kinézni)
        self.joint_names = [
            'right_shoulder_pitch_joint', 
            'right_shoulder_roll_joint', 
            'right_shoulder_yaw_joint',
            'right_elbow_joint',
            'right_wrist_roll_joint',
            'right_wrist_pitch_joint',
            'right_wrist_yaw_joint'
        ]
        
        self.get_logger().info("DIRECT Orientációs követés elindítva! Mozgasd a Rigid Body-t.")

    def pose_callback(self, msg):
        self.get_logger().info("Adat beérkezett, azonnali mozgatás indul!")

        q = msg.pose.orientation
        roll, pitch, yaw = euler_from_quaternion(q.x, q.y, q.z, q.w)
        
        # Összerakjuk az üzenetet a motorvezérlőnek
        traj_msg = JointTrajectory()

        traj_msg.header.stamp = self.get_clock().now().to_msg()

        traj_msg.joint_names = self.joint_names
        
        point = JointTrajectoryPoint()
        
        # ITT LESZ A TESZT: Melyik szög hová kerül? 
        # Most csak a váll 3 motorjának adjuk oda a 3 szöget, a többi marad 0 (egyenes)
        point.positions = [
            pitch,  # váll pitch
            roll,   # váll roll
            yaw,    # váll yaw
            0.0,    # könyök
            0.0,    # csukló 1
            0.0,    # csukló 2
            0.0     # csukló 3
        ]
        
        # A vezérlő tudni akarja, mennyi idő alatt érjen oda. 
        # Mivel másodpercenként 120-szor jön adat, adunk neki egy pici időt (pl 0.1 mp)
        point.time_from_start.sec = 0
        point.time_from_start.nanosec = 100000000 
        
        traj_msg.points.append(point)
        
        # Parancs kiküldése azonnal!
        self.publisher_.publish(traj_msg)

def main(args=None):
    rclpy.init(args=args)
    node = G1DirectTeleop()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()