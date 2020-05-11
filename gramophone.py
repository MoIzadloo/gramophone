from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
from glob import glob
from io import BytesIO
import mutagen.mp3
from PIL import Image
from PyQt5.QtGui import *
import pygame
from threading import Thread
from time import sleep

global clicked
clicked = False

class PicButton(QtWidgets.QAbstractButton):
    def __init__(self, pixmap, pixmap_pressed, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap
        self.pixmap_pressed = pixmap_pressed

        self.pressed.connect(self.update)
        self.released.connect(self.update)

    def paintEvent(self, event):
        pix = self.pixmap
        if clicked:
            pix = self.pixmap_pressed
        self.update()
        painter = QtGui.QPainter(self)
        painter.drawPixmap(event.rect(), pix)

    def enterEvent(self, event):
        self.update()

    def leaveEvent(self, event):
        self.update()

    def sizeHint(self):
        return QtCore.QSize(50, 50)



class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self,main_window):
        super().__init__()
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.main_window = main_window
        self.musics_path = self.path + "/musics"
        os.makedirs(self.musics_path, exist_ok=True)
        self.music_paths = glob(self.musics_path + "/*.mp3")
        self.music_names = list(map(lambda item: item.replace(self.musics_path + "\\","").replace(".mp3","").replace("/","") ,self.music_paths))
        self.pict = list(map(lambda item: self.apic_extract(item),self.music_paths))
        self.legths =  list(map(lambda item: self.get_lenght(item),self.music_paths))
        self.labels = []
        self.buttons = []
    

        # self.album_images = list(map(lambda item: item.get("APIC:").data , self.tags))
    def get_lenght(self,mp3):
        song = mutagen.mp3.Open(mp3)
        return song.info.length

    def apic_extract(self,mp3):
        try:
            tags = mutagen.mp3.Open(mp3)
        except:
            return False
        data = ""
        for i in tags:
            if i.startswith("APIC"):
                data = tags[i].data
                break
        if not data:
            return None
        return data


    def setupUi(self):
        self.main_window.setObjectName("gramophone")
        self.main_window.resize(593, 523)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.path  + "/res/vinyl.ico"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.main_window.setWindowIcon(icon)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.main_window.setPalette(palette)
        self.widget = QtWidgets.QWidget(self.main_window)
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.logo = QtWidgets.QLabel(self.widget)
        self.logo.setMaximumSize(QtCore.QSize(200, 200))
        self.logo.setAutoFillBackground(False)
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap(self.path + "/res/vinyl-record.png"))
        self.logo.setScaledContents(True)
        self.logo.setObjectName("logo")
        self.horizontalLayout_2.addWidget(self.logo)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.album_img = QtWidgets.QLabel(self.widget)
        self.album_img.setMaximumSize(QtCore.QSize(200, 16777215))
        self.album_img.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.album_img.setText("")
        self.album_img.setScaledContents(False)
        self.album_img.setObjectName("album_img")
        self.horizontalLayout_2.addWidget(self.album_img)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        previous_pix = QtGui.QPixmap(self.path + "/res/previous.png")
        self.back = PicButton(previous_pix,previous_pix, self)
        self.horizontalLayout.addWidget(self.back)
        pause_pix = QtGui.QPixmap(self.path  + "/res/pause.png")
        play_pix = QtGui.QPixmap(self.path + "/res/play.png")
        self.play = PicButton(play_pix,pause_pix, self)
        self.horizontalLayout.addWidget(self.play)
        next_pix = QtGui.QPixmap(self.path + "/res/next.png")
        self.next = PicButton(next_pix,next_pix, self)
        self.horizontalLayout.addWidget(self.next)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.gridLayout_2.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.scrollArea = QtWidgets.QScrollArea(self.widget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.scrollArea.setFont(font)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 569, 232))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_3.setObjectName("gridLayout_3")
        for i in range(0,len(self.music_names)):
            label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            label.setFont(font)
            label.setTextFormat(QtCore.Qt.RichText)
            label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
            label.setObjectName("label_{}".format(i))
            self.labels.append(label)
            self.gridLayout_3.addWidget(label, i, 0, 1, 1)
            play_pix = QtGui.QPixmap(self.path + "/res/play.png")
            btn =  PicButton(play_pix,play_pix, self)
            btn.setMaximumSize(QtCore.QSize(40, 40))
            self.buttons.append(btn)
            self.gridLayout_3.addWidget(btn, i, 1, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 1, 0, 1, 1)
        self.main_window.setCentralWidget(self.widget)
        self.music = None

        self.retranslateUi(self.main_window)
        QtCore.QMetaObject.connectSlotsByName(self.main_window)
        for btn in self.buttons:
            btn.clicked.connect(lambda _, b=btn: self.btn_musics(btn=b))
        self.play.clicked.connect(self.play_btn)
        self.next.clicked.connect(self.next_music)
        self.back.clicked.connect(self.previous_music)


    def previous_music(self):
        try:
            previous_song = self.music - 1
            if previous_song < 0:
                previous_song = len(self.music_paths) - 1
            try:
                image = Image.open(BytesIO(self.pict[previous_song])).resize([200,190])
                image.save(self.path + "/res/album.jpg")
                self.album_img.setPixmap(QtGui.QPixmap(self.path + "/res/album.jpg"))
            except:
                self.album_img.setPixmap(QtGui.QPixmap(self.path + "/res/vinyl.png"))
            self.update_background(previous_song)
            pygame.mixer.init()
            pygame.mixer.music.load(self.music_paths[previous_song])
            pygame.mixer.music.play(0)
            self.music = previous_song
        except:
            try:
                try:
                    image = Image.open(BytesIO(self.pict[0])).resize([200,190])
                    image.save(self.path + "/res/album.jpg")
                    self.album_img.setPixmap(QtGui.QPixmap(self.path + "/res/album.jpg"))
                except:
                    self.album_img.setPixmap(QtGui.QPixmap(self.path + "/res/vinyl.png"))
                self.update_background(0)
                pygame.mixer.init()
                pygame.mixer.music.load(self.music_paths[0])
                pygame.mixer.music.play(0)
                self
                self.music = 0
            except:
                self.empty_folder()


    def next_music(self):
        try:
            next_song = self.music + 1
            if next_song >= len(self.music_names):
                next_song = 0
    
            try:
                image = Image.open(BytesIO(self.pict[next_song])).resize([200,190])
                image.save(self.path + "/res/album.jpg")
                self.album_img.setPixmap(QtGui.QPixmap(self.path + "/res/album.jpg"))
            except:
                self.album_img.setPixmap(QtGui.QPixmap(self.path + "/res/vinyl.png"))
            self.update_background(next_song)
            pygame.mixer.init()
            pygame.mixer.music.load(self.music_paths[next_song])
            pygame.mixer.music.play(0)
            self.music = next_song
        except:
            try:
                try:
                    image = Image.open(BytesIO(self.pict[0])).resize([200,190])
                    image.save(self.path + "/res/album.jpg")
                    self.album_img.setPixmap(QtGui.QPixmap(self.path + "/res/album.jpg"))
                except:
                    self.album_img.setPixmap(QtGui.QPixmap(self.path + "/res/vinyl.png"))
                self.update_background(0)
                pygame.mixer.init()
                pygame.mixer.music.load(self.music_paths[0])
                pygame.mixer.music.play(0)
                self.music = 0
            except :
                self.empty_folder()

    
    def update_background(self,idx):
        for label in self.labels:
            if self.labels.index(label) == idx:
                label.setStyleSheet("background-color: white")
                label.update()
            else:
                label.setStyleSheet("")
                label.update()


    def btn_musics(self,btn):
        global clicked
        clicked = True
        self.play.update()
        idx = self.buttons.index(btn)
        try:
            image = Image.open(BytesIO(self.pict[idx])).resize([200,190])
            image.save(self.path + "/res/album.jpg")
            self.album_img.setPixmap(QtGui.QPixmap(self.path + "/res/album.jpg"))
        except:
            self.album_img.setPixmap(QtGui.QPixmap(self.path + "/res/vinyl.png"))
        self.update_background(idx)
        pygame.mixer.init()
        pygame.mixer.music.load(self.music_paths[idx])
        pygame.mixer.music.play(0)
        self.music = idx

    def empty_folder(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setWindowIcon(QtGui.QIcon(self.path  + "/res/vinyl.ico"))
        msg.setWindowTitle('no file!')
        msg.setText('add your musics into musics folder!')
        msg.exec_()
  


    def play_btn(self):
        global clicked
        clicked = not clicked
        if clicked == False:
            pygame.mixer.music.pause()
        else:
            try:
                pygame.mixer.music.unpause()
            except :
                try:
                    try:
                        image = Image.open(BytesIO(self.pict[0])).resize([200,190])
                        image.save(self.path + "/res/album.jpg")
                        self.album_img.setPixmap(QtGui.QPixmap(self.path + "/res/album.jpg"))
                    except:
                        self.album_img.setPixmap(QtGui.QPixmap(self.path + "/res/vinyl.png"))
                    self.update_background(0)
                    pygame.mixer.init()
                    pygame.mixer.music.load(self.music_paths[0])
                    pygame.mixer.music.play(0)
                    self.music = 0
                except:
                    self.empty_folder()


    



        


    def retranslateUi(self,main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "gramophone"))
        for idx,lable in enumerate(self.labels):
            lable.setText(_translate("main_window", self.music_names[idx]))
  



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(main_window)
    ui.setupUi()
    main_window.show()
    sys.exit(app.exec_())
