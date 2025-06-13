import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QHBoxLayout,
    QPushButton,
    QStyle,
    QVBoxLayout,
    QComboBox,
)
from PyQt6.QtGui import QIcon, QPixmap, QImage
from PyQt6.QtCore import QTimer, QThread, pyqtSignal
from Pipeline_Implementation.liveVideoPipeline import framePipeline
import cv2
import numpy as np
import queue


class AIThread(QThread):
    finished = pyqtSignal(np.ndarray)  # Signal to emit processed frame and its ID

    def __init__(self, frame, frame_id, userResolution, userInterpolation, onlyDetection):
        super().__init__()
        self.frame = frame
        self.frame_id = frame_id
        self.userResolution = userResolution
        self.userInterpolation = userInterpolation
        self.onlyDetection = onlyDetection

    def run(self):
        outputFrame = framePipeline(
            self.frame, self.frame_id, self.userResolution, self.userInterpolation, self.onlyDetection
        )  # Process the frame
        self.finished.emit(outputFrame)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clear Vision Live Video Player")
        self.setGeometry(360, 200, 800, 600)
        self.setWindowIcon(QIcon("Assets/Icon.ico"))

        self.frame_id = 0
        self.isCapturing = False
        self.is_processing = False  # Flag to track if AIThread is running
        self.pauseCapture = False  # Flag to track the pause and play state.
        self.cap = None  # Flag to set the cap object to none
        self.onlyDetection = False
        self.frame_queue = queue.Queue()  # Queue to store frames

        self.createPlayer()

    def createPlayer(self):
        self.frameViewer = QLabel(self)
        self.frameViewer.setScaledContents(True)
        self.capture_timer = QTimer(self)
        self.process_timer = QTimer(self)

        self.startBtn = QPushButton("Start Capture")
        self.startBtn.clicked.connect(self.startVideoCapture)

        self.playPauseBtn = QPushButton("Pause Capture")
        self.playPauseBtn.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause)
        )
        self.playPauseBtn.clicked.connect(self.pauseFrameCapture)

        self.fullScreenBtn = QPushButton("Full Screen")
        self.fullScreenBtn.clicked.connect(self.toggleFullScreen)

        self.resolutionLabel = QLabel("Select Resolution")
        self.resolutionDropdown = QComboBox()
        self.resolutionDropdown.addItem("1x", 1.0)
        self.resolutionDropdown.addItem("0.75x", 0.75)
        self.resolutionDropdown.addItem("0.5x", 0.5)
        self.resolutionDropdown.addItem("0.25x", 0.25)
        self.resolutionDropdown.setToolTip(
            "1x: Default Resolution\n0.75x: Quarter of the orginal resolution\n0.5x: Half the orignal resolution\n0.25x: One-Quarter of the orignal resolution"
        )

        self.resolutionDropdown.activated.connect(self.currentValue)

        self.interPolationLabel = QLabel("Select Downscaling Option")
        self.interPolationDropdown = QComboBox()
        self.interPolationDropdown.addItem("Performance", "INTER_NEAREST")
        self.interPolationDropdown.addItem("Balanced", "INTER_AREA")
        self.interPolationDropdown.addItem("Quality", "INTER_CUBIC")
        self.interPolationDropdown.addItem("Ultra Quality", "INTER_LANCZOS4")
        self.interPolationDropdown.setCurrentText("Balanced")
        self.interPolationDropdown.setToolTip(
            "Performance: Fastest, lower quality\nBalanced: Good speed and quality\nQuality: Better detail, slower\nUltra Quality: Best detail, high-end systems only"
        )
        self.interPolationDropdown.activated.connect(self.currentValue)

        self.onlyDetectionBtn = QPushButton("Only Detection")
        self.onlyDetectionBtn.clicked.connect(self.onlyDetectionMethod)

        vboxLayout = QVBoxLayout()
        hboxLayoutOne = QHBoxLayout()
        hboxLayoutTwo = QHBoxLayout()

        hboxLayoutOne.addWidget(self.startBtn)
        hboxLayoutOne.addWidget(self.playPauseBtn)
        hboxLayoutOne.addWidget(self.fullScreenBtn)

        hboxLayoutTwo.addWidget(self.interPolationLabel)
        hboxLayoutTwo.addWidget(self.interPolationDropdown)
        hboxLayoutTwo.addWidget(self.resolutionLabel)
        hboxLayoutTwo.addWidget(self.resolutionDropdown)
        hboxLayoutTwo.addWidget(self.onlyDetectionBtn)

        vboxLayout.addWidget(self.frameViewer)
        vboxLayout.addLayout(hboxLayoutOne)
        vboxLayout.addLayout(hboxLayoutTwo)

        self.setLayout(vboxLayout)

    def currentValue(self):
        selectedResoultion = self.resolutionDropdown.currentData()
        selectedInterpolation = self.interPolationDropdown.currentData()
        return selectedResoultion, selectedInterpolation

    def startVideoCapture(self):
        if self.isCapturing == False:
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

            if not self.cap.isOpened():
                print("Error: Could not open video.")
                return
            # Timer to capture frames at a fixed rate (e.g., 30 FPS)
            self.capture_timer.timeout.connect(self.updateFrame)
            self.capture_timer.start(33)  # ~30 FPS

            # Getting the desired user resolution
            self.userResolution, self.userInterpolation = self.currentValue()

            # Timer to process frames from the queue
            self.process_timer.timeout.connect(self.processNextFrame)
            self.process_timer.start(100)  # Check queue every 100ms
            self.isCapturing = True
            self.startBtn.setText("Stop Capture")

        elif self.isCapturing == True:
            self.cap.release()
            self.capture_timer.stop()
            self.process_timer.stop()
            self.isCapturing = False
            self.startBtn.setText("Start Capture")

    def pauseFrameCapture(self):
        if self.pauseCapture == False:
            self.capture_timer.stop()
            self.pauseCapture = True
            self.playPauseBtn.setText("Play Capture")
            self.playPauseBtn.setIcon(
                self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay)
            )
        elif self.pauseCapture == True:
            self.capture_timer.start(33)
            self.pauseCapture = False
            self.playPauseBtn.setText("Pause Capture")
            self.playPauseBtn.setIcon(
                self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause)
            )

    def updateFrame(self):
        ret, frame = self.cap.read()
        if ret:
            # Add frame and its ID to the queue
            self.frame_queue.put((frame, self.frame_id))
            # print(self.frame_queue)
            self.frame_id += 1

    def processNextFrame(self):
        # Only process if no AI thread is currently running
        if not self.is_processing and not self.frame_queue.empty():
            self.is_processing = True
            frame, frame_id = self.frame_queue.get()
            # Start the FrameSaverThread
            self.processFrameWithAI(
                frame, frame_id, self.userResolution, self.userInterpolation, self.onlyDetection
            )

    def processFrameWithAI(self, frame, frame_id, userResolution, userInterpolation, onlyDetection):
        self.aiThread = AIThread(frame, frame_id, userResolution, userInterpolation, onlyDetection)
        self.aiThread.finished.connect(self.displayProcessedFrame)
        self.aiThread.start()

    def displayProcessedFrame(self, processed_frame):
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
        height, width, channel = rgb_frame.shape
        bytesPerLine = channel * width
        qImg = QImage(
            rgb_frame.data, width, height, bytesPerLine, QImage.Format.Format_RGB888
        )
        self.frameViewer.setPixmap(QPixmap.fromImage(qImg))

        # AI processing is done, allow the next frame to be processed
        self.is_processing = False

    def toggleFullScreen(self):
        if self.isFullScreen():
            self.showNormal()
            self.fullScreenBtn.setText("Full Screen")
        else:
            self.showFullScreen()
            self.fullScreenBtn.setText("Minimize Screen")

    def onlyDetectionMethod(self):
        if self.onlyDetection == False:
            self.onlyDetection = True
        elif self.onlyDetection == True:
            self.onlyDetection = False

    def closeEvent(self, event):
        if self.cap is not None:
            self.cap.release()
        self.capture_timer.stop()
        self.process_timer.stop()
        event.accept()


# For executing the application
app = QApplication([])
window = Window()
window.show()
sys.exit(app.exec())
