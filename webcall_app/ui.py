from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGridLayout, QFrame
)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QTimer
import sys
import psutil

class GestureApp(QWidget):
    def __init__(self):
        super().__init__()

        # Screen resolution for a 7-inch Waveshare screen (assumed 1024x600 resolution)
        self.setFixedSize(1024, 600)
        self.setWindowTitle("Gesture Detection App")

        # Layouts
        main_layout = QVBoxLayout()

        # Top bar: Toggle button and battery status
        self.toggle_button = QPushButton("Switch to ML Camera")
        self.toggle_button.clicked.connect(self.toggle_camera)

        self.battery_label = QLabel()
        self.update_battery_status()

        top_bar = QHBoxLayout()
        top_bar.addWidget(self.toggle_button)
        top_bar.addStretch()
        top_bar.addWidget(self.battery_label)

        # Timer to update battery status every 10 seconds
        self.battery_timer = QTimer()
        self.battery_timer.timeout.connect(self.update_battery_status)
        self.battery_timer.start(10000)

        # Video feed section
        video_layout = QGridLayout()

        self.video_deaf = QLabel("Deaf Person Video")
        self.video_deaf.setFixedSize(320, 240)
        self.video_deaf.setStyleSheet("border: 2px solid black;")
        self.video_deaf.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.video_translator = QLabel("Translator Video")
        self.video_translator.setFixedSize(640, 480)
        self.video_translator.setStyleSheet("border: 2px solid black;")
        self.video_translator.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.video_speaker = QLabel("Speaker Video")
        self.video_speaker.setFixedSize(320, 240)
        self.video_speaker.setStyleSheet("border: 2px solid black;")
        self.video_speaker.setAlignment(Qt.AlignmentFlag.AlignCenter)

        video_layout.addWidget(self.video_translator, 0, 0, 2, 2)
        video_layout.addWidget(self.video_deaf, 0, 2)
        video_layout.addWidget(self.video_speaker, 1, 2)

        # ML model output section
        self.ml_output_label = QLabel("ML Model Output: No Gesture Detected")
        self.ml_output_label.setStyleSheet("font-size: 18px; border: 1px solid gray;")
        self.ml_output_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Adding sections to the main layout
        main_layout.addLayout(top_bar)
        main_layout.addLayout(video_layout)
        main_layout.addWidget(self.ml_output_label)

        self.setLayout(main_layout)

    def toggle_camera(self):
        if self.toggle_button.text() == "Switch to ML Camera":
            self.toggle_button.setText("Switch to Normal Camera")
            self.ml_output_label.setText("ML Model Output: Detecting Gestures...")
        else:
            self.toggle_button.setText("Switch to ML Camera")
            self.ml_output_label.setText("ML Model Output: No Gesture Detected")

    def update_battery_status(self):
        battery = psutil.sensors_battery()
        if battery:
            charge = battery.percent
            plugged = battery.power_plugged
            icon = "\u26A1" if plugged else "\uD83D\uDD0B"
            self.battery_label.setText(f"Battery: {charge}% {icon}")
        else:
            self.battery_label.setText("Battery: Unknown")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GestureApp()
    window.show()
    sys.exit(app.exec())
