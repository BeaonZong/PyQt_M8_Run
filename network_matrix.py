from PyQt5 import QtNetwork
from PyQt5.QtCore import pyqtSignal, QObject


class Network_Matrix(QObject):

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
        # self.__socket.readyRead.connect(self.on_socket_receive)
        # self.__socket.bytesWritten.connect(self.on_socket_transmit)

        self.isConnectedToServer = True
        return True

    def on_socket_connected(self):
        self.network_connect_status.emit(True)

    def on_socket_disconnected(self):
        self.network_connect_status.emit(False)
        self.disconnect()

    def on_socket_receive(self):
        # __rxData = self.__socket.readAll()
        pass

    def on_socket_transmit(self, num_bytes):
        try:
            self.__socket.write(num_bytes.encode("utf-8"))
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
