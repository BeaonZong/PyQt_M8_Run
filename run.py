from PyQt5 import QtWidgets, QtCore
import sys

import constants
from mainwindows import My_MainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    settings = QtCore.QSettings("network.ini", QtCore.QSettings.Format.IniFormat)
    settings.setIniCodec("UTF8")

    if not settings.contains("SERVER/server_ip") or not settings.contains(
            "SERVER/device_port") or not settings.contains("SERVER/matrix_port"):
        settings.setValue("SERVER/server_ip", "192.168.1.7")
        settings.setValue("SERVER/device_port", "39998")
        settings.setValue("SERVER/matrix_port", "39999")
        settings.setValue("INFO/notice", "软件已开源，开源地址：https://github.com/BeaonZong/PyQt_M8_Run.git")

    constants.SERVICE_IP = settings.value("SERVER/server_ip")
    constants.DEVICE_PORT = int(settings.value("SERVER/device_port"))
    constants.MATRIX_PORT = int(settings.value("SERVER/matrix_port"))

    my = My_MainWindow()
    # my.setWindowFlags(QtCore.Qt.WindowType.WindowCloseButtonHint)
    my.show()
    sys.exit(app.exec_())

# 设置背景方法一：
# my.setStyleSheet("#MainWindow{background-color:red}")
# my.setStyleSheet("#MainWindow{border-image:url(image/bk.png)}")
# my.setStyleSheet("#MainWindow{background-image:url(image/bk.png)}")

# 设置背景方法二：
# palette = QtGui.QPalette()
# palette.setColor(QtGui.QPalette.Background, Qt.GlobalColor.red)
# palette.setBrush(QtGui.QPalette.Background, QBrush(QPixmap("./image/bk.png")))  # 会出现显示不全情况

# palette.setBrush(my.backgroundRole(),
#                  QBrush(QPixmap("./image/bk.png")
#                         .scaled(my.size(),
#                                 Qt.AspectRatioMode.IgnoreAspectRatio,
#                                 Qt.TransformationMode.SmoothTransformation)))
# my.setPalette(palette)

##
## pyinstaller --paths C:\Users\tianx\Desktop\pythonDevelop\venv\Lib\site-packages\PyQt5\Qt5\bin -F -w run.py
##
