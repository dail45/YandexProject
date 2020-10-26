import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QSystemTrayIcon, QAction, QMenu, qApp
import win32api


class MainWindow(QtWidgets.QWidget):
    qss = '''
    QWidget {
        background-color: #222222;
        color: #BBBBBB;
        border-color: #BBBBBB;
    } 
    ::tab {
        background: rgb(0, 0, 0);
        color: white;
    } 
    ::tab:selected {
        background-color: rgb(50, 50, 50);
        color: #BBBBBB;
    } 
    QTabWidget::pane {
        border-top: 2px solid #C2C7CB;
    }
    QPushButton {
        background-color: rgb(255, 255, 255);
        color: #000000;
    }
    QHeaderView::section {
        background: rgb(0, 0, 0);
        color: white;
    }
    '''

    def __init__(self):
        super().__init__()
        self.oldPos = self.pos()
        self.setupUi()

    def setupUi(self):
        self.resize(411, 560)
        self.setStyleSheet(self.qss)
        self.setMinimumSize(232, 250)
        self.system_icon = QtGui.QIcon("TrayIcon.png")
        self.setWindowIcon(self.system_icon)
        self.setWindowTitle("Будильники и часы")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QtWidgets.QTabWidget()
        self.tabWidget.setIconSize(QtCore.QSize(30, 30))
        self.tabWidget.setDocumentMode(True)
        self.tab = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab, QtGui.QIcon("b.png"), "Будильник")
        self.tab_2 = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab_2, QtGui.QIcon("m.png"), "Часы")
        self.tab_3 = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab_3, QtGui.QIcon("t.png"), "Таймер")
        self.tab_4 = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab_4, QtGui.QIcon("s.png"), "Секундомер")

        self.verticalLayout.addWidget(self.tabWidget)

        self.alarm_table_widget = QtWidgets.QTableWidget(self.tab)
        self.alarm_table_widget.resize(QtCore.QSize(411, 480))
        self.alarm_table_widget.setColumnCount(4)
        self.alarm_table_widget.setRowCount(1)
        self.alarm_table_widget.setHorizontalHeaderLabels(
            ["Название", "Время", "Милодия", "Состояние"])

        self.timer_table_widget = QtWidgets.QTableWidget(self.tab_3)
        self.timer_table_widget.resize(QtCore.QSize(411, 480))
        self.timer_table_widget.setColumnCount(5)
        self.timer_table_widget.setRowCount(0)
        self.timer_table_widget.setHorizontalHeaderLabels(
            ["Название", "Время", "Ост. Время", "Милодия", "Состояние"])

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QtGui.QIcon("TrayIcon.png"))
        self.show_action = QAction("Показать", self)
        self.quit_action = QAction("Закрыть", self)
        self.hide_action = QAction("Спрятать", self)
        self.show_action.triggered.connect(self.show)
        self.hide_action.triggered.connect(self.hide)
        self.quit_action.triggered.connect(qApp.quit)
        self.tray_menu = QMenu()
        self.tray_menu.addAction(self.hide_action)
        self.tray_menu.addAction(self.quit_action)
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

    def fun(self, state):
        sender = self.sender()
        if state:
            sender.setIcon(QtGui.QIcon("onbtn.png"))
        else:
            sender.setIcon(QtGui.QIcon("offbtn.png"))

    def settrayFunctions(self):
        self.tray_menu.addAction(self.quit_action)

    def trayEvent(self, a):
        if a:
            self.tray_menu.clear()
            self.tray_menu.addAction(self.show_action)
        else:
            self.tray_menu.clear()
            self.tray_menu.addAction(self.hide_action)
        self.settrayFunctions()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        x, y = self.size().width(), self.size().height()
        if x < 411:
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), "")
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), "")
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), "")
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), "")
            self.alarm_table_widget.resize(x, self.alarm_table_widget.size().height())
            self.timer_table_widget.resize(x, self.timer_table_widget.size().height())
        elif x >= 411:
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), "Будильник")
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), "Часы")
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), "Таймер")
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), "Секундомер")
            self.alarm_table_widget.resize(x, self.alarm_table_widget.size().height())
            self.timer_table_widget.resize(x, self.timer_table_widget.size().height())
        if y >= 480 + 80:
            self.alarm_table_widget.resize(self.alarm_table_widget.size().width(), 480)
            self.timer_table_widget.resize(self.timer_table_widget.size().width(), 480)
        elif y < 480 + 80:
            self.alarm_table_widget.resize(self.alarm_table_widget.size().width(), y - 80)
            self.timer_table_widget.resize(self.timer_table_widget.size().width(), y - 80)

    def hideEvent(self, a0: QtGui.QHideEvent) -> None:
        self.trayEvent(True)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.trayEvent(False)

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint(event.globalPos() - self.oldPos)
        # print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())
