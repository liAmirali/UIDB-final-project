from views.utils import clear_screen, print_header, read_menu_opt
from src.app import app
def show_manager_screen():
  while True:
    clear_screen()
    print_header("Manager Page")
    
    print("1. Show customer list")
    print("2. Show rental detail of a film")
    print("3. Show active rentals")
    print("4. Show rental requests")
    print("5. show reserve requests")
    print("6. show shop info")
    print("7. Edit shop info")
    print("8. View all films")
    print("9. View all films by category")
    print("10. Search on films")
    print("11. Payment details")
    print("12. BestSeller films")

    option = read_menu_opt()
    if (option == "1"):
          pass
    elif (option == "2"):
      pass
    elif (option == "3"):
      pass
    elif (option == "4"):
      pass
    elif (option == "5"):
      pass
    elif (option == "6"):
      pass
    elif (option == "7"):
      pass
    elif (option == "8"):
      pass
    elif (option == "9"):
      pass
    elif (option == "10"):
      pass
    elif (option == "11"):
      pass
    elif (option == "12"):
      pass
    

