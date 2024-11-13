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


if not phone_no:
    phone_no = None
    print("No valid phone number provided.")
