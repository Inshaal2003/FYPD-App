import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout
from PyQt6.QtGui import QIcon, QPixmap, QImage
from PyQt6.QtCore import QThread, pyqtSignal
from Pipeline_Implementation.liveVideoPipeline import framePipeline
import cv2
import os
import numpy as np


class FrameSaverThread(QThread):
    frame_saved = pyqtSignal(
        np.ndarray
    )  # Emit the saved frame to be passed to AIThread

    def __init__(self, frame, frame_id):
        super().__init__()
        self.frame = frame
        self.frame_id = frame_id
        self.save_dir = os.path.join(
            os.path.dirname(__file__),
            "Pipeline_Implementation",
            "Dehazing_Models",
            "Input_Folder",
        )
        os.makedirs(self.save_dir, exist_ok=True)

    def run(self):
        filename = os.path.join(self.save_dir, f"frame_{self.frame_id:04d}.png")
        cv2.imwrite(filename, self.frame)
        self.frame_saved.emit(self.frame)


class AIThread(QThread):
    finished = pyqtSignal(np.ndarray)  # Signal to emit when the processing is complete

    def __init__(self, frame):
        super().__init__()
        self.frame = frame

    def run(self):
        outputFrame = framePipeline(self.frame)  # Call the frame processing function
        self.finished.emit(
            outputFrame
        )  # Emit the finished signal with the output frame


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clear Vision Live Video Player")
        self.setGeometry(360, 200, 800, 600)
        self.setWindowIcon(QIcon("Assets/Icon.ico"))
        self.frame_id = 0
        self.createPlayer()
        self.startVideo()

    def createPlayer(self):
        # Creating the Frame Viewer
        self.frameViewer = QLabel(self)
        self.frameViewer.setScaledContents(True)

        # Adding the frame viewer to the layout
        hboxLayout = QHBoxLayout()
        hboxLayout.addWidget(self.frameViewer)
        self.setLayout(hboxLayout)

    def startVideo(self):
        self.cap = cv2.VideoCapture(0)  # Creating A Video Capture Object
        if not self.cap.isOpened():
            print("Error: Could not open video.")
            return

        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.updateFrame)
        # self.timer.start(30)
        self.updateFrame()

    def updateFrame(self):
        ret, frame = self.cap.read()
        if ret:
            # Start the AI processing in a separate thread
            self.frame_id += 1
            self.frameSaverThread = FrameSaverThread(frame, self.frame_id)
            self.frameSaverThread.frame_saved.connect(self.processFrameWithAI)
            self.frameSaverThread.start()

    def processFrameWithAI(self, saved_frame):
        self.aiThread = AIThread(saved_frame)
        self.aiThread.finished.connect(self.displayProcessedFrame)
        self.aiThread.start()

    def displayProcessedFrame(self, processed_frame):
        # Convert BGR to RGB if needed
        rgb_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)

        height, width, channel = rgb_frame.shape
        bytesPerLine = channel * width
        qImg = QImage(
            rgb_frame.data, width, height, bytesPerLine, QImage.Format.Format_RGB888
        )
        self.frameViewer.setPixmap(QPixmap.fromImage(qImg))

        self.updateFrame()

    def closeEvent(self, event):
        self.cap.release()  # Release the camera when closing the window
        event.accept()


# For executing the application
app = QApplication([])
window = Window()
window.show()
sys.exit(app.exec())
