from flask import Flask, request
import requests
import json
import random
import MySQLdb
import re
import praw
import os
import soundcloud

#variable initialization
app = Flask(__name__)
bot_id = '<YOUR BOT ID HERE>'
bot_name = 'Robertobot'
prevUser = ""
count = 0
r = praw.Reddit('RobBot_UserAgent')

@app.route('/', methods=['POST'])
def rob_callback():
		global prevUser
		global count
		conn = MySQLdb.connect(host= "127.0.0.1",user="<USER>",passwd="<PASSWORD>",db="<DATABASE NAME>",charset='utf8')
		messageData = json.loads(request.data)
		print (messageData['user_id'], messageData['name'])

		if messageData['user_id'] == "<USER ID>":
			theUser = "<NAME>"
		elif messageData['user_id'] == "<ANOTHER USER>":
			theUser = "<NAME>"
		else:
			theUser = prevUser
		if theUser == prevUser:
			count += 1
		else :
			count = 0

		if messageData['name'] != bot_name:
			if ".jpg" in messageData['text'].lower() or len(messageData['attachments'])>0:
				rating = random.randrange(1,10+1)
				if rating > 7:
					gmeSendback = ""
					gmeSendback = str(rating)+"/10 wouldBang.exe, nice pic %s" % (theUser,)
				if rating <= 7:
					gmeSendback = ""
					gmeSendback = str(rating)+"/10 wouldn'tBang.exe(ERROR), bad post %s" % (theUser,)
			elif count == 5:
				gmeSendback = "Please stop talking with yourself %s" % (theUser,)				
			elif ".gif" in messageData['text'].lower() and "/" not in messageData['text'].lower():
				x = conn.cursor()
				messageS = messageData['text'].lower()
				checkList = messageS.split()
				if len(checkList) == 1:
					try:
						x.execute("""SELECT imgurLink FROM TheBIN WHERE callGif=%s""",(str(messageData['text'].lower()), ))
						gmeSendback=x.fetchone()[0]
					except:
						gmeSendback = "Sorry %s, no gif found in the bin" % (theUser,)
			elif "r/" in messageData['text'].lower() and "www." not in messageData['text'].lower() and ".com" not in messageData['text'].lower():
				m= re.search('(?<=r/)\w+',messageData['text'].lower())
				gmeSendback = "Here is your link %s! http://www.reddit.com/r/" % (theUser,)+m.group(0)
			elif "you just got burned." in messageData['text'].lower():
				gmeSendback = "Get help with your burn! http://en.wikipedia.org/wiki/List_of_burn_centers_in_the_United_States"
			elif "link?" in messageData['text'].lower():
				gmeSendback = "Here's Link, The Hero of Time: http://imgur.com/NNmOyg3.jpg"
			elif bot_name.lower() in messageData['text'].lower():       
				messageSentiment = requests.post('http://text-processing.com/api/sentiment/', ('text=' + str(messageData['text'])))
				sLabel = messageSentiment.json()['label']
				gmeSendback = ""
				if sLabel == 'pos':
					gmeSendback = "Your response was very nice %s ! Keep it up!" % (theUser,)
				elif sLabel == 'neutral':
					gmeSendback = "Your response was meh %s ! Try harder!" % (theUser,)
				else:
					gmeSendback = "U wot %s? il rek u cheeky cunt" % (theUser,)

				
			elif "right bot?" in messageData['text'].lower():       
				gmeSendback = "You are correct %s" %(theUser,)

			elif "bot, say:" in messageData['text']:
				text=messageData['text']
				editText=text[text.rfind(':')+2:]
				editText=re.sub(r'[^\w]', ' ', editText)
				textoo = editText
				os.system("espeak \" %s \"  -w \"%s.wav\" -s 140"%(editText,textoo))
				 # create client object with app credentials
				client = soundcloud.Client(client_id='<SOUNDCLOUD ID>',client_secret='<SOUNDCLOUD PASS>',username='<SOUNDCLOUD USERNAME>',password='<SOUNDCLOUD PASS>')
				# upload audio file
				track = client.post('/tracks', track={'title': '%s'%(editText,),'asset_data': open('%s.wav'%(editText,), 'rb')})
				# print track link
				gmeSendback = track.permalink_url

			elif "reddit.com" in messageData['text'].lower()and"comments"in messageData['text'].lower():
				submission = r.get_submission(messageData['text']).comments[0]
				if len(submission.body) > 430:
					gmeSendback = "TL;TR (Too lazy to read that long ass comment)"
				else:
					gmeSendback = submission.body
			elif "are you alive bot?" in messageData['text'].lower():
				gmeSendback = "yes master, I am fully functional"
			else:
				gmeSendback = ""

			gmePayload = {'text' : gmeSendback, 'bot_id' : bot_id}
			gmeRespond = requests.post('https://api.groupme.com/v3/bots/post', data=gmePayload)
		conn.close()
		prevUser = theUser	
		return 'All Good'

def main():
        print 'Starting'

if __name__ == "__main__":
        main()
        app.debug = True
        app.run('0.0.0.0', 8081)

 
