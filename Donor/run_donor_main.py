#!/usr/bin/env python3

from donor import *

if __name__ == "__main__":
    dc = DonorCollection()
    while True:
        user_input = int(input("\
        1. add new donor\n\
        2. add donation to existing donor\n\
        3. full report\n\
        4. send thank you\n\
        5. write letter into txt file\n\
        6. quit"))

        if user_input == 1:
            input_name = input("What's the name of new donor?")
            dc.add_new_donor(input_name)
            
        if user_input == 4:
            print(dc.thank_you_letter())
            
        if user_input == 2:
            input_name2 = input("what's the name?")
            input_donation = int(input("how much would you like to donate?"))
            dc.add_donation(input_name2, input_donation)
            
        if user_input == 3:
            print(dc.generate_report())
            
        if user_input == 5:
            dc.write_to_file()

        if user_input == 6:
            break
