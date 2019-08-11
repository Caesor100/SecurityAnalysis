from settings import Settings
from calculation_of_points import CalculationOfPoints
import numpy as np


class FundamentalAnalysis:
    """Class to obtain an assessment of the company's financial indicators"""
    def __init__(self, company_details):
        self.company_details = company_details
        self.estimates = {
            1: 'very badly',
            2: 'bad',
            3: 'below normal',
            4: 'normal',
            5: 'good'
        }

    def gross_margin_estimate(self):
        gross_margin = CalculationOfPoints().gross_margin(self.company_details.indicators['gross_profit'],
                                                          self.company_details.indicators['revenue'])
        try:
            value_1 = float(gross_margin['LTM'].replace(' %', ''))
            value_2 = float(gross_margin[Settings().dates[-2]].replace(' %', ''))
        except ValueError:
            return 'Gross margin estimate: no data'
        except KeyError:
            return 'Gross margin estimate: no data'

        value_3 = (value_1+value_2)*0.5
        if value_3 >= 40:
            self.company_details.estimates['gross_margin'] = 5
        elif value_3 < 30:
            self.company_details.estimates['gross_margin'] = 1
        else:
            estimate_index = round(abs(40-value_3)/2)
            self.company_details.estimates['gross_margin'] = estimate_index

        return 'Gross margin estimate: ' + self.estimates[self.company_details.estimates['gross_margin']]

    def sg_and_a_estimate(self):
        result = []
        for date in Settings().dates:
            try:
                value = float(self.company_details.indicators['sg_and_a'][date].replace(' %', ''))
            except ValueError:
                continue
            result.append(value)

        if not result:
            return 'SG&A estimate: no data'

        mean = np.mean(result)

        std = np.std(result)
        v = (std/mean)*100
        if 65 > mean > 25:
            if v <= 30:
                self.company_details.estimates['sg_and_a'] = 5
            if 35 >= v > 30:
                self.company_details.estimates['sg_and_a'] = 4
            if 40 >= v > 35:
                self.company_details.estimates['sg_and_a'] = 3
            if 45 >= v > 40:
                self.company_details.estimates['sg_and_a'] = 2
            if v > 45:
                self.company_details.estimates['sg_and_a'] = 1
        else:
            if v <= 30:
                self.company_details.estimates['sg_and_a'] = 4
            if 35 >= v > 30:
                self.company_details.estimates['sg_and_a'] = 3
            if 40 >= v > 35:
                self.company_details.estimates['sg_and_a'] = 2
            if v > 40:
                self.company_details.estimates['sg_and_a'] = 1

        return 'SG&A estimate: ' + self.estimates[self.company_details.estimates['sg_and_a']]

    def p_e_and_p_bv_estimate(self):
        try:
            p_e = float(self.company_details.indicators['p_e']['LTM'])
            p_bv = float(self.company_details.indicators['p_bv']['LTM'])
        except ValueError or NameError:
            return 'P/E and P/B estimate: no data'

        estimate = p_e * p_bv
        if estimate > 10 or estimate < 0.25:
            self.company_details.estimates['p_e_and_p_bv'] = 2
        elif 10 >= estimate > 8:
            self.company_details.estimates['p_e_and_p_bv'] = 4
        else:
            self.company_details.estimates['p_e_and_p_bv'] = 5

        return 'P/E and P/B estimate: ' + self.estimates[self.company_details.estimates['p_e_and_p_bv']]

    def amortization_estimate(self):
        result = []
        for date in Settings().dates:
            try:
                amortization_estimate = float(self.company_details.indicators['amortization'][date])
                gross_profit = float(self.company_details.indicators['gross_profit'][date])
                value = (amortization_estimate/gross_profit)*100
            except ValueError:
                continue
            result.append(value)

        if not result:
            return 'Amortization estimate: no data'

        v = (np.std(result)/np.mean(result))*100
        if np.mean(result) < 10 and v < 30:
            self.company_details.estimates['amortization'] = 5
        elif np.mean(result) < 12 and v < 35:
            self.company_details.estimates['amortization'] = 4
        elif np.mean(result) < 14 and v < 40:
            self.company_details.estimates['amortization'] = 3
        elif np.mean(result) < 16 and v < 45:
            self.company_details.estimates['amortization'] = 2
        else:
            self.company_details.estimates['amortization'] = 1

        return 'Amortization estimate: ' + self.estimates[self.company_details.estimates['amortization']]

    def net_income_estimate(self):
        result = []
        for date in Settings().dates:
            try:
                net_income = float(self.company_details.indicators['net_income'][date])
                gross_profit = float(self.company_details.indicators['gross_profit'][date])
                value = (net_income/gross_profit)*100
            except ValueError:
                continue
            result.append(value)

        if not result:
            return 'Net income estimate: no data'

        if result[-1] < 20:
            self.company_details.estimates['net_income'] = 1
        elif result[-1] > 20 and np.mean(result) > 20:
            self.company_details.estimates['net_income'] = 5
        elif result[-1] > 20 and (15 < np.mean(result) <= 20):
            self.company_details.estimates['net_income'] = 4
        elif result[-1] > 20 and (10 < np.mean(result) <= 15):
            self.company_details.estimates['net_income'] = 3
        elif result[-1] > 20 and (5 < np.mean(result) <= 10):
            self.company_details.estimates['net_income'] = 2
        else:
            self.company_details.estimates['net_income'] = 1

        return 'Net income estimate: ' + self.estimates[self.company_details.estimates['net_income']]

    def roa_estimate(self):
        try:
            roa = float(self.company_details.indicators['roa']['LTM'].replace(' %', ''))
        except ValueError:
            return 'ROA estimate: no data'

        if roa > 10:
            self.company_details.estimates['roa'] = 5
        else:
            self.company_details.estimates['roa'] = 2

        return 'ROA estimate: ' + self.estimates[self.company_details.estimates['roa']]

    def long_term_debt_estimate(self):
        try:
            long_term_debt = float(self.company_details.indicators['long_term_debt'][Settings().dates[-2]])
            net_income = float(self.company_details.indicators['net_income'][Settings().dates[-2]])
        except ValueError:
            return 'Long term debt estimate: no data'

        long_term_debt_to_net_income = long_term_debt/net_income

        if long_term_debt_to_net_income <= 4:
            self.company_details.estimates['long_term_debt'] = 5
        elif long_term_debt_to_net_income <= 6:
            self.company_details.estimates['long_term_debt'] = 4
        elif long_term_debt_to_net_income <= 8:
            self.company_details.estimates['long_term_debt'] = 3
        elif long_term_debt_to_net_income <= 10:
            self.company_details.estimates['long_term_debt'] = 2
        elif long_term_debt_to_net_income > 10:
            self.company_details.estimates['long_term_debt'] = 1

        return 'Long term debt estimate: ' + self.estimates[self.company_details.estimates['long_term_debt']]
