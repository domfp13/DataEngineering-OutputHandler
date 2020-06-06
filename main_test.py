# -*- coding: utf-8 -*-
# Luis Enrique Fuentes Plata

from main import function_handler

# When debugging locally
if __name__=="__main__":
    function_handler({'name': 'distribution/DBI_LOAD_0001_TECHDATA_CAD_2020-06-01.csv',
             'bucket': 'app-script-data-extraction-output'}, 'context')