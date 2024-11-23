"""
Here i will make the funcitons and needful things for user table 
related codes and working, i have only do these user code here in this module

1. register_for_new_user()

"""

import datetime

from faker import Faker

from sqlmodel import (
    Session,
    select,
    # SQLModel,
)
from sqlalchemy.exc import IntegrityError

from my_modules.colorful_terminal_module import TColor

from my_modules.models import UserPart
from my_modules.database import engine


fake = Faker()


def register_for_new_user():
    """
    I am making this fun which will take inputs from
    the user in the terminal part and add a new user data in the
    database.
    """
    print(TColor.BOLD + "Please Register Below For New Accoutn👇:" + TColor.RESET)
    message = (
        "Please Fillup The Details Below & Press Enter to Proceed..."
        " Write '***' and press enter to exit this process"
    )
    print(message)

    while True:
        username = input("Choose a username (Required): ").strip()

        # Exist when *** Comes
        valid_username = fake.user_name()
        if username == "***":
            print(f"Registration Process Has been cancelled")
            return None

        if len(username) <= 3:
            print(
                f"Username should be at least 4 characters long, "
                f"e.g., {TColor.BLUE}@{valid_username}{TColor.RESET}"
            )
            continue

        if username.isdigit():
            print(
                f"Username cannot be entirely numeric. "
                f"e.g., {TColor.BLUE}@{valid_username}{TColor.RESET}"
            )
            continue
        
        if " " in username:
            print(
                f"Username should not contain whitespace, "
                f"e.g., {TColor.BLUE}@{valid_username}{TColor.RESET}"
            )
            continue

        else:
            print(f"Your Username is: {username}")
            break

    # 🍌🍌🍌 Just For Checking the final value in the loop

    while True:
        full_name = input(f"Please Enter Your Full Name: ").strip()

        if not full_name:
            print(f"Hello {username} You havn't any Full Name ❌")
        else:
            print(f"Your Full Name is: {full_name} ✅")
        break

    while True:
        email_id = input("Please Enter Your Email ID (Optional): ").strip()
        if not email_id:
            print("No email ID provided. Skipping... 🚫")
        else:
            print(f"Your Email ID is: {email_id} ✅")
        break

    while True:
        phone_no = input("What is the SIM card number? (Optional) ").strip()

        #  user dont write anything so it is None now ok below
        if not phone_no:
            phone_no = None
            print("No Phone Number is Provided ❌")
            break  # Exit loop, phone number is optional

        # Check if the input is a valid 10-digit Indian number
        # Below i make some condition to think if the number is valid or not
        elif phone_no.isdigit() and len(phone_no) == 10 and phone_no[0] in "6789":
            phone_no = int(phone_no)  # Convert to integer for storing in the database
            print(f"Your Valid Phone Number: {phone_no} ✅✅✅")
            break  # Valid phone number, exit loop

        # Handle invalid cases based on the first digit
        elif phone_no.isdigit() and phone_no[0] in "012345":
            print(
                f"❌ The number you entered starts with {phone_no[0]}, "
                "which is invalid. Please try again."
            )

        else:
            print(
                "❌ Invalid input. Please enter a 10-digit Indian mobile "
                "number starting with 6, 7, 8, or 9."
            )

    password = input("Select a Password For YOUR Account: ")
    if not password:
        password = None
        print(f"No Password is given by you ❌")
    else:
        print(
            f"Your Password is: {TColor.YELLOW}{password}{TColor.RESET} "
            f"Your Password  is {len(password)} char longs."
        )

    # Below Part is for starting of database logic to insert my data
    # The user_id will generated from the faker library for now🍌
    # This will give 7 digit integer, maybe sometiem it can not unique
    # for now i have no more idea on how to takle this
    while True:
        # Generate user_id initially
        user_id = fake.random_number(digits=5, fix_len=True)

        now_time_ist = datetime.datetime.now(
            datetime.timezone(datetime.timedelta(hours=5, minutes=30))
        )
        user_obj = UserPart(
            username=username,
            user_id=user_id,
            full_name=full_name,
            email_id=email_id,
            phone_no=phone_no,
            register_time=now_time_ist,
            password=password,
        )

        try:
            with Session(engine) as session:
                session.add(user_obj)
                session.commit()
                session.refresh(user_obj)
                print(
                    f"{TColor.GREEN}"
                    f"User '{username}' registered successfully with ID {user_id}!"
                    f"{TColor.RESET}"
                )
                break

        except IntegrityError as e:
            error_message = str(e.orig)

            if "user_data.username" in error_message:
                print(
                    f"{TColor.YELLOW}"
                    f"❌ The username({username}) is already taken. "
                    "Please choose a different username."
                    f"{TColor.RESET}"
                )
                username = input(f"Please select Another Username: {username}")

                if len(username) <= 3:
                    print(f"Username Should be minimum 4 character long")

                continue

            elif "user_data.user_id" in error_message:
                print(
                    "❌ The generated User ID already exists. Generating a new User ID..."
                )
                user_id = fake.random_number(5, fix_len=True)

            else:
                print(
                    "❌ An unexpected error occurred. Please check your input values."
                )
                break


def delete_a_user_data():
    """This will ask for users username, and password to del"""
    print(
        f"{TColor.RED}"
        "You Are Going To Delete Your Account Please Be Careful🚨🚨🚨"
        f"{TColor.RESET}"
    )

    # Asking for user name and password
    while True:
        username = input(f"What is your username: ")
        if not username:
            print("Please Enter a valid username and press enter")
            continue
        if username == "***":
            print(f"You are exiting from delete your user account")
            return None
        if username:
            print("Searching For your username's existance 🔍🔍🔍.")

            with Session(engine) as session:
                statement = select(UserPart).where(UserPart.username == username)
                user_row = session.exec(statement).first()
                if not user_row:
                    print(f"This Username:- {username} is not Found. Pls Retry 🔄")
                    continue
                else:
                    print(
                        f"{TColor.RED}"
                        f"You are going to delete @{username} Account 🗑️"
                        f"{TColor.RESET}"
                    )
                    password_of_the_row = user_row.password
                    if password_of_the_row:
                        print(f"Password Hint Len: {len(password_of_the_row)}")
                    else:
                        print(f"You have not any password for your profile")
                    break

    # Checking for passowrd match or not
    while True:
        password = input(f"Hello @{username}, what is Password: ")
        if not password:
            password = None
        if password == password_of_the_row:
            print(f"You have write Right Password✅")
            break
        else:
            print(f"This password not matched pls retry again.")

    # i want to make a logic here of deleting this user's notes
    # or not, i am not understand how to do this , i want suppose
    # give user two choice,
    # 1: their notes will got deleted,
    # 2: there notes will be transferred to othres account,
    # 3: they for now want to del this note and later want to own this note,
    #   so here i need to pass some unique id after account delete, which
    #   they can use to overown their own notes

    print(f"User Account Delete Logic has not made Yet, 💔💔💔 ")
