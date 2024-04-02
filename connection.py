from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

# uri = "mongodb+srv://<username>:<password>@cluster0.ia5uqdw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
uri = "mongodb+srv://"+(os.environ.get('MONGODB_USERNAME'))+":"+(os.environ.get('MONGODB_PASSWORD'))+"@cluster0.ia5uqdw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)