# -*- coding: utf-8 -*-
# Luis Enrique Fuentes Plata

from main import function_handler

# When debugging locally
if __name__=="__main__":
    function_handler({'name' : 'appusma206_apps/UPS_ALLOCATION/CMCC_Weekly_Carrier_Report_2020_05_19.xlsx',
             'bucket' : 'appusma206_apps_output'}, 'context')