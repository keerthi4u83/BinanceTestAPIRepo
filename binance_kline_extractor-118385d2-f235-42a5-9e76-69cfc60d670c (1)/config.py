kline_candlestick_key_list = ["open_time" ,"open" ,"high" ,"low" ,"close" ,"volume" ,"close_time" ,"quote_asset_volume" ,"number_of_trades" ,"taker_buy_base_asset_volume" ,"taker_buy_quote_asset_volume" ,"ignore" ]
base_url = "https://api.binance.com/api/v3/klines"
api_key = "xxxxx" # fetch_api_key_from_secrets_manager()
secret = 'xxxxx' # fetch_secret_key_from_secrets_manager
all_orders_base_url = "https://api.binance.us/api/v3/allOrders"
orders_delivery_stream = "orders_delivery_stream"
kline_delivery_stream = "kline_delivery_stream"

def fetch_api_key_from_secrets_manager():
    pass
    #  api key will be stored in the AWS secret manager
    # This method will have the implementation for fetching the api key from secret manager

def fetch_secret_key_from_secrets_manager():
    pass
    #  api key will be stored in the AWS secret manager
    # This method will have the implementation for fetching the secret key from secret manager