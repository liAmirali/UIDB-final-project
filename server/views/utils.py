import os
import platform

def clear_screen():
    # Get the operating system
    operating_system = platform.system()

    # Clear the screen based on the operating system
    if operating_system == 'Windows':
        os.system('cls')
    else:  # Linux, macOS, etc.
        os.system('clear')

def read_menu_opt():
    while True:
        option = input("\n > Please enter menu option: ")
        option = option.strip()
        if option == "":
            continue
        break
    return option


def wait_on_enter():
    input("\nPress Enter to continue...")

def print_header(text):
    header_text = f"""
    -----------------------------------------
    {text}
    -----------------------------------------
    """
    print(header_text)
    

def print_error(text):
    print("\033[91m{}\033[00m".format(text))

def print_success(text):
    print("\033[92m{}\033[00m".format(text))
