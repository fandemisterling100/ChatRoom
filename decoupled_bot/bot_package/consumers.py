import pika
from  .api import StooqAPI

QUEUE = 'stock'

# Connection to channel for answer redistribution
def redistribute(client, message):
    
    print("Trying to redistribute bot answer...")
    queue = f"BotStocks-{client}"
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(
        exchange='',
        routing_key=queue,
        body=message)
    connection.close()
    
class _BotConsumer:
    
    RETURNS ={"API_error": "I couln't retrieve the information.",
              "Success": "stock_code quote is $value per share",
              "user_error": "Please verify your stock command."}
    
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=QUEUE)
        self.channel.basic_consume(QUEUE,
                                   self.callback,
                                   auto_ack=False)
        self.client = ''
        self.start_consuming()
    
    def start_consuming(self):
        print("BotConsumer has started consuming...")
        self.channel.start_consuming()
        
    def callback(self, ch, method, properties, body):
        print("BotConsumer received a message from the queue...")
        self.client, stock_code = self._validate_message(body)
        
        if not self.client:
            return

        if stock_code:
            try:
                share_value = StooqAPI.get_stock_quote(stock_code)
            except:
                redistribute(self.client, self.RETURNS.get('API_error'))
            else:
                print("API answered!")
                # The request was completed successfully,
                # it sends share value to channel
                bot_answer = self.RETURNS.get("Success")
                bot_answer = bot_answer.replace("stock_code", stock_code)
                bot_answer = bot_answer.replace("value", str(share_value))
                redistribute(self.client, bot_answer)
        else:
            redistribute(self.client, self.RETURNS.get('user_error'))
    
    @staticmethod     
    def _validate_message(message):
        message = message.decode('utf-8')
        try:
            return message.split(':')
        except:
            return None, None
        
if __name__ == '__main__':
    print("Starting BotConsumer...")
    _BotConsumer()
                
        