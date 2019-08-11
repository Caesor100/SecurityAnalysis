from settings import Settings


class CalculationOfPoints:
    """Class for the calculation of the other indicators of the company."""
    @staticmethod
    def _get_percentage_of_two_numbers(a, b):
        """"(a/b) * 100%"""
        result = dict()
        for date in Settings().dates:
            if a[date] == '' or b[date] == '':
                result[date] = ''
                continue
            result[date] = str(round((float(a[date]) / float(b[date]) * 100), 3)) + ' %'
        return result

    @staticmethod
    def gross_profit(revenue, cost_of_production):
        """"gross_profit = revenue - cost_of_production"""
        result = dict()
        for date in Settings().dates:
            if revenue[date] == '' or cost_of_production[date] == '':
                result[date] = ''
                continue
            result[date] = str(round(float(revenue[date]) - float(cost_of_production[date]), 2))
        return result

    def gross_margin(self, gross_profit, revenue):  # Валовая маржа
        return self._get_percentage_of_two_numbers(gross_profit, revenue)

    def sg_and_a(self, sga, gross_profit):  # Коэффициент SG&A от величины валовой прибыли
        return self._get_percentage_of_two_numbers(sga, gross_profit)

    def coefficient_of_amortization(self, amortization, gross_profit): # Коэффициент амортизации от величины валовой прибыли
        return self._get_percentage_of_two_numbers(amortization, gross_profit)

    def net_profit_to_gross_profit_ratio(self, net_income, gross_profit):  # Отношение чистой прибыли к валовой
        return self._get_percentage_of_two_numbers(net_income, gross_profit)

    def interest_expense_to_operating_income_ratio(self, interest_expense, operating_income):  # Отношение процентных расходов к операционной прибыли
        return self._get_percentage_of_two_numbers(interest_expense, operating_income)

    def roa(self, net_income, sum_asset):  # Рентабельность активов (ROA)
        return self._get_percentage_of_two_numbers(net_income, sum_asset)

    def roe(self, net_income, equity):  # Рентабельность акционерного капитала (ROE)
        return self._get_percentage_of_two_numbers(net_income, equity)

    def dept_to_equity_ratio(self, dept, equity):  # Соотношение заёмных и собсвенных средств
        return self._get_percentage_of_two_numbers(dept, equity)

