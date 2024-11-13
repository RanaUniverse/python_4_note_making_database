from my_modules.colorful_terminal_module import TColor


text = "This is a text"


abc = TColor.YELLOW + text + TColor.RESET
print(abc)
print(text.upper())

TColor.reset_colors_old()
abc = TColor.YELLOW + text + TColor.RESET
print(abc)
print(text.upper())