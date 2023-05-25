from datetime import datetime

current_date = datetime.now()
day_of_year = current_date.timetuple().tm_yday

print("Current day of the year:", day_of_year)
