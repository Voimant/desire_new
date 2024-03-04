import datetime


def get_log_errors(rep):
    with open('report_errors.txt', 'a') as file:
        file.write(f'\n{rep} --------{datetime.date.today()}')