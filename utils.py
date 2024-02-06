import datetime

def get_date_range(start_date):
    date_format = "%y-%m-%d"
    start_date_obj = datetime.datetime.strptime(start_date, date_format).date()
    end_date_obj = datetime.datetime.now().date()
    date_range = []

    current_date = start_date_obj
    while current_date <= end_date_obj:
        date_range.append(current_date.strftime(date_format))
        current_date += datetime.timedelta(days=1)

    return date_range