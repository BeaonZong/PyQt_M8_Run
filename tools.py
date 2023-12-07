import constants
import re
import socket


def is_check_ip_ok(remote_ip, port):
    if remote_ip is None:
        return False

    if port < 0 or port > constants.PORT_MAX:
        return False

    __pattern = constants.IP_MATCH_LAW

    if not re.match(__pattern, remote_ip):
        return False

    try:
        __s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        __s.settimeout(5)
        __s.connect((remote_ip, port))
        __s.close()
        return True
    except:
        return False
