from pymongo import MongoClient
from dotenv import dotenv_values
import motor.motor_asyncio

config = dotenv_values(".env")

client =  motor.motor_asyncio.AsyncIOMotorClient(config["ATLAS_URI"])

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.get_database(config["DB_NAME"])
# user_collection = db["users"]
user_collection = db.get_collection("users")