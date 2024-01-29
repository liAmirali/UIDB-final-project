import datetime

def get_datetime_input(prompt):
    while True:
        try:
            datetime_str = input(prompt + " (YYYY-MM-DD HH:MM:SS): ")
            datetime_obj = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            return datetime_obj
        except ValueError:
            print("Invalid datetime format. Please enter datetime in YYYY-MM-DD HH:MM:SS format.")
