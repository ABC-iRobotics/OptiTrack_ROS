import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from pymoveit2 import MoveIt2
import math

def euler_from_quaternion(x, y, z, w):
    """
    Átalakítja a Quaterniont (Motive rotáció) Euler szögekké (Radián).
    """
    # Roll (X tengely körüli forgás)
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = math.atan2(t0, t1)
    
    # Pitch (Y tengely körüli forgás)
    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = math.asin(t2)
    
    # Yaw (Z tengely körüli forgás)
    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = math.atan2(t3, t4)
    
    return roll_x, pitch_y, yaw_z

class G1VectorTeleop(Node):
    def __init__(self):
        super().__init__('g1_vector_teleop')
        
        # Inicializáljuk a MoveIt2-t a hiányzó argumentumokkal
        self.moveit2 = MoveIt2(
            self, 
            "right_arm",             # Tervezési csoport neve (ellenőrizd, hogy ez-e az!)
            "pelvis",                # A robot alap koordináta-rendszere (amit az RViz-ben is láttunk)
            "right_wrist_yaw_link"   # A kar végpontja (end effector)
        )
        
        # Feliratkozás az OptiTrack adatokra - CSERÉLD KI a Rigid Body nevére!
        self.subscription = self.create_subscription(
            PoseStamped,
            '/vrpn/Szog/pose', 
            self.pose_callback,
            10)
            
        self.get_logger().info("Orientációs követés elindítva! Mozgasd a Rigid Body-t lassan.")

    def pose_callback(self, msg):
        self.get_logger().info("Adat beérkezettaz Optitrack-től!")

        # 1. Kinyerjük a quaternion rotációt (a pozíciót figyelmen kívül hagyjuk)
        q = msg.pose.orientation
        
        # 2. Átalakítjuk a rotációt motorok által értelmezhető szögekké (radián)
        roll, pitch, yaw = euler_from_quaternion(q.x, q.y, q.z, q.w)
        
        # 3. Összerakjuk a parancsot. 
        # A sorrend a G1 csuklóinak sorrendje: Váll(3) -> Könyök(1) -> Csukló(3)
        # Ideiglenesen a könyököt és a csuklót 0.0-n (egyenesen) hagyjuk.
        target_joint_positions = [
            pitch,  # right_shoulder_pitch_joint
            roll,   # right_shoulder_roll_joint
            yaw,    # right_shoulder_yaw_joint
            0.0,    # right_elbow_joint
            0.0,    # right_wrist_roll_joint
            0.0,    # right_wrist_pitch_joint
            0.0     # right_wrist_yaw_joint
        ]
        
        # 4. Küldés a robotnak. A MoveIt megtervezi és végrehajtja a kar mozgatását.
        self.moveit2.move_to_configuration(target_joint_positions)

def main(args=None):
    rclpy.init(args=args)
    node = G1VectorTeleop()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()