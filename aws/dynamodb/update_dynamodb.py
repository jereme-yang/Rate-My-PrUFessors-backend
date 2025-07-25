import boto3
import json

# Load your JSON file
with open("data.json", "r") as f:
    data = json.load(f)

# Connect to DynamoDB
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("MyTable")

# Insert each item
for name, digits in data.items():
    item = {
        "name": name,
        "d1": digits[0],
        "d2": digits[1],
        "d3": digits[2],
        "d4": digits[3],
        "d5": digits[4],
        "d6": digits[5],
    }

    table.put_item(Item=item)
    print(f"Inserted {name}")() 