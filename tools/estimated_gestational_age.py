from datetime import datetime

def compute_gestational_age(current_date, menstrual_date):
    date2 = current_date
    date1 = menstrual_date
    datetime1 = datetime.strptime(date1, '%m/%d/%Y')
    datetime2 = datetime.strptime(date2, '%m/%d/%Y')
    delta = abs(datetime2 - datetime1)
    weeks = delta.days // 7
    days = delta.days % 7
    return (f'{weeks} weeks', f'{days} days')
