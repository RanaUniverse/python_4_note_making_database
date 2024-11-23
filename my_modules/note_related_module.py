"""
Here will only the fun mainly focus on making the notes
and notes data and so on to retrieve and so on
"""

import datetime

from faker import Faker

from sqlmodel import (
    select,
    Session,
)

# import some error
from sqlalchemy.exc import IntegrityError

from my_modules.colorful_terminal_module import TColor

from my_modules.database import engine
from my_modules.models import NotePart, UserPart


fake = Faker()


def make_a_new_note():
    """
    what i plan to make is: First it will ask for users verification,
    if the verificaion is successful then it will prompts to make new note
    otherwise it will ask the user to make new account there,
    0. It will first try to get the username if username not given it will ask for user id,

    1. it need Title
    2. it need the data to keep in record
    3. the note id will automatically generated
    """
    # thsi will break when there is correct username otherwise only reprompt
    print(
        f"{TColor.MAGENTA}{TColor.BOLD}"
        "Please fill in all details to create a new note.👇👇👇"
        f"{TColor.RESET}"
    )

    while True:
        username = input("Just give your username here: ").strip()
        if username == "***":
            print("No Note is Making ❌❌❌, Exiting...")
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
                    print(f"Hello, @{username}, Please Write Your Password Below👇👇👇")
                    break

    # Now it will ask for passwrod if he give wrong password it will ask
    # to give right password then others logic will come to execute
    while True:
        password_from_user = input("Please Give Your Correct Password: ").strip()
        if password_from_user == "":
            password_from_user = None
        if password_from_user == user_obj.password:
            print("You have give correct password✅")
            break
        else:
            print("❌❌❌Wrong Password Try Again ❌❌❌")

    # After this password got verified, i will check about the note part
    # saying user to make a new note
    print("I will give You note id after this note making is successful")
    print("🎉🎉🎉You Can Now make new Note below🎉🎉🎉")

    # This below is note making started logic start
    while True:
        note_title = input("What is the TITLE of your Note: ")
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
    print("Write The Subject Of Your Note 👇👇👇")
    note_content = input("Wtite Your Note's Subject Here and press Enter: ")

    if not note_content:
        note_content = None
        print("This Note is Empty🪹")
    else:
        print(f"Subject Of Your Note is:👇👇👇\n\n{note_content}")

    # Below part is for trying to save the note in the database
    while True:
        # i will change the below note id logic
        # making a random note id 🍌🍌🍌
        note_id = fake.random_number(digits=5, fix_len=True)
        now_time_ist = datetime.datetime.now(
            datetime.timezone(datetime.timedelta(hours=5, minutes=30))
        )
        # i am using user obj as there is relationship
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
                    "Your Note Data is saved with the Note id: "
                    f"{note_obj.note_id}"
                    f"{TColor.RESET}"
                )
            break

        except IntegrityError as e:
            error_message = str(e.orig)
            if "note_obj.note_id" in error_message:
                print("This note id is already exists,Generating a new one again.")
            else:
                print("One Unknow error when saving, Retry pls: ", e)


def edit_a_old_note():
    """
    This Funcion will take the note id and then
    ask for correct user id and password and then it will
    edit the old note
    """
    print(
        f"{TColor.MAGENTA}{TColor.BOLD}"
        f"Please Fillup all the details Below to edit your own note."
        f"{TColor.RESET}"
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

    # This is for checking the username
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

    # This is for checking the password
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
        f"Now you can edit your note title. If you leave it blank, "
        f"no changes will be made."
    )

    # Now i will give user a way if he want to delete the note
    # or he want to edit his note part
    del_or_edit = input(
        f"{TColor.RED}If you want to delete type 'Delete' or 'del' or 'remove' {TColor.RESET}"
        f"and press enter otherwise press none: "
    ).lower()

    # if del_or_edit == "delete" or del_or_edit == "del":
    if del_or_edit in {"delete", "del", "remove"}:
        with Session(engine) as session:
            session.delete(note_obj)
            session.commit()
            print(
                f"{TColor.RED}This Note has been deleted successfully. "
                f"{TColor.RESET}\nOld Note Data is:\n"
                f"{TColor.YELLOW}{note_obj}{TColor.RESET}"
            )

        return None
    else:
        print("You are now going to edit your note.")

    # Now i will make the logic of chnage the title and content
    print(f"Current title: \n" f"{TColor.BLUE}{note_obj.title}{TColor.RESET}")

    new_title = input("Enter a new title or press Enter to keep the current title: ")
    if new_title:
        note_obj.title = new_title
        print("Title updated.✅")
    else:
        print("Title remains unchanged.")

    print(f"Current Note Subject is: " f"{TColor.BLUE}{note_obj.note}{TColor.RESET}")
    # new_note_data = input("Enter new content or nothing to unchange: ")

    text = (
        "To append new information, type '0' or 'append'.\n"
        "To replace the old content with new content, type '1' or 'replace': "
    )

    # below part checks if i am choose correct thigs to append or
    # replace whole note content so i use while
    while True:
        edit_choice = input(text)

        # if edit_choice == "0" or edit_choice == "append":
        if edit_choice in {"0", "append"}:

            extra_data = input("Please Write New Data to append to the last: ")
            if extra_data:

                if not note_obj.note:
                    note_obj.note = ""
                note_obj.note += f"\n{extra_data}"
                now_time_ist = datetime.datetime.now(
                    datetime.timezone(datetime.timedelta(hours=5, minutes=30))
                )
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

        # elif edit_choice == "1" or edit_choice == "replace":
        elif edit_choice in {"1", "replace"}:

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


def all_note_of_a_user():
    """
    This will show all the note one user have
    made for him, it will show the note id and title of all the notes

    *** Here the username and password checking part is
        i just copy paste from previous funcion
    """

    print("Please provide the correct details, and I will display all Your Notes")

    # Asking for user name and password
    while True:
        username = input(f"What is your username: ")
        if username == "***":
            print(f"THis work is cancelling start again")
            return None
        if not username:
            print("Please Enter a valid username and press enter")
            continue
        if username:
            print("Searching For your username's existance 🔍🔍🔍.")
            with Session(engine) as session:
                statement = select(UserPart).where(UserPart.username == username)
                user_row = session.exec(statement).first()
                if not user_row:
                    print(
                        f"❌❌❌This Username:- @{username} is not in our system. "
                        "Pls Retry❌❌❌"
                    )
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
        password = input(f"Hello @{username}, Write Password: ")
        if not password:
            password = None
        if password == password_of_the_row:
            print(f"You have write Right Password✅")
            break
        else:
            print("❌❌❌Wrong Password Try Again ❌❌❌")

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
