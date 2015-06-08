import datetime
def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%d-%b-%Y')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")
