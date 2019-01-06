import datetime
from UnconventionalLiving.Tax import CanadaTax
from UnconventionalLiving.Deductions import Deductions

"""
Things to consider here, Full income before tax might be good to know, to calculate best places to put money,
If I assume to always contribute to TFSA first than RRSP I should state as much in the info sheet.

Amount that is wanted as an annual budget needs to be taken into consideration, I need to decide if that will be dealt
with here or elsewhere.
"""

"""
How much is saved by RRSP contribution is off
"""


class Savings:
    def __init__(self, income, age, province, self_employed, annual_budget=30000, in_TFSA=0):
        """
        Initialize an instance of savings with different savings options

        :param income:
        :param annual_budget:
        :param in_TFSA: The amount that the user already has in their TFSA
        """
        self.age = int(age)
        self.province = province
        self.self_employed = self_employed

        # Annual
        self.annual_budget = int(annual_budget)
        self.income = int(income)
        self.og_taxable_income = int(income)
        self.taxable_income = int(income)
        self.ct = CanadaTax()

        # Deductions
        self.deductions = Deductions(self.income, self.province, self.self_employed)
        self.CPP_contribution = self.deductions.CPP_deductions()
        self.EI_deduction = self.deductions.EI_dedicution()

        taxed = self.ct.after_tax_income(self.income, self.province)
        self.income_after_tax = taxed  - self.EI_deduction - self.CPP_contribution
        print("After tax and deductions: ", self.income_after_tax)

        self.amount_to_save = self.income_after_tax - self.annual_budget
        self.annual_TFSA = 0
        self.annual_RRSP = 0
        self.annual_savings = 0
        self.in_TFSA = int(in_TFSA)

        self.TFSA_eligible = self.TFSA_eligible()

        while self.amount_to_save != 0:
            self.annual_savings_location()

            self.taxable_income = self.taxable_income - self.annual_RRSP
            # Currently the refund is not correct
            """ walkthrough. income is 80,000 after tax say it is 65,000 I contribute 20,000 to RRSP. now I should be
            taxed as if I made 60,000. The money I get back would be the tax difference, say 60,000 after tax is 45,000
            I will not be taxed on the 20,000, to so this I would do (amount after tax of 80,000 - amount after tax of
            60,000) which is the same as (65,000 - 45,000) = 20,000. So I would get 20,000 dollars back in tax?.

            How about this way. The amount I am taxed on 80,000 - the amount I am taxed on 60,000 (15,000 - 15,000)
            """
            self.RRSP_refund = self.ct.amount_taxed(self.og_taxable_income, self.province) - \
                               self.ct.amount_taxed(self.taxable_income, self.province)
            print("With this RRSP contribution, you will save ", round(self.RRSP_refund, 2), " in taxes")
            #self.RRSP_refund = self.income_after_tax - self.ct.after_tax_income(self.taxable_income, self.province)

            # If the annual max RRSP contributions have been made, put the rest in annual savings
            # Maybe I should account for it going in th TFSA instead
            if (self.max_RRSP_contribution() - self.annual_RRSP) == 0:
                self.annual_savings = self.RRSP_refund + self.amount_to_save
                self.amount_to_save = 0

            elif self.RRSP_refund > 0:
                self.RRSP_refund = 0

        # This might not be the appropiate location as this function isnt initiated every year. It would go best
        # in the functions that calculate more than one year
        #self.TFSA_eligible += 5500

        print("suggested amount to contribute to your TFSA: ", round(self.annual_TFSA, 2))
        print("suggested amount to contribute to your RRSP: ", round(self.annual_RRSP, 2))
        print("suggested amount to contribute to your Unregistered Savings: ", round(self.annual_savings, 2))

    def annual_savings_location(self):

        if self.income > 70000:
            print("It is suggested that you contribute to your RRSP before you Contribute to your TFSA")
            self.RRSP_contribution()
            self.TFSA_contribution()

        else:
            print("It is suggested that you contribute to your TFSA before you Contribute to your RRSP")

            self.TFSA_contribution()
            self.RRSP_contribution()


    def total_contributions_for_FI(self):
        """
        Return the total amount in each account that will be accumulated after the number of years to hit FI

        :return:
        """
    # Consider if this function should be located in this class or not
    def years_to_FI(self):
        """
        Return the number of years of working until FI is reached
        :return:
        """

    def RRSP_contribution(self):
        """
        Return the suggested annual amount to place in an RRSP

        :return: NoneType
        """
        max_contribution = self.max_RRSP_contribution() - self.annual_RRSP

        # Note to Self: make sure that self.annual_RRSP isn't just a pointer to self.amount to save but takes on the
        #  number
        if self.amount_to_save < max_contribution:
            self.annual_RRSP = self.amount_to_save
            self.amount_to_save = 0
            self.taxable_income -= self.annual_RRSP
            # amount saved by tax benefits should be refactored into "amount to save" and savings locations should be
            # rerun
        else:
            self.annual_RRSP = max_contribution
            self.amount_to_save -= max_contribution

    def TFSA_contribution(self):
        """
        Return the suggested annual amount to place in a TFSA

        :return: NoneType
        """
        # if this gets rerun twice in a year (it will add two years of contribution room
        if self.amount_to_save <= self.TFSA_eligible:
            self.annual_TFSA = self.amount_to_save
            # this sets TFSA_eligible to be ready for next years calculations. 5500 is hardcoded based on th assumption
            # that it will always be the annual increase
            self.TFSA_eligible -= (self.amount_to_save)
            self.amount_to_save = 0

        else:
            self.annual_TFSA = self.TFSA_eligible
            self.amount_to_save -= self.TFSA_eligible
            self.TFSA_eligible = 0

    def savings_contributions(self):
        """
        Return the suggested annual contributions to a savings account. This is taxed fully.

        :return:
        """

    # Helper Function for TFSA contributions
    def TFSA_eligible(self):
        """
        Design Note: Make sure this is only calculated for the initial year and not every year in the future.
        Based on your birthday, it calculates how much you are able to put in your TFSA as of today.

        :param age: int
        :return:
        """
        # 2009 - 2012 $5000 annual contribution
        # 2013 - 2014 $5500 annual contribution
        # 2015 $10,000 annual contribution
        # 2016 - 2018 $5500 annual contribution
        eligible = [5000, 5000, 5000, 5000, 5500, 5500, 10000, 5500, 5500]

        # Account for this calculator being used in future years
        now = datetime.datetime.now()
        curr_year = now.year
        future = curr_year - 2018
        to_extend = [5500] * future
        eligible.extend(to_extend)

        # 18 years old in 2009
        if ((curr_year - self.age) + 18) <= 2009:
            total_eligible = sum(eligible) - self.in_TFSA
        else:
            turned_18 = ((curr_year - self.age) + 18)
            years_not_eligible = turned_18 - 2009
            # -1 for index
            total_eligible = sum(eligible[years_not_eligible - 1:]) - self.in_TFSA

        return total_eligible


    # Helper Function For RRSP contributions
    def max_RRSP_contribution(self):
        """
        Return the maximum contribution to an RRSP given your Before tax income

        :param income: float
        :return: float
        """
        option1 = 0.18 * self.income
        cap_contribution = 24270

        if option1 <= cap_contribution:
            max_contribution = option1
        else:
            max_contribution = cap_contribution

        return max_contribution

    def total_saved(self):
        return round(self.annual_TFSA + self.annual_RRSP + (self.annual_savings), 2)

    def get_suggested_RRSP(self):
        return self.annual_RRSP

    def get_suggested_TFSA(self):
        return self.annual_TFSA

    def get_suggested_unregisted(self):
        return self.annual_savings
