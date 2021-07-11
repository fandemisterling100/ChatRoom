"""RabbitMQ consumer and producer layer for the chat
application. The producer class posts users share
quotes queries in a queue named 'stock' with the format:
username:stock_code

The consuming class receives the responses from the
decoupled bot to the queries of the previous queue.
"""


import pika

QUERY = 'stock'


class _Producer:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost'))

        self.channel = self.connection.channel()

    def publish_query(self, message, username):
        try:
            print("Publishing stock command...")
            stock_code = message.split('=')[1]
            body = f"{username}:{stock_code}"
            self.channel.queue_declare(queue=QUERY)
            self.channel.basic_publish(
                exchange='',
                routing_key=QUERY,
                body=body)
            self.connection.close()
        except:
            print("Wrong query format")


class Consumer:
    def __init__(self, interface, queue):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue)
        self.channel.basic_consume(queue,
                                   self.callback,
                                   auto_ack=True)
        self.interface = interface
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        print("The APP received bot answer!")
        # Send answer from bot to chat
        self.interface.send_stock_quote(body.decode("utf-8"))
