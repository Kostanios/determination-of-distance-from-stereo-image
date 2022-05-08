from PIL import Image
from PyQt5.QtCore import Qt, QPoint, QRect, QLine
from PyQt5.QtGui import QImage, QPixmap, QPalette, QPainter, QPen
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import QLabel, QSizePolicy, QScrollArea, QMessageBox, QMainWindow, QMenu, QAction, \
    qApp, QFileDialog, QDockWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QWidget, QRadioButton
from numpy import asarray

from calculateDistance import calculate_distance
from getCombineDelta import get_combune_delta
from getDelta import get_delta

class QImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.image = QImage()
        self.imageCopy = QImage()
        self.printer = QPrinter()
        self.scaleFactor = 0.0
        self.painter = QPainter()

        self.main_img_array = []
        self.second_img_array = []

        self.dockWidget = QDockWidget('info', self)

        self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)
        self.imageLabel.mousePressEvent = self.iMousePressEvent
        self.imageLabel.mouseMoveEvent = self.iMouseMoveEvent
        self.imageLabel.mouseReleaseEvent = self.iMouseReleaseEvent

        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setVisible(False)

        self.setCentralWidget(self.scrollArea)

        self.distanceRadio = QRadioButton('distance')
        self.sizeRadio = QRadioButton('size')
        self.focus_edit = QLineEdit()
        self.matrix_width = QLineEdit()
        self.matrix_height = QLineEdit()
        self.camera_delta = QLineEdit()
        self.pixel_size = QLineEdit()
        self.submit_camera = QPushButton('calculate distance')
        self.distance = QLabel('undefined')
        self.submit_camera.mousePressEvent = self.mousePressSubmitCamera

        self.DockInit()

        self.createActions()
        self.createMenus()

        self.setWindowTitle("Image Viewer")

        self.pix = QPixmap()

        self.begin, self.destination = QPoint(), QPoint()

        self.pixel_delta = 1
        self.combine_pixel_delta = 1

    def mousePressSubmitCamera(self, event) -> None:
        if self.distanceRadio.isChecked():
            self.distance.setText(str(calculate_distance(
                self.camera_delta.text(),
                self.pixel_delta,
                self.focus_edit.text(),
                [
                    self.matrix_width.text(),
                    self.matrix_height.text()
                ],
                self.pixel_size.text()
            )))

    def iMousePressEvent(self, event) -> None:
        if event.buttons() & Qt.LeftButton:
            self.begin = event.pos()
            self.destination = self.begin
            self.update()

    def iMouseMoveEvent(self, event) -> None:
        if event.buttons() & Qt.LeftButton:
            self.destination = event.pos()
            self.update()

    def iMouseReleaseEvent(self, event) -> None:
        if self.distanceRadio.isChecked():
            self.pixel_delta = get_delta(self.begin, self.destination, self.main_img_array, self.second_img_array)
        if self.sizeRadio.isChecked():
            self.combine_pixel_delta = get_combune_delta(
                self.begin, self.destination,
                self.main_img_array, self.second_img_array)

        if event.buttons() & Qt.LeftButton:
            self.destination, self.begin = QPoint(), QPoint()
            self.update()


    def paintEvent(self, event):
        QMainWindow.paintEvent(self, event)
        if not self.begin.isNull() and not self.destination.isNull():
            rect = QRect(self.begin, self.destination)
            line = QLine(self.begin, self.destination)

            painter = self.painter
            self.pix = QPixmap.fromImage(self.imageCopy)

            painter.drawPixmap(QPoint(), self.pix)
            painter.setPen(QPen(Qt.black, 1, Qt.SolidLine,
                                Qt.RoundCap, Qt.RoundJoin))
            if self.distanceRadio.isChecked():
                painter.drawRect(rect.normalized())

            if self.sizeRadio.isChecked():
                painter.drawLine(line)

        self.imageLabel.setPixmap(QPixmap.fromImage(self.image))

    def open(self):
        options = QFileDialog.Options()
        # fileName = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath())
        self.fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                  'Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)
        self.fileName2, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                  'Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)
        if self.fileName:
            self.image = QImage(self.fileName)
            self.imageCopy = QImage(self.fileName)

            self.painter = QPainter(self.image)

            self.main_img_array = asarray(Image.open(self.fileName))
            self.second_img_array = asarray(Image.open(self.fileName2))

            if self.image.isNull():
                QMessageBox.information(self, "Image Viewer", "Cannot load %s." % self.fileName)
                return

            self.imageLabel.setPixmap(QPixmap.fromImage(self.image))

            self.scrollArea.setVisible(True)
            self.printAct.setEnabled(True)
            self.fitToWindowAct.setEnabled(True)
            self.updateActions()

            if not self.fitToWindowAct.isChecked():
                self.imageLabel.adjustSize()

    def print_(self):
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
            painter = QPainter(self.printer)
            rect = painter.viewport()
            size = self.imageLabel.pixmap().size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.imageLabel.pixmap().rect())
            painter.drawPixmap(0, 0, self.imageLabel.pixmap())

    def zoomIn(self):
        self.imageLabel.adjustSize()
        self.scaleImage(1.25)

    def zoomOut(self):
        self.imageLabel.adjustSize()
        self.scaleImage(0.8)

    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()

        self.updateActions()

    def about(self):
        QMessageBox.about(self, "About Work",
          "<p>the work was done by Konstantin Maksimovich Kotov</p>"
        )

    def createActions(self):
        self.openAct = QAction("&Open...", self, shortcut="Ctrl+O", triggered=self.open)
        self.printAct = QAction("&Print...", self, shortcut="Ctrl+P", enabled=False, triggered=self.print_)
        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)
        self.zoomInAct = QAction("Zoom &In (25%)", self, shortcut="Ctrl++", enabled=False, triggered=self.zoomIn)
        self.zoomOutAct = QAction("Zoom &Out (25%)", self, shortcut="Ctrl+-", enabled=False, triggered=self.zoomOut)
        self.normalSizeAct = QAction("&Normal Size", self, shortcut="Ctrl+S", enabled=False, triggered=self.normalSize)
        self.fitToWindowAct = QAction("&Fit to Window", self, enabled=False, checkable=True, shortcut="Ctrl+F", triggered=self.fitToWindow)
        self.aboutAct = QAction("&About", self, triggered=self.about)
        self.aboutQtAct = QAction("About &Qt", self, triggered=qApp.aboutQt)

    def createMenus(self):
        self.fileMenu = QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.viewMenu = QMenu("&View", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)

        self.helpMenu = QMenu("&Help", self)
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.viewMenu)
        self.menuBar().addMenu(self.helpMenu)

    def updateActions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)
    def DockInit(self):
        camera_info_widget = QVBoxLayout()

        mode_widget = QHBoxLayout()
        mode_label = QLabel('choose application calculate mode')
        mode_widget.addWidget(mode_label)
        self.distanceRadio.setChecked(True)
        mode_widget.addWidget(self.distanceRadio)
        mode_widget.addWidget(self.sizeRadio)

        focus_widget = QHBoxLayout()
        focus_label = QLabel('focus 1/f')
        focus_widget.addWidget(focus_label)
        focus_widget.addWidget(self.focus_edit)

        matrix_width_widget = QHBoxLayout()
        matrix_width_label = QLabel('matrix width (mm)')
        matrix_width_widget.addWidget(matrix_width_label)
        matrix_width_widget.addWidget(self.matrix_width)

        matrix_height_widget = QHBoxLayout()
        matrix_height_label = QLabel('matrix height (mm)')
        matrix_height_widget.addWidget(matrix_height_label)
        matrix_height_widget.addWidget(self.matrix_height)

        camera_delta_widget = QHBoxLayout()
        camera_delta_label = QLabel('camera delta (mm)')
        camera_delta_widget.addWidget(camera_delta_label)
        camera_delta_widget.addWidget(self.camera_delta)

        pixel_size_widget = QHBoxLayout()
        pixel_size_label = QLabel('pixel size (mm)')
        pixel_size_widget.addWidget(pixel_size_label)
        pixel_size_widget.addWidget(self.pixel_size)

        distance_widget = QHBoxLayout()
        distance_widget_label = QLabel('distance (mm)')
        distance_widget.addWidget(distance_widget_label)
        distance_widget.addWidget(self.distance)

        camera_info_widget.addLayout(mode_widget)
        camera_info_widget.addLayout(focus_widget)
        camera_info_widget.addLayout(matrix_width_widget)
        camera_info_widget.addLayout(matrix_height_widget)
        camera_info_widget.addLayout(camera_delta_widget)
        camera_info_widget.addLayout(pixel_size_widget)
        camera_info_widget.addLayout(distance_widget)
        camera_info_widget.addWidget(self.submit_camera)

        dockedWidget = QWidget()

        self.dockWidget.setWidget(dockedWidget)
        self.dockWidget.setFloating(False)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dockWidget)
        dockedWidget.setLayout(camera_info_widget)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                               + ((factor - 1) * scrollBar.pageStep() / 2)))



import sys
from PyQt5.QtWidgets import QApplication

def app():
    app = QApplication(sys.argv)
    imageViewer = QImageViewer()
    imageViewer.showMaximized()
    sys.exit(app.exec_())
