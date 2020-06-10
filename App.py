# -*- coding: utf-8 -*-

import random
from googletrans import Translator
import praw
import pdb
import re
import os
import time

# A list of unpopular languages; the more popular, the better the translation, and that's exactly NOT what we want here
language_list = ["af", "am", "hy", "eu", "ceb", "co", "eo", "ig", "kn", "ky", "mr", "gd", "tg", "xh", "zu"]

# Checks comment for instance of !translatify and handles accordingly
def check_comment(comment):
    if(re.search("!translatify", comment.body, re.IGNORECASE)):
        # Check if comment is older than 15 min; if so, skip
        if(time.time() - comment.created_utc > 900):
            print("Comment older than 15 min!")
            return

        # Check if the post's replies contains /u/TranslatifierBot; if so, skip
        if(len(comment.replies) > 0):
            for reply in comment.replies:
                if(reply.author.name == "TranslatifierBot"):
                    print("Already contains reply!")
                    return


        # Take the submission post, translatify it, and reply to the comment
        submission_text = comment.submission.selftext
        translated = translate(submission_text)
        if(len(translated) == 0): return
        try:
            comment.reply(translated + "\n***\n^(Beep boop. I am a bot. Contact my) [^(owner)](https://www.reddit.com/u/iidatkat) ^(for any issues.)")
        except:
            print("Reddit API limitation – try again later.")

# Runs the string s through Google Translate randomly
def translate(s):
    translator = Translator()

    try:
        for i in range(random.randint(5, 10)):
            # Choose a random language
            language_selected = language_list[random.randint(0, len(language_list) - 1)]
            
            print(language_selected)
            try:
                s = translator.translate(s, dest=language_selected).text
            except:
                # if it fails, whatever, next language
                continue
            print("Translating to " + language_selected + ": " + s)
            print("\n")

        # Translate it back to English
        s = translator.translate(s, dest="en").text
        print("Final translation: " + s)
    except:
        # if it messes up, do nothing
        print("Error somewhere!")
        return ""

    return s

def main():
    reddit = praw.Reddit("TranslatifierBot", user_agent="/u/TranslatifierBot user agent")
    
    subreddit = reddit.subreddit("copypasta")

    for comment in subreddit.stream.comments(skip_existing=True):
        print("Comment: " + comment.body)
        check_comment(comment)

if __name__ == "__main__":
    main()