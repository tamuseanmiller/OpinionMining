# OpinionMining
Social Media service that assigns a score based on sentiment analysis of the public's replies.

Right now, it takes in a YouTube ChannelID and Twitter keywords and parses through the last x amount of comments as well as the last 7 days of tweets and applies a score of sentiment to each comment and tweet that effects the overall score of the channel.

Only supports YouTube Channels and Twitter keywords right now, but will hopefully be able to access more social platforms in the future.

Credits to:
Minqing Hu and Bing Liu. "Mining and Summarizing Customer Reviews." 
;       Proceedings of the ACM SIGKDD International Conference on Knowledge 
;       Discovery and Data Mining (KDD-2004), Aug 22-25, 2004, Seattle, 
;       Washington, USA, 
for the positive and negative words

and

https://github.com/feconroses/gather-tweets-from-stream
@feconroses for the twitter script
