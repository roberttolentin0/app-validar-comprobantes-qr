import datetime
import pytz
import re

from datetime import datetime

peru_timezone = pytz.timezone('America/Lima')

class DateFormat():

    @classmethod
    def get_curr_time_peru(self):
        return datetime.now(peru_timezone)

    @classmethod
    def convert_date_to_ddmmyy(self, date):
        '''@return dd/mm/yyyy'''
        return datetime.strftime(date, '%d/%m/%Y')

    @classmethod
    def convert_time_to_HHMM(self, time):
        '''@return 12:00'''
        return time.strftime('%H:%M')

    @classmethod
    def convert_time_to_12h(self, time):
        '''@return 12:00 PM '''
        return time.strftime("%I:%M %p")

    @classmethod
    def parse_date_to_ddmmyy(self, date_str):
        '''
            @params date_str: 'yyyy-mm-dd' | 'dd-mm-yyyy | dd/mm/yyyy'
            @return dd/mm/yyyy
        '''
        # Intentar analizar la fecha en formato 'yyyy-mm-dd'
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            return date_obj.strftime('%d/%m/%Y')
        except ValueError:
            pass

        # Intentar analizar la fecha en formato 'dd-mm-yyyy'
        try:
            date_obj = datetime.strptime(date_str, '%d-%m-%Y')
            return date_obj.strftime('%d/%m/%Y')
        except ValueError:
            pass

        # Intentar analizar la fecha en formato 'dd-mm-yyyy'
        try:
            date_obj = datetime.strptime(date_str, '%d/%m/%Y')
            return date_obj.strftime('%d/%m/%Y')
        except ValueError:
            pass

        # Si ninguna conversión es válida, devolver None
        return None

    @classmethod
    def find_and_format_date(self, data):
        '''
            Utilizar una expresión regular para encontrar fechas en los formatos 'dd-mm-yyyy' | 'yyyy-mm-dd'
        '''
        fecha = data.replace("'", "-")  # Para separaciones por '''
        match = re.search(r'\d{4}-\d{2}-\d{2}|\d{2}[-/]\d{2}[-/]\d{4}', fecha)
        print('match', match)
        if match:
            date_str = match.group(0)
            print('date_str', date_str)
            formatted_date = self.parse_date_to_ddmmyy(date_str)
            if formatted_date:
                return formatted_date
        return "No se encontró una fecha válida en el formato esperado."