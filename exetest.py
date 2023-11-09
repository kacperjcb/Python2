import sys
import socket
import platform
import psutil
import wmi
import urllib.request
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QTextEdit, QWidget
from PyQt5.QtCore import Qt, QSize, QTimer


class MyTestApp(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.initUI()
        self.current_button_index = 0
        self.test_results = {}

    def initUI(self):
        self.setWindowTitle('MyTest')
        self.setGeometry(0, 0, 1920, 1080)
        self.setWindowFlag(Qt.FramelessWindowHint)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.text_output = QTextEdit(self)
        self.text_output.setFixedSize(800, 600)
        layout.addWidget(self.text_output)

        self.button_ipv4_info = QPushButton('My Ipv4', self)
        self.button_proxy_info = QPushButton('Proxy Info', self)
        self.button_system_info = QPushButton('System Info', self)
        self.button_bios_info = QPushButton('Bios Info', self)
        self.button_hostname_info = QPushButton('Host Name', self)

        for button in [self.button_ipv4_info, self.button_proxy_info, self.button_system_info, self.button_bios_info,
                       self.button_hostname_info]:
            button.setFixedSize(QSize(200, 50))
            layout.addWidget(button)

        central_widget.setLayout(layout)

        self.button_ipv4_info.clicked.connect(self.click_ipv4_info)
        self.button_proxy_info.clicked.connect(self.click_proxy_info)
        self.button_system_info.clicked.connect(self.click_system_info)
        self.button_bios_info.clicked.connect(self.click_bios_info)
        self.button_hostname_info.clicked.connect(self.click_hostname_info)

    def get_ipv4_info(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        is_static = socket.gethostbyaddr(ip)
        interface = None
        if ip == '192.168.56.1':
            self.test_results["IP Test"] = "Success"
        else:
            self.test_results["IP Test"] = "Failure"
        result = f"IP: {ip}\nStatic: {is_static}\nInterface: {interface}"
        self.text_output.append(result)
        print("IP Test:", self.test_results["IP Test"])

    def get_proxy_info(self):
        proxy_handler = urllib.request.ProxyHandler()
        opener = urllib.request.build_opener(proxy_handler)

        try:
            opener.open("http://www.google.com", timeout=5)
            is_proxy_enabled = True
        except Exception:
            is_proxy_enabled = False

        if is_proxy_enabled:
            self.test_results["Proxy Test"] = "Success"
            proxy_status = "Proxy is enabled"
        else:
            self.test_results["Proxy Test"] = "Failure"
            proxy_status = "Proxy is disabled"
        result = f"Proxy Status: {proxy_status}"
        self.text_output.append(result)
        print("Proxy Test:", self.test_results["Proxy Test"])

    def get_system_info(self):
        os_version = platform.platform()
        os_architecture = platform.architecture()
        num_cores = psutil.cpu_count(logical=False)
        ram = round(psutil.virtual_memory().total / (1024 ** 3), 2)

        if os_version == 'Windows-10-10.0.19045-SP0':
            self.test_results["OS Test"] = "Success"
        else:
            self.test_results["OS Test"] = "Failure"
        if os_architecture == ('64bit', 'WindowsPE'):
            self.test_results["Architecture Test"] = "Success"
        else:
            self.test_results["Architecture Test"] = "Failure"
        if num_cores == 6:
            self.test_results["Cores Test"] = "Success"
        else:
            self.test_results["Cores Test"] = "Failure"
        if ram == 31.93:
            self.test_results["RAM Test"] = "Success"
        else:
            self.test_results["RAM Test"] = "Failure"
        result = f"OS Version: {os_version}\nArchitecture: {os_architecture}\nCores: {num_cores}\nRAM: {ram} GB"
        self.text_output.append(result)
        print("OS Test:", self.test_results["OS Test"])
        print("Architecture Test:", self.test_results["Architecture Test"])
        print("Cores Test:", self.test_results["Cores Test"])
        print("RAM Test:", self.test_results["RAM Test"])

    def get_bios_info(self):
        c = wmi.WMI()
        bios = c.Win32_BIOS()[0]

        if bios.Manufacturer == 'American Megatrends International, LLC.':
            self.test_results["BIOS Vendor Test"] = "Success"
        else:
            self.test_results["BIOS Vendor Test"] = "Failure"
        if bios.Version == 'ALASKA - 1072009':
            self.test_results["BIOS Version Test"] = "Success"
        else:
            self.test_results["BIOS Version Test"] = "Failure"
        if bios.ReleaseDate == '20230630000000.000000+000':
            self.test_results["BIOS Release Date Test"] = "Success"
        else:
            self.test_results["BIOS Release Date Test"] = "Failure"
        result = f"BIOS Vendor: {bios.Manufacturer}\nBIOS Version: {bios.Version}\nBIOS Release Date: {bios.ReleaseDate}"
        self.text_output.append(result)
        print("BIOS Vendor Test:", self.test_results["BIOS Vendor Test"])
        print("BIOS Version Test:", self.test_results["BIOS Version Test"])
        print("BIOS Release Date Test:", self.test_results["BIOS Release Date Test"])

    def get_hostname(self):
        hostname = socket.gethostname()
        if hostname == 'glowacs':
            self.test_results["Hostname Test"] = "Success"
        else:
            self.test_results["Hostname Test"] = "Failure"
        self.text_output.append(f"Host Name: {hostname}")
        print("Hostname Test:", self.test_results["Hostname Test"])

    def click_ipv4_info(self):
        self.get_ipv4_info()
        self.current_button_index += 1
        self.auto_click_buttons()

    def click_proxy_info(self):
        self.get_proxy_info()
        self.current_button_index += 1
        self.auto_click_buttons()

    def click_system_info(self):
        self.get_system_info()
        self.current_button_index += 1
        self.auto_click_buttons()

    def click_bios_info(self):
        self.get_bios_info()
        self.current_button_index += 1
        self.auto_click_buttons()

    def click_hostname_info(self):
        self.get_hostname()
        self.complete_test()

    def auto_click_buttons(self):
        buttons = [
            self.click_ipv4_info,
            self.click_proxy_info,
            self.click_system_info,
            self.click_bios_info,
            self.click_hostname_info
        ]

        if self.current_button_index < len(buttons):
            QTimer.singleShot(2000, buttons[self.current_button_index])
        else:
            self.complete_test()

    def complete_test(self):
        self.text_output.append("\nTest Results:")
        for test, result in self.test_results.items():
            self.text_output.append(f"{test}: {result}")
        success = all(result == "Success" for result in self.test_results.values())
        if success:
            self.text_output.append("\nTest: Success")
            print("Test: Success")
        else:
            self.text_output.append("\nTest: Failure")
            print("Test: Failure")
        self.app.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyTestApp(app)
    window.showFullScreen()

    window.auto_click_buttons()
    sys.exit(app.exec_())
