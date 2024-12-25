# code a simple text editor with cool visual effects using PyQt5

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QFileDialog, QMessageBox, QColorDialog, QToolBar,
    QTextEdit, QVBoxLayout, QWidget, QStatusBar, QLabel, QDockWidget, QTreeView, QFileSystemModel,
    QInputDialog, QMenu, QTextBrowser, QLineEdit
)
from PyQt5.QtGui import QIcon, QColor, QFont, QPixmap, QPalette, QBrush
from PyQt5.Qsci import QsciScintilla, QsciLexerPython, QsciAPIs
from PyQt5.QtCore import QRect, QPropertyAnimation, QProcess, QTimer, QTime, Qt
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
import os
import venv


class Editor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.commandEdit = None
        self.venv_dir = None
        self.process = None
        self.chatWindow = None
        self.chatDock = None
        self.projectModel = None
        self.projectTree = None
        self.timer = None
        self.venvLabel = None
        self.timeLabel = None
        self.projectDock = None
        self.statusBar = None
        self.console = None
        self.codeEditor = None
        self.initUI()

    def initUI(self):
        self.setupEditor()
        self.setupConsole()
        self.setupStatusBar()
        self.setupMenuBar()
        self.setupToolBar()
        self.setupDockWidgets()
        self.setupConsoleToolbar()
        self.setupEffects()
        self.show()

    def setupEditor(self):
        try:
            self.codeEditor = QsciScintilla(parent=self)
            lexer = QsciLexerPython(parent=self.codeEditor)
            self.codeEditor.setLexer(lexer)

            api = QsciAPIs(lexer)
            api.add("import")
            api.add("from")
            api.add("class")
            api.add("def")
            api.prepare()

            self.codeEditor.setAutoCompletionSource(QsciScintilla.AcsAll)
            self.codeEditor.setAutoCompletionCaseSensitivity(False)
            self.codeEditor.setAutoCompletionThreshold(1)
            self.codeEditor.setAutoIndent(True)
            self.codeEditor.setIndentationGuides(True)
            self.codeEditor.setIndentationWidth(4)
            self.codeEditor.setPaper(QColor("#2b2b2b"))
            self.codeEditor.setColor(QColor("#ffffff"))

            font = QFont()
            font.setFamily("Consolas")
            font.setFixedPitch(True)
            font.setPointSize(14)
            self.codeEditor.setFont(font)
            self.codeEditor.setMarginsFont(font)
            self.codeEditor.setMarginWidth(0, "0000")
            self.codeEditor.setMarginLineNumbers(0, True)
            self.codeEditor.setMarginsBackgroundColor(QColor("#313335"))
            self.codeEditor.setMarginsForegroundColor(QColor("#FFFFFF"))

            centralWidget = QWidget()
            layout = QVBoxLayout(centralWidget)
            layout.addWidget(self.codeEditor)
            self.setCentralWidget(centralWidget)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to setup editor: {e}")

    def setupConsole(self):
        try:
            self.console = QTextEdit(parent=self)
            self.console.setReadOnly(True)
            self.console.hide()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to setup console: {e}")

    def setupStatusBar(self):
        try:
            self.statusBar = QStatusBar()
            self.setStatusBar(self.statusBar)

            self.timeLabel = QLabel()
            self.venvLabel = QLabel("Venv: Not Loaded")
            self.statusBar.addPermanentWidget(self.timeLabel)
            self.statusBar.addPermanentWidget(self.venvLabel)

            self.timer = QTimer(self)
            self.timer.timeout.connect(self.updateTime)
            self.timer.start(1000)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to setup status bar: {e}")

    def setupMenuBar(self):
        try:
            menubar = self.menuBar()
            fileMenu = menubar.addMenu('&File')

            openAction = QAction(QIcon('icons/open.png'), 'Open', self)
            openAction.setShortcut('Ctrl+O')
            openAction.setStatusTip('Open new file')
            openAction.triggered.connect(self.openFile)
            fileMenu.addAction(openAction)

            saveAction = QAction(QIcon('icons/save.png'), 'Save', self)
            saveAction.setShortcut('Ctrl+S')
            saveAction.setStatusTip('Save file')
            saveAction.triggered.connect(self.saveFile)
            fileMenu.addAction(saveAction)

            createVenvAction = QAction('Create venv', self)
            createVenvAction.setStatusTip('Create virtual environment')
            createVenvAction.triggered.connect(self.createVenv)
            fileMenu.addAction(createVenvAction)

            loadVenvAction = QAction('Load venv', self)
            loadVenvAction.setStatusTip('Load virtual environment')
            loadVenvAction.triggered.connect(self.loadVenv)
            fileMenu.addAction(loadVenvAction)

            installPackageAction = QAction('Install Package', self)
            installPackageAction.setStatusTip('Install a package')
            installPackageAction.triggered.connect(self.installPackage)
            fileMenu.addAction(installPackageAction)

            listPackagesAction = QAction('List Packages', self)
            listPackagesAction.setStatusTip('List installed packages')
            listPackagesAction.triggered.connect(self.listPackages)
            fileMenu.addAction(listPackagesAction)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to setup menu bar: {e}")

    def setupToolBar(self):
        try:
            toolbar = QToolBar("Main Toolbar")
            toolbar.setMovable(False)
            self.addToolBar(Qt.TopToolBarArea, toolbar)

            openAction = QAction(QIcon('icons/open.png'), 'Open', self)
            openAction.setShortcut('Ctrl+O')
            openAction.setStatusTip('Open new file')
            openAction.triggered.connect(self.openFile)
            toolbar.addAction(openAction)

            saveAction = QAction(QIcon('icons/save.png'), 'Save', self)
            saveAction.setShortcut('Ctrl+S')
            saveAction.setStatusTip('Save file')
            saveAction.triggered.connect(self.saveFile)
            toolbar.addAction(saveAction)

            runAction = QAction(QIcon('icons/run.jpg'), 'Run', self)
            runAction.setShortcut('Ctrl+R')
            runAction.setStatusTip('Run code')
            runAction.triggered.connect(self.runCode)
            toolbar.addAction(runAction)

            debugAction = QAction(QIcon('icons/debug.jpg'), 'Debug', self)
            debugAction.setShortcut('Ctrl+D')
            debugAction.setStatusTip('Debug code')
            debugAction.triggered.connect(self.debugCode)
            toolbar.addAction(debugAction)

            darkModeAction = QAction('Dark Mode', self)
            darkModeAction.setStatusTip('Switch to dark mode')
            darkModeAction.triggered.connect(self.switchToDarkMode)
            toolbar.addAction(darkModeAction)

            lightModeAction = QAction('Light Mode', self)
            lightModeAction.setStatusTip('Switch to light mode')
            lightModeAction.triggered.connect(self.switchToLightMode)
            toolbar.addAction(lightModeAction)

            changeBgColorAction = QAction('Change Background Color', self)
            changeBgColorAction.setStatusTip('Change background color')
            changeBgColorAction.triggered.connect(self.changeBackgroundColor)

            setBgImageAction = QAction('Set Background Image', self)
            setBgImageAction.setStatusTip('Set background image')
            setBgImageAction.triggered.connect(self.setBackgroundImage)

            backgroundMenu = QMenu()
            backgroundMenu.addAction(changeBgColorAction)
            backgroundMenu.addAction(setBgImageAction)
            backgroundAction = QAction(QIcon('icons/Toolbar.jpg'), 'Background Properties', self)
            backgroundAction.setMenu(backgroundMenu)
            toolbar.addAction(backgroundAction)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to setup toolbar: {e}")

    def setupDockWidgets(self):
        try:
            self.projectDock = QDockWidget("Projects", self)
            self.projectDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
            self.projectTree = QTreeView()
            self.projectModel = QFileSystemModel()
            self.projectModel.setRootPath('')
            self.projectTree.setModel(self.projectModel)
            self.projectDock.setWidget(self.projectTree)
            self.addDockWidget(Qt.LeftDockWidgetArea, self.projectDock)

            self.chatDock = QDockWidget("AI Chat", self)
            self.chatDock.setAllowedAreas(Qt.RightDockWidgetArea)
            self.chatWindow = QTextBrowser()
            self.chatDock.setWidget(self.chatWindow)
            self.addDockWidget(Qt.RightDockWidgetArea, self.chatDock)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to setup dock widgets: {e}")

    def setupConsoleToolbar(self):
        try:
            consoleToolbar = QToolBar("Console Toolbar")
            self.addToolBar(Qt.BottomToolBarArea, consoleToolbar)
            cliAction = QAction(QIcon('icons/CLI.png'), 'Open CLI', self)
            cliAction.triggered.connect(self.openCLI)
            consoleToolbar.addAction(cliAction)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to setup console toolbar: {e}")

    def setupEffects(self):
        try:
            self.addShadowEffect()
            self.addAnimation()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to setup effects: {e}")

    def addShadowEffect(self):
        try:
            shadowEffect = QGraphicsDropShadowEffect()
            shadowEffect.setBlurRadius(15)
            shadowEffect.setXOffset(5)
            shadowEffect.setYOffset(5)
            self.codeEditor.setGraphicsEffect(shadowEffect)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add shadow effect: {e}")

    def addAnimation(self):
        try:
            animation = QPropertyAnimation(self, b"geometry")
            animation.setDuration(1000)
            animation.setStartValue(QRect(300, 300, 800, 600))
            animation.setEndValue(QRect(300, 300, 800, 600))
            animation.start()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add animation: {e}")

    def switchToDarkMode(self):
        try:
            self.codeEditor.setPaper(QColor("#2b2b2b"))
            self.codeEditor.setColor(QColor("#ffffff"))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to switch to dark mode: {e}")

    def switchToLightMode(self):
        try:
            self.codeEditor.setPaper(QColor("#ffffff"))
            self.codeEditor.setColor(QColor("#000000"))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to switch to light mode: {e}")

    def updateTime(self):
        try:
            currentTime = QTime.currentTime().toString('hh:mm:ss')
            self.timeLabel.setText(currentTime)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update time: {e}")

    def openFile(self):
        try:
            filename, _ = QFileDialog.getOpenFileName(self, 'Open file', '/home')
            if filename:
                with open(filename, 'r') as f:
                    file = f.read()
                    self.codeEditor.setText(file)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open file: {e}")

    def saveFile(self):
        try:
            filename, _ = QFileDialog.getSaveFileName(self, 'Save file', '/home')
            if filename:
                with open(filename, 'w') as f:
                    text = self.codeEditor.text()
                    f.write(text)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file: {e}")

    def createVenv(self):
        try:
            venv_dir = QFileDialog.getExistingDirectory(self, 'Select Directory for Virtual Environment')
            if venv_dir:
                venv.create(venv_dir, with_pip=True)
                QMessageBox.information(self, 'Virtual Environment', f'Virtual environment created at {venv_dir}')
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create virtual environment: {e}")

    def loadVenv(self):
        try:
            self.venv_dir = QFileDialog.getExistingDirectory(self, 'Select Virtual Environment Directory')
            if self.venv_dir:
                self.venvLabel.setText(f"Venv: {self.venv_dir}")
                QMessageBox.information(self, 'Virtual Environment', f'Virtual environment loaded from {self.venv_dir}')
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load virtual environment: {e}")

    def installPackage(self):
        try:
            if not self.venv_dir:
                QMessageBox.warning(self, 'Error', 'No virtual environment loaded.')
                return
            package, ok = QInputDialog.getText(self, 'Install Package', 'Enter package name:')
            if ok and package:
                self.console.clear()
                self.console.show()
                self.process = QProcess(self)
                self.process.setProcessChannelMode(QProcess.MergedChannels)
                self.process.readyReadStandardOutput.connect(self.updateConsole)
                self.process.finished.connect(self.processFinished)
                self.process.start(f"{self.venv_dir}/bin/pip", ["install", package])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to install package: {e}")

    def listPackages(self):
        try:
            if not self.venv_dir:
                QMessageBox.warning(self, 'Error', 'No virtual environment loaded.')
                return
            self.console.clear()
            self.console.show()
            self.process = QProcess(self)
            self.process.setProcessChannelMode(QProcess.MergedChannels)
            self.process.readyReadStandardOutput.connect(self.updateConsole)
            self.process.finished.connect(self.processFinished)
            self.process.start(f"{self.venv_dir}/bin/pip", ["list"])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to list packages: {e}")

    def runCode(self):
        try:
            self.console.clear()
            self.console.show()
            code = self.codeEditor.text()
            self.process = QProcess(self)
            self.process.setProcessChannelMode(QProcess.MergedChannels)
            self.process.readyReadStandardOutput.connect(self.updateConsole)
            self.process.finished.connect(self.processFinished)
            self.process.start("python", ["-c", code])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to run code: {e}")

    def debugCode(self):
        try:
            self.console.clear()
            self.console.show()
            code = self.codeEditor.text()
            self.process = QProcess(self)
            self.process.setProcessChannelMode(QProcess.MergedChannels)
            self.process.readyReadStandardOutput.connect(self.updateConsole)
            self.process.finished.connect(self.processFinished)
            self.process.start("python", ["-m", "pdb", "-c", code])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to debug code: {e}")

    def changeBackgroundColor(self):
        try:
            color = QColorDialog.getColor()
            if color.isValid():
                self.codeEditor.setPaper(color)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to change background color: {e}")

    def setBackgroundImage(self):
        try:
            imagePath, _ = QFileDialog.getOpenFileName(self, 'Select Background Image', '', 'Images (*.png *.jpg *.bmp)')
            if imagePath:
                palette = QPalette()
                palette.setBrush(QPalette.Base, QBrush(QPixmap(imagePath)))
                self.codeEditor.setPalette(palette)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to set background image: {e}")

    def openCLI(self):
        try:
            self.console.clear()
            self.console.show()
            self.process = QProcess(self)
            self.process.setProcessChannelMode(QProcess.MergedChannels)
            self.process.readyReadStandardOutput.connect(self.updateConsole)
            self.process.finished.connect(self.processFinished)
            self.process.start("cmd.exe")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open CLI: {e}")

    def runCommand(self):
        try:
            self.commandEdit = QLineEdit()
            self.commandEdit.setPlaceholderText('Enter command')
            self.commandEdit.returnPressed.connect(self.executeCommand)
            self.setCentralWidget(self.commandEdit)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to run command: {e}")

    def executeCommand(self):
        try:
            command = self.commandEdit.text()
            self.process.start(command)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to execute command: {e}")

    def updateConsole(self):
        try:
            output = self.process.readAllStandardOutput().data().decode()
            self.console.append(output)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update console: {e}")

    def processFinished(self):
        try:
            self.console.append("Process finished with exit code 0")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to handle process finish: {e}")

    def closeEvent(self, event):
        try:
            reply = QMessageBox.question(self, 'Message', 'Are you sure you want to quit?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to handle close event: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = Editor()
    sys.exit(app.exec_())
