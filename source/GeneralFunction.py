# -*- coding: utf-8 -*-
# Luis Enrique Fuentes Plata

#Importing global lib
from pathlib import Path
from os import environ

def decoratorGetPath(function):
    def wrapper(file_name:str):
        return Path('/tmp', file_name)
    return wrapper
@decoratorGetPath
def getPath(file_name:str):
    """Getting the local Path, deactivate decorator for local testing

    Arguments:
        file_name {str} -- my_file.csv

    Returns:
        Path
    """
    from os import getcwd
    return Path(getcwd(), file_name)

def decoratorGetHostName(function):
    def wrapper():
        return environ['HOSTNAME']
    return wrapper
@decoratorGetHostName
def getHostName()->str:
    """Returns a string for the FTP Hostname, deactivate decorator for local testing

    Returns:
        str -- HOSTNAME
    """
    return ''

def decoratorGetUserName(function):
    def wrapper():
        return environ['USERNAME']
    return wrapper
@decoratorGetUserName
def getUserName()->str:
    """Returns a string for the FTP UserName, deactivate decorator for local testing

    Returns:
        str -- USERNAME
    """
    return ''

def decoratorGetPassword(function):
    def wrapper():
        return environ['PASSWORD']
    return wrapper
@decoratorGetPassword
def getPassword()->str:
    """Returns a string for the FTP Password, deactivate decorator for local testing

    Returns:
        str -- PASSWORD
    """
    return ''

def decoratorGetDistributionList(function):
    def wrapper():
        return environ.get('TOLIST')
    return wrapper
@decoratorGetDistributionList
def getDistributionList()->str:
    """Returns a string for the SMTP distribution list separated by ;

    Returns:
        str -- [@mail;@mail;etc]
    """
    return ''

def decoratorGetSendgridAPIKey(function):
    def wrapper():
        return environ.get('SENDGRID_API_KEY')
    return wrapper
@decoratorGetSendgridAPIKey
def getSendgridAPIKey()->str:
    """Return a string for the Sengrid API KEY

    Returns:
        str -- [API KEY]
    """
    return ''

def download_blob(bucket_name:str, source_blob_name:str, destination_file_name:str)->None:
    """This function downloads a cloud object locally

    Arguments:
        bucket_name {str} -- "your-bucket-name"
        source_blob_name {str} -- "storage-object-name"
        destination_file_name {str} -- "local/path/to/file"
    """
    from google.cloud import storage

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)