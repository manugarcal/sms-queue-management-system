from flask import jsonify
from twilio.rest import Client
import os

class Queue:
#create a class queue and define all atributes
    def __init__(self):
        self.account_sid = os.environ['TWILIO_ACCOUNT_SID'] #and instance of account sid, auth token and client saved in .env fro privacy
        self.auth_token = os.environ['TWILIO_AUTH_TOKEN']
        self.client = Client(self.account_sid, self.auth_token)
        self._queue = []
        self._mode = 'FIFO'
        
    
    def enqueue(self, item):
        self._queue.append(item)

        message = self.client.messages \
        .create(
         body='Hello, '+ str(item['name'])+ ' you have ' + str(self.size()) + ' people ahead',
         from_='+13516668915',
         to='+56988859660'
        )

        return message.sid

    def dequeue(self):
        if self.size() > 0:
            if self._mode ==  'FIFO':
                queue = self._queue.pop(0)
                message = self.client.messages \
                .create(
                body='Dear, ' + str(self._queue[0]['name']) + ' your turn has come',
                from_='+13516668915',
                to='+56988859660'
                )
                return message.sid
        else:
            return "empty list"
 
    def get_queue(self):
        return self._queue
    def size(self):
        return len(self._queue) 

