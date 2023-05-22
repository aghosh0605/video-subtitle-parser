import boto3
import datetime
from boto3.dynamodb.conditions import Key, Attr
from botocore.config import Config

# value = os.getenv('AWS_ACCESS_KEY_ID')
# print(value)

# Get the service resource.

class DynamoDBServices:
    __dynamodb = None
    table = None
    _instance = None
    
    __config = Config(
   retries = {
      'max_attempts': 10,
      'mode': 'standard'
   }
)

    def __new__(cls):
        if cls._instance is None:
            print('Creating the object')
            DynamoDBServices.__dynamodb = boto3.resource('dynamodb',config=DynamoDBServices.__config)
            DynamoDBServices.table = DynamoDBServices.__dynamodb.Table('ecowiser')
            print(f"Connected DynamoDB At: {datetime.datetime.now()}")
            cls._instance = super(DynamoDBServices, cls).__new__(cls)
        print(f"Table Created At: {DynamoDBServices.table.creation_date_time}")
        return cls._instance        

    def searchItem(self,query,table=None):
        if table is None:
            table='ecowiser'
        response = DynamoDBServices.table.scan(FilterExpression=Attr('subtitle').contains(query))

        return response

# Check singleton functionality

def checkSingleton():
    # The client code.

    s1 = DynamoDBServices()
    s2 = DynamoDBServices()
    print(s1._instance)
    print(s2._instance)

    if id(s1) == id(s2):
        print("Singleton works, both variables contain the same instance.")
    else:
        print("Singleton failed, variables contain different instances.")

# checkSingleton()