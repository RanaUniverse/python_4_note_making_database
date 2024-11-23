"""
First to work with existing sample data run this below command in the terminal:


cp my_files/fake_database_file.db database.db && echo "✅ Successfully copied to database.db. 
This file contains some sample data." || echo "❌ Failed to copy the database file."


This will be my app part completely

This app will be a note storing app

1. I have the tables in the models.py
2. i have the engine and table created files in the database.py 
3. i have changes my functions into different my modules for clean interface
"""

from my_modules.colorful_terminal_module import TColor

from my_modules.database import create_db_and_engine

from my_modules.note_related_module import (
    all_note_of_a_user,
    edit_a_old_note,
    make_a_new_note,
)
from my_modules.user_related_module import (
    delete_a_user_data,
    register_for_new_user,
)


def terminal_color_check(show_color: bool = True):
    """
    Prints colorful text in the terminal. If show_color is False,
    disables color by uncommenting the disable_color line.
    """
    if not show_color:
        TColor.disable_color()  # This disables color output in the terminal

    print(
        f"{TColor.RED}This "
        f"{TColor.GREEN}is "
        f"{TColor.YELLOW}Colorful "
        f"{TColor.BLUE}Text "
        f"{TColor.MAGENTA}in "
        f"{TColor.BOLD}Terminal.{TColor.RESET}"
    )


def main_old():
    "This part is just for chekcing code"
    terminal_color_check()
    create_db_and_engine()

    # delete_a_user_data()
    all_note_of_a_user()

    # register_for_new_user()
    # make_a_new_note()
    # edit_a_old_note()


def main():
    import time

    terminal_color_check(show_color=True)
    create_db_and_engine()

    # This below part will just for Showing off 🍌🍌🍌
    print(f"\n{TColor.MAGENTA}Starting Rana Universe App 🍌🍌🍌{TColor.RESET}", end=" ")
    for _ in range(25):
        time.sleep(0.04)
        print(".", end="", flush=True)
    # time.sleep(1)
    time.sleep(0.1)

    while True:
        print(f"\n{TColor.MAGENTA}{TColor.BOLD}Choose an action: {TColor.RESET}")

        print("0. Exit")
        time.sleep(0.1)

        print("1. Register a new user")
        time.sleep(0.1)

        print("2. Make a new note")
        time.sleep(0.1)

        print("3. Edit an old note")
        time.sleep(0.1)

        print("4. Delete a user")
        time.sleep(0.1)

        print("5. View all notes of a user")
        time.sleep(0.1)

        choice = input("Please choose anything here (0-5): ").strip()

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
        elif choice == "0":
            print("Exiting the program. Goodbye! 👋👋👋")
            break
        else:
            print("Invalid choice. Please try again. ⚠️")

        # Wait for 1 seconds to show the loop again
        print("\nLoading", end=" ")
        for _ in range(20):
            time.sleep(0.01)
            print(".", end="", flush=True)
        time.sleep(1)


if __name__ == "__main__":
    # main_old()
    main()
