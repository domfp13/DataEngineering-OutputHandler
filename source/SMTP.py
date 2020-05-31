# -*- coding: utf-8 -*-
# Created by Luis Fuentes

import logging
import base64
from os.path import basename
from sendgrid import SendGridAPIClient, Personalization
from sendgrid.helpers.mail import (
    Mail, Email, Attachment, FileContent, FileName,
    FileType, Disposition, ContentId
    )
from python_http_client.exceptions import HTTPError
from source.GeneralFunction import getSendgridAPIKey, getDistributionList, download_blob, getPath

def send_email(bucket_name:str, source_blob_name:str)->None:
    """Sends an Excel file attache to SMTP 

    Arguments:
        bucket_name {str} -- app-script-data-extraction
        source_blob_name {str} -- global/UPSAllocation/CMCC_Weekly_Carrier_Report_20190906.xlsx
    """
    logging.info('SMTP')

    SENDGRID_API_KEY = getSendgridAPIKey()

    report_name = basename(source_blob_name)
    
    subject = "Metrix Batch Report {report_name}".format(report_name=report_name)
    html_content='''
    <html>
    <body>
        <strong>Metrix Batch Repor Report Name: {report_name}</strong>
        <table>
            <tr>
                <td> 
                    <p style="margin-left:2.5em">This notification is regarding {report_name} that is being sent to you</p>
                    <p style="margin-left:2.5em">The report: {report_name} is attached.</p>
                    <p style="margin-left:2.5em"></p>
                </td>
            </tr>
        </table>
        Regards
    </body>
    </html>
    '''.format(report_name=report_name)

    message = Mail(
    from_email='luis.fuentes@compucom.com',
    subject=subject,
    html_content=html_content)

    TOLIST = getDistributionList()

    to_list = Personalization()

    for email in TOLIST.split(";"):
        to_list.add_to (Email(email.strip())) 

    message.add_personalization(to_list)

    download_blob(bucket_name, source_blob_name, getPath(basename(source_blob_name)))
    destination = getPath(basename(source_blob_name))

    with open(destination, 'rb') as f:
        data = f.read()
    
    encoded = base64.b64encode(data).decode()

    attachment = Attachment()
    attachment.file_content = FileContent(encoded)
    attachment.file_type = FileType('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    attachment.file_name = FileName(report_name)
    attachment.disposition = Disposition('attachment')
    message.attachment = attachment

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
        logging.info('Email has been sent')
    except Exception as e:
        logging.warning(e)