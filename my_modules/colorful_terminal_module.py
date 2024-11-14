"""
This module help me to get colorful terminal
i will import this module's Tcolor part to use in my terminal print
part

Most interesting part is i make a setattribut fun: Tcolor.desable_color()
if i call this in my main.py this will not use any color setup anymore in terminal.

A simple use case of this is below:

from my_modules.colorful_terminal_module import TColor


text = "This is a text"


abc = TColor.YELLOW + text + TColor.RESET
print(abc)
print(text.upper())

TColor.reset_colors_old()
abc = TColor.YELLOW + text + TColor.RESET
print(abc)
print(text.upper())

"""


class TColor:
    """
    I just need to import this class and use the below str
    formats color as .COLOR_NAME
    and it will work goodly without any issue
    """

    RESET = "\033[0m"  # Reset to default color and style
    BOLD = "\033[1m"  # This will give me bold text  of the default color
    UNDERLINE = "\033[4m"  # Underlined text

    # Text colorss

    RED = "\033[31m"  # Red (often used for failures)
    GREEN = "\033[32m"  # Green
    YELLOW = "\033[33m"  # Yellow (often used for warnings)
    BLUE = "\033[34m"  # Blue like color
    MAGENTA = "\033[95m"  # Magenta (often used as header) like pink color

    OKCYAN = "\033[96m"  # This cyan has some problem with my color theme

    # Background Colors (uppercase names)
    ON_BLACK = "\033[40m"  # Black Background
    ON_RED = "\033[41m"  # Red Background
    ON_GREEN = "\033[42m"  # Green Background
    ON_YELLOW = "\033[43m"  # Yellow Background
    ON_BLUE = "\033[44m"  # Blue Background
    ON_PURPLE = "\033[45m"  # Purple Background

    CHECKING = OKCYAN  # This is for checing purpose only

    @classmethod
    def disable_color_old(cls):
        """
        Reset all the color codes to empty string so that i can call this in my main fun and
        all the formatting color will disable properly
        so i need to use below classmethod fucnion.
        """
        cls.RED = ""  # type: ignore
        cls.GREEN = ""  # type: ignore
        cls.YELLOW = ""  # type: ignore
        cls.BLUE = ""  # type: ignore
        cls.MAGENTA = ""  # type: ignore
        cls.OKCYAN = ""  # type: ignore
        cls.RESET = ""  # type: ignore
        cls.BOLD = ""  # type: ignore
        cls.UNDERLINE = ""  # type: ignore
        cls.ON_BLACK = ""  # type: ignore
        cls.ON_RED = ""  # type: ignore
        cls.ON_GREEN = ""  # type: ignore
        cls.ON_YELLOW = ""  # type: ignore
        cls.ON_BLUE = ""  # type: ignore
        cls.ON_PURPLE = ""  # type: ignore
        cls.CHECKING = ""  # type: ignore

    @classmethod
    def disable_color(cls):
        """
        Reset all the color codes to None, effectively disabling color formatting.
        This will use setattr to modify class attributes dynamically.
        """
        color_attributes = [
            "RED",
            "GREEN",
            "YELLOW",
            "BLUE",
            "MAGENTA",
            "OKCYAN",
            "RESET",
            "BOLD",
            "UNDERLINE",
            "ON_BLACK",
            "ON_RED",
            "ON_GREEN",
            "ON_YELLOW",
            "ON_BLUE",
            "ON_PURPLE",
            "CHECKING",
        ]

        for color in color_attributes:
            setattr(cls, color, "")  # change the value to "" empty str.


def checking_upper_format():

    print(f"{TColor.RED}This is a message in Red!{TColor.RESET}")
    print(f"{TColor.GREEN}This is a message in Green!{TColor.RESET}")
    print(f"{TColor.YELLOW}This is a message in Yellow!{TColor.RESET}")
    print(f"{TColor.BLUE}This is a message in Blue!{TColor.RESET}")
    print(f"{TColor.MAGENTA}This is a message in Magenta!{TColor.RESET}")
    print(f"{TColor.OKCYAN}This is a  Experimental not work On Cyan!{TColor.RESET}")
    print(f"{TColor.BOLD}This is a message in Bold!{TColor.RESET}")
    print(f"{TColor.UNDERLINE}This is a message in Underlined text!{TColor.RESET}")
    print(f"{TColor.ON_BLACK}This is a message with Black Background!{TColor.RESET}")
    print(f"{TColor.ON_RED}This is a message with Red Background!{TColor.RESET}")
    print(f"{TColor.ON_GREEN}This is a message with Green Background!{TColor.RESET}")
    print(f"{TColor.CHECKING}This is a message for checking purpose !{TColor.RESET}")


def main():
    checking_upper_format()


if __name__ == "__main__":
    TColor.disable_color()
    main()
