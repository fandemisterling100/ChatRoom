"""Class to receive information about the value
   of the shares from the API https://stooq.com/
   as csv, decode it and return the maximum value
   of the share by stock code
"""
import requests
import csv


class StooqAPI:

    @classmethod
    def get_stock_quote(cls, stock_code):
        print("Connecting to API...")
        # Get CSV data from API by stock code
        CSV_URL = ('https://stooq.com/q/l/?s=', '&f=sd2t2ohlcv&h&e=csv')
        url = f"{CSV_URL[0]}{stock_code.lower()}{CSV_URL[1]}"

        with requests.Session() as s:
            download = s.get(url)

        return cls._parse_csv(download)

    @staticmethod
    def _parse_csv(data, separator=','):
        """Parse CSV retrieved from API
           and get maximum value (fourth
           coulmn)
           
           Parameters:
                data (requests.models.Response): API response
                separator (str): Default ,
            Returns:
                (int): Share quote. Default 0 to 
                handle errors
        """
        try:
            decoded_content = data.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=separator)
            second_row = list(cr)[1]
            max_value = float(second_row[4])
        except:
            print("Couldn't parse")
            return 0
        else:
            print("Parsing finished...")
            return max_value
