#!/usr/bin/env python
import pika
import commands
import socket
import base64

connection = pika.BlockingConnection(pika.ConnectionParameters(
         host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')
def on_request(ch, method, props, body):
    #print body
    body = base64.b64decode(body)
    print body
    run = commands.getoutput(body)
    response = socket.gethostname()
    print response
    ch.basic_publish(exchange='',
                    routing_key=props.reply_to,
                    properties=pika.BasicProperties(correlation_id = \
                                                  props.correlation_id),
                    body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')
print " [x] Awaiting RPC requests"
channel.start_consuming()