class Settings:
    def __init__(self):
        # screen options
        self.screen_width = 1000
        self.screen_height = 800

        # table size
        self.table_width = 627
        self.table_height = 798

        self.distance_from_table = 10

        self.distance_between_items = 60

        self.dates = ['2009', '2010', '2011',
                      '2012', '2013', '2014',
                      '2015', '2016', '2017',
                      '2018', 'LTM']

        # cells in table
        self.list_of_financial_performance_items = {
            'revenue': 'Revenue',
            'cost_of_production': 'Cost Of Production',
            'gross_profit': 'Gross Profit',
            'sg_and_a': 'SG&A',
            'amortization': 'amortization',
            'interest_expenses': 'Interest Expenses',
            'opex': 'OPEX',
            'ebit': 'EBIT',
            'corporate_tax': 'Corporate tax',
            'net_income': 'Net Income',

            'cash': 'Cash',
            'accounts_receivable': 'Accounts receivable',
            'net_goodwill': 'Net Goodwill',
            'assets': 'assets',
            'number_of_shares': 'Number of Shares',
            'short_term_debt': 'Short-Term Debt',
            'long_term_debt': 'Long-Term Debt',
            'obligations': 'Obligations',
            'uncovered_loss': 'Uncovered Loss',

            'eps': 'EPS',
            'd_e': 'D/E',
            'roa': 'ROA',
            'roe': 'ROE',
            'p_e': 'P/E',
            'p_bv': 'P/BV'
        }

        self.version = '1.0'

    def get_list_of_financial_performance_items(self):
        return list(self.list_of_financial_performance_items.values())

