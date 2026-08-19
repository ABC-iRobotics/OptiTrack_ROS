import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from rclpy.qos import QoSProfile, QoSDurabilityPolicy

class FakeBody(Node):
    def __init__(self):
        super().__init__('fake_body')
        
        # Transient Local
        qos_profile = QoSProfile(
            depth=10,
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL
        )
        
        self.pub = self.create_publisher(JointState, '/joint_states', qos_profile)
        self.timer = self.create_timer(0.1, self.timer_cb) 
        
        self.missing = [
            "left_hip_pitch_joint", "left_hip_roll_joint", "left_hip_yaw_joint", "left_knee_joint",
            "left_ankle_pitch_joint", "left_ankle_roll_joint", "right_hip_pitch_joint", "right_hip_roll_joint",
            "right_hip_yaw_joint", "right_knee_joint", "right_ankle_pitch_joint", "right_ankle_roll_joint",
            "waist_yaw_joint", "waist_roll_joint", "waist_pitch_joint", "left_shoulder_pitch_joint",
            "left_shoulder_roll_joint", "left_shoulder_yaw_joint", "left_elbow_joint", "left_wrist_roll_joint",
            "left_wrist_pitch_joint", "left_wrist_yaw_joint", "left_hand_index_0_joint", "left_hand_index_1_joint",
            "left_hand_middle_0_joint", "left_hand_middle_1_joint", "left_hand_thumb_0_joint",
            "left_hand_thumb_1_joint", "left_hand_thumb_2_joint"
        ]

    def timer_cb(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.missing
        msg.position = [0.0] * len(self.missing)
        msg.velocity = [0.0] * len(self.missing)
        msg.effort = [0.0] * len(self.missing)
        self.pub.publish(msg)

def main():
    rclpy.init()
    node = FakeBody()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()