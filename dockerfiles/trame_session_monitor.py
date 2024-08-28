import os
import socket
import time

if __name__ == '__main__':
    while True:
        # check_running_session.sh takes about 2 seconds to execute
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for port in range(9001, 9501):
            try:
                s.connect(("localhost", int(port)))
                s.shutdown(socket.SHUT_WR)
                open(f"/opt/trame/session_ports/{port}", "a")
            except:
                if os.path.exists(f"/opt/trame/session_ports/{port}"):
                    os.remove(f"/opt/trame/session_ports/{port}")
                continue
        time.sleep(1)
