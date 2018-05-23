from datetime import datetime


class Date:
    @staticmethod
    def convert_date_for_saving(date):
        if not len(date) > 0 or date == 'DD-MM-YYYY':
            return ''
        date = datetime.strptime(date, "%d-%m-%Y")
        return date.strftime('%Y-%m-%d')

    @staticmethod
    def convert_date_for_printing(date):
        if not len(date) > 0:
            return ''
        date = datetime.strptime(date, '%Y-%m-%d')
        return date.strftime('%d-%m-%Y')

    @staticmethod
    def convert_date_time_for_printing(date):
        if not len(date) > 0:
            return ''
        date = datetime.strptime(date, '%Y-%m-%d %H:%M')
        return date.strftime('%d/%m/%Y %H:%M')
