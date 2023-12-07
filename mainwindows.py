import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont

import constants
from data_query import Data_Query
from network_device import Network_Device
from network_matrix import Network_Matrix
from ui_mainwindows import Ui_MainWindow


class My_MainWindow(QtWidgets.QMainWindow):
    __pushButton_01_status: bool
    __pushButton_02_status: bool
    __pushButton_03_status: bool
    __pushButton_04_status: bool
    __pushButton_05_status: bool
    __pushButton_06_status: bool
    __pushButton_07_status: bool
    __pushButton_08_status: bool
    __network_device_flg: bool
    __network_matrix_flg: bool
    __device_control: Network_Device
    __matrix_control: Network_Matrix
    __count_times: int

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__ui = Ui_MainWindow()  # 创建UI对象
        self.__ui.setupUi(self)  # 构造UI

        # 网络连接状态位
        self.__network_device_flg = False
        self.__network_matrix_flg = False
        self._close_app = False

        self.init_device()

        self.init_matrix()

        # 初始化发送队列长度
        self.__send_data_query = Data_Query(constants.QUERY_LENGTH)

        self._net_status_01 = QtWidgets.QLabel()
        self._net_status_02 = QtWidgets.QLabel()

        # device 网络连接
        self.network_device_connect()

        # matrix 网络连接
        if constants.DEVICE_PORT != constants.MATRIX_PORT:
            self.network_matrix_connect()
        else:
            self.pop_error_info("设备服务器和矩阵服务器端口相同")
            self._net_status_02.setText("矩阵服务器未连接")
            self._net_status_02.setStyleSheet("color:#ff842c;")
            self.__ui.statusbar.addPermanentWidget(self._net_status_02)

        # 状态位数据显示方位
        self.__ui.statusbar.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        # 网络连接中断时，循环队列中所有不处理
        # 启动定时循环线程,间隔5s向循环队列中添加状态查询,同时判断只有队列为空时，才向其中添加查询状态指令
        # 启动定时循环线程，间隔300ms，先判断是否为空，有则取出队列中的数据将对应指令，通过串口服务器下发
        timer = QTimer(self)
        timer.timeout.connect(self.execute_code)
        timer.start(300)

    # >>>>>>>>>>>>>>>>>>>>>>>>>>> device control part <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # 初始化 device 控制部分
    def init_device(self):
        self.__count_times = 0  # 控制查询状态的间隔次数，从而控制间隔时间

        self.init_device_view_button_status()
        self.init_device_connect()

    # 初始化按键状态标志位
    def init_device_view_button_status(self):
        self.__pushButton_01_status = False
        self.__pushButton_02_status = False
        self.__pushButton_03_status = False
        self.__pushButton_04_status = False
        self.__pushButton_05_status = False
        self.__pushButton_06_status = False
        self.__pushButton_07_status = False
        self.__pushButton_08_status = False

    # 初始化槽
    def init_device_connect(self):
        self.__ui.pushButton_01.clicked.connect(self.on_pushbutton_1_click)
        self.__ui.pushButton_02.clicked.connect(self.on_pushbutton_2_click)
        self.__ui.pushButton_03.clicked.connect(self.on_pushbutton_3_click)
        self.__ui.pushButton_04.clicked.connect(self.on_pushbutton_4_click)
        self.__ui.pushButton_05.clicked.connect(self.on_pushbutton_5_click)
        self.__ui.pushButton_06.clicked.connect(self.on_pushbutton_6_click)
        self.__ui.pushButton_07.clicked.connect(self.on_pushbutton_7_click)
        self.__ui.pushButton_08.clicked.connect(self.on_pushbutton_8_click)

    # device 网络检查
    def network_device_connect(self):

        self.__device_control = Network_Device()
        if self.__device_control.connect(constants.SERVICE_IP, constants.DEVICE_PORT):
            self.__network_device_flg = True
            self._net_status_01.setText("设备服务器已连接")
            self._net_status_01.setStyleSheet("color:#2b2b2b;")

        else:
            self.__network_device_flg = False
            self._net_status_01.setText("设备服务器未连接")
            self._net_status_01.setStyleSheet("color:#ff842c;")
            self.pop_error_info("设备服务器：网络连接失败")
            return

        self.__ui.statusbar.addPermanentWidget(self._net_status_01)
        # 通过自定义槽函数与信号，对接收数据绑定
        self.__device_control.status_signal.connect(self.net_work_data_received)
        self.__device_control.network_connect_status.connect(self.device_net_work_status_received)

    # Qtimer 定时器触发操作
    def execute_code(self):
        self.push_status_cmd_into_array()
        self.send_data_from_array()

    # 用于定时循环中，将查询状态指令加入队列中
    def push_status_cmd_into_array(self):
        if not self.__network_device_flg:
            self.__count_times = 0
            return

        if self.__send_data_query.is_empty() and self.__count_times >= 15:
            self.__send_data_query.push(constants.SWITCH_QUERY_FLG)
            self.__count_times = 0
        else:
            self.__count_times = self.__count_times + 1

    # 用于定时取出循环队列数据，发送数据，定时循环用于控制数据间隔
    def send_data_from_array(self):
        if not self.__network_device_flg or self.__send_data_query.is_empty():
            return

        temp = self.__send_data_query.pop()

        if temp == constants.SWITCH_QUERY_FLG:
            self.__device_control.write(constants.QUERY_SWITCH_DEVICE_STATUS)
            return

        if temp == constants.SWITCH_ON_FLG_01:
            self.__device_control.write(constants.SWITCH_NUM_01_ON)
            return

        if temp == constants.SWITCH_OFF_FLG_01:
            self.__device_control.write(constants.SWITCH_NUM_01_OFF)
            return

        if temp == constants.SWITCH_ON_FLG_02:
            self.__device_control.write(constants.SWITCH_NUM_02_ON)
            return

        if temp == constants.SWITCH_OFF_FLG_02:
            self.__device_control.write(constants.SWITCH_NUM_02_OFF)
            return

        if temp == constants.SWITCH_ON_FLG_03:
            self.__device_control.write(constants.SWITCH_NUM_03_ON)
            return

        if temp == constants.SWITCH_OFF_FLG_03:
            self.__device_control.write(constants.SWITCH_NUM_03_OFF)
            return

        if temp == constants.SWITCH_ON_FLG_04:
            self.__device_control.write(constants.SWITCH_NUM_04_ON)
            return

        if temp == constants.SWITCH_OFF_FLG_04:
            self.__device_control.write(constants.SWITCH_NUM_04_OFF)
            return

        if temp == constants.SWITCH_ON_FLG_05:
            self.__device_control.write(constants.SWITCH_NUM_05_ON)
            return

        if temp == constants.SWITCH_OFF_FLG_05:
            self.__device_control.write(constants.SWITCH_NUM_05_OFF)
            return

        if temp == constants.SWITCH_ON_FLG_06:
            self.__device_control.write(constants.SWITCH_NUM_06_ON)
            return

        if temp == constants.SWITCH_OFF_FLG_06:
            self.__device_control.write(constants.SWITCH_NUM_06_OFF)
            return

        if temp == constants.SWITCH_ON_FLG_07:
            self.__device_control.write(constants.SWITCH_NUM_07_ON)
            return

        if temp == constants.SWITCH_OFF_FLG_07:
            self.__device_control.write(constants.SWITCH_NUM_07_OFF)
            return

        if temp == constants.SWITCH_ON_FLG_08:
            self.__device_control.write(constants.SWITCH_NUM_08_ON)
            return

        if temp == constants.SWITCH_OFF_FLG_08:
            self.__device_control.write(constants.SWITCH_NUM_08_OFF)
            return

    # 处理界面点击事件
    def on_pushbutton_1_click(self):
        if not self.__network_device_flg:
            self.pop_error_info("")
            return

        if self.__send_data_query.is_full():
            return

        if self.__pushButton_01_status:
            self.__pushButton_01_status = False
            self.__ui.pushButton_01.setStyleSheet("border-image: url(:/png/images/device_off.png);")
            self.__count_times = 0
            self.__send_data_query.push(constants.SWITCH_OFF_FLG_01)
        else:
            self.__pushButton_01_status = True
            self.__ui.pushButton_01.setStyleSheet("border-image: url(:/png/images/device_on.png);")
            self.__count_times = 0
            self.__send_data_query.push(constants.SWITCH_ON_FLG_01)

    def on_pushbutton_2_click(self):
        if not self.__network_device_flg:
            self.pop_error_info("")
            return

        if self.__send_data_query.is_full():
            return

        if self.__pushButton_02_status:
            self.__pushButton_02_status = False
            self.__ui.pushButton_02.setStyleSheet("border-image: url(:/png/images/device_off.png);")
            self.__count_times = 0
            self.__send_data_query.push(constants.SWITCH_OFF_FLG_02)
        else:
            self.__pushButton_02_status = True
            self.__ui.pushButton_02.setStyleSheet("border-image: url(:/png/images/device_on.png);")
            self.__count_times = 0
            self.__send_data_query.push(constants.SWITCH_ON_FLG_02)

    def on_pushbutton_3_click(self):
        if not self.__network_device_flg:
            self.pop_error_info("")
            return

        if self.__send_data_query.is_full():
            return

        if self.__pushButton_03_status:
            self.__pushButton_03_status = False
            self.__ui.pushButton_03.setStyleSheet("border-image: url(:/png/images/device_off.png);")
            self.__count_times = 0
            self.__send_data_query.push(constants.SWITCH_OFF_FLG_03)
        else:
            self.__pushButton_03_status = True
            self.__ui.pushButton_03.setStyleSheet("border-image: url(:/png/images/device_on.png);")
            self.__count_times = 0
            self.__send_data_query.push(constants.SWITCH_ON_FLG_03)

    def on_pushbutton_4_click(self):
        if not self.__network_device_flg:
            self.pop_error_info("")
            return

        if self.__send_data_query.is_full():
            return

        if self.__pushButton_04_status:
            self.__pushButton_04_status = False
            self.__ui.pushButton_04.setStyleSheet("border-image: url(:/png/images/device_off.png);")
            self.__count_times = 0
            self.__send_data_query.push(constants.SWITCH_OFF_FLG_04)
        else:
            self.__pushButton_04_status = True
            self.__ui.pushButton_04.setStyleSheet("border-image: url(:/png/images/device_on.png);")
            self.__count_times = 0
            self.__send_data_query.push(constants.SWITCH_ON_FLG_04)

    def on_pushbutton_5_click(self):
        if not self.__network_device_flg:
            self.pop_error_info("")
            return

        if self.__send_data_query.is_full():
            return

        if self.__pushButton_05_status:
            self.__pushButton_05_status = False
            self.__ui.pushButton_05.setStyleSheet("border-image: url(:/png/images/device_off.png);")
            self.__count_times = 0
            self.__send_data_query.push(constants.SWITCH_OFF_FLG_05)
        else:
            self.__pushButton_05_status = True
            self.__ui.pushButton_05.setStyleSheet("border-image: url(:/png/images/device_on.png);")
            self.__count_times = 0
            self.__send_data_query.push(constants.SWITCH_ON_FLG_05)

    def on_pushbutton_6_click(self):
        if not self.__network_device_flg:
            self.pop_error_info("")
            return

        if self.__send_data_query.is_full():
            return

        if self.__pushButton_06_status:
            self.__pushButton_06_status = False
            self.__ui.pushButton_06.setStyleSheet("border-image: url(:/png/images/device_off.png);")
            self.__count_times = 0
            self.__send_data_query.push(constants.SWITCH_OFF_FLG_06)
        else:
            self.__pushButton_06_status = True
            self.__ui.pushButton_06.setStyleSheet("border-image: url(:/png/images/device_on.png);")
            self.__count_times = 0
            self.__send_data_query.push(constants.SWITCH_ON_FLG_06)

    def on_pushbutton_7_click(self):
        if not self.__network_device_flg:
            self.pop_error_info("")
            return

        if self.__send_data_query.is_full():
            return

        if self.__pushButton_07_status:
            self.__pushButton_07_status = False
            self.__ui.pushButton_07.setStyleSheet("border-image: url(:/png/images/device_off.png);")
            self.__count_times = 0
            self.__send_data_query.push(constants.SWITCH_OFF_FLG_07)
        else:
            self.__pushButton_07_status = True
            self.__ui.pushButton_07.setStyleSheet("border-image: url(:/png/images/device_on.png);")
            self.__count_times = 0
            self.__send_data_query.push(constants.SWITCH_ON_FLG_07)

    def on_pushbutton_8_click(self):
        if not self.__network_device_flg:
            self.pop_error_info("")
            return

        if self.__send_data_query.is_full():
            return

        if self.__pushButton_08_status:
            self.__pushButton_08_status = False
            self.__ui.pushButton_08.setStyleSheet("border-image: url(:/png/images/device_off.png);")
            self.__count_times = 0
            self.__send_data_query.push(constants.SWITCH_OFF_FLG_08)
        else:
            self.__pushButton_08_status = True
            self.__ui.pushButton_08.setStyleSheet("border-image: url(:/png/images/device_on.png);")
            self.__count_times = 0
            self.__send_data_query.push(constants.SWITCH_ON_FLG_08)

    # 处理接收的数据，对页面按键状态进行更新
    def net_work_data_received(self, msg):
        if (int.from_bytes(msg, byteorder="little") & 0x01) == 0:
            if not self.__pushButton_08_status:
                self.__ui.pushButton_08.setStyleSheet("border-image: url(:/png/images/device_on.png);")
                self.__pushButton_08_status = True
        else:
            if self.__pushButton_08_status:
                self.__ui.pushButton_08.setStyleSheet("border-image: url(:/png/images/device_off.png);")
                self.__pushButton_08_status = False

        if (int.from_bytes(msg, byteorder="little") >> 1 & 0x01) == 0:
            if not self.__pushButton_07_status:
                self.__ui.pushButton_07.setStyleSheet("border-image: url(:/png/images/device_on.png);")
                self.__pushButton_07_status = True
        else:
            if self.__pushButton_07_status:
                self.__ui.pushButton_07.setStyleSheet("border-image: url(:/png/images/device_off.png);")
                self.__pushButton_07_status = False

        if (int.from_bytes(msg, byteorder="little") >> 2 & 0x01) == 0:
            if not self.__pushButton_06_status:
                self.__ui.pushButton_06.setStyleSheet("border-image: url(:/png/images/device_on.png);")
                self.__pushButton_06_status = True
        else:
            if self.__pushButton_06_status:
                self.__ui.pushButton_06.setStyleSheet("border-image: url(:/png/images/device_off.png);")
                self.__pushButton_06_status = False

        if (int.from_bytes(msg, byteorder="little") >> 3 & 0x01) == 0:
            if not self.__pushButton_05_status:
                self.__ui.pushButton_05.setStyleSheet("border-image: url(:/png/images/device_on.png);")
                self.__pushButton_05_status = True
        else:
            if self.__pushButton_05_status:
                self.__ui.pushButton_05.setStyleSheet("border-image: url(:/png/images/device_off.png);")
                self.__pushButton_05_status = False

        if (int.from_bytes(msg, byteorder="little") >> 4 & 0x01) == 0:
            if not self.__pushButton_04_status:
                self.__ui.pushButton_04.setStyleSheet("border-image: url(:/png/images/device_on.png);")
                self.__pushButton_04_status = True
        else:
            if self.__pushButton_04_status:
                self.__ui.pushButton_04.setStyleSheet("border-image: url(:/png/images/device_off.png);")
                self.__pushButton_04_status = False

        if (int.from_bytes(msg, byteorder="little") >> 5 & 0x01) == 0:
            if not self.__pushButton_03_status:
                self.__ui.pushButton_03.setStyleSheet("border-image: url(:/png/images/device_on.png);")
                self.__pushButton_03_status = True
        else:
            if self.__pushButton_03_status:
                self.__ui.pushButton_03.setStyleSheet("border-image: url(:/png/images/device_off.png);")
                self.__pushButton_03_status = False

        if (int.from_bytes(msg, byteorder="little") >> 6 & 0x01) == 0:
            if not self.__pushButton_02_status:
                self.__ui.pushButton_02.setStyleSheet("border-image: url(:/png/images/device_on.png);")
                self.__pushButton_02_status = True
        else:
            if self.__pushButton_02_status:
                self.__ui.pushButton_02.setStyleSheet("border-image: url(:/png/images/device_off.png);")
                self.__pushButton_02_status = False

        if (int.from_bytes(msg, byteorder="little") >> 7 & 0x01) == 0:
            if not self.__pushButton_01_status:
                self.__ui.pushButton_01.setStyleSheet("border-image: url(:/png/images/device_on.png);")
                self.__pushButton_01_status = True
        else:
            if self.__pushButton_01_status:
                self.__ui.pushButton_01.setStyleSheet("border-image: url(:/png/images/device_off.png);")
                self.__pushButton_01_status = False

    # 处理接收网络状态，断开时弹窗
    def device_net_work_status_received(self, connect_status):

        self.__network_device_flg = connect_status

        if not connect_status:
            self.pop_error_info("设备服务器：网络连接失败！")

    # >>>>>>>>>>>>>>>>>>>>>>>>>>> matrix control part <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # 初始化 device 控制部分
    def init_matrix(self):
        self.init_matrix_connect()

    def init_matrix_connect(self):
        self.__ui.input_01.toggled.connect(self.on_input_01_check)
        self.__ui.input_02.toggled.connect(self.on_input_02_check)
        self.__ui.input_03.toggled.connect(self.on_input_03_check)
        self.__ui.input_04.toggled.connect(self.on_input_04_check)
        self.__ui.input_05.toggled.connect(self.on_input_05_check)
        self.__ui.input_06.toggled.connect(self.on_input_06_check)
        self.__ui.input_07.toggled.connect(self.on_input_07_check)
        self.__ui.input_08.toggled.connect(self.on_input_08_check)

        self.__ui.output_01.clicked.connect(self.on_output_01_check)
        self.__ui.output_02.clicked.connect(self.on_output_02_check)
        self.__ui.output_03.clicked.connect(self.on_output_03_check)
        self.__ui.output_04.clicked.connect(self.on_output_04_check)
        self.__ui.output_05.clicked.connect(self.on_output_05_check)
        self.__ui.output_06.clicked.connect(self.on_output_06_check)
        self.__ui.output_07.clicked.connect(self.on_output_07_check)
        self.__ui.output_08.clicked.connect(self.on_output_08_check)

    # matrix 初始化输出端状态
    def init_view_matrix_output_status(self):
        temp = self.__ui.gb_output.findChildren(QtWidgets.QPushButton)
        for i in temp:
            if i.property("checked"):
                i.setProperty("autoExclusive", "False")
                i.setProperty("checked", "False")
                i.setProperty("autoExclusive", "True")

    # matrix 初始化输入端状态
    def init_view_matrix_input_status(self):
        temp = self.__ui.gb_input.findChildren(QtWidgets.QPushButton)
        for i in temp:
            if i.property("checked"):
                i.setProperty("autoExclusive", "False")
                i.setProperty("checked", "False")
                i.setProperty("autoExclusive", "True")

    # 矩阵指令发送 --input
    def on_input_01_check(self, checked: bool):
        if not self.__network_matrix_flg:
            self.pop_error_info("")
            return

        if checked:
            self.__matrix_control.on_socket_transmit(constants.MATRIX_INPUT_01)
        else:
            self.init_view_matrix_output_status()

    def on_input_02_check(self, checked: bool):
        if not self.__network_matrix_flg:
            self.pop_error_info("")
            return

        if checked:
            self.__matrix_control.on_socket_transmit(constants.MATRIX_INPUT_02)
        else:
            self.init_view_matrix_output_status()

    def on_input_03_check(self, checked: bool):
        if not self.__network_matrix_flg:
            self.pop_error_info("")
            return

        if checked:
            self.__matrix_control.on_socket_transmit(constants.MATRIX_INPUT_03)
        else:
            self.init_view_matrix_output_status()

    def on_input_04_check(self, checked: bool):
        if not self.__network_matrix_flg:
            self.pop_error_info("")
            return

        if checked:
            self.__matrix_control.on_socket_transmit(constants.MATRIX_INPUT_04)
        else:
            self.init_view_matrix_output_status()

    def on_input_05_check(self, checked: bool):
        if not self.__network_matrix_flg:
            self.pop_error_info("")
            return

        if checked:
            self.__matrix_control.on_socket_transmit(constants.MATRIX_INPUT_05)
        else:
            self.init_view_matrix_output_status()

    def on_input_06_check(self, checked: bool):
        if not self.__network_matrix_flg:
            self.pop_error_info("")
            return

        if checked:
            self.__matrix_control.on_socket_transmit(constants.MATRIX_INPUT_06)
        else:
            self.init_view_matrix_output_status()

    def on_input_07_check(self, checked: bool):
        if not self.__network_matrix_flg:
            self.pop_error_info("")
            return

        if checked:
            self.__matrix_control.on_socket_transmit(constants.MATRIX_INPUT_07)
        else:
            self.init_view_matrix_output_status()

    def on_input_08_check(self, checked: bool):
        if not self.__network_matrix_flg:
            self.pop_error_info("")
            return

        if checked:
            self.__matrix_control.on_socket_transmit(constants.MATRIX_INPUT_08)
        else:
            self.init_view_matrix_output_status()

    # 矩阵指令发送 --output
    def on_output_01_check(self, checked: bool):
        if not self.__network_matrix_flg:
            self.pop_error_info("")
            return

        self.__matrix_control.on_socket_transmit(constants.MATRIX_OUTPUT_01)
        self.init_view_matrix_input_status()

    def on_output_02_check(self, checked: bool):
        if not self.__network_matrix_flg:
            self.pop_error_info("")
            return

        self.__matrix_control.on_socket_transmit(constants.MATRIX_OUTPUT_02)
        self.init_view_matrix_input_status()

    def on_output_03_check(self, checked: bool):
        if not self.__network_matrix_flg:
            self.pop_error_info("")
            return

        self.__matrix_control.on_socket_transmit(constants.MATRIX_OUTPUT_03)
        self.init_view_matrix_input_status()

    def on_output_04_check(self, checked: bool):
        if not self.__network_matrix_flg:
            self.pop_error_info("")
            return

        self.__matrix_control.on_socket_transmit(constants.MATRIX_OUTPUT_04)
        self.init_view_matrix_input_status()

    def on_output_05_check(self, checked: bool):
        if not self.__network_matrix_flg:
            self.pop_error_info("")
            return

        self.__matrix_control.on_socket_transmit(constants.MATRIX_OUTPUT_05)
        self.init_view_matrix_input_status()

    def on_output_06_check(self, checked: bool):
        if not self.__network_matrix_flg:
            self.pop_error_info("")
            return

        self.__matrix_control.on_socket_transmit(constants.MATRIX_OUTPUT_06)
        self.init_view_matrix_input_status()

    def on_output_07_check(self, checked: bool):
        if not self.__network_matrix_flg:
            self.pop_error_info("")
            return

        self.__matrix_control.on_socket_transmit(constants.MATRIX_OUTPUT_07)
        self.init_view_matrix_input_status()

    def on_output_08_check(self, checked: bool):
        if not self.__network_matrix_flg:
            self.pop_error_info("")
            return

        self.__matrix_control.on_socket_transmit(constants.MATRIX_OUTPUT_08)
        self.init_view_matrix_input_status()

    # matrix 网络检查
    def network_matrix_connect(self):

        self.__matrix_control = Network_Matrix()
        if self.__matrix_control.connect(constants.SERVICE_IP, constants.MATRIX_PORT):
            self.__network_matrix_flg = True
            self._net_status_02.setText("矩阵网络已连接")
            self._net_status_02.setStyleSheet("color:#2b2b2b;")

        else:
            self.__network_matrix_flg = False
            self._net_status_02.setText("矩阵网络未连接")
            self._net_status_02.setStyleSheet("color:#ff842c;")
            self.pop_error_info("矩阵服务器：网络未连接")
            return

        self.__ui.statusbar.addPermanentWidget(self._net_status_02)
        # 通过自定义槽函数与信号，对网络状态绑定
        self.__device_control.network_connect_status.connect(self.matrix_net_work_status_received)

    # 处理接收网络状态，断开时弹窗
    def matrix_net_work_status_received(self, connect_status):

        self.__network_matrix_flg = connect_status

        if not connect_status:
            self.pop_error_info("矩阵服务器，网络已断开")

    def pop_error_info(self, err):

        if self._close_app:
            return

        if len(err) == 0:
            self.__ui._select = QtWidgets.QMessageBox.warning(self, "警告", "当前网络连接不正确",
                                                              QtWidgets.QMessageBox.StandardButton.Retry |
                                                              QtWidgets.QMessageBox.StandardButton.Ok)
        else:
            self.__ui._select = QtWidgets.QMessageBox.warning(self, "警告", err,
                                                              QtWidgets.QMessageBox.StandardButton.Ok)

        if not self.__network_matrix_flg:
            self._net_status_02.setText("矩阵服务器未连接")
            self.__ui.statusbar.addPermanentWidget(self._net_status_02)

        if not self.__network_device_flg:
            self._net_status_01.setText("设备服务器未连接")
            self.__ui.statusbar.addPermanentWidget(self._net_status_01)

        if self.__ui._select == QtWidgets.QMessageBox.StandardButton.Retry:
            # device 网络重连
            if not self.__network_device_flg:
                self.network_device_connect()

            # matrix 网络重连
            if constants.DEVICE_PORT != constants.MATRIX_PORT and not self.__network_matrix_flg:
                self.network_matrix_connect()

    # 退出时关闭相关网络连接
    def closeEvent(self, event):
        self._close_app = True

        if self.__network_matrix_flg:
            self.__matrix_control.disconnect()

        if self.__network_device_flg:
            self.__device_control.disconnect()

    # def resizeEvent(self, evt):
    #     high = self.size().height()
    #     width = self.size().width()
    #     size = min(high, width)
    #     font_size = size / 100 + 1
    #     font_size = int(max(font_size, 5))
    #
    #     temp1 = self.__ui.gb_input.findChildren(QtWidgets.QLabel)
    #     for i in temp1:
    #         font = i.property("font")
    #         font.setPointSize(int(font_size))
    #         i.setProperty("font", font)
    #
    #     temp2 = self.__ui.gb_output.findChildren(QtWidgets.QLabel)
    #     for i in temp2:
    #         font = i.property("font")
    #         font.setPointSize(font_size)
    #         i.setProperty("font", font)
    #
    #     self.size().setWidth(width)
    #     self.size().setHeight(high)
