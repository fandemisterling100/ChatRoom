from django.test import TestCase
from decoupled_bot.bot_package.api import * 

class ApiTest(TestCase):
    # Get maximum share quote from API
    def test_get_stock_quote(self):
        print("Testing API connection...")
        stock_value = StooqAPI.get_stock_quote("aapl.us")
        print(f"Apple quote is ${stock_value} per share")
        self.assertEqual(isinstance(stock_value, float), True)
        self.assertEqual(stock_value > 0, True)
    
    
    
        
        