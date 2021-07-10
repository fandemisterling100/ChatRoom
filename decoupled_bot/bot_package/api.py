import requests
import json
import grequests

class StooqAPI:

    @classmethod
    def get_stock_quote(cls, stock_code):
        print("Connecting to API...")
        # Get CSV data from API by stock code
        CSV_URL = ('https://stooq.com/q/l/?s=', '&f=sd2t2ohlcv&h&e=csv​')
        url = f"{CSV_URL[0]}{stock_code}{CSV_URL[1]}"  
        #response = requests.get(url)
        response = grequests.get(url)

        data =  cls._parse_csv(response)
        return cls._calculate_quote(data)
        
    @staticmethod
    def _parse_csv(csv, separator=','):
        print("Parsing Data...")
        # Parse CSV retrieved from API
        print(csv)
        print(type(csv))
        try:
            print(csv.json())
        except:
            print("Couln't parse")
        else:
            print("Parsing finished...")
        return 0
    
    @staticmethod
    def _calculate_quote(data):
        print("Calculating value...")
        # get the highest value from the returned data
        return 10
    
        
    