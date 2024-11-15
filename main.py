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


def register_for_new_user():
    """
    I am making this fun which will take inputs from
    the user in the terminal part and add a new user data in the
    database
    """
    print(TColor.BOLD + "A New User Register Page has Open:" + TColor.RESET)
    message = (
        "Please Fillup The Details Below & Press Enter to Proceed..."
        " Write '***' and press enter to exit this process"
    )
    print(message)

    while True:
        username = input("Choose a username (Required): ").strip()

        # Exist when *** Comes
        if username == "***":
            print(f"Registration Process Has been cancelled")
            return None

        if len(username) <= 3:
            print(f"Username Should be minimum 4 character long")
            continue
        else:
            print(f"Your Username is: {username}")
            break

    # 🍌🍌🍌 Just For Checking the final value in the loop
    # print(f"After the loop finish the username is: {username}")

    while True:
        full_name = input(f"Please Enter Your Full Name: ")

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
        print(f"No Password is given by you ❌")
    else:
        print(f"Your Password is: {password} which is {len(password)} char longs.")

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
                    f"❌ The username({username}) is already taken. Please choose a different username."
                    f"{TColor.RESET}"
                )
                username = input(f"Please select another username than: {username}")

                if len(username) <= 3:
                    print(f"Username Should be minimum 4 character long")
                    continue

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


def make_a_new_note():
    """
    what i plan to make is: First it will ask for users verification,
    if the verificaion is successful then it will prompts to make new note
    otherwise it will ask the user to make new account there,
    1. It will first try to get the username if username not given it will ask for user id,

    1. it need Title
    2. it need the data to keep in record
    3. the note id will automatically generated
    """
    # thsi will break when there is correct username otherwise only reprompt
    print(
        f"{TColor.MAGENTA}{TColor.BOLD}Please fill in all details "
        f"to create a new note.{TColor.RESET}"
    )

    while True:
        username = input("Just give your username here: ").strip()
        if username == "***":
            print("No Note is Making, Exiting...")
            return None

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
            print("You have give correct password✅")
            break
        else:
            print("❌❌❌Wrong Password❌❌❌")

    # After this password got verified, i will check about the note part
    # saying user to make a new note
    print("I will give You note id after this note making is successful")
    print("🎉🎉🎉You Can Now make new Note below🎉🎉🎉")

    while True:
        note_title = input("What is the title of your note: ")
        if not note_title:
            note_title = None  # i make it so that it will insert Null in the database
            print("You have not any title for this note.")
            break
        elif len(note_title) > 25:
            print("Please write the note title in 25 letter")
        else:
            print("Your Title:", note_title)
            break

    # Below is the part for writing the note
    print("Write The Content of your NOte. I'll send your note_id afterward.")
    note_content = input("Wtite Your Note Here and press Enter: ")

    if not note_content:
        note_content = None
        print("This Note is Empty🪹")
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
                print(
                    f"{TColor.GREEN}"
                    "Your Note Data is saved with the Note id:"
                    f"{note_obj.note_id}"
                    f"{TColor.RESET}"
                )
            break

        except IntegrityError as e:
            error_message = str(e.orig)
            if "note_obj.note_id" in error_message:
                print("This note id is already, i am generating a new one again.")
            else:
                print("One Unknow error when saving, retry pls: ", e)


def edit_a_old_note():
    """
    This Funcion will take the note id and then
    ask for correct user id and password and then it will
    edit the old note
    """
    print(
        f"{TColor.MAGENTA}{TColor.BOLD}Please Fillup all the details"
        f"Below to edit your own note.{TColor.RESET}"
    )

    # This below part is for giving note id checking;
    while True:
        note_id = input(f"What is the note id of your note which you get previously: ")

        if not note_id:
            print("Please Write Your Note's ID and press enter.")
            continue
        else:
            if not note_id.isdigit():
                print("Please Give Correct note id which is integer value.")
                continue
            if note_id:
                note_id = int(note_id)
                print(f"Searching For This Note ID: {note_id}🔍")
            with Session(engine) as session:
                statement = select(NotePart).where(NotePart.note_id == note_id)
                note_obj = session.exec(statement).first()
                if not note_obj:
                    print("This Note Id is not associated with any Note")
                    continue
                if note_obj:
                    note_password = note_obj.user.password  # type: ignore
                    if note_password:
                        print(
                            f"You have set password for this note, pls write ur passwrod."
                        )
                    else:
                        print(f"You have not any passwrod setup for this note.")
                    break

    # Now it will verify the user's password to allow him to edit note
    print(f"Please Give Correct Id Password for this Note: {note_id}")

    while True:
        username = input(f"What is Your Username: ")
        if not username:
            print(f"Please Write ur username Connected with {note_id}🔁")
            continue
        if username == "***":
            print(f"You are exiting from edit this note")
            return None
        if username != note_obj.user.username:  # type: ignore
            print(f"This username is not associated with this {note_id}❌")
            continue

        if username == note_obj.user.username:  # type: ignore
            print(f"Your Username is matched against this note thanks.✅")
            break

    while True:
        password = input(f"What is ur password(username: {username}): ")
        if not password:
            password = None
        if note_obj.user.password != password:  # type: ignore
            print(f"Hello @{username}, Please Give correct id password, try agian")
            continue
        if note_obj.user.password == password:  # type: ignore
            print(f"Hello @{username.upper()}, Thanks For Verify Your Account.")
            break

    # NOw on this line the user has verified username and password

    print(
        f"NOw you can edit your note title, if you dont press "
        f"anything then i will not chang anything"
    )

    # Now i will give user a way if he want to delete the note
    # or he want to edit his note part
    del_or_edit = input(
        "If you want to delete type Delete and press enter otherwise press none: "
    )
    if del_or_edit == "delete" or del_or_edit == "del":
        with Session(engine) as session:
            session.delete(note_obj)
            session.commit()
            print(
                f"This Note has been deleted successully.\nOld Note Data is:\n{note_obj}"
            )
        return None
    else:
        print("You are now going to edit your note.")

    # Now i will make the logic of chnage the title and content
    print(f"Current title: {note_obj.title}")
    new_title = input("Enter a new title or press Enter to keep the current title: ")
    if new_title:
        note_obj.title = new_title
        print("Title updated.✅")
    else:
        print("Title remains unchanged.")

    print(f"Current note content: {note_obj.note}")
    # new_note_data = input("Enter new content or nothing to unchange: ")

    text = (
        f"If you want to append new information press 0 or 'append' "
        f"If you want to replace old content by new content press 1 or 'replace',"
    )

    # below part checks if i am choose correct thigs to append or
    # replace whole note content so i use while
    while True:
        edit_choice = input(text)

        if edit_choice == "0" or edit_choice == "append":
            extra_data = input("Please Write New Data to append to the last: ")
            if extra_data:

                if not note_obj.note:
                    note_obj.note = ""
                now_time_ist = datetime.datetime.now(
                    datetime.timezone(datetime.timedelta(hours=5, minutes=30))
                )
                note_obj.note += f"\n{extra_data}"
                note_obj.edited_date = now_time_ist
                print("New Data Appended.➕")

                with Session(engine) as session:
                    session.add(note_obj)
                    session.commit()

            elif not extra_data:
                print("No Extra Data is appending")

            else:
                print("No extra data has been appendedd")
            break

        elif edit_choice == "1" or edit_choice == "replace":
            new_data = input("Enter the new data to replace fully or just enter:")
            if new_data:
                now_time_ist = datetime.datetime.now(
                    datetime.timezone(datetime.timedelta(hours=5, minutes=30))
                )
                note_obj.note = new_data
                note_obj.edited_date = now_time_ist
                with Session(engine) as session:
                    session.add(note_obj)
                    session.commit()
            else:
                print("No New data is given. note will not change")
            break
        else:
            print("Please select any valid either 0=append or 1=replace")
            continue


def delete_a_user_data():
    """This will ask for users username, and password to del"""
    print("You Are Going To Delete Your Account Please Be Careful🚨🚨🚨")

    # Asking for user name and password
    while True:
        username = input(f"What is your username: ")
        if not username:
            print("Please Enter a valid username and press enter")
            continue
        if username == "***":
            print(f"Exiting This current Deleting Work")
            return None
        if username:
            print("Searching For your username existance...")
            with Session(engine) as session:
                statement = select(UserPart).where(UserPart.username == username)
                user_row = session.exec(statement).first()
                if not user_row:
                    print(f"This Username:- {username} is not in our system. Pls Retry")
                    continue
                else:
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

    print(
        f"This Function has not made yet, as it need some confusion "
        f"of what to do with the notes the user own, this is why i am "
        f"not able to do this task for now"
    )


def all_note_of_a_user():
    """
    This will show all the note one user have
    made for him, it will show the note id and title of all the notes

    *** Here the username and password checking part is
        i just copy paste from previous funcion
    """

    print(f"Please Fillup Correct Details and i will show all the note you have")

    # Asking for user name and password
    while True:
        username = input(f"What is your username: ")
        if not username:
            print("Please Enter a valid username and press enter")
            continue
        if username:
            print("Searching For your username existance...")
            with Session(engine) as session:
                statement = select(UserPart).where(UserPart.username == username)
                user_row = session.exec(statement).first()
                if not user_row:
                    print(f"This Username:- {username} is not in our system. Pls Retry")
                    continue
                else:
                    password_of_the_row = user_row.password
                    if password_of_the_row:
                        print(f"Password Hint Len: {len(password_of_the_row)}")
                    else:
                        print(f"You have not any password for your profile")
                    break

    user_id_of_him = user_row.user_id

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

    with Session(engine) as session:
        statement = select(NotePart).where(NotePart.user_id == user_id_of_him)
        results = session.exec(statement).all()
        print(results)

        # Display note_id and title line by line

        if results:
            print(f"Hello @{username}, This below are your Notes:👇👇👇")
            for note in results:
                print(
                    f"Note ID: {TColor.RED}{note.note_id}{TColor.RESET}, "
                    f"Title: {TColor.YELLOW}{note.title}{TColor.RESET}"
                )

        else:
            print(
                f"Hello Boss @{username} You have not any note here, pls go make a note first"
            )


def terminal_color_check():
    """
    I just need to uncomment first line if i want to not any color
    """
    # TColor.disable_color()
    print(
        f"{TColor.RED}This "
        f"{TColor.GREEN}is "
        f"{TColor.YELLOW}Colorful "
        f"{TColor.BLUE}Text "
        f"{TColor.MAGENTA}in "
        f"{TColor.BOLD}Terminal.{TColor.RESET}"
    )


def main_old():
    terminal_color_check()
    create_db_and_engine()

    # delete_a_user_data()
    all_note_of_a_user()

    # register_for_new_user()
    # make_a_new_note()
    # edit_a_old_note()


def main():
    import time

    terminal_color_check()
    create_db_and_engine()

    # This below part will just for Showing off 🍌🍌🍌
    print(f"\n{TColor.MAGENTA}Starting Rana Universe App 🍌🍌🍌{TColor.RESET}", end=" ")
    for _ in range(3):
        time.sleep(1)
        print(".", end="", flush=True)
    time.sleep(1)
    time.sleep(0.1)

    while True:
        print(f"\n{TColor.MAGENTA}{TColor.BOLD}Choose an action: {TColor.RESET}")
        print("1. Register a new user")
        time.sleep(0.2)

        print("2. Make a new note")
        time.sleep(0.2)

        print("3. Edit an old note")
        time.sleep(0.2)

        print("4. Delete a user")
        time.sleep(0.2)

        print("5. View all notes of a user")
        time.sleep(0.2)

        print("6. Exit")

        choice = input("Please choose anything here (1-6): ").strip()

        if choice == "1":
            register_for_new_user()
        elif choice == "2":
            make_a_new_note()
        elif choice == "3":
            edit_a_old_note()
        elif choice == "4":
            delete_a_user_data()
        elif choice == "5":
            all_note_of_a_user()
        elif choice == "6":
            print("Exiting the program. Goodbye! 👋👋👋")
            break
        else:
            print("Invalid choice. Please try again. ⚠️")

        # Wait for 3 seconds to show the loop again
        print("\nLoading", end=" ")
        for _ in range(3):
            time.sleep(1)
            print(".", end="", flush=True)
        time.sleep(1)


if __name__ == "__main__":
    # main_old()
    main()
