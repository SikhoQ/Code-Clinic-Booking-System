from rich.console import Console
from datetime import datetime, timedelta
from rich.table import Table
from rich.text import Text
import src.booking_system.calendars.calendar_utilities as calendar_utilities
import src.booking_system.calendars.calendar_api as calendar_api


def print_table():
    service = calendar_api.authorise_google_calendar()
    calendars = calendar_utilities.create_coding_clinic_calendar(service)
    calendar_data = calendar_utilities.read_calendar_data(calendars)
    events = calendar_data["cohort 2023"]["events"]

    console = Console()

    title_text = Text("CALENDAR: COHORT 2023", style="italic bold orange4 underline")

    # Create a table with row_styles and border_style parameters
    table = Table(title=title_text, row_styles=["dim"], border_style="bold grey23 on grey23")
    table.add_column("[dark_red]Index[/dark_red]", style="bold", justify="center")
    table.add_column("[green]Time[/green]", style="bold", justify="center")

    today = datetime.now().date()
    num_days = 7
    date_list = [today + timedelta(days=i) for i in range(num_days)]
    formatted_dates = [date.strftime('%Y-%m-%d') for date in date_list]

    for date_str in formatted_dates:
        # Convert the date string to a datetime object
        date_object = datetime.strptime(date_str, '%Y-%m-%d')

        # Get the name of the day
        day_name = date_object.strftime('%A')
        table.add_column(Text(day_name, style="steel_blue", justify="center"))

    start_working_time = datetime.strptime("07:30", "%H:%M")

    for i in range(20):
        start_time = start_working_time
        end_time = start_time + timedelta(minutes=30)
        formatted_time_range = f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
        start_working_time += timedelta(minutes=30)

        index_text = Text(str(i + 1), style="dark_red bold")
        time_text = Text(formatted_time_range, style="bold green")

        table.add_row(index_text, time_text)

    console.print(table)

    return events


if __name__ == "__main__":
    print_table()
