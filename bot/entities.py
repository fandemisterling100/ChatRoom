import pika

QUERY = 'stock'

class _Producer:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost'))
        
        self.channel = self.connection.channel()
        
    def create_queue(self, message, username):
        
        stock_code = message.split('=')[1]
        body = f"{username}: {stock_code}"
        self.channel.queue_declare(queue=QUERY)
        self.channel.basic_publish(
            exchange='',
            routing_key=QUERY,
            body=body)
        self.connection.close()
        
class Consumer:
    pass