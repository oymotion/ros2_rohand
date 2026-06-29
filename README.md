# Package ROHand

Nodes for ROHand. One bus, i.e. one port need one node.

## 1. Preparation

### 1.1. Install PCAN-Linux-Driver

Download from https://www.peak-system.com/fileadmin/media/linux/index.php

```bash
tar -xzf peak-linux-driver-8.20.0.tar.gz
cd peak-linux-driver-8.20.0
sudo make && sudo make install
```

### 1.2. Install PCAN-Basic lib

Download from https://www.peak-system.com/PCAN-Basic-Linux.433.0.html?&L=1

```BASH
tar -xzf PCAN-Basic_Linux-4.10.0.4.tar.gz
cd PCAN-Basic_Linux-4.10.0.4/libpcanbasic/pcanbasic
make clean
sudo make && sudo make install
```

### 1.3. Install python-can

```BASH
cd /path/to/workspace  # Should be ~/ros2_ws/src

# Create a vertual env for python
virtualenv -p python3 ./venv

# Make sure that colcon doesn’t try to build the venv
touch ./venv/COLCON_IGNORE

# Activate
source ./venv/bin/activate

# Install python module
python3 -m pip install -e .

Edit `~/bashrc` and add virtual env lib path to PYTHONPATH

```BASH
export PYTHONPATH=$PYTHONPATH:~/ros2_ws/src/venv/lib/python3.12/site-packages  # Modify python3.12 to your actual version
source ~/.bashrc
```

## 2. Clone

```BASH
cd ~
mkdir -p ros2_ws/src
cd ros2_ws/src
git clone ssh://git@github.com/oymotion/rohand_ros2_pkg
```

## 3. Compile

```BASH
cd /path/to/workspace
colcon build
```

### 3.1. Install requirements

```BASH
cd /path/to/workspace/rohand_ros2_pkg
pip3 install -r requirements.txt
```

## 4. Node rohand_can_serial

ROHand node for SerialCtrl Protocol, Dual Protocol is NOT supported. Please confirm protocol type in OHandSetting.
Listens to topic 'target_joint_state' and controls ROHand, reads current joint state and publish to 'current_joint_state'.

### 4.1 Topics

| Topic                 | Description                                                                              |
| --------------------- | ---------------------------------------------------------------------------------------- |
| "current_joint_state" | current joint state in message type JointState, frame_id in header distinguishes hand id |
| "target_joint_state"  | target joint state in message type JointState, frame_id in header distinguishes hand id  |
| "finger_state"        | finger status in message type UInt8MultiArray                                            |

### 4.2 Run

```BASH
# Prepare package
source install/setup.bash

# Run ROH-LiteS001 node
ros2 run rohand rohand_can_serial_lites001

# Or parse parameters:

ros2 run rohand rohand_can_serial_lites001 --ros-args -p baudrate:=1000000 -p hand_ids:=[2,3] -p master_ids:=[1,4]  # Modify parameters according to your real case

#Run ROH-ap001 node
ros2 run rohand rohand_can_serial_ap001 --ros-args -p baudrate:=1000000 -p hand_ids:=[2,3] -p master_ids:=[1,4]  # Modify parameters according to your real case

#Run ROH-a001 node
ros2 run rohand rohand_can_serial_a001 --ros-args -p baudrate:=1000000 -p hand_ids:=[2,3] -p master_ids:=[1,4]  # Modify parameters according to your real case
```

Finger status code:

| Name                 | Code  | Description                |
| -------------------- | :---: | -------------------------- |
| STATUS_OPENING       |   0   | Spreading                  |
| STATUS_CLOSING       |   1   | Grasping                   |
| STATUS_POS_REACHED   |   2   | Position reached stop      |
| STATUS_OVER_CURRENT  |   3   | Current protection stop    |
| STATUS_FORCE_REACHED |   4   | Force control reached stop |
| STATUS_STUCK         |   5   | Motor stuck stop           |

## 5. Node rohand_modbus

ROHand node for ModBus-RTU or ModBus-RTU & SerialCtrl Dual Protocol. Please confirm protocol type in OHandSetting.
Listens to topic 'target_joint_state' and controls ROHand, reads current joint state and publish to 'current_joint_state'.

### 5.1 Topics

| Topic                 | Description                                                                              |
| --------------------- | ---------------------------------------------------------------------------------------- |
| "current_joint_state" | current joint state in message type JointState, frame_id in header distinguishes hand id |
| "target_joint_state"  | target joint state in message type JointState, frame_id in header distinguishes hand id  |

### 5.2 Run

```BASH
# Prepare package
source /path/to/workspace/install/bash

# Insert USB-485 module to USB port then add permission to users
# Run following command every time you plug in your USB-485 module
sudo chmod o+rw /dev/ttyUSB0  # Modify ttyUSB0 to your actual device name

# Run ROHand node according to your type
#
# Run ROH-A001 node
ros2 run rohand rohand_modbus_a001 --ros-args -p port_name:="/dev/ttyUSB0" -p baudrate:=115200 -p hand_ids:=[2]  # Modify parameters according to your real case

# Run ROH-AP001 node
ros2 run rohand rohand_modbus_ap001 --ros-args -p port_name:="/dev/ttyUSB0" -p baudrate:=115200 -p hand_ids:=[2]  # Modify parameters according to your real case

# Run ROH-LiteS001 node
ros2 run rohand rohand_modbus_lites001 --ros-args -p port_name:="/dev/ttyUSB0" -p baudrate:=115200 -p hand_ids:=[2]  # Modify parameters according to your real case
```

## 6. Node rohand_serial

ROHand node for SerialCtrl Protocol, Dual Protocol is NOT supported. Please confirm protocol type in OHandSetting.
Listens to topic 'target_joint_state' and controls ROHand, reads current joint state and publish to 'current_joint_state'.

### 6.1 Topics

| Topic                 | Description                                                                              |
| --------------------- | ---------------------------------------------------------------------------------------- |
| "current_joint_state" | current joint state in message type JointState, frame_id in header distinguishes hand id |
| "target_joint_state"  | target joint state in message type JointState, frame_id in header distinguishes hand id  |
| "finger_state"        | finger status in message type UInt8MultiArray                                            |

### 6.2 Run

```BASH
# Prepare package
source /path/to/workspace/install/bash

# Insert USB-485 module to USB port then add permission to users
# Run following command every time you plug in your USB-485 module
sudo chmod o+rw /dev/ttyUSB0  # Modify ttyUSB0 to your actual device name

# Run ROHand node according to your type
#
# Run ROH-A001 node
ros2 run rohand rohand_serial_a001 --ros-args -p port_name:="/dev/ttyUSB0" -p baudrate:=115200 -p hand_ids:=[2]  # Modify parameters according to your real case

# Run ROH-AP001 node
ros2 run rohand rohand_serial_ap001 --ros-args -p port_name:="/dev/ttyUSB0" -p baudrate:=115200 -p hand_ids:=[2]  # Modify parameters according to your real case

# Run ROH-LiteS001 node
ros2 run rohand rohand_serial_lites001 --ros-args -p port_name:="/dev/ttyUSB0" -p baudrate:=115200 -p hand_ids:=[2]  # Modify parameters according to your real case
```

Finger status code:

| Name                 | Code  | Description                |
| -------------------- | :---: | -------------------------- |
| STATUS_OPENING       |   0   | Spreading                  |
| STATUS_CLOSING       |   1   | Grasping                   |
| STATUS_POS_REACHED   |   2   | Position reached stop      |
| STATUS_OVER_CURRENT  |   3   | Current protection stop    |
| STATUS_FORCE_REACHED |   4   | Force control reached stop |
| STATUS_STUCK         |   5   | Motor stuck stop           |

## 7. Node rohand_teleop

Reads keys to modify target joint angles, then publish to 'target_joint_state'.

### 7.1 Topics

| Topic                | Description                                                                             |
| -------------------- | --------------------------------------------------------------------------------------- |
| "target_joint_state" | target joint state in message type JointState, frame_id in header distinguishes hand id |

### 7.2 Run

```BASH
# Prepare package
source /path/to/workspace/install/bash

# Run ROH-a001 node
ros2 run rohand rohand_teleop_a001 --ros-args -r rohand_teleop_node/target_joint_states:=/rohand_node/target_joint_states -p hand_id:=2  # Modify parameters according to your real case

# Run ROH-ap001 node
ros2 run rohand rohand_teleop_ap001 --ros-args -r rohand_teleop_node/target_joint_states:=/rohand_node/target_joint_states -p hand_id:=2  # Modify parameters according to your real case

# Run ROH-lites_001 node
ros2 run rohand rohand_teleop_lites001 --ros-args -r rohand_teleop_node/target_joint_states:=/rohand_node/target_joint_states -p hand_id:=2  # Modify parameters according to your real case
```

Press following keys to operate:

| key | Description            |
| --- | ---------------------- |
| q   | quit                   |
| z   | thumb bends by step    |
| a   | thumb relaxes by step  |
| x   | index bends by step    |
| s   | index relaxes by step  |
| c   | middle bends by step   |
| d   | middle relaxes by step |
| v   | ring bends by step     |
| f   | ring relaxes by step   |
| b   | little bends by step   |
| g   | little relaxes by step |
| n   | thumb rotation +step   |
| h   | thumb rotation -step   |

Step is range / 10.
