
QUERY_LENGTH = 64
PORT_MAX = 65535
IP_MATCH_LAW = r'(?<![\.\d])(([1-9]?\d|1\d\d|2[0-4]\d|25[0-5])\.){3}([1-9]?\d|1\d\d|2[0-4]\d|25[0-5])(?![\.\d])'

SERVICE_IP = "192.168.1.7"
DEVICE_PORT = 39998
MATRIX_PORT = 39999

SWITCH_ON_FLG_01 = 0x01
SWITCH_ON_FLG_02 = 0x02
SWITCH_ON_FLG_03 = 0x03
SWITCH_ON_FLG_04 = 0x04
SWITCH_ON_FLG_05 = 0x05
SWITCH_ON_FLG_06 = 0x06
SWITCH_ON_FLG_07 = 0x07
SWITCH_ON_FLG_08 = 0x08

SWITCH_OFF_FLG_01 = 0xF1
SWITCH_OFF_FLG_02 = 0xF2
SWITCH_OFF_FLG_03 = 0xF3
SWITCH_OFF_FLG_04 = 0xF4
SWITCH_OFF_FLG_05 = 0xF5
SWITCH_OFF_FLG_06 = 0xF6
SWITCH_OFF_FLG_07 = 0xF7
SWITCH_OFF_FLG_08 = 0xF8

SWITCH_QUERY_FLG = 0xFF

QUERY_SWITCH_DEVICE_STATUS = (0x4C, 0x1C, 0x06, 0x03, 0x01, 0x23)

SWITCH_NUM_01_ON = (0x4C, 0x1C, 0x07, 0x01, 0x01, 0x00, 0x23)
SWITCH_NUM_01_OFF = (0x4C, 0x1C, 0x07, 0x01, 0x01, 0x80, 0x23)

SWITCH_NUM_02_ON = (0x4C, 0x1C, 0x07, 0x01, 0x01, 0x01, 0x23)
SWITCH_NUM_02_OFF = (0x4C, 0x1C, 0x07, 0x01, 0x01, 0x81, 0x23)

SWITCH_NUM_03_ON = (0x4C, 0x1C, 0x07, 0x01, 0x01, 0x02, 0x23)
SWITCH_NUM_03_OFF = (0x4C, 0x1C, 0x07, 0x01, 0x01, 0x82, 0x23)

SWITCH_NUM_04_ON = (0x4C, 0x1C, 0x07, 0x01, 0x01, 0x03, 0x23)
SWITCH_NUM_04_OFF = (0x4C, 0x1C, 0x07, 0x01, 0x01, 0x83, 0x23)

SWITCH_NUM_05_ON = (0x4C, 0x1C, 0x07, 0x01, 0x01, 0x04, 0x23)
SWITCH_NUM_05_OFF = (0x4C, 0x1C, 0x07, 0x01, 0x01, 0x84, 0x23)

SWITCH_NUM_06_ON = (0x4C, 0x1C, 0x07, 0x01, 0x01, 0x05, 0x23)
SWITCH_NUM_06_OFF = (0x4C, 0x1C, 0x07, 0x01, 0x01, 0x85, 0x23)

SWITCH_NUM_07_ON = (0x4C, 0x1C, 0x07, 0x01, 0x01, 0x06, 0x23)
SWITCH_NUM_07_OFF = (0x4C, 0x1C, 0x07, 0x01, 0x01, 0x86, 0x23)

SWITCH_NUM_08_ON = (0x4C, 0x1C, 0x07, 0x01, 0x01, 0x07, 0x23)
SWITCH_NUM_08_OFF = (0x4C, 0x1C, 0x07, 0x01, 0x01, 0x87, 0x23)


MATRIX_INPUT_01 = "*I1!"
MATRIX_INPUT_02 = "*I2!"
MATRIX_INPUT_03 = "*I3!"
MATRIX_INPUT_04 = "*I4!"
MATRIX_INPUT_05 = "*I5!"
MATRIX_INPUT_06 = "*I6!"
MATRIX_INPUT_07 = "*I7!"
MATRIX_INPUT_08 = "*I8!"

MATRIX_OUTPUT_01 = "*O1!"
MATRIX_OUTPUT_02 = "*O2!"
MATRIX_OUTPUT_03 = "*O3!"
MATRIX_OUTPUT_04 = "*O4!"
MATRIX_OUTPUT_05 = "*O5!"
MATRIX_OUTPUT_06 = "*O6!"
MATRIX_OUTPUT_07 = "*O7!"
MATRIX_OUTPUT_08 = "*O8!"



