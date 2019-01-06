class FinancialIndependence():

    def __init__(self, in_TFSA, in_RRSP, in_unregistered, suggested_TFSA, suggested_RRSP, suggested_unregistered,
                 annual_budget):
        """
        Initialize an Instance of Financial Independence
        """
        # Possible issue is that TFSA is only 5500 even if first year can be more
        self.TFSA_annual_contribution_room = 5500
        # To account for cases where previously unused TFSA space is being contributed to first year
        if suggested_TFSA > self.TFSA_annual_contribution_room:
            suggested_unregistered += (suggested_TFSA - self.TFSA_annual_contribution_room)
            suggested_TFSA = self.TFSA_annual_contribution_room

        self.annual_savings = suggested_RRSP + suggested_TFSA + suggested_unregistered
        self.annual_budget = int(annual_budget)

        # Total Savings
        self.TFSA_total = int(in_TFSA)
        self.RRSP_total = int(in_RRSP)
        self.unregistered_total = int(in_unregistered)

        self.total_savings = self.unregistered_total + self.TFSA_total + self.RRSP_total

        # Assumptions
        self.annual_interest = 1.055  # Interest is Historically 9.5%, with inflation being counted as 4% a year that
        # leaves 5.5%
        self.suggested_TFSA = suggested_TFSA
        self.suggested_RRSP = suggested_RRSP
        self.suggested_unregistered = suggested_unregistered

        # self.in_TFSA = int(in_TFSA)
        # self.in_RRSP = int(in_RRSP)
        # self.in_unregistered = int(in_unregistered)

    def aggregate_interest(self):
        """
        calculate agregate interest: for instance if $10,000 is saved every year with an 8% return. What will be in the
        savings after x years. In this case. We stop calculating after 4% of total savings is =< annual budget

        :return:
        """
        years = 0
        while (self.total_savings * 0.04) < self.annual_budget:


            self.total_savings *= self.annual_interest
            # print(self.total_savings)
            #self.RRSP_total *= self.annual_interest
            #self.TFSA_total *= self.annual_interest
            self.unregistered_total *= self.annual_interest
            self.total_savings += self.annual_savings
            # self.RRSP_total += self.suggested_RRSP
            #self.TFSA_total += self.suggested_TFSA
            #self.unregistered_total += self.suggested_unregistered

            years += 1
        print( "Years to Financial Independence: ", years)
        print( "Amount in RRSP, TFSA, Unregistered respectively: ", round(self.RRSP_total,2),", ",
               round(self.TFSA_total, 2), ", ", round(self.unregistered_total,2))
        print("Total savings: ", round(self.total_savings, 2))
