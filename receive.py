#!/usr/bin/env python
import pika
import time
import commands

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='sox_queue', durable=True)
print ' [*] Waiting for messages. To exit press CTRL+C'

def callback(ch, method, properties, body):
    #print " [x] Received %r" % (body,)
    print commands.getstatusoutput(body);
    ch.basic_ack(delivery_tag = method.delivery_tag)
    #print " [x] Done "
channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='task_queue')

channel.start_consuming()