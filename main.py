from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from gui.mainWindowGUI import Ui_MainWindow
import sys
import os
from gui.lib import *
from ploter import *

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Main window of the application. Contains all global parameters of the GUI application.
    """

    def __init__(self, parent=None):
        """
        Initializes the main window and sets up the entire GUI application.
        :param parent: No parent
        :return: None
        """
        # Initiate parent class
        super(MainWindow, self).__init__(parent)

        # Setup GUI
        self.setupUi(self)
        self.setWindowIcon(QIcon('./img/icon.ico'))
        self.setGeometry(100, 100, 400, 400)
        self.statusBar()
        self.change_qss('actionDarkBlue')

        # Connections
        self.addBtn.clicked.connect(self.add)
        self.removeBtn.clicked.connect(self.remove)
        self.plotBtn.clicked.connect(self.plot)
        self.upBtn.clicked.connect(self.up)
        self.downBtn.clicked.connect(self.down)


    def change_qss(self, theme):
        themes = {'actionAqua': './gui/css/aqua/aqua.qss',
                  'actionBasicWhite': './gui/css/basicWhite/basicWhite.qss',
                  'actionBlueGlass': './gui/css/blueGlass/blueGlass.qss',
                  'actionDarcula': './gui/css/darcula/darcula.qss',
                  'actionDark': './gui/css/dark/darkstyle.qss',
                  'actionDarkBlue': './gui/css/darkBlue/style.qss',
                  'actionDarkBlueFreeCAD': './gui/css/darkBlue(FreeCAD)/stylesheet.qss',
                  'actionDarkGreen': './gui/css/darkGreen/darkGreen.qss',
                  'actionDarkGreenFreeCAD': './gui/css/darkGreen(FreeCAD)/stylesheet.qss',
                  'actionDarkOrange': './gui/css/darkOrange/darkOrange.qss',
                  'actionDarkOrangeFreeCAD': './gui/css/darkOrange(FreeCAD)/stylesheet.qss',
                  'actionLight': './gui/css/light/light.qss',
                  'actionLightBlueFreeCAD': './gui/css/lightBlue(FreeCAD)/stylesheet.qss',
                  'actionLightGreenFreeCAD': './gui/css/lightGreen(FreeCAD)/stylesheet.qss',
                  'actionLightOrangeFreeCAD': './gui/css/lightOrange(FreeCAD)/stylesheet.qss',
                  'actionMachinery': './gui/css/machinery/machinery.qss',
                  'actionMinimalist': './gui/css/minimalist/Minimalist.qss',
                  'actionNightMapping': './gui/css/nightMapping/style.qss',
                  'actionWombat': './gui/css/wombat/stylesheet.qss',
                  }
        # for i in themes.keys():
        #     eval('self.{}.setChecked(False)'.format(i))
        # eval('self.{}.setChecked(True)'.format(theme))

        qss = open_qss(themes[theme])
        app.setStyleSheet(qss)

    def add(self):
        last = self.tableWidget.rowCount()
        self.tableWidget.insertRow(last)
        filename = QFileDialog.getOpenFileName(self, 'Open File', './save', filter="CSV File (*.csv)")[0]
        self.tableWidget.setItem(last, 0, QTableWidgetItem(filename))
        self.tableWidget.setItem(last, 1, QTableWidgetItem(f'Label {last + 1}'))
        self.tableWidget.setItem(last, 2, QTableWidgetItem('Automatic'))

    def remove(self):
        selected = self.tableWidget.currentRow()
        self.tableWidget.removeRow(selected)

    def plot(self):
        plotList = []
        plt.clf()
        rowCount = self.tableWidget.rowCount()
        for i in range(rowCount):
            filename = get_text(self.tableWidget.item(i, 0))
            label = get_text(self.tableWidget.item(i, 1))
            color = get_text(self.tableWidget.item(i, 2))
            if color == 'Automatic':
                color = None

            plotList.append(read_csv(filename, label, color))

        xlabel = get_text(self.xlabelLE)
        ylabel = get_text(self.ylabelLE)
        title = get_text(self.titleLE)
        grid = self.gridCB.isChecked()
        legend = self.legendCB.isChecked()
        plot(plotList, xlabel=xlabel, ylabel=ylabel, title=title, grid=grid, legend=legend)

    def up(self):
        current = self.tableWidget.currentRow()
        file = get_text(self.tableWidget.item(current, 0))
        label = get_text(self.tableWidget.item(current, 1))
        color = get_text(self.tableWidget.item(current, 2))
        try:
            self.tableWidget.insertRow(current-1)
            self.tableWidget.setItem(current - 1, 0, QTableWidgetItem(file))
            self.tableWidget.setItem(current - 1, 1, QTableWidgetItem(label))
            self.tableWidget.setItem(current - 1, 2, QTableWidgetItem(color))
            self.tableWidget.removeRow(current + 1)
        except:
            pass

    def down(self):
        current = self.tableWidget.currentRow()
        file = get_text(self.tableWidget.item(current, 0))
        label = get_text(self.tableWidget.item(current, 1))
        color = get_text(self.tableWidget.item(current, 2))
        try:
            if current + 2 > self.tableWidget.rowCount():
                raise Exception
            self.tableWidget.insertRow(current + 2)
            self.tableWidget.setItem(current + 2, 0, QTableWidgetItem(file))
            self.tableWidget.setItem(current + 2, 1, QTableWidgetItem(label))
            self.tableWidget.setItem(current + 2, 2, QTableWidgetItem(color))
            self.tableWidget.removeRow(current)
        except:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec_())