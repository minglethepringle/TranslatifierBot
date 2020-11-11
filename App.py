# -*- coding: utf-8 -*-

import random
from googletrans import Translator
import praw
import pdb
import re
import os
import time

# A list of unpopular languages; the more popular, the better the translation, and that's exactly NOT what we want here
# language_list = ["af", "am", "hy", "eu", "ceb", "co", "eo", "ig", "kn", "ky", "mr", "gd", "tg", "xh", "zu"]
language_list = ["ar", "hy", "zh-CN", "fr", "de", "he", "ja", "ko", "ru", "es", "th", "vi", "it"]

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
            comment.reply(translated + "\n***\n^(Beep boop. I am a bot. Here's my) [^(owner.)](https://www.reddit.com/u/iidatkat) ^(Here's my) [^(source code.)](https://github.com/minglethepringle/TranslatifierBot)")
        except:
            print("Reddit API limitation – try again later.")

# Checks post for instance of !translatify and handles accordingly
def check_post(post):
    # Take the submission post, translatify it, and reply to the post
    submission_text = post.selftext
    if(len(submission_text) > 14999): return
    translated = translate(submission_text)
    if(len(translated) == 0): return
    try:
        post.reply(translated + "\n***\n^(Beep boop. I am a bot. Here's my) [^(owner.)](https://www.reddit.com/u/iidatkat) ^(Here's my) [^(source code.)](https://github.com/minglethepringle/TranslatifierBot)")
    except:
        print("Reddit API limitation – try again later.")


# Runs the string s through Google Translate randomly
def translate(s):
    translator = Translator()

    try:
        for i in range(random.randint(5, 10)):
            # Choose a random language
            language_selected = language_list[random.randint(0, len(language_list) - 1)]
            
            print("Trying to translate to: " + language_selected)
            try:
                translated_string = translator.translate(s, dest=language_selected).text
                if(len(translated_string) > 0): s = translated_string
            except:
                # if it fails, whatever, next language
                continue

            print("Translated to " + language_selected + ": " + s)
            print("\n")

        # Translate it back to English
        s = translator.translate(s, dest="en").text
        print("Final translation: " + s)
    except:
        # if it messes up, do nothing
        print("Error somewhere!")
        return translate(s)

    return s

def main():
    reddit = praw.Reddit("TranslatifierBot", user_agent="/u/TranslatifierBot user agent")
    
    subreddit = reddit.subreddit("copypasta")

    for post in subreddit.stream.submissions(skip_existing=True):
        print("Post: " + post.selftext)
        check_post(post)

# def main():
#     reddit = praw.Reddit("TranslatifierBot", user_agent="/u/TranslatifierBot user agent")
    
#     submission_text = """
#         Ok so I used to love posting on r/chonkers with pics of my overweight dog named Chungus. I don't really walk him that much, but I do feed him a shit ton of food so he can stay heckin' wholesome. Recently, my posts haven't been getting karma liked they used to. They dropped from 20k to 12k and I also noticed a decrease in awards, so I decided to let Chungus go out with a bang by getting a glock from my dad's drawer and shooting him in the head. Now that I think about it, this reminds me of my favorite movie (Joker lol) when he shot that guy in the face haha. So anyways I was about to post a picture of Chungus' corpse for 100k karma when I realized that they're gonna notice the bullet hole. I decided not to post it and I threw Chungus in the trash. Am I the asshole?
#     """

#     translate(submission_text)

if __name__ == "__main__":
    main()