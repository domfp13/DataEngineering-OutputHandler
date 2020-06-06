# -*- coding: utf-8 -*-
# Luis Enrique Fuentes Plata

from os.path import basename, dirname
from source.FTP import send_to_ftp
from source.SMTP import send_email
from json import dumps, loads
import logging, base64

REGISTRY = {
    'UPS_ALLOCATION': send_email,
    'BMO_Disposition': send_to_ftp,
    'distribution': send_to_ftp
}

def function_handler(event, context)->None:
    """Trigger by a change to a Cloud Storage bucket

    Arguments:
        event {dict} -- Event Payload
        context {google.cloud.functions.Contex} -- Metada for the event
    """
    try:
        
        logging.info("Start")

        pubsub_message = loads(base64.b64decode(event['data']).decode('utf-8'))
        
        directory_name = basename(dirname(pubsub_message.get('name')))
        #directory_name = basename(dirname(event['name'])) # Local Testing
        
        if directory_name in REGISTRY.keys():
            
            logging.info(f"Processing {pubsub_message.get('name')}")
            
            REGISTRY[directory_name](pubsub_message.get('bucket'), pubsub_message.get('name'))
            #REGISTRY[directory_name](event['bucket'], event['name'])
            
            logging.info("End")
            
            return dumps({'success': True}), 200, {'ContentType': 'application/json'}
        else:
            raise NotImplementedError 
    
    except NotImplementedError:
        logging.exception('This file has no implementation method')
        return dumps({'success': False}), 501, {'ContentType': 'application/json'}
    except Exception as e:
        logging.exception(e)
        return dumps({'success': False}), 400, {'ContentType': 'application/json'}