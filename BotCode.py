#----------------------------------------------------------------------------------------
#		Rineroth's GroupMe Bot
#		Bot Functions:
#			*Rate images that come from links that end in .jpg
#			*Fix Reddit links. (Links must be the last thing written in the message)
#			*ReactionGif Replacement
#			*Bot agrees with you when asked "Right Bot?" 
#			*Bot analyzes the message when it is mentioned in a message and then replies
#-----------------------------------------------------------------------------------------


from flask import Flask, request
import requests
import json
import random
import MySQLdb
import re



app = Flask(__name__)

#Make sure to get your Bot key and name from the Group Me development page
bot_id = '<Bot ID Goes Here>'
bot_name = '<Bot Name Goes Here>'


@app.route('/', methods=['POST'])
def rob_callback():
		#Database connection is established
		conn = MySQLdb.connect(host= "127.0.0.1",user="<MySQL Username>",passwd="<MySQL Password>",db="<Database Name>",charset='utf8')
		messageData = json.loads(request.data)
		#This statement helps avoid infinite loops
		if messageData['name'] != bot_name:
			#Here is where the images get rated with a random number
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
			#Reaction Gif replacement block
			if ".gif" in messageData['text'].lower() and "/" not in messageData['text'].lower():
				x = conn.cursor()
				messageS = messageData['text'].lower()
				checkList = messageS.split()
				if len(checkList) == 1:
					try:
						x.execute("""SELECT imgurLink FROM TheBIN WHERE callGif=%s""",(str(messageData['text'].lower()), ))
						gmeSendback=x.fetchone()[0]
					except:
						gmeSendback = "Sorry mate, no gif found in the bin, add it on http://rineroth.com/gifbin/ "
					gmePayload = {'text' : gmeSendback, 'bot_id' : bot_id}
					gmeResponse = requests.post('https://api.groupme.com/v3/bots/post', data=gmePayload)
			#Reddit link fixer
			if "r/" in messageData['text'].lower() and "www." not in messageData['text'].lower():
				wordList = re.split('\W+',messageData['text'].lower())
				gmeSendback = "Here is your link! www.reddit.com/r/"+wordList[-1]
				gmePayload = {'text' : gmeSendback, 'bot_id' : bot_id}
				gmeResponse = requests.post('https://api.groupme.com/v3/bots/post', data=gmePayload)

		#Bot analyzes messages directed towards him
		if bot_name.lower() in messageData['text'].lower():       
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
		#Bot agrees with you when asked
		if "right bot?" in messageData['text'].lower():       
			gmeSendback = "You are correct"
			gmePayload = {'text' : gmeSendback, 'bot_id' : bot_id}
			gmeResponse = requests.post('https://api.groupme.com/v3/bots/post', data=gmePayload)
		conn.close()	
		return 'All Good'

def main():
        print 'Starting'
#IMPORTANT: Bot runs on port 8081 of your server, make sure to set up GroupMe to ping this server port
if __name__ == "__main__":
        main()
        app.debug = True
        app.run('0.0.0.0', 8081)

