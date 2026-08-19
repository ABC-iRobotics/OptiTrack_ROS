# OptiTrack and ROS 2 Integration for Unitree G1 Humanoid Robot

This repository contains a real-time teleoperation framework that connects the OptiTrack optical motion capture system with the Unitree G1 humanoid robot via the ROS 2 network. This project was developed as part of a thesis work at the Antal Bejczy Center for Intelligent Robotics at Óbuda University.

## 🛠️ Technologies and Versions
* **OS:** Ubuntu 22.04.5 LTS (via WSL)
* **ROS Version:** ROS 2 Humble Hawksbill
* **OptiTrack Software:** Motive 2.2
* **Communication Protocol:** VRPN

## ⚙️ System Operation
The framework processes raw spatial Rigid Body data received from the OptiTrack system. Instead of the classic "Plan-Execute" motion planning, the system utilizes a velocity-based control approach built on the **MoveIt Servo** module. This solution converts the raw spatial data into real-time relative velocity vectors (Twist messages), enabling continuous, dynamic control at the robot arm's end-effector, secured by built-in collision checking.

## 📦 Dependencies
To run this package, you need to clone and build the following external ROS 2 packages in your workspace's `src` directory:

1. **vrpn_client_ros2** - For receiving VRPN data.
2. **Unitree-G1-MoveIt2-Arm-Manipulation** (https://github.com/sharan05032000/Unitree-G1-Movelt2-Arm-Manipulation) (Created by: Sharan Rabinson Mohanraj) - For Unitree G1 robot visualization and MoveIt simulation.
3. **pymoveit2** - For the MoveIt Python interface.

## 🚀 Installation and Usage

1. Create the ROS 2 workspace and clone this repository:
   ```bash
   mkdir -p ~/g1_ws/src
   cd ~/g1_ws/src
   git clone [https://github.com/ABC-iRobotics/OptiTrack_ROS.git](https://github.com/ABC-iRobotics/OptiTrack_ROS.git)

   ---

## 🚀 Running the Project

The project includes two different control approaches. You must open separate terminals for each step and run the commands provided.

### Approach 1: Direct Euler Control (First Solution)

**Terminal 1 - Start VRPN:**
```bash
nc -vz [your IP] 3883
colcon build --packages-select vrpn_listener
source install/setup.bash
ros2 launch vrpn_listener sync_entity_state.launch
```

**Terminal 2 - Start Virtual Simulation:**
```bash
cd ~/g1_ws
colcon build
source install/setup.bash
ros2 launch g1_arm demo.launch.py
```

**Terminal 3 - Control Node:**
```bash
cd ~/g1_ws
source install/setup.bash
ros2 launch g1_teleop direct_teleop
```

### Approach 2: MoveIt Servo Control (Second Solution)
**Terminal 1 - Start VRPN:**
```bash
nc -vz [your IP] 3883
colcon build --packages-select vrpn_listener
source install/setup.bash
ros2 launch vrpn_listener sync_entity_state.launch
```
**Terminal 2 - Start Virtual Simulation:**
```bash
cd ~/g1_ws
colcon build
source install/setup.bash
ros2 launch g1_arm demo.launch.py
```

**Terminal 3 - Fake Body Publisher:**
```bash
cd ~/g1_ws
source install/setup.bash
ros2 run g1_teleop fake_body
```

**Terminal 4 - Start MoveIt Servo:**
```bash
cd ~/g1_ws
source install/setup.bash
ros2 launch g1_teleop g1_servo.launch.py
```

**Terminal 5 - Servo Teleoperation Node:**
```bash
cd ~/g1_ws
source install/setup.bash
ros2 run g1_teleop servo_teleop
```

### Optional Debugging Terminals:
**Terminal 6: Joint status tracking

**Terminal 7: Servo status tracking 

**Terminal 8: Joint trajectory status tracking  

**Terminal 9: Visualize node graph using rqt_graph

