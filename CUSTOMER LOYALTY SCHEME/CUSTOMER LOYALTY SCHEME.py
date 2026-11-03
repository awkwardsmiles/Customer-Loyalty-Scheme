filename = ("employees.txt")
import random
from datetime import *

def CLS():
    #========== CUSTOMER LOYALTY SCHEME==============
    FILENAME = "hotelmembers.txt"
    limit = 14
    satus = "silver"

    #================ SUBPROGRAMS ====================
    #-------------------- MENU -----------------------
    def menu():
        print("--------CRAWDALE HOTEL GROUP----------")
        print("ENTER [1] TO ADD A NEW CH MEMBER")
        print("ENTER [2] TO ADD EDIT MEMBER'S RESERVATION")
        print("ENTER [3] TO VIEW CURRENT MEMBERS")
        print("ENTER [4] TO DELETE MEMBER")
        print("ENTER [5] TO VIEW MEMBERSHIP REPORT")
    #---------------ADD NEW MEMBER--------------------
    def add_member():
        name = input("Enter customer's surname: ").capitalize()
        while not name.isalpha():
            print("Name must include only letters")
            name = input("Enter customer's surname: ").capitalize()
        today = datetime.today()
        year = today.strftime("%Y")                           # Make ID
        number = random.randint(100,1000)
        digit = str(number)
        ID = name[:3] + digit  + year[2:]

        night_book = int(input("Enter how many night are you staying: "))
        while night_book > limit or night_book < 1:
            print("you can only book 14 night per booking")                       # Enters nights and gives points
            night_book = int(input("Enter how many night are you staying: "))

        points = night_book * 2500

        file = open(FILENAME,"a")
        thestring = ID + "," + name + "," + year+ "," + satus + "," + str(night_book) +","+ str(points) + "\n"
        file.write(thestring)
        file.close()
        
    #--------------EDIT MEMBER NIGHTS-----------------
    def edit_member():
        member_id = input("Enter member's code: ").strip()
        updated_data = []
        member_found = False
        total_nights = 0
        limit = 14  

        with open(FILENAME, "r") as file:
            for line in file:
                line = line.strip()
                member_details = line.split(",")
                if member_id == member_details[0]:
                    member_found = True
                    try:
                        redeem = input(
                            "WOULD YOU LIKE TO REDEEM NIGHTS WITH POINTS (Y|N)\nENTER 'Half' TO DO A SPLIT TRANSACTION: ").capitalize()

                        if redeem == "Y":
                            print("1 NIGHT = 25000 POINTS")
                            amount = int(input("ENTER NUMBER OF NIGHTS TO REDEEM: "))
                            while amount > limit or amount < 1:
                                print("You cannot book more than or less than 14 nights")
                                amount = int(input("ENTER NUMBER OF NIGHTS TO REDEEM: "))

                            points_needed = amount * 25000
                            balance = int(member_details[5])

                            if balance >= points_needed:
                                balance -= points_needed
                                member_details[5] = str(balance)
                                member_details[4] = str(int(member_details[4]) + amount)
                                total_nights = int(member_details[4])
                            else:
                                print(f"Not enough points. Your current balance: {balance}")

                        elif redeem == "N":
                            add_nights = int(input(f"How many additional nights will {member_details[1]} be staying? "))
                            while add_nights > limit or add_nights < 1:
                                print("You cannot book more than or less than 14 nights")
                                add_nights = int(input(f"How many additional nights will {member_details[1]} be staying? "))

                            total_nights = int(member_details[4]) + add_nights
                            member_details[4] = str(total_nights)
                            member_details[5] = str(int(member_details[5]) + add_nights * 2500)

                        elif redeem == "Half":
                            points_needed_per_night = 25000
                            night = int(input("HOW MANY NIGHTS ARE YOU STAYING: "))
                            while night < 1 or night > limit:
                                night = int(input("Invalid input. Enter a number of nights between 1 and 14: "))

                            points = int(input("HOW MANY NIGHTS ARE YOU PAYING WITH POINTS: "))
                            while points < 0 or points > night:
                                points = int(input(f"Invalid input. Enter a number of nights (0 to {night}): "))

                            money = night - points
                            points_needed = points * points_needed_per_night
                            balance = int(member_details[5])

                            if points > 0 and balance >= points_needed:
                                balance -= points_needed
                                member_details[5] = str(balance)
                                member_details[4] = str(int(member_details[4]) + points)
                                print(f"Points redeemed for {points} night(s). Remaining balance: {balance}")
                            elif points > 0:
                                print(f"Not enough points. Available balance: {balance}")

                            total_nights = int(member_details[4]) + night
                            member_details[4] = str(total_nights)
                            member_details[5] = str(int(member_details[5]) + money * 2500)

                        else:
                            print("INVALID CHOICE")

                        
                        if total_nights >= 100:
                            member_details[3] = "platinum"
                        elif total_nights >= 30:
                            member_details[3] = "gold"
                        else:
                            member_details[3] = "silver"

                    except ValueError as e:
                        print(f"Invalid input: {e}")

                updated_data.append(",".join(member_details))

        if member_found:
            with open(FILENAME, "w") as file:
                for member in updated_data:
                    file.write(member + "\n")
            print("Member details updated successfully.")
        else:
            print(f"{member_id} is not in our records.")
        
    #-----------------VIEW MEMBERS--------------------
    def view():
        member_details = []
        layout = "{:<10} | {:<12}| {:<12} | {:<18} | {:<15} | {:<15}"
        print(layout.format("member-id","Surname","year-joined","membership-status","nights-booked","points-balance"))
        print("-" * 100)
        with open(FILENAME,"r") as file:
            for line in file:
                line = line.strip()
                member_details = line.split(",")
                if len(member_details) == 6:
                    print(layout.format(member_details[0],member_details[1],member_details[2],member_details[3],member_details[4],member_details[5]))
    #--------------- DELETE MEMBER -------------------
    def delete_member():
        try:
            name = ""
            while name == "":
                print("PLEASE ENTER A VALID MEMEBR CODE")
                name = input("Enter member's code delete membership: ").capitalize()
                
            name = name.strip()
            member_table = []

            thefile = open(FILENAME, "r")
            for line in thefile:
                lines = line.strip()
                member_details = lines.split(",")
                if member_details[0] != name:
                    member_table.append(member_details)
            thefile.close()

            thefile = open(FILENAME, "w")
            for member in member_table:
                thestring = ",".join(member) + "\n"
                thefile.write(thestring)
            thefile.close()
            view()
        except Exception as e:
            print(f"An error occurred while processing input: {e}")
    #----------- VIEW MEMBERSHIP REPORT---------------
    def report():
        status = ""
        while status == "":
            status = input("Enter  a status to see how many members are in it: ").lower()
            
        
        status = status.strip()

        thefile = open(FILENAME, "r")
        member_table = []
        members_s = []
        count = 0

        for line in thefile:
            member_details = line.strip().split(",")
            member_table.append(member_details)

            if member_details[3] == status:
                members_s.append(member_details[1])
                count += 1
        thefile.close()

        members_s = ", ".join(members_s)
        print(f"{status} members: {members_s} \nTotal:{count}")
    #================ MAIN PROGRAM ===================
    menu()
    choice = input("ENTER: ").capitalize()
    while choice != "Q":
        if choice == "1":
            add_member()
        elif choice == "2":
            edit_member()
        elif choice == "3":
            view()
        elif choice == "4":
            delete_member()
        elif choice == "5":
            report()
        else:
            print("INVALID CHOICE")
        menu()
        choice = input("ENTER(Q TO QUIT): ")

#============== MAIN MAIN PROGRAM =================   
with open(filename,"r") as file:
    print("------LOGIN TO CLS SYSTEM---------")
    name = input("ENTER YOUR NAME: ").capitalize()
    code = input("ENTER YOUR EMPLOYEE CODE: ")
    
    access_granted = False  
    
    for line in file:
        line = line.strip()
        employee_details = line.split(",")
        
        if name == employee_details[0] and code == employee_details[1]:
            CLS()  
            access_granted = True
            break  

    if not access_granted:
        print("ACCESS DENIED")