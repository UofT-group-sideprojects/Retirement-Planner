class Deductions:

    def __init__(self, income, province, self_employed):
        """

        :param income:
        :param province:
        """
        if self_employed.lower().strip() == "yes":
            self.self_employed = True
        else:
            self.self_employed = False

        self.income = income
        self.province = province

        # Employment Insurance deduction
        self.ei_max = 51700
        self.ei_rate = 0.0166

        # CPP contribution
        self.CPP_contribution_rate = 0.0495
        self.CPP_max = 52400

    def EI_dedicution(self):
        """
        # ToDo: Take into consideration self employment. This is calculated differently.
        Calculate Emplyment Insurace deduction. as of 2018 the rates are: up to $51,700 will be taxed	1.66%
        :return:
        """
        if self.province != "Quebec":
            if self.income > self.ei_max:
                return self.ei_max * self.ei_rate

            else:
                return self.income * self.ei_rate
        else:
            print("EI deductions for Quebec cannot be calculated at the moment")
            return 0

    def CPP_deductions(self):
        """
        Return the amount deducted from pay for the Canadian Pension Plan. This does not account for Quebec.

        2018 : min amount deductions are allowed on $3,500 , max	$52,400, percentage for employee if employed 4.95
         (employer matches
        :return:
        """
        if self.province != "Quebec":

            CPP_contribution_rate = self.CPP_contribution_rate

            if self.self_employed:
                CPP_contribution_rate = self.CPP_contribution_rate * 2

            if self.income < 3500:
                return 0
            elif self.income < self.CPP_max:
                return self.income * CPP_contribution_rate
            else:
                return self.CPP_max * CPP_contribution_rate
        else:
            print("Quebec Pension Contributions cannot be calculated yet")
            return 0