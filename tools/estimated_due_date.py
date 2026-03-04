from datetime import datetime, timedelta

def add_40_weeks(menstrual_date, cycle_length):
    input_date_str = menstrual_date
    cycle_length = cycle_length
    input_date = datetime.strptime(input_date_str, '%m/%d/%Y')
    future_date = input_date + timedelta(weeks=40)
    if cycle_length == 28:
        pass
    elif cycle_length < 28:
        cycle_length_gap = cycle_length - 28
        future_date = future_date + timedelta(days=cycle_length_gap)
    elif cycle_length > 28:
        cycle_length_gap = cycle_length - 28
        future_date = future_date + timedelta(days=cycle_length_gap)
    return future_date.strftime('%m/%d/%Y')
