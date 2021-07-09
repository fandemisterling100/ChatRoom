import pika

QUERY = 'stock'

class _Producer:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost'))
        
        self.channel = self.connection.channel()
        
    def publish_query(self, message, username):
        # Post query on a queue named stock
        # with the format username:stock_code
        stock_code = message.split('=')[1]
        body = f"{username}:{stock_code}"
        self.channel.queue_declare(queue=QUERY)
        self.channel.basic_publish(
            exchange='',
            routing_key=QUERY,
            body=body)
        self.connection.close()
        
class Consumer:
    
    TIMEOUT = 10
    
    def __init__(self, interface, queue):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue)
        self.channel.basic_consume(self.callback,
                                   queue=queue,
                                   no_ack=True)
        self.connection.add_timeout(self.TIMEOUT, self.on_timeout)
        self.interface = interface
        self.accomplished = False
        self.channel.start_consuming()
        
    def on_timeout(self):
        self.channel.stop_consuming()
        
        if not self.accomplished:
            print("Timeout")
        else:
            print("finished")
    
    def callback(self, ch, method, properties, body):
        self.accomplished = True
        
        # Receive data from decoupled bot
        self.interface.on_worker_result(body.decode("utf-8"))