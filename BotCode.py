#----------------------------------------------------------------------------------------
#		Rineroth's GroupMe Bot
#		Bot Functions:
#			*Rate images that come from links that end in .jpg
#			*Fix Reddit links. (Links must be the last thing written in the message)
#			*ReactionGif Replacement
#			*Bot agrees with you when asked "Right Bot?" 
#			*Bot analyzes the message when it is mentioned in a message and then replies
#			*Bot will read the first comment of a reddit thread when linked
#			*Bot will adress each chat member properly by their name
#			*Bot will react to specific calls such as "link?" and "you just got burned"
#-----------------------------------------------------------------------------------------
from flask import Flask, request
import requests
import json
import random
import MySQLdb
import re
import praw

#variable initialization
app = Flask(__name__)
bot_id = 'YOUR_BOT_ID_HERE'
bot_name = 'YOUR_BOT_NAME'
prevUser = ""
count = 0
r = praw.Reddit('REDDIT_USER_AGENT')

@app.route('/', methods=['POST'])
def rob_callback():
		global prevUser
		global count
		conn = MySQLdb.connect(host= "127.0.0.1",user="DB_USERNAME",passwd="db_PASSWORD",db="DB_NAME",charset='utf8')
		messageData = json.loads(request.data)
		print (messageData['user_id'], messageData['name'])
		if messageData['user_id'] == "USER ID NUMBER":
			theUser = "USERNAME"
		if messageData['user_id'] == "USER ID NUMBER":
			theUser = "USERNAME"
		if messageData['user_id'] == "USER ID NUMBER":
			theUser = "USERNAME"
		if messageData['user_id'] == "USER ID NUMBER":
			theUser = "USERNAME"
		#Keep adding statements for username. The reason why usernames are not dinamic is because the users in my chat change their names constantly


		else:
			theUser = prevUser
		if theUser == prevUser:
			count += 1
		else :
			count = 0
		#This statement stops the bot from replying to himself
		if messageData['name'] != bot_name:
			#statement to check for jpg links
			if ".jpg" in messageData['text'].lower():
				rating = random.randrange(1,10+1)
				if rating > 7:
					gmeSendback = ""
					gmeSendback = str(rating)+"/10 wouldBang.exe, nice pic %s" % (theUser,)
				if rating <= 7:
					gmeSendback = ""
					gmeSendback = str(rating)+"/10 wouldn'tBang.exe(ERROR), bad post %s" % (theUser,)
			#if a user talks too much, the bot will complain
			elif count == 5:
				gmeSendback = "Please stop talking with yourself %s" % (theUser,)	
			#statement to check for gifs in the database			
			elif ".gif" in messageData['text'].lower() and "/" not in messageData['text'].lower():
				x = conn.cursor()
				messageS = messageData['text'].lower()
				checkList = messageS.split()
				if len(checkList) == 1:
					try:
						x.execute("""SELECT COLUMN_NAME FROM TABLE_NAME WHERE ATTRIBUTE=%s""",(str(messageData['text'].lower()), ))
						gmeSendback=x.fetchone()[0]
					except:
						gmeSendback = "Sorry %s, no gif found in the bin, add it on THE DATABASE" % (theUser,)
			#reddit link fixer
			elif "r/" in messageData['text'].lower() and "www." not in messageData['text'].lower() and ".com" not in messageData['text'].lower():
				m= re.search('(?<=r/)\w+',messageData['text'].lower())
				gmeSendback = "Here is your link %s! www.reddit.com/r/" % (theUser,)+m.group(0)
			#you just got burned statement
			elif "you just got burned." in messageData['text'].lower():
				gmeSendback = "Get help with your burn! http://en.wikipedia.org/wiki/List_of_burn_centers_in_the_United_Stateshttp://en.wikipedia.org/wiki/List_of_burn_centers_in_the_United_States"
			#link statement
			elif "link?" in messageData['text'].lower():
				gmeSendback = "Here's Link, The Hero of Time: http://imgur.com/NNmOyg3.jpg"
			#when the bot's name is mentioned in a message, it will analyse the message and reply based on the comment
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
			#the bot will agree with you
			elif "right bot?" in messageData['text'].lower():       
				gmeSendback = "You are correct %s" %(theUser,)
			#the bot will read the first comment of a reddit thread
			elif "reddit.com" in messageData['text'].lower()and"comments"in messageData['text'].lower():
				submission = r.get_submission(messageData['text']).comments[0]
				if len(submission.body) > 430:
					gmeSendback = "TL;TR (Too lazy to read that long ass comment)"
				else:
					gmeSendback = submission.body
			#the bot will reply if he's up and running
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