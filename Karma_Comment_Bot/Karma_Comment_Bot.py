import praw
import time
import random
import timeit

startTime = timeit.default_timer()	# get the local machine's time
timeCheck  = 0	# init this var so it's an int


mainReddit = praw.Reddit(user_agent='REDDIT-APP-NAME',
				  client_id='REDDIT-APP-ID',
				  client_secret='APP-SECRET-ID',
				  username='REDDIT-USERNAME',
				  password='REDDIT-PASSWORD')


subReddit = mainReddit.subreddit('all')
comments = subReddit.stream.comments()

# list of subs this account is banned in, will be used to avoid an error for an unsucessful post attempt
bannedSubs = ["blahblahblah", "qwertyuiop"]


print("- - - - - - - - - - - -")
print(" - - - - - - - - - - - ")
print("- - - S T A R T - - - -")
print(" - - - - - - - - - - - ")
print("- - - - - - - - - - - -")

for comment in comments:

	text = comment.body # text body of this comment
	author = comment.author # comment author of this comment

	currentCommentSub = comment.subreddit # parent subreddit of this comment

	commentTimeCreated = comment.created_utc # time comment was posted... in "unix time"
	commentURL = comment.permalink

	message = "Fair enough" 	# this string will be my "bot's" reply

	sleepyTime = random.randint(61, 97) # randomize sleep time, in range: minimum seconds to max seconds
	
	textFile = open("recent_subs.txt", "r")
	recentSubs = textFile.readlines()
	textFile.close()

	if str(currentCommentSub) in bannedSubs:
		print("~~~~~~~~~~~~~")
		print("Banned from posting in ", currentCommentSub, " LOL")
		print("Trying a new subreddit")
		print("~~~~~~~~~~~~~")
	elif (str(currentCommentSub)+"\n") in recentSubs:
		print("~~~~~~~~~~~~~")
		print("Already posted in ", currentCommentSub, " recently")
		print("Trying a new subreddit")
		print("~~~~~~~~~~~~~")
	elif 'cause' in text.lower():	# if someone's comment contains cause, because, etc...
		
		if 'Mod' not in author.name:	# let's not reply to AutoMods and whatnot!

			timeCheck = timeit.default_timer()	
			print("Current Runtime: " + str(round(timeCheck, 2)) + " seconds")

			print("Author:", author)
			print("Sub:", currentCommentSub)

			# posts a reply to the comment with my *messsage phrase, "Fair Enough"
			comment.reply(message)
			# upvote the comment being replied to
			comment.upvote()
			# get the parent comment of comment being replied to and upvote that too
			parent = comment.parent()
			parent.upvote()


			textFile = open("recent_subs.txt", "r")
			recentSubs = textFile.readlines()
			textFile.close()
			print(recentSubs)

			textFile = open("recent_subs.txt", "a")
			textFile.write("%s\n" %currentCommentSub)
			textFile.close()

			textFile = open("recent_subs.txt", "r")
			recentSubs = textFile.readlines()
			textFile.close()

			if len(recentSubs) > 10:	# if recently commented in > 10 different subreddits:
				
				open('recent_subs.txt', 'w').close()	# clear recent_subs.txt file

				textFile = open("recent_subs.txt", "a")
				for i in range(1,11):
					textFile.write("%s" %recentSubs[i])
				textFile.close()

			textFile = open("recent_subs.txt", "r")
			recentSubs = textFile.readlines()
			textFile.close()
			print(recentSubs)


			print("Sleeping for " + str(sleepyTime) + " seconds")
			print("-------------")
			time.sleep(sleepyTime) # sleep for however many seconds sleepyTime was randomly set to
