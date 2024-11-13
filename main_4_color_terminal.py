class bcolors:
    # Colors
    RED = '\033[31m'
    WHITE = '\033[37m'

    # Styles
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Example of printing a sentence with the chosen colors and styles
print(f"{bcolors.RED}This is a red sentence!{bcolors.ENDC}")
print(f"{bcolors.WHITE}This is a white sentence!{bcolors.ENDC}")
print(f"{bcolors.BOLD}{bcolors.OKCYAN}This is bold and cyan!{bcolors.ENDC}")
print(f"{bcolors.WARNING}This is a warning message!{bcolors.ENDC}")
print(f"{bcolors.HEADER}This is a header message!{bcolors.ENDC}")
