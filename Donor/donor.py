#!/usr/bin/env python3
"""Donor module to keep records of donations"""

class Donor:
    """for individula donor"""
    def __init__(self, name, initial_donation=None):
        self.__name = name
        self.__donations = []
        if initial_donation is not None:
            self.__donations.append(initial_donation)

    @property
    def name(self):
        """get donor name"""
        return self.__name

    @property
    def donation(self):
        """get donation amount"""
        return self.__donations

    @property
    def num_donations(self):
        """how many times this donor has donated"""
        return len(self.__donations)

    @property
    def total_donations(self):
        """get total donations"""
        return sum(self.__donations)

    @property
    def avg_donation(self):
        """average donation amount"""
        return self.total_donations/self.num_donations

    #you can call instance.__dict__ to view this information
    def __str__(self):
        return "[Donor name = {}, donations = {}]".format(self.__name, self.__donations)

    #__is not directly viewed from outside, make attribute invisible from outside
    def add_donation(self, donation):
        """add donation to donor"""
        self.__donations.append(donation)

    #generate report row
    def generate_report_row(self):
        """a report of donations"""
        return "|{:>12}|{:>12}|{:>12}|{}|".format(self.__name, self.total_donations,\
         self.avg_donation, self.__donations)

    def thank_you(self):
        """print a thank you letter to the donor"""
        message = "Dear {},\n Thank you for your donation of {}!\n".format(self.__name, \
        self.__donations)
        print(message)
        return message


class DonorCollection:
    """this class is to record different donors"""
    def __init__(self):
        self.__donors = {} #name: Donor pairs

    def add_new_donor(self, name):
        """add a new donor to the collection"""
        if name in self.__donors:
            raise ValueError("name({}) already exists".format(name))
        self.__donors[name] = Donor(name)

    def add_donation(self, name, donation):
        """add new donation"""
        self.__donors[name].add_donation(donation)

    def get_donor(self, name):
        """get donor history of a specific donor"""
        return self.__donors[name]

    def generate_report(self):
        """generate a report of all donors"""
        header = "|{:>12}|{:>12}|{:>12}|{:>12}|".format("Name", "Total", "Average", "# donations")
        lines = [header]
        #values(), donor object, an instance of donor class
        for donor in self.__donors.values():
            lines.append(donor.generate_report_row())
        return "\n".join(lines)

    def thank_you_letter(self):
        """send a thank you letter to each donor"""
        for donor in self.__donors.values():
            donor.thank_you()

    def write_to_file(self):
        """write letters into txt files"""
        for name in self.__donors.keys():
            with open(name, "w") as f:
                f.write(self.__donors[name].thank_you())

if __name__ == "__main__":
    D_C = DonorCollection()
    D_C.add_new_donor("Bill")
    D_C.add_donation("Bill", 1234)
    D_C.add_donation("Bill", 5678)
    D_C.add_new_donor("Paul")
    D_C.add_donation("Paul", 1000)
    D_C.generate_report()
    D_C.thank_you_letter()
