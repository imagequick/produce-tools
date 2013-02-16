#!/usr/bin/env python
from __future__ import with_statement
import pika
import commands
import socket
import base64
import json
from contextlib import closing
from zipfile import ZipFile, ZIP_DEFLATED
import os, time



def zipdir(basedir, archivename):
    assert os.path.isdir(basedir)
    with closing(ZipFile(archivename, "w", ZIP_DEFLATED)) as z:
        for root, dirs, files in os.walk(basedir):
            #NOTE: ignore empty directories
            for fn in files:
                absfn = os.path.join(root, fn)
                zfn = absfn[len(basedir)+len(os.sep):] #XXX: relative path
                z.write(absfn, zfn)

connection = pika.BlockingConnection(pika.ConnectionParameters(
         host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='bulk_produce_queue')

def on_request(ch, method, props, body):
    #print body
    soxs = base64.b64decode(body)
    soxs = json.loads(soxs)
    #make new directory for the files
    foldername = str(time.time()).replace('.','')
    zippath = '/var/produced/'
    path = zippath + foldername
    os.makedirs(path)
    os.chdir(path)

    '''Run the SOX Code'''
    for sox in soxs:
        commands.getoutput(sox)

    os.chdir('../')
    zipdir(path,foldername+'.zip')    
    link = socket.gethostname() + '.image-quick.com/' + foldername +'.zip'

    
    response = link
    print response
    ch.basic_publish(exchange='',
                    routing_key=props.reply_to,
                    properties=pika.BasicProperties(correlation_id = \
                                                  props.correlation_id),
                    body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='bulk_produce_queue')
print " [x] Awaiting RPC requests"
channel.start_consuming()