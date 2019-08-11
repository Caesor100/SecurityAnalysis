from settings import Settings


class CompanyDetails:
    """The class contains information about the company.
     Stock Ticker, financial indicators, etc."""
    def __init__(self):
        self.ticker = ''
        self.indicators = self._create_indicators()
        self.estimates = {
            'gross_margin': None,
            'sg_and_a': None,
            'p_e_and_p_bv': None,
            'net_income': None,
            'roa': None,
            'capex': None,
            'amortization': None,
            'long_term_debt': None,
            'uncovered_loss': None
        }

    @staticmethod
    def _items_to_fill_voids():
        result = dict()
        for date in Settings().dates:
            result[date] = ''
        return result

    def _create_indicators(self):
        result = dict()
        for item in Settings().list_of_financial_performance_items.keys():
            result[item] = self._items_to_fill_voids()
        return result

    def cancel_data(self):
        self.indicators = self._create_indicators()

    def get_financial_indicator(self, financial_indicator):
        pass
