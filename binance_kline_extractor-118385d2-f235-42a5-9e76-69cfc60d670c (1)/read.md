This python package is designed to retrive data from binance api's- kline/candel grain and all_orders.
This python file is developed to run as AWS lambda function and able to produce events to kinesis firehose.
Reponse recieved from  apis are written to kinesis firehose using boto3 firehose client library.
Input request for the python function is in the below json format.

{
  "symbol": "BTCUSDT",
  "start_time": "1610904690381",
  "end_time": "1610991090381",
  "interval": "1m"
}

Secrets Manager should be used for storing api keys, This implementation is not done as part of this current development. But this would be an enhancement in the future
that can be added to the package.

api_caller_all_orders and api_caller functions are both used for calling apis for the mentioned url, these functions can be optimized or can be made more
functional by removing redundant logics. This can be done as part of further enhancments (when more api calls are made and identifying commanalities).
For now since hashing signature has to be implemented in orders api, i chose to have it as a separate function.

Retry logic can be implemented when there is a network issue, this can be identified by http response code. MAX of 3 retries can be made on the api calls made as part
of the retry. If there are failures after 3 retries, then the failed query strings can be persisted externally to lambda function say dynamodb
and batch retry can be performed over the failed list. This would be an enhancement to the current implementation.

api responses are mapped to corresponding firehose, These values are currently fetched from config file. These values can be externalized in environmental variables 
in lambda functions so that these routing changes does not need a code change. This can be part of the enhancement effort in the future.