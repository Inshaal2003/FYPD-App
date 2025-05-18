import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QStyle,
    QSlider,
    QFileDialog,
    QLabel,
    QProgressBar,
    QSizePolicy,
)
from PyQt6.QtGui import QIcon
from PyQt6.QtMultimedia import QMediaPlayer, QMediaFormat
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import Qt, QUrl, QThread, pyqtSignal
from Pipeline_Implementation.recordedVideoPipeline import pipeLinemain


class AIThread(QThread):
    # This is a signal that will be emitted when the thread is finished
    progress = pyqtSignal(
        int, str
    )  # Signal to emit progress updates (percentage and status text)
    finished = pyqtSignal(str)  # Signal to emit when the processing is complete

    def __init__(self, videoPath):
        super().__init__()
        self.videoPath = videoPath  # Path to the video file to be processed

    def reportProgress(self, value, text):
        self.progress.emit(
            value, text
        )  # Emit the progress signal with percentage and status text

    def run(self):
        # Call the `pipeLinemain` function to process the video
        # Pass the `reportProgress` method as a callback to update progress
        outputVideoPath = pipeLinemain(
            self.videoPath, progressCallback=self.reportProgress
        )
        self.finished.emit(
            outputVideoPath
        )  # Emit the finished signal with the output video path


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clear Vision Player")
        self.setGeometry(360, 200, 800, 600)
        self.setWindowIcon(QIcon("Assets/Icon.ico"))
        self.createPlayer()

    def createPlayer(self):
        self.mediaPlayer = QMediaPlayer()
        self.videoWidget = QVideoWidget()
        self.videoWidget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # Creating The Browser Video Button
        self.openBtn = QPushButton("Select Video")
        self.openBtn.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DialogOpenButton)
        )
        self.openBtn.clicked.connect(self.openFile)

        # Creating The Play Button
        self.playBtn = QPushButton("Play")
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay)
        )
        self.playBtn.clicked.connect(self.playVideo)

        # Creating The Video Slider
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.setPosition)

        # Creating The Label For the Timestamp
        self.timeStampLabel = QLabel("00:00 | 00:00")

        # Creating the Full Screen Btn
        self.fullScreenBtn = QPushButton("Full Screen")
        self.fullScreenBtn.clicked.connect(self.toggleFullScreen)

        # Creating The Stop Button
        self.stopBtn = QPushButton()
        self.stopBtn.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_MediaStop)
        )
        self.stopBtn.clicked.connect(self.mediaPlayer.stop)

        # Creating the Progress bar
        self.progressBar = QProgressBar()
        # self.progressBar
        self.progressBar.setValue(0)
        self.progressBar.setMinimumWidth(100)
        # self.progressBar.setMinimumHeight(10)
        # self.progressBar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progressLabel = QLabel("")
        self.progressLabel.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        self.progressLabel.setFixedHeight(20)  # Adjust the height to your preference

        self.progressLabel.setStyleSheet("height:20px;")
        # self.progressLabel.setStyleSheet("background-color: rgba(255, 0, 0, 100);")
        # self.progressBar.setStyleSheet("background-color: rgba(0, 255, 0, 100);")

        # Creating The Horizontal Layout
        hboxLayoutPrim = QHBoxLayout()
        hboxLayoutSec = QHBoxLayout()
        hboxLayoutPrim.setContentsMargins(0, 0, 0, 0)
        hboxLayoutSec.setContentsMargins(0, 0, 0, 0)

        # Adding The Widgets To The Horizontal Layout
        hboxLayoutSec.addWidget(self.openBtn)
        hboxLayoutSec.addWidget(self.playBtn)
        hboxLayoutSec.addWidget(self.stopBtn)
        hboxLayoutPrim.addWidget(self.timeStampLabel)
        hboxLayoutPrim.addWidget(self.slider)
        hboxLayoutSec.addWidget(self.fullScreenBtn)
        hboxLayoutSec.addWidget(self.progressBar)
        hboxLayoutSec.addWidget(self.progressLabel)

        # Creating The Vertical Layout
        vboxLayout = QVBoxLayout()
        # Adding the Stacked widget to the vertical layout
        vboxLayout.addWidget(self.videoWidget)
        # Adding the Horizontal layout to the vertical layout
        vboxLayout.addLayout(hboxLayoutPrim)
        vboxLayout.addLayout(hboxLayoutSec)
        # Don't Know What This Does
        self.mediaPlayer.setVideoOutput(self.videoWidget)

        # Setting The Main Window Layout To The Vertical Layout
        self.setLayout(vboxLayout)
        self.mediaPlayer.playbackStateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)

    def openFile(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Video")
        print(filename)  # This is just to see the file path in the console
        if filename != "":
            self.progressBar.show()
            self.progressLabel.show()

            self.workerThread = AIThread(filename)
            self.workerThread.progress.connect(self.updateProgressBar)
            self.workerThread.finished.connect(self.onProcessingDone)
            self.workerThread.start()

    def onProcessingDone(self, outputVideoPath):
        self.mediaPlayer.setSource(QUrl.fromLocalFile(outputVideoPath))
        self.progressBar.setValue(100)
        self.progressBar.setFormat("Processing Done")
        self.playBtn.setEnabled(True)

    def playVideo(self):
        if self.mediaPlayer.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.playBtn.setText("Pause")
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause)
            )
        else:
            self.playBtn.setText("Play")
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay)
            )

    def positionChanged(self, position):
        self.slider.setValue(position)
        self.updateTimeStamp()

    def durationChanged(self, duration):
        self.slider.setRange(0, duration)
        self.updateTimeStamp()

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def formatTime(self, msecs):
        # Convert the time in milliseconds to minutes and seconds
        seconds = (msecs // 1000) % 60  # 125000//1000 = 125, 125%60 = 5
        minutes = (msecs // 60000) % 60  # 125000//60000 = 2, 2%60 = 2
        return f"{minutes:02}:{seconds:02}"

    def updateTimeStamp(self):
        currentTime = self.formatTime(self.mediaPlayer.position())
        totalTime = self.formatTime(self.mediaPlayer.duration())
        self.timeStampLabel.setText(f"{currentTime} | {totalTime}")

    def toggleFullScreen(self):
        if self.isFullScreen():
            self.showNormal()
            self.fullScreenBtn.setText("Full Screen")
        else:
            self.showFullScreen()
            self.fullScreenBtn.setText("Minimize Screen")

    def updateProgressBar(self, value, text):
        self.progressBar.setValue(value)
        self.progressLabel.setText(text)


# For executing the application
app = QApplication([])
window = Window()
window.show()
sys.exit(app.exec())
