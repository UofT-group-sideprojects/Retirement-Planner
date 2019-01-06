from UnconventionalLiving.Tax import CanadaTax
from UnconventionalLiving.Savings import Savings
from UnconventionalLiving.FinancialIndependence import FinancialIndependence

if __name__ == "__main__":
    again = input("Would you like to plan an unconventional lifestyle? ")
    while again.lower() == 'yes':
        canada_tax = CanadaTax()
        # Income
        income = input("Annual Income: ")
        # Province
        province = input("Province: ")

        after_tax = canada_tax.after_tax_income(income, province)
        # Age
        age = input("Your age: ")
        # Self Employed?
        self_employed= input("Are you self_employed: ")

        # In TFSA
        in_TFSA = input("Amount currently in your TFSA: ")
        in_RRSP = input("Amount currently in your RRSP: ")
        in_unregistered = input("Amount in other savings accounts: ")

        annual_budget = int(input("Desired monthly Budget: ")) * 12

        # ToDo: instead of printing these numbers, return them that way it can be used for Unconventinal Life style planning
        savings = Savings(income, age, province, self_employed, annual_budget, in_TFSA)
        total_saved = savings.total_saved()

        # I need to pass in the amount of money currently in each location as well as the amount that should be added each
        # year
        FI = FinancialIndependence( in_TFSA, in_RRSP, in_unregistered, savings.get_suggested_TFSA(),
                                    savings.get_suggested_RRSP(), savings.get_suggested_unregisted(), annual_budget)
        FI.aggregate_interest()

        print("")
        print("")
        again = input("Would you like to plan an unconventional lifestyle? ")
        # ToDO: make the amount you want to live off of after retirement different than current amount
        # (have this as an option)
        # Calculate tax on interes