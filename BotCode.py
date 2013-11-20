from flask import Flask, request
import requests
import json
import random

app = Flask(__name__)
bot_id = 'YourBotID'
bot_name = 'YourBotName'


@app.route('/rob_callback', methods=['POST'])
def bot_callback():
        messageData = json.loads(request.data)
        if messageData['name'] != bot_name:
                if ".jpg" in messageData['text'].lower():
			rating = random.randrange(1,10+1)
			if rating > 7:
                        	gmeSendback = ""
                        	gmeSendback = str(rating)+"/10 would bang.exe"
			if rating <= 7:
				gmeSendback = ""
				gmeSendback = str(rating)+"/10 would not bang.exe(FATAL ERROR)"
			gmePayload = {'text' : gmeSendback, 'bot_id' : bot_id}
			gmeResponse = requests.post('https://api.groupme.com/v3/bots/post', data=gmePayload)
                
			if bot_name in messageData['text']:       
				messageSentiment = requests.post('http://text-processing.com/api/sentiment/', ('text=' + str(messageData['text'])))
				sLabel = messageSentiment.json()['label']
				gmeSendback = ""

				if sLabel == 'pos':
					gmeSendback = "Your response was very nice! Keep it up!"
				elif sLabel == 'neutral':
					gmeSendback = "Your response was meh! Try harder!"
				else:
					gmeSendback = "You dick! Try harder to be nice or my creator will slap you!"

				gmePayload = {'text' : gmeSendback, 'bot_id' : bot_id}
				gmeResponse = requests.post('https://api.groupme.com/v3/bots/post', data=gmePayload)
        return 'All Good'

def main():
        print 'Starting'

if __name__ == "__main__":
        main()
        app.debug = True
        app.run('0.0.0.0', 80)

