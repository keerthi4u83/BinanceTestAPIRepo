import hmac
from urllib.parse import urlencode
import hashlib

def csv_to_json_converter(key_list, value_list):
    '''
    key_list: Has the list of keys for json that will be constructed
    value_list: Has the list of values that needs to assigned to json keys
    csv_to_json_converter: Function that assigns the input values to the keys read from config for the given api 
    '''
    converted_json = {}
    for index, elem in enumerate(key_list):
        converted_json[elem] =  value_list[index]    
    return converted_json
    
    '''
    converted_json: Returns the converted json from csv
    '''
    
def url_constructor(symbol_value,interval_value,starttime_value,endtime_value,base_url):
    '''
    constructs url from the given query strings passed as arguments
    '''
    
    full_url = "{base_url}?symbol={symbol_value}&interval={interval_value}&startTime={starttime_value}&endTime={endtime_value}".format(base_url=base_url,symbol_value=symbol_value,interval_value=interval_value,starttime_value=starttime_value,endtime_value=endtime_value)
    return full_url
    
    '''full_url:constructed url'''
    
def hashing(query_string,secret):
    '''
    hashes the input query strings and secret key using hmac, hashlib
    '''
    
    return hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    
    '''
    returns the hashed secret and query strings
    '''