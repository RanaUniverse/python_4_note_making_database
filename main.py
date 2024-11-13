"""
This will be my app part completely

This app will be a note storing app

1. I have the tables in the models.py
2. i have the engine and table created files in the database.py 
3. I 
"""

import datetime

from faker import Faker

from sqlmodel import (
    select,
    Session,
)

# import some error
from sqlalchemy.exc import IntegrityError

from my_modules.database import create_db_and_engine, engine
from my_modules.models import NotePart, UserPart

from my_modules.colorful_terminal_module import TColor


fake = Faker()


def insert_one_new_user_row(
    username: str,
    user_id: int,
    full_name: str | None = None,
    email_id: str | None = None,
    phone_no: int | None = None,
    register_time: datetime.datetime | None = None,
    notes_count: int | None = None,
    is_allowed: bool = True,
    password: str | None = None,
):
    """
    This is incomplete no need to use
    i am making this fun which will take the parameter of the UserPart table
    columns and then it will save them in the database table i will just call
    this fun in other places.
    """
    user_obj = UserPart(
        username=username,
        user_id=user_id,
        full_name=full_name,
        email_id=email_id,
        phone_no=phone_no,
        register_time=register_time,
        notes_count=notes_count,
        is_allowed=is_allowed,
        password=password,
    )
    print(user_obj)


def register_for_new_user():
    """
    I am making this fun which will take inputs from
    the user in the terminal part and add a new user data in the
    database
    """
    print(TColor.BOLD + "A New User Register Page has Open:" + TColor.RESET)
    message = (
        "Please make ready your: Username, Full Name, Email ID, Phone No, "
        "Password.\nAfter this, we will make a unique user ID for you. Only "
        "the username section is required. If you do not provide other "
        "information, we will generate it for you and send it back. If the "
        "username already exists, you need to choose a new one.\n"
        "Making a new User Account!!!"
    )
    print(message)

    # i need to take username from user

    username = input("CHoose a username (required): ").strip()
    if username == "***":
        return None  # i just want to exis the fun
    while not username:
        print("Username is required.")
        username = input("Please enter a username and then press enter: ").strip()
    print(f"Your Valid Username: {username} ✅✅✅")

    full_name = input("Please Enter Your Full Name: ").strip()

    if not full_name:
        full_name = None
        print(f"No Full Name is Provided ❌❌❌")
    else:
        print(f"Your Full Name is: {full_name} ✅✅✅")

    email_id = input("What is your Email Id(Optional): ")
    if not email_id:
        email_id = None
        print(f"No Email Id is Provided ❌❌❌")
    else:
        print(f"Your Email id is: {email_id} ✅✅✅")

    while True:
        phone_no = input("What is the SIM card number? (Optional) ").strip()

        #  user dont write anything so it is None now ok below
        if not phone_no:
            phone_no = None
            print("No Phone Number is Provided ❌❌❌")
            break  # Exit the loop, phone number is optional

        # Check if the input is a valid 10-digit Indian number
        elif phone_no.isdigit() and len(phone_no) == 10 and phone_no[0] in "6789":
            phone_no = int(phone_no)  # Convert to integer for storing in the database
            print(f"Your Valid Phone Number: {phone_no} ✅✅✅")
            break  # Valid phone number, exit loop

        # Handle invalid cases based on the first digit
        elif phone_no.isdigit() and phone_no[0] in "012345":
            print(
                f"❌ The number you entered starts with {phone_no[0]}, which is invalid. Please try again."
            )

        else:
            print(
                "❌ Invalid input. Please enter a 10-digit Indian mobile number starting with 6, 7, 8, or 9."
            )

    password = input("Select a Password For YOur account: ")
    if not password:
        password = None
        print(f"No Password is given by you ❌❌❌")
    else:
        print(f"Your Password is: {password} which is {len(password)} char longs.")

    now_time_ist = datetime.datetime.now(
        datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    )

    # Below Part is for starting of database logic to insert my data
    # The user_id will generated from the faker library for now🍌
    # This will give 7 digit integer, maybe sometiem it can not unique
    # for now i have no more idea on how to takle this
    while True:
        # Generate user_id initially
        user_id = fake.random_number(digits=5, fix_len=True)
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
                print(f"User '{username}' registered successfully with ID {user_id}!")
                break

        except IntegrityError as e:
            error_message = str(e.orig)

            if "user_data.username" in error_message:
                print(
                    "❌ The username is already taken. Please choose a different username."
                )
                username = input("Enter a new username: ").strip()

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


def make_a_new_note():
    """
    what i plan to make is: First it will ask for users verification,
    if the verificaion is successful then it will prompts to make new not
    otherwise it will ask the user to make new account there,
    1. It will first try to get the username if username not given it will ask for user id,

    1. it need Title
    2. it need the data to keep in record
    3. the note id will automatically generated
    """
    # thsi will break when there is correct username otherwise only reprompt
    print(f"Please Fillup all the details Below to make a new Note.")
    while True:
        username = input("Just give your username here: ").strip()
        if not username:
            print("Please write ur username👇👇👇")
            # break # loop will continue if the username not given
        else:
            with Session(engine) as session:
                statement = select(UserPart).where(UserPart.username == username)
                user_obj = session.exec(statement).first()
                if not user_obj:
                    print("This is not any valid username👇👇👇")
                else:
                    print(f"Hello, {username}, Please Write Your Password Below👇👇👇")
                    break
    # Now it will ask for passwrod if he give wrong password it will ask
    # to give right password then others logic will come to execute
    while True:
        password_from_user = input("Please Give Your Correct Password: ")
        if password_from_user == "":
            password_from_user = None
        if password_from_user == user_obj.password:
            print("✅✅✅You have give correct password✅✅✅")
            break
        else:
            print("❌❌❌Wrong Password❌❌❌")

    # After this password got verified, i will check about the not part saying user
    # to make a new note
    print("I will give You note id after this note making is successful")
    print("🎉🎉🎉You Can Now make new Note below🎉🎉🎉")

    while True:
        note_title = input("What is the title of your note: ")
        if not note_title:
            note_title = None  # i make it so that it will insert Null in the database
            print("You have not any title for this note.")
            break
        elif len(note_title) > 25:
            print("Please write the note title as small as 25 letter")
        else:
            print("Your Title:", note_title)
            break

    # Below is the part for writing the note
    print("Write The Content of your NOte. I'll send your note_id afterward.")
    note_content = input("Wtite Your Note Here and press Enter: ")

    if not note_content:
        note_content = None
        print("This Note is Empty🪹🪹🪹")
    else:
        print(f"Your Note has been saved:\n\n{note_content}")

    # Below part is for trying to save the note in the database
    while True:
        # making a random note id
        note_id = fake.random_number(digits=5, fix_len=True)
        now_time_ist = datetime.datetime.now(
            datetime.timezone(datetime.timedelta(hours=5, minutes=30))
        )
        note_obj = NotePart(
            title=note_title,
            note=note_content,
            note_id=note_id,
            created_date=now_time_ist,
            # user_id=user_obj.user_id,
            user=user_obj,
        )
        try:
            with Session(engine) as session:
                session.add(note_obj)
                session.commit()
                session.refresh(note_obj)
                print("Your Note Data is saved with the Note id:", note_obj.note_id)
            break
        except IntegrityError as e:
            error_message = str(e.orig)
            if "note_obj.note_id" in error_message:
                print("This note id is already, i am generating a new one again.")
            else:
                print("One Unknow error when saving:", e)


def terminal_color_check():
    # TColor.reset_colors()
    print(
        f"{TColor.RED}This "
        f"{TColor.GREEN}is "
        f"{TColor.YELLOW}Colorful "
        f"{TColor.BLUE}Text "
        f"{TColor.MAGENTA}in "
        f"{TColor.BOLD}Terminal.{TColor.RESET}"
    )


def main():
    terminal_color_check()
    create_db_and_engine()
    register_for_new_user()
    make_a_new_note()
    ...


if __name__ == "__main__":
    main()
