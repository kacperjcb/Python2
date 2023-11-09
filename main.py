import sys
import socket
import platform
import psutil
import wmi
import urllib.request
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QTextEdit, QWidget
from PyQt5.QtCore import Qt
import argparse

class MyTestApp(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.initUI()

    def initUI(self):
        self.setWindowTitle('MyTest')
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.text_output = QTextEdit(self)
        layout.addWidget(self.text_output)

        self.button_ipv4_info = QPushButton('Moje Ipv4', self)
        self.button_proxy_info = QPushButton('Proxy Info', self)
        self.button_system_info = QPushButton('System Info', self)
        self.button_bios_info = QPushButton('Bios Info', self)
        self.button_hostname_info = QPushButton('Host Name', self)

        layout.addWidget(self.button_ipv4_info)
        layout.addWidget(self.button_proxy_info)
        layout.addWidget(self.button_system_info)
        layout.addWidget(self.button_bios_info)
        layout.addWidget(self.button_hostname_info)

        central_widget.setLayout(layout)

        self.button_ipv4_info.clicked.connect(self.get_ipv4_info)
        self.button_proxy_info.clicked.connect(self.get_proxy_info)
        self.button_system_info.clicked.connect(self.get_system_info)
        self.button_bios_info.clicked.connect(self.get_bios_info)
        self.button_hostname_info.clicked.connect(self.get_hostname)

    def print_to_ui(self, text):
        self.text_output.append(text)

    def get_ipv4_info(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        is_static = socket.gethostbyaddr(ip)
        interface = None
        if "Wi-Fi" in platform.platform():
            interface = "Wi-Fi"
        elif "Ethernet" in platform.platform():
            interface = "Ethernet"
        result = f"IP: {ip}\nStatic: {is_static}\nInterface: {interface}"
        self.print_to_ui(result)

    def get_proxy_info(self):
        proxy_handler = urllib.request.ProxyHandler()
        opener = urllib.request.build_opener(proxy_handler)

        try:
            opener.open("http://www.google.com", timeout=5)
            is_proxy_enabled = True
        except Exception:
            is_proxy_enabled = False

        if is_proxy_enabled:
            proxy_status = "Proxy is enabled"
        else:
            proxy_status = "Proxy is disabled"

        result = f"Proxy Status: {proxy_status}"
        self.print_to_ui(result)

        return result
    def get_system_info(self):
        os_version = platform.platform()
        os_architecture = platform.architecture()
        num_cores = psutil.cpu_count(logical=False)
        ram = round(psutil.virtual_memory().total / (1024 ** 3), 2)
        result = f"OS Version: {os_version}\nArchitecture: {os_architecture}\nCores: {num_cores}\nRAM: {ram} GB"
        self.print_to_ui(result)
        return result  # Dodaj to zwracanie wyniku


    def display_help(self):
        help_text = "Available commands:\n"
        help_text += "get_ipv4_info - Get IPv4 information\n"
        help_text += "get_proxy_info - Get proxy information\n"
        help_text += "get_system_info - Get system information\n"
        help_text += "get_bios_info - Get BIOS information\n"
        help_text += "get_hostname - Get host name"
        return help_text

    def get_bios_info(self):
        c = wmi.WMI()
        bios = c.Win32_BIOS()[0]
        result = f"BIOS Vendor: {bios.Manufacturer}\nBIOS Version: {bios.Version}\nBIOS Release Date: {bios.ReleaseDate}"
        self.print_to_ui(result)
        return result

    def get_hostname(self):
        hostname = socket.gethostname()
        self.print_to_ui(f"Host Name: {hostname}")
        return hostname

def run_with_args(args):
    app = QApplication(sys.argv)
    window = MyTestApp(app)
    window.show()

    if args.command:
        if args.command == "help":
            result = window.display_help()
            print(result)
        elif args.command in ["get_ipv4_info", "get_proxy_info", "get_system_info", "get_bios_info", "get_hostname"]:
            result = ""
            func = getattr(window, args.command)
            if func:
                result = func()
            print(result)
        else:
            print("Unknown command. Use 'main.py help' to see available commands")
    else:
        sys.exit(app.exec_())

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs="?", help="Command to execute")
    args = parser.parse_args()
    run_with_args(args)
