import sqlite3
from message_bar import MessageBar


class SearchInfo:
    """Company search by Ticker in database."""
    @staticmethod
    def get_info(ticker, indicators):
        con = sqlite3.connect('base.db')
        cur = con.cursor()
        try:
            cur.execute('SELECT * FROM table_' + ticker)
        except sqlite3.OperationalError:
            return 'Такой компании нет в базе данных'
        data_table = cur.fetchall()
        list_indicators = list(indicators.keys())
        for line in data_table:
            date = line[0]
            for i, item in enumerate(line[1:]):
                indicators[list_indicators[i]][date] = item
        return MessageBar().signal_true
