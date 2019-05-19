import praw
import pdb
import re
import os
import time
from fuzzywuzzy import fuzz

SUB_STMT_TXT = "submission statement"
MIN_SUB_STMT_LEN = 70
RATIO_THRESH = 85
MIN_AGE_SECS = 1200 #1200 #20 minutes
REPLY_STMT = "This post was removed because it appears to be missing a submission statement.\n\n"+"Submission statements are required\n\n"+"* on all non-text posts\n"+"* to be a top-level comment from OP\n"+'* to start with the text "Submission statement"\n'+'* to be at least 70 characters in length (excluding "Submission statement")\n'+'* to be posted within 20 minutes of post creation\n\n'+'Once you have posted your submission statement, it will be approved by the moderators.\n\n'+'*I am a bot, and this action was performed automatically. Please* [*contact the moderators of this subreddit*](https://www.reddit.com/message/compose/?to=/r/IntellectualDarkWeb) *if you have any questions or concerns.*'
DO_IT = False

# Create the Reddit instance and log in
reddit = praw.Reddit('bot1')

# Create a list
if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []

# Or load the list of posts we have replied to
else:
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))

#connect to a subreddit and grab the posts in "new"
subreddit = reddit.subreddit('IntellectualDarkWeb')
curTime = time.time()
for submission in subreddit.new():
    print(submission.title)
    age_in_secs = curTime - submission.created_utc
    # Make sure you didn't already reply to this post and that the post is not text-only and the post is 20 minutes old.
    if submission.id not in posts_replied_to and submission.is_self == False and age_in_secs >= MIN_AGE_SECS:
        # loop through top level comments
        hasSubStmt = False 
        for comment in submission.comments:
            # if there is a top level comment from the submitter
            if comment.author == submission.author:
                #if the comment meets length requirements
                if (len(comment.body) - len(SUB_STMT_TXT)) >=MIN_SUB_STMT_LEN:
                    splitComment = comment.body.split(" ")
                    #if the comment has at least two words
                    if len(splitComment) >= 2:
                        cmnt4Check = splitComment[0] + " " + splitComment[1]
                        #check the first two words for similarity to default text
                        if max(fuzz.ratio(SUB_STMT_TXT,cmnt4Check.lower()),fuzz.token_sort_ratio(SUB_STMT_TXT,cmnt4Check)) >= RATIO_THRESH:
                            hasSubStmt = True
                            break
        #if we didn't find a submission statement
        if not hasSubStmt:
            print("Replied to " + submission.title + " at " + submission.shortlink)
            #for debeugging
            if DO_IT:
                addSubStmtCmt = submission.reply(REPLY_STMT)
                addSubStmtCmt.mod.distinguish(how='yes', sticky=False)
                submission.mod.remove()
                posts_replied_to.append(submission.id)

# Write updated list to file
with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")
