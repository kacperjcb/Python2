import unittest
from PyQt5.QtWidgets import QApplication, QTextEdit
from main import MyTestApp


class Test(unittest.TestCase):
    def test_ipv4_info(self):
        app = QApplication([])
        window = MyTestApp(app)
        window.get_ipv4_info()
        text_output = window.text_output.toPlainText()
        self.assertIn("IP:", text_output)
        self.assertIn("Static:", text_output)
        self.assertIn("Interface:", text_output)
        app.quit()

    def test_system_info(self):
        app = QApplication([])
        window = MyTestApp(app)
        window.get_system_info()
        text_output = window.text_output.toPlainText()
        self.assertIn("OS Version:", text_output)
        self.assertIn("Architecture:", text_output)
        self.assertIn("Cores:", text_output)
        self.assertIn("RAM:", text_output)
        app.quit()

    def test_bios_info(self):
        app = QApplication([])
        window = MyTestApp(app)
        window.get_bios_info()
        text_output = window.text_output.toPlainText()
        self.assertIn("BIOS Vendor:", text_output)
        self.assertIn("BIOS Version:", text_output)
        self.assertIn("BIOS Release Date:", text_output)
        app.quit()

    def test_hostname(self):
        app = QApplication([])
        window = MyTestApp(app)
        window.get_hostname()
        text_output = window.text_output.toPlainText()
        self.assertIn("Host Name:", text_output)
        app.quit()


if __name__ == '__main__':
    unittest.main()
