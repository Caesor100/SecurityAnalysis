import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt

import xlwt, xlrd

from settings import Settings
from message_bar import MessageBar
from company_details import CompanyDetails
from fundamental_analysis import FundamentalAnalysis
from search_info import SearchInfo


class Validator(QtGui.QValidator):
    def validate(self, string, pos):
        return QtGui.QValidator.Acceptable, string.upper(), pos


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.file_name = None
        self.initUI(self)

    def initUI(self, MainWindow):
        settings = Settings()
        self.company_details = CompanyDetails()

        dates = settings.dates
        row_label = settings.get_list_of_financial_performance_items()

        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(settings.screen_width, settings.screen_height)
        self.setWindowTitle('Security Analysis ' + settings.version)
        self.setWindowIcon(QtGui.QIcon('img/graph.png'))

        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.resize(settings.table_width, settings.table_height)

        width_table = self.centralWidget.width()

        distance_from_table = settings.distance_from_table
        distance_between_items = settings.distance_between_items

        vbox = QtWidgets.QVBoxLayout(self.centralWidget)
        self.TableWidget = QtWidgets.QTableWidget()
        vbox.addWidget(self.TableWidget)
        self.TableWidget.setColumnCount(len(dates))
        self.TableWidget.setRowCount(len(row_label))

        self.line_input_ticker = QtWidgets.QLineEdit(self)
        self.line_input_ticker.move(width_table + distance_from_table, 32)
        line_width = width_table + self.line_input_ticker.width()
        self.line_input_ticker.resize(70, 33)
        self.line_input_ticker.setAlignment(Qt.AlignCenter)
        self.line_input_ticker.setFont(QtGui.QFont("Calibri", 14, QtGui.QFont.Bold))
        self.line_input_ticker.setPlaceholderText("----")
        self.line_input_ticker.setMaxLength(4)
        self.line_input_ticker.setValidator(Validator(self))
        self.line_input_ticker.setToolTip('enter ticker of company')

        self.information_panel = QtWidgets.QTextEdit(self)
        self.information_panel.move(width_table + distance_from_table, 84 + distance_between_items*7)
        self.information_panel.resize(350 , 285)
        self.information_panel.setFont(QtGui.QFont("Calibri", 12))
        self.information_panel.setReadOnly(True)
        self.message = MessageBar(bar=self.information_panel)

        self.button_search_info = QtWidgets.QPushButton(QtGui.QIcon('img/Search_find_locate_1892.png'), '', self)
        self.button_search_info.move(line_width, 32)
        self.button_search_info.resize(41, 33)
        self.button_search_info.setToolTip('Click to find and\n'
                                           ' fill in the table\n'
                                           ' with company information')
        self.button_search_info.clicked.connect(self.search_info)

        self.button_to_get_estimate = QtWidgets.QPushButton(QtGui.QIcon('img/a_4466.png'), '  Get estimate', self)
        self.button_to_get_estimate.move(width_table + distance_from_table, 32 + distance_between_items)
        self.button_to_get_estimate.resize(130, 33)
        self.button_to_get_estimate.setStyleSheet("QPushButton {text-align: left;}")
        self.button_to_get_estimate.clicked.connect(self.obtain_estimate)

        self.button_save_as = QtWidgets.QPushButton(QtGui.QIcon('img/savetheapplication_guardar_2958.png'),
                                                    '  Save as', self)
        self.button_save_as.move(width_table + distance_from_table, 32 + distance_between_items*2)
        self.button_save_as.resize(130, 33)
        self.button_save_as.setStyleSheet("QPushButton {text-align: left;}")
        self.button_save_as.clicked.connect(self.file_save_as)

        self.button_save = QtWidgets.QPushButton(QtGui.QIcon('img/savetheapplication_guardar_2958.png'),
                                                 '  Save', self)
        self.button_save.move(width_table + distance_from_table, 32 + distance_between_items*3)
        self.button_save.resize(130, 33)
        self.button_save.setStyleSheet("QPushButton {text-align: left;}")
        self.button_save.setEnabled(False)
        self.button_save.clicked.connect(self.file_save)

        self.button_open = QtWidgets.QPushButton(QtGui.QIcon('img/open-folder_icon-icons.com_70017.png'),
                                                 '  Open', self)
        self.button_open.move(width_table + distance_from_table, 32 + distance_between_items*4)
        self.button_open.resize(130, 33)
        self.button_open.setStyleSheet("QPushButton {text-align: left;}")
        self.button_open.clicked.connect(self.file_open)

        self.button_clear_message = QtWidgets.QPushButton(QtGui.QIcon('img/clear.png'),
                                                 '  Clear', self)
        self.button_clear_message.move(width_table + distance_from_table, 32 + distance_between_items*7)
        self.button_clear_message.resize(130, 33)
        self.button_clear_message.setStyleSheet("QPushButton {text-align: left;}")
        self.button_clear_message.clicked.connect(self.message_clear)

        self.TableWidget.setHorizontalHeaderLabels(dates)
        self.TableWidget.setVerticalHeaderLabels(row_label)

        style = """        
        QTableWidget::item {background-color: white;
        border-style: outset} 

        QHeaderView::section{Background-color: rgb(230,230,230)}

        QTableWidget::item:selected {border-width: 1px; color: black ; border-color: green}
        """

        self.setStyleSheet(style)

        self.show()

    def file_open(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', ".", "Text Files(*.xl* )")
        if file[0]:
            self.file_name = file
            print(self.file_name[0])
            xl = xlrd.open_workbook(self.file_name[0], formatting_info=False)
            sheet = xl.sheet_by_index(0)
            for i, item in enumerate(Settings().list_of_financial_performance_items, 1):
                r = sheet.row_values(i)
                for j, date in enumerate(Settings().dates, 1):
                    if r[0] == Settings().list_of_financial_performance_items[item]:
                        self.company_details.indicators[item][date] = r[j]

            self.fill_table()
            self.button_save.setEnabled(True)

    def file_save_as(self):
        file = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', ".", "Text Files(*.xls)")
        if file[0]:
            self.file_name = file
            self.file_save()
            self.button_save.setEnabled(True)

    def file_save(self):
        wb = xlwt.Workbook()
        ws = wb.add_sheet('Security Analysis')

        for i, date in enumerate(Settings().dates):
            ws.write(0, i + 1, date)
        for i, item in enumerate(Settings().list_of_financial_performance_items.values()):
            ws.write(i + 1, 0, item)

        for i, item in enumerate(Settings().list_of_financial_performance_items.keys()):
            for j, date in enumerate(Settings().dates):
                ws.write(i + 1, j + 1, self.company_details.indicators[item][date])

        try:
            wb.save(self.file_name[0])
            self.message.send_message("Document was saved successfully")
        except PermissionError:
            self.message.send_message("Program cannot execute the command, " +
                                      "while file is open.")

    def message_clear(self):
        self.message.clear()

    def write_table(self):
        for i, item in enumerate(Settings().list_of_financial_performance_items.keys()):
            for j, date in enumerate(Settings().dates):
                try:
                    value = self.TableWidget.item(i, j).text()
                except AttributeError:
                    continue
                if value == 'null':
                    value = ''
                self.company_details.indicators[item][date] = value

    def fill_table(self):
        for i, item in enumerate(Settings().list_of_financial_performance_items.keys()):
            for j, date in enumerate(Settings().dates):
                widget_item = QtWidgets.QTableWidgetItem(self.company_details.indicators[item][date])
                self.TableWidget.setItem(i, j, widget_item)

    def obtain_estimate(self):
        self.button_to_get_estimate.setEnabled(False)
        QtWidgets.qApp.processEvents()

        analysis = FundamentalAnalysis(self.company_details)
        self.message.send_block_message(analysis.gross_margin_estimate(),
                                        analysis.sg_and_a_estimate(),
                                        analysis.p_e_and_p_bv_estimate(),
                                        analysis.net_income_estimate(),
                                        analysis.roa_estimate(),
                                        analysis.amortization_estimate(),
                                        analysis.long_term_debt_estimate(),
                                        ticker=self.company_details.ticker)

        self.button_to_get_estimate.setEnabled(True)

    def search_info(self):
        self.button_search_info.setEnabled(False)
        QtWidgets.qApp.processEvents()
        ticker = self.line_input_ticker.text()
        if len(self.line_input_ticker.text()) == 4:
            self.company_details.cancel_data()
            search_info = SearchInfo()
            result = search_info.get_info(ticker.lower(), self.company_details.indicators)
            self.message.clear()
            self.message.send_message(str(result))
            self.fill_table()
        else:
            self.message.send_message('enter ticker')
        self.button_search_info.setEnabled(True)


def main_application():
    """
    function to initialize and display the main application window
    """
    app = QApplication(sys.argv)
    app.setStyle('cleanlooks')
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main_application()
