import sys
import serial
import serial.tools.list_ports
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer
from datetime import datetime
import time
from Des import Ui_MainWindow


class TermiteMain(QMainWindow):
    def __init__(self):

        self.flash_value = None
        self.ram_value = None

        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.seriall = None  

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.obtain_set_date_time)
        self.timer.start(1000)

        self.serial_timer = QTimer(self)
        self.serial_timer.timeout.connect(self.read_serial_data)

        self.red_style = """
            QPushButton {
                background-color: red;
                color: black;
                border: none;
                border-radius: 15px;
                min-width: 30px;
                min-height: 30px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b30000;
            }
            QPushButton:pressed {
                background-color: #800000;
            }
        """
        self.green_style = """
            QPushButton {
                background-color: green;
                color: black;
                border: none;
                border-radius: 15px;
                min-width: 30px;
                min-height: 30px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """

        self.ui.ConnectButton.setStyleSheet(self.red_style)
        self.ui.ConnectionLabel.setText("Not Connected")

        self.update_port()
        self.ui.ConnectButton.clicked.connect(self.chk_esp)
        self.ui.lineEdit.returnPressed.connect(self.send_text_over_serial)

    def update_port(self):
        ports = serial.tools.list_ports.comports()
        self.ui.PortBox.clear()
        for port in ports:
            self.ui.PortBox.addItem(port.device)

    def chk_esp(self):
        port_name = self.ui.PortBox.currentText()

        if not port_name:
            self.ui.ConnectionLabel.setText("No Port")
            self.ui.ConnectButton.setStyleSheet(self.red_style)
            self.ui.ConnectButton.repaint()
            self.ui.textBrowser_5.append("No port selected.")
            return

        try:
            self.seriall = serial.Serial(port_name, 115200, timeout=0.1)

            self.seriall.reset_input_buffer()  

            self.seriall.write(b"\n")  
            self.seriall.reset_input_buffer()

            time.sleep(1)

            response = self.seriall.readline().decode('utf-8').strip()

            if response == "":
                self.ui.ConnectButton.setStyleSheet(self.green_style)
                self.ui.ConnectButton.repaint()
                self.ui.ConnectionLabel.setText("Connected")
                self.ui.portchn.setText(port_name)
                self.ui.textBrowser_5.append(f"Connected to {port_name} successfully.")
                self.seriall.write(b"p\n")  
                time.sleep(1)

                self.serial_timer.start(100)
                self.seriall.write(b"p\n")  
                time.sleep(1)


                def read_serial_data(self):
                    if self.seriall and self.seriall.is_open:
                        try:
                            while self.seriall.in_waiting > 0:
                                line = self.seriall.readline().decode('utf-8').strip()
                                
                                board=line.split()[0]
                                mem=line.split()[1]
                                space=line.split()[2]
                                self.ui.Mcuchn.setText(board)
                                self.ui.memchn.setText(mem)
                                self.ui.spcchn.setText(space)

                                if line:
                                    self.ui.textBrowser_5.append(f"Received: {line}")
                        except serial.SerialException as e:
                            self.ui.textBrowser_5.append(f"Serial Read Error: {str(e)}")
                    else:
                        self.serial_timer.stop()  
                read_serial_data(self)
                self.ui.RamUsageChn.setValue(0);
                self.ui.TempUsageChn.setValue(0);
            else:
                self.ui.ConnectButton.setStyleSheet(self.red_style)
                self.ui.ConnectButton.repaint()
                self.ui.ConnectionLabel.setText("Echo Failed ❌")
                self.ui.textBrowser_5.append(f"Echo failed. Expected 'K', got '{response}'")
                self.seriall.close()
                self.seriall = None

        except serial.SerialException as e:
            self.ui.ConnectButton.setStyleSheet(self.red_style)
            self.ui.ConnectButton.repaint()
            self.ui.ConnectionLabel.setText("Not Connected ❌")
            self.ui.textBrowser_5.append(f"Failed to connect to {port_name}: {str(e)}")

        

    def send_text_over_serial(self):
        if self.seriall and self.seriall.is_open:
            message = self.ui.lineEdit.text().strip()
            if message:
                try:
                    self.seriall.write((message + '\n').encode())
                    self.ui.textBrowser_5.append(f"Sent: {message}")
                    self.ui.lineEdit.clear()
                except serial.SerialException as e:
                    self.ui.textBrowser_5.append(f"Error sending: {str(e)}")
        else:
            self.ui.textBrowser_5.append("Serial not connected.")

    def read_serial_data(self):
        if self.seriall and self.seriall.is_open:
            try:
                while self.seriall.in_waiting > 0:
                    line = self.seriall.readline().decode('utf-8').strip()

                    if line:
                        self.ui.textBrowser_5.append(f"Received: {line}")

                        if line.startswith("ram-"):
                            try:
                                percent = int(line.split("-")[1])
                                self.ui.RamUsageChn.setValue(percent)
                            except ValueError:
                                pass

                        elif line.startswith("Arduino"):
                            try:
                                parts = line.split()
                                if len(parts) == 3:
                                    board = parts[0]
                                    mem = parts[1]
                                    space = parts[2]

                                    self.ui.Mcuchn.setText(board)
                                    self.ui.memchn.setText(mem)
                                    self.ui.spcchn.setText(space)
                            except Exception as e:
                                self.ui.textBrowser_5.append(f"Parse Error: {str(e)}")

            except serial.SerialException as e:
                self.ui.textBrowser_5.append(f"Serial Read Error: {str(e)}")
        else:
            self.serial_timer.stop()


    def obtain_set_date_time(self):
        now = datetime.now()
        self.ui.time.setText(now.strftime("%H:%M"))
        self.ui.date.setText(now.strftime("%d-%m"))

    def closeEvent(self, event):
        if self.seriall and self.seriall.is_open:
            self.seriall.close()
        self.serial_timer.stop()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TermiteMain()
    window.show()
    sys.exit(app.exec())
