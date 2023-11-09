import pytest
from PyQt5.QtWidgets import QApplication, QTextEdit
from main import MyTestApp


@pytest.fixture
def app():
    return QApplication([])


@pytest.fixture
def window(app):
    return MyTestApp(app)


def test_ipv4_info(window):
    window.get_ipv4_info()
    text_output = window.text_output.toPlainText()
    assert "IP:" in text_output
    assert "Static:" in text_output
    assert "Interface:" in text_output


def test_system_info(window):
    window.get_system_info()
    text_output = window.text_output.toPlainText()
    assert "OS Version:" in text_output
    assert "Architecture:" in text_output
    assert "Cores:" in text_output
    assert "RAM:" in text_output


def test_bios_info(window):
    window.get_bios_info()
    text_output = window.text_output.toPlainText()
    assert "BIOS Vendor:" in text_output
    assert "BIOS Version:" in text_output
    assert "BIOS Release Date:" in text_output


def test_hostname(window):
    window.get_hostname()
    text_output = window.text_output.toPlainText()
    assert "Host Name:" in text_output


def test_display_help(window):
    help_text = window.display_help()

    expected_help_text = (
        "Available commands:\n"
        "get_ipv4_info - Get IPv4 information\n"
        "get_proxy_info - Get proxy information\n"
        "get_system_info - Get system information\n"
        "get_bios_info - Get BIOS information\n"
        "get_hostname - Get host name"
    )

    assert help_text == expected_help_text
