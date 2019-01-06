"""
Take into account Savings tax on RRSP and normal savings accounts
"""

class CanadaTax:

    def __init__(self):
        """
        Initialize an instance of all Canadian Taxes
        """
        # ToDO: Quebec Tax

        # Federal Tax
        self.federal_tax_buckets =[(46605, 0.15), (46603, 0.205), (51281, 0.26), (61353, 0.29)]
        self.federal_tax_max = 0.33

        # Ontario Tax
        self.ontario_tax_buckets = [(42960, 0.0505), (42963, 0.0915), (64077, 0.1116), (70000, 0.1216)]
        self.ontario_tax_max = 0.1316

        # British Columbia Tax
        self.bc_tax_buckets = [(39676, 0.0506), (39677, 0.077), (11754, 0.1015), (19523, 0.1229), (39370, 0.1417)]
        self.bc_tax_max = 0.168

        # Newfoundland an Labrador
        self.nl_tax_buckets = [(36926, 0.087), (36926, 0.145), (57998, 0.158), (52740, 0.173)]
        self.nl_tax_max = 0.183

        # Prince Edward Island Tax
        self.pei_tax_buckets = [(31984, 0.098), (31985, 0.138)]
        self.pei_tax_max = 0.167

        # Nova Scotia Tax
        self.ns_tax_buckets = [(29590, 0.0879), (29590, 0.1495), (33820, 0.1667), (57000, 0.175)]
        self.ns_tax_max = 0.21

        # New Brunswick Tax
        self.nb_tax_buckets = [(41675, 0.0968), (41676, 0.1482), (52159, 0.1652), (18872, 0.1784)]
        self.nb_tax_max = 0.203

        # Manitoba Tax
        self.manitoba_tax_buckets = [(31843, 0.108), (36978, 0.1275)]
        self.manitoba_tax_max = 0.174

        # Saskatchewan Tax
        self.saskatchewan_tax_buckets = [(41675, 0.105), (41676, 0.125)]
        self.saskatchewan_tax_max = 0.145

        # Alberta Tax
        self.alberta_tax_buckets = [(128145, 0.10), (25628, 0.12), (51258, 0.13), (102516, 0.14)]
        self.alberta_tax_max = 0.15

        # Yukon Tax
        self.yukon_tax_buckets = [(46605, 0.064), (46603, 0.09), (51281, 0.109), (355511, 0.128)]
        self.yukon_tax_max = 0.15

        # North West Territories Tax
        self.nwt_tax_buckets = [(42209, 0.059), (42211, 0.086), (52828, 0.122)]
        self.nwt_tax_max = 0.1405

        # Nunavut Tax
        self.nunavut_tax_buckets = [(44437, 0.04), (44437, 0.07), (55614, 0.09)]
        self.nunavut_tax_max = 0.115

        self.all_provinces = {
            "Newfoundland and Labrador": {"bucket": self.nl_tax_buckets , "tax_max": self.nl_tax_max},
            "PEI": {"bucket": self.pei_tax_buckets , "tax_max": self.pei_tax_max },
            "Nova Scotia": {"bucket": self.ns_tax_buckets, "tax_max": self.ns_tax_max},
            "New Brunswick": {"bucket": self.nb_tax_buckets, "tax_max": self.nb_tax_max},
            "Quebec": {"bucket": [], "tax_max": 0.0}, # ToDo
            "Ontario": {"bucket": self.ontario_tax_buckets, "tax_max": self.ontario_tax_max},
            "Manitoba": {"bucket": self.manitoba_tax_buckets, "tax_max": self.manitoba_tax_max},
            "Saskatchewan": {"bucket": self.saskatchewan_tax_buckets, "tax_max": self.saskatchewan_tax_max},
            "Alberta": {"bucket": self.alberta_tax_buckets, "tax_max": self.alberta_tax_max},
            "British Columbia": {"bucket": self.bc_tax_buckets, "tax_max": self.bc_tax_max},
            "Yukon": {"bucket": self.yukon_tax_buckets, "tax_max": self.yukon_tax_max},
            "Northwest Territories": {"bucket": self.nwt_tax_buckets, "tax_max": self.nwt_tax_max},
            "Nunavut": {"bucket": self.nunavut_tax_buckets, "tax_max": self.nunavut_tax_max}
        }
    def amount_taxed(self, income, province):
        income = int(income)
        federal_tax = self.compute_tax(income, province)
        provincial_tax = self.compute_tax(income, province)
        total_tax = round(federal_tax + provincial_tax, 2)
        return total_tax

    def after_tax_income(self, income, province):
        income = int(income)
        federal_tax = self.compute_tax(income, province)
        provincial_tax = self.compute_tax(income, province)
        total_tax = round(federal_tax + provincial_tax, 2)
        return round((income - total_tax), 2)

    def compute_tax(self, income, province):
        """
        Calculate the tax for a given income and province. This does not calculate Federal and Provincial.
        Each are calculated seperately

        :param income: float or int: annual income
        :param province: String of the province the income is made in
        :return: float The tax that will be deducted from the income
        """
        income = int(income)
        if province in self.all_provinces:
            bucket = self.all_provinces[province]["bucket"]
            tax_max = self.all_provinces[province]["tax_max"]
        else:
            print ("Unknown Province for tax purposes")
            return 0

        total_tax = 0.0
        counted_income = income
        bucket_index = 0
        while True:
            if bucket_index == len(bucket):
                total_tax += counted_income * tax_max
                break;
            if bucket[bucket_index][0] > counted_income:
                total_tax += counted_income * bucket[bucket_index][1]
                break;
            counted_income -= bucket[bucket_index][0]
            total_tax += bucket[bucket_index][0] * bucket[bucket_index][1]
            bucket_index += 1

        return round(total_tax, 2)

# ToDo


class USTax:

    def __init__(self):
        """
        Initialize an instance of all US Taxes
        """
