import datetime


class DateFormat():

    @classmethod
    def convert_date_to_ddmmyy(self, date):
        '''@return 01/01/1999'''
        return datetime.datetime.strftime(date, '%d/%m/%Y')

    @classmethod
    def convert_time_to_HHMM(self, time):
        '''@return 12:00'''
        return time.strftime('%H:%M')

    @classmethod
    def convert_time_to_12h(self, time):
        '''@return 12:00 PM '''
        return time.strftime("%I:%M %p")