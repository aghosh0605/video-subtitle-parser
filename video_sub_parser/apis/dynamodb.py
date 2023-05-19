import os
import boto3
import datetime

# value = os.getenv('AWS_ACCESS_KEY_ID')
# print(value)

# Get the service resource.


class DynamoServices:
    __dynamodb = None
    __table = None
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print('Creating the object')
            DynamoServices.__dynamodb = boto3.resource('dynamodb')
            DynamoServices.__table = DynamoServices.__dynamodb.Table('ecowiser')
            print(f"Connected DynamoDB At: {datetime.datetime.now()}")
            cls._instance = super(DynamoServices, cls).__new__(cls)
        print(f"Table Created At: {DynamoServices.__table.creation_date_time}")
        return cls._instance

    def createItem(self,data):
        # For Single item
        # DynamoServices.__table.put_item(Item= data)
        
        #For multiple items use below
        with DynamoServices.__table.batch_writer() as batch:
            for item in data:
                response = batch.put_item(Item=item)
        print("Uploaded all items to DynamoDB")



# Check singleton functionality

def checkSingleton():
    # The client code.

    s1 = DynamoServices()
    s2 = DynamoServices()
    print(s1._instance)
    print(s2._instance)

    if id(s1) == id(s2):
        print("Singleton works, both variables contain the same instance.")
    else:
        print("Singleton failed, variables contain different instances.")

# checkSingleton()