import binascii

from PyQt5 import QtNetwork
from PyQt5.QtCore import pyqtSignal, QObject


class Network_Device(QObject):
    status_signal = pyqtSignal(bytes)
    network_connect_status = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__socket = None
        self.isConnectedToServer = False

    def connect(self, remote_address, port):
        if self.isConnectedToServer:
            return True

        """Establishes a session with the debugger"""
        self.__socket = QtNetwork.QTcpSocket()
        self.__socket.connectToHost(remote_address, port)

        if not self.__socket.waitForConnected(2500):
            return False

        self.__socket.connected.connect(self.on_socket_connected)
        self.__socket.disconnected.connect(self.on_socket_disconnected)
        self.__socket.readyRead.connect(self.on_socket_receive)
        # self.__socket.bytesWritten.connect(self.on_socket_transmit)
        self.isConnectedToServer = True

        return True

    def on_socket_connected(self):
        self.network_connect_status.emit(True)

    def on_socket_disconnected(self):
        self.network_connect_status.emit(False)
        self.disconnect()

    def on_socket_receive(self):
        msg = self.__socket.readAll()
        if len(msg) != 7:
            return

        # 查询指令返回的数据 0x01 指定设备地址
        if msg[3] != binascii.unhexlify("03") \
                or msg[4] != binascii.unhexlify("01"):
            return

        ab = msg[5]
        self.status_signal.emit(ab)

    def write_date_from_service(self, num_bytes):
        self.__socket.write(bytearray(num_bytes))
        self.__socket.flush()

    def on_socket_transmit(self, num_bytes):
        self.__socket.write(bytearray(num_bytes))
        self.__socket.flush()
        return

    def write(self, send_data):
        try:
            self.__socket.write(bytearray(send_data))
            self.__socket.flush()
            return True
        except:
            return False

    def disconnect(self):
        if not self.isConnectedToServer:
            return

        try:
            self.__socket.connected.disconncet()
        except:
            pass

        try:
            self.__socket.disconnected.disconncet()
        except:
            pass

        try:
            self.__socket.readyRead.disconncet()
        except:
            pass

        try:
            self.__socket.bytesWritten.disconncet()
        except:
            pass

        self.__socket.close()

        self.isConnectedToServer = False

#
# class MThread(threading.Thread):
#     def __init__(self, socket, status_signal):
#         threading.Thread.__init__(self)
#         self.m_socket = socket
#         self.status_signal = status_signal
#
#     def run(self):
#         while True:
#             msg = self.m_socket.readAll()
#
#             if len(msg) != 7:
#                 continue
#
#             # 查询指令返回的数据 0x01 指定设备地址
#             if msg[3] != 0x03 or msg[4] != 0x01:
#                 continue
#
#             ab = msg[5]
#             self.status_signal.emit(ab)
