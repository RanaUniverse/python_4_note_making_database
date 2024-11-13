empty_msg = "If you don't want any data, just press Enter without typing anything."
phone_no = input(" What is the sim card number? (Optional) " + empty_msg).strip()


# below logic is when i will have phone nubmer and not start with 0 then it will breake the loop
while phone_no:
    if phone_no.isdigit() and len(phone_no) == 10:
        if phone_no[0] in "6789":
            print(f"Your phone number: {phone_no}")
            phone_no = int(phone_no)
            print(f"This is a valid phone number. {type(phone_no)}")
            break
        else:
            print("Number should start with a digit between 6 and 9.")

    else:
        print("Invalid phone number. Please enter a 10-digit Indian mobile number.")
    phone_no = input(
        "Please enter a valid 10-digit number or press Enter to skip: "
    ).strip()


if not phone_no:
    phone_no = None
    print("No valid phone number provided.")


# Below is the new learning and easy way


# Define the prompt message
empty_msg = "If you don't want any data, just press Enter without typing anything."
phone_no = input("What is the SIM card number? (Optional) " + empty_msg).strip()

while True:
    if not phone_no:
        phone_no = None
        print(
            "You just press enter means you dont want to give ur number so i am not saving ur number"
        )
        break  # Exit the loop since no input was provided

    # Check if the input is a valid 10-digit number that starts with 6, 7, 8, or 9
    elif phone_no.isdigit() and len(phone_no) == 10 and phone_no[0] in "6789":
        print(f"Your phone number: {phone_no}")
        phone_no = int(phone_no)
        print(f"This is a valid phone number. {(phone_no)}")
        break  # Exit the loop since we got a valid phone number

    elif phone_no.isdigit() and len(phone_no) == 10 and phone_no[0] in "012345":
        print(
            f"YOu have give a 10 digit number but it not start with valid it satart with {phone_no[0]}, which is invalid for indian phone number so pls try again"
        )
        phone_no = input(
            "Please enter a valid 10-digit number or press Enter to skip: "
        ).strip()

    # If the input is invalid, re-prompt the user
    else:
        print(
            "Invalid phone number. Please enter a 10-digit Indian mobile number starting with 6, 7, 8, or 9."
        )
        phone_no = input(
            "Please enter a valid 10-digit number or press Enter to skip: "
        ).strip()
