import sys
import os
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QInputDialog, QMessageBox, QListWidgetItem
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
import yt_dlp

class Programm(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("maket.ui", self)

        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)

        self.player.setVideoOutput(self.video_widget)
        self.video_widget.hide()

        self.btn_new.clicked.connect(self.new_video)
        self.folders_list.itemDoubleClicked.connect(self.play_video)
        self.btn_new.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_settings.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.colections_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.folders_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def resizeEvent(self, _):
        width = self.width()
        height = self.height()

        self.colections_list.setGeometry(10, 50, 260, height - 110)
        self.folders_list.setGeometry(290, 55, width - 300, height - 65)
        self.btn_settings.setGeometry(10, height - 60, 40, 40)
        self.search_line.setGeometry(290, 10, width - 300, 35)
        self.btn_new.setGeometry(width - 70, height - 70, 50, 50)
        self.video_widget.setGeometry(0, 0, width, height)

    def new_video(self):
        url, ok = QInputDialog.getText(self, "Скачать видео", "Вставьте ссылку на видео")

        if ok and url:
            try:
                ydl_opts = {
                    "format": "bestvideo+bestaudio/best",
                    "outtmpl": os.path.join(os.path.join(os.getcwd(), "downloads"), "%(title)s.%(ext)s"),
                    "merge_output_format": "mp4",
                    "ffmpeg_location": os.getcwd(),
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=True)
                    video_name = info_dict.get("title")
                    local_file_path = ydl.prepare_filename(info_dict)

                    base, _ = os.path.splitext(local_file_path)
                    local_file_path = base + ".mp4"

                item = QListWidgetItem(video_name)
                item.setData(Qt.ItemDataRole.UserRole, local_file_path)

                self.folders_list.addItem(item)
                QMessageBox.information(self, "Найс", f"Видео {video_name} успешно скачано!")
            except Exception:
                pass

    def play_cliked_video(self, item):
        local_path = item.data(Qt.ItemDataRole.UserRole)
        if local_path and os.path.exists(local_path):
            self.play_video(local_path)

    def play_video(self, file_path):
            self.colections_list.hide()
            self.btn_settings.hide()
            self.search_line.hide()
            self.btn_new.hide()
            self.folders_list.hide()
            self.video_widget.show()

            self.player.setSource(QUrl.fromLocalFile(file_path))
            self.audio_output.setVolume(0.67)
            self.player.play()
            self.setFocus()

    def keyPressEvent(self, event):
            if event.key() == Qt.Key.Key_Escape:
                self.player.stop()
                self.video_widget.hide()

                self.colections_list.show()
                self.folders_list.show()
                self.search_line.show()
                self.btn_new.show()
                self.btn_settings.show()

            if event.key() == Qt.Key.Key_Space:
                if self.video_widget.isVisible():
                    if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
                        self.player.pause()
                    else:
                        self.player.play()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Programm()
    ex.show()
    sys.exit(app.exec())