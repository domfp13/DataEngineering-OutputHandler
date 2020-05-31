# -*- coding: utf-8 -*-
# Luis Enrique Fuentes Plata

#Importing global lib
import logging
from os.path import basename, dirname
from source.GeneralFunction import getPath, getHostName, getUserName, getPassword, download_blob

def send_to_ftp(bucket_name:str, source_blob_name:str)->None:
    """Transfers a file to an FTP Server

    Arguments:
        bucket_name {str} -- app-script-data-extraction
        source_blob_name {str} -- global/UPSAllocation/CMCC_Weekly_Carrier_Report_20190906.xlsx
    """
    import paramiko
    try:
        
        bucket_name = bucket_name
        source_blob_name = source_blob_name
        file_name = basename(source_blob_name)
        file_path = dirname(source_blob_name)
        destination_file_name = getPath(file_name)

        logging.info(f'Downloading file {file_name}')
        download_blob(bucket_name, source_blob_name, destination_file_name)

        # Getting enviromental variables
        logging.info('Loading enviromental variables')
        HOSTNAME = getHostName()
        USERNAME = getUserName()
        PASSWORD = getPassword()

        # Starting Paramikio client
        logging.info('Starting Paramikio client')
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=HOSTNAME, username=USERNAME, password=PASSWORD)

        # Transfering object to FTP
        logging.info('Transfering object to FTP')
        with ssh_client.open_sftp() as ftp:
            # ftp.put(path, file_name)
            ftp.put(destination_file_name, bytes(f'/Inbound/{file_path}/{file_name}', 'utf-8')) # This needs to be change
            ftp.close()

    except Exception:
        logging.warning('The system cannot find the path specified in the FTP server')
    finally:
        ssh_client.close()
