from googleapiclient.discovery import build
import os

api_key = os.environ.get('YouTube_API')
service = build('youtube', 'v3', developerKey=api_key)
request = service.channels().list(
    part='statistics', id='UC0VkiYFJ-_ZAGdu8YmqR3pg')

response = request.execute()
print(response)
