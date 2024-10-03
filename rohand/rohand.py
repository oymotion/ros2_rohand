#!/usr/bin/env python3

import threading
import time
import rclpy
from rclpy.node import Node
import rclpy.node
from sensor_msgs.msg import JointState

#from pymodbus import FramerType
from pymodbus.client import ModbusSerialClient
from pymodbus import ModbusException

from common.roh_registers_v1 import *

FRAME_ID_PREFIX = 'rohand_'


class ROHandNode(Node):

    def __init__(self):
        super().__init__('rohand_node')
        self.bus_mutex = threading.Lock()

        self.get_logger().info("node %s init.." % self.get_name())

        self.declare_parameters(
            namespace='',
            parameters=[
                ('port_name', rclpy.Parameter.Type.STRING),
                ('baudrate', rclpy.Parameter.Type.INTEGER),
                ('hand_ids', rclpy.Parameter.Type.INTEGER_ARRAY)
            ]
        )

        self.port_name_ = self.get_parameter_or('port_name', "/dev/ttyUSB0")
        self.baudrate_ = self.get_parameter_or('baudrate', 115200)
        self.hand_ids_ = self.get_parameter_or('hand_ids', [2])
        self.get_logger().info("port: %s, baudrate: %d, hand_ids: %s" % (self.port_name_, self.baudrate_, str(self.hand_ids_)))

        # 创建并初始化发布者成员属性pub_joint_states_
        self.joint_states_subscriber_ = self.create_subscription(msg_type=JointState, topic="~/target_joint_states", callback=self._joint_states_callback, qos_profile=10)

        # 创建并初始化发布者成员属性pub_joint_states_
        self.joint_states_publisher_ = self.create_publisher(msg_type=JointState, topic="~/current_joint_states", qos_profile=10)

        # 初始化数据
        #self._init_joint_states()
        self.pub_rate = self.create_rate(30)

	# Initialize modbus 
        self.modbus_client_ = ModbusSerialClient(port=self.port_name_, baudrate=self.baudrate_)
        self.modbus_client_.connect()

        self.thread_ = threading.Thread(target=self._thread_pub)
        self.thread_.start()


    #def _init_joint_states(self):
        #self.joint_states = JointState()
    
        #self.joint_states.header.stamp = self.get_clock().now().to_msg()
        #self.joint_states.header.frame_id = ""
        #self.joint_states.name = ['thumb', 'index', 'middle', 'ring', 'little', 'thumb_rotation']
        #self.joint_states.position = [0, 0, 0, 0, 0, 0]
        #self.joint_states.velocity = [0, 0, 0, 0, 0, 0]
        #self.joint_states.effort = []


    def _joint_states_callback(self, msg):
        self.get_logger().info("I heard: %s" % msg)

        hand_id = int(msg.header.frame_id.replace(FRAME_ID_PREFIX, ''))

        if self.hand_ids_.index(hand_id) >= 0:
            # Set speed
            values = []

            for i in range(msg.velocity):
                values.append(int(msg.velocity[i]))
            try:
                self.bus_mutex.acquire
                wr = self.modbus_client_.write_register(ROH_FINGER_SPEED0, values, slave=hand_id)
                self.bus_mutex.release
            except ModbusException as exc:
                self.get_logger().error(f"ERROR: exception in pymodbus {exc}")
                # raise exc
                return

            if wr.isError():
                self.get_logger().error(f"ERROR: pymodbus write_register returned an error: ({wr})")
                # raise ModbusException(txt)
                return

            # 设置目标位置
            values = []

            for i in range(msg.position):
                values.append(int(msg.position[i] * 100))     # scale

            try:
                self.bus_mutex.acquire
                wr = self.modbus_client_.write_register(ROH_FINGER_ANGLE_TARGET0, values, slave=hand_id)
                self.bus_mutex.release
            except ModbusException as exc:
                self.get_logger().error(f"ERROR: exception in pymodbus {exc}")
                # raise exc
                return

            if wr.isError():
                self.get_logger().error(f"ERROR: pymodbus returned an error: ({wr})")
                # raise ModbusException(txt)
                return


    def _thread_pub(self):
        last_update_time = time.time()

        while rclpy.ok():
            delta_time = time.time() - last_update_time
            last_update_time = time.time()

            for hand_id in self.hand_ids_:
                joint_states = JointState()

                joint_states.header.stamp = self.get_clock().now().to_msg()
                joint_states.header.frame_id = FRAME_ID_PREFIX + str(hand_id)
                joint_states.name = ['thumb', 'index', 'middle', 'ring', 'little', 'thumb_rotation']

                # 读取当前位置
                try:
                    self.bus_mutex.acquire
                    rr = self.modbus_client_.read_holding_registers(ROH_FINGER_ANGLE0, count=6, slave=hand_id)
                    self.bus_mutex.release
                except ModbusException as exc:
                    self.get_logger().error(f"ERROR: exception in pymodbus {exc}")
                    # raise exc
                    time.sleep(1.0)
                    continue

                if rr.isError():
                    self.get_logger().error(f"ERROR: pymodbus read_holding_registers() returned an error: ({rr})")
                    # raise ModbusException(txt)
                else:
                    for i in range(len(rr.registers)):
                        joint_states.position.append(rr.registers[i] / 100)    # scale


                # TODO：读取当前速度
                joint_states.velocity = []

                # TODO: Read current forces
                joint_states.effort = []

                self.bus_mutex.release

                # 更新 header
                joint_states.header.stamp = self.get_clock().now().to_msg()

                # 发布关节数据
                self.joint_states_publisher_.publish(joint_states)

            self.pub_rate.sleep()


def main(args=None):
    rclpy.init(args=args)  # 初始化rclpy

    node = ROHandNode()  # 新建一个节点

    rclpy.spin(node)  # 保持节点运行，检测是否收到退出指令（Ctrl+C）
    node.destroy_node()
    rclpy.shutdown()  # 关闭rclpy

