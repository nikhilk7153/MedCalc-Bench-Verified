from datetime import datetime, timedelta

def add_2_weeks(menstrual_date):
    input_date_str = menstrual_date
    input_date = datetime.strptime(input_date_str, '%m/%d/%Y')
    future_date = input_date + timedelta(weeks=2)
    return future_date.strftime('%m/%d/%Y')
