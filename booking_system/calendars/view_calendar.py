import calendar
from datetime import *
import csv

def view_dates():
    today = datetime.now()
    slots = []
    print("Today's date:", today.strftime("%d-%m-%Y"), calendar.day_name[today.weekday()])
    print("> Available Slots:")
    for _ in range(6):
        
        today += timedelta(days=1)
        slots.append(today.strftime("%d-%m-%Y"))
        print(today.strftime("%d-%m-%Y"), calendar.day_name[today.weekday()])


    return slots


def write_2_csv():

    slots = view_dates()
    with open('dates.csv', 'w', newline='') as available_dates:
        
        csv_writer = csv.writer(available_dates)
        csv_writer.writerow(['Available Dates'])

    
        for date_str in slots:
            
            csv_writer.writerow([date_str])

def show_calendar():
    write_2_csv()
    


if __name__ == '__main__':
    show_calendar()