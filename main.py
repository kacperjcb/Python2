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
        print(result)  # Wypisz wynik w konsoli

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

        print(f"Proxy Status: {proxy_status}")  # Wypisz wynik w konsoli

    def get_system_info(self):
        os_version = platform.platform()
        os_architecture = platform.architecture()
        num_cores = psutil.cpu_count(logical=False)
        ram = round(psutil.virtual_memory().total / (1024 ** 3), 2)
        result = f"OS Version: {os_version}\nArchitecture: {os_architecture}\nCores: {num_cores}\nRAM: {ram} GB"
        print(result)  # Wypisz wynik w konsoli

    def display_help(self):
        print("Available commands:")
        print("get_ipv4_info - Get IPv4 information")
        print("get_proxy_info - Get proxy information")
        print("get_system_info - Get system information")
        print("get_bios_info - Get BIOS information")
        print("get_hostname - Get host name")

    def get_bios_info(self):
        c = wmi.WMI()
        bios = c.Win32_BIOS()[0]
        result = f"BIOS Vendor: {bios.Manufacturer}\nBIOS Version: {bios.Version}\nBIOS Release Date: {bios.ReleaseDate}"
        print(result)  # Wypisz wynik w konsoli

    def get_hostname(self):
        hostname = socket.gethostname()
        print(f"Host Name: {hostname}")  # Wypisz wynik w konsoli

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyTestApp(app)
    window.show()

    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="Command to execute")
    args = parser.parse_args()

    if args.command == "help":
        window.display_help()
        input("Press enter to close window")
    elif args.command in ["get_ipv4_info", "get_proxy_info", "get_system_info", "get_bios_info", "get_hostname"]:
        getattr(window, args.command)()
        input("Press enter to close window")
    else:
        print("Unknown command. Use 'main.py help' to see available commands.")
        input("Press enter to close window")
