# TranslatifierBot
A Reddit copypasta bot with the power of Google Translate.

Hosted on Heroku and summoned with `!translatify` on [/r/copypasta](https://www.reddit.com/r/copypasta) posts. Under the Reddit user [/u/TranslatifierBot](https://www.reddit.com/user/TranslatifierBot/).

Idea taken from ["Let It Go" from Frozen according to Google Translate (PARODY)](https://www.youtube.com/watch?v=2bVAoVlFYf0)

### Process
- When !translatify is read in a comment, the script reads the body of the copypasta post
- If the bot has already replied to a comment, or if the comment is older than 15 minutes, then it disregards it
- The script iterates through a loop a random number of times and translates the post body to a random language from an array
- It ends with a translation back to English and a reply to the comment.

*Creation Date: 06/09/2020*
