import json
import base64
import boto3
from botocore.vendored import requests
from utils import url_constructor,csv_to_json_converter, hashing
from config import *
import logging
from constants import HttpErrorCodes

firehose_client = boto3.client('firehose',region_name = 'us-east-2')

def lambda_handler_kline(event, context):
    '''
    lambda_handler code designed to invoke kline/candle_grain api
    Converts the comma separated data to json format using utils function
    Writes the response to Fireshose in json format
    '''
    try:
        trade_pair, interval, start_time, end_time = event['symbol'], event['interval'], event['start_time'], event['end_time']
        # print("trade_pair:",trade_pair)
        # api_url = url_constructor("BTCUSDT","1m","1610904690381","1610991090381",base_url)
        api_url = url_constructor(trade_pair,interval,start_time,end_time,base_url)
        resp = api_caller(api_url,api_key)
        extracted_response = resp.json()
        # print("extracted_response:",extracted_response)
        if(resp.status_code==HttpErrorCodes.success.value): 
            if len(extracted_response) > 0:
                data_extracted_response = list(map(lambda rec:{"Data":"{}\n".format(csv_to_json_converter(kline_candlestick_key_list,rec))},extracted_response))
                full_lambda_response = firehose_client.put_record_batch(
                    DeliveryStreamName= kline_delivery_stream,
                    Records=data_extracted_response
                    )
                lambda_response = full_lambda_response["ResponseMetadata"]
        else:
            lambda_response = { "binance_api": "kline_candlestick",
                                "http_error_code":resp.status_code,
                                "response_error_message":extracted_response
                              }
        return lambda_response
        
    except Exception as e:
        logging.debug("Exception while parsing/handling kline api response:",e)
    '''
    returns the successful/errored response from lambda function in json format
    '''

def api_caller(api_url,api_key):    
    '''
    api_url: api url for posting the request
    api_key: api key fetched from config file in turn will be read from secrets manager
    '''
    try:
        r=requests.get(api_url, headers={"X-MBX-APIKEY":api_key})
        return r
    except Exception as e:
        logging.debug("Error while retrieving response from binance kline api:",e)

    '''
    returns the response from api call in list of lists format.
    '''
    
def lambda_handler_all_orders(event, context):
    '''
    lambda_handler code designed to invoke order api
    Writes the response to Fireshose in json format
    '''
    try:
        trade_pair = event['symbol']
        # print("trade_pair:",trade_pair)
        resp = api_caller_all_orders(all_orders_base_url,trade_pair)
        extracted_response = resp.json()
        # print("extracted_response:",extracted_response)
        if(resp.status_code==HttpErrorCodes.success.value): 
            if len(extracted_response) > 0:
                data_extracted_response = list(map(lambda rec:{"Data":"{}\n".format(rec)},extracted_response))
                full_lambda_response = firehose_client.put_record_batch(
                    DeliveryStreamName= orders_delivery_stream,
                    Records= data_extracted_response
                    )
                lambda_response = full_lambda_response["ResponseMetadata"]
        else:
            lambda_response = { "binance_api": "all_orders",
                                "http_error_code":r.status_code,
                                "response_error_message":extracted_response}
        return lambda_response
    except Exception as e:
        logging.debug("Exception while parsing/handling binance all_orders api response:",e)
    '''
    returns the successful/errored response from lambda function in json format
    '''
    
def api_caller_all_orders(base_url,trade_pair):
    '''
    base_url:base url on which query strings and hashing signatures  are appended 
    trade_pair: input trade_pair symbol 
    api_caller_all_orders: function that constructs url, signatures (using utils functions) and inokes api
    '''
    
    try:
        servertimeint = requests.get("https://api.binance.us/api/v1/time")
        timestamp = servertimeint.json()['serverTime']
        # query_string = 'timestamp={}&symbol={}'.format(timestamp,"BTCUSDT")
        query_string = 'timestamp={}&symbol={}'.format(timestamp,trade_pair)
        url = base_url + '?' + query_string + '&signature=' + hashing(query_string, secret)
        r=requests.get(url, headers={"X-MBX-APIKEY":api_key})
        return r
    except Exception as e:
        logging.debug("Error while retrieving response from binance all_orders api:",e)

    '''returns the response from api call in List of jsons format'''