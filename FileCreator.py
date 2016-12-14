#Matt Kim
#File Creator

import requests

#Grab list of emojis from unicode.org
url = "http://unicode.org/cldr/utility/list-unicodeset.jsp?a=%5B%3Aemoji%3A%5D&g=emoji"
responsetext = requests.get(url).text
unicodecode = responsetext.find('<code>')
emojis = []
while unicodecode != -1:
    responsetext = responsetext[unicodecode + 5:]
    endoftag = responsetext.find("</a>")
    unicodecode = responsetext[:endoftag]
    unicodecode = unicodecode[unicodecode.rfind(">") + 1:].lower()
    emojis.append(unicodecode)
    responsetext = responsetext[responsetext.find("/code>") + 6:]
    unicodecode = responsetext.find("<code>")
    
emojiunicodelist = open("EmojiUnicodeList.csv","w")
#Header
emojiunicodelist.write('%s\n' % ("Emoji_Unicode"))

#Convert to unicode escape and output to csv
for emoji in emojis:
    if len(emoji[2:]) == 4:
        emoji = "\u" + emoji[2:]
    else:
        emoji = "\U000" + emoji[2:]
    emojiunicodelist.write('%s\n' % (emoji))

#Grab list of emojis with sentiment
url = "http://kt.ijs.si/data/Emoji_sentiment_ranking/"
responsetext = requests.get(url).text
locateinformation = responsetext.find("0x")
someemojisentiments = open("EmojiSentimentList.csv","w")
someemojisentiments.write('%s, %s\n' % ("Emoji_Unicode", "Sentiment"))
while locateinformation != -1:
    responsetext = responsetext[locateinformation + 2:]
    unicodeinfo = responsetext[:responsetext.find("</td>")]
    #Convert to unicode escape then output to csv
    if len(unicodeinfo) == 4:
        unicodeinfo = "\u" + unicodeinfo
        unicodeinfo = unicodeinfo.lower()
    else:
        unicodeinfo = "\U000" + unicodeinfo
        unicodeinfo = unicodeinfo.lower()
    sentiment = responsetext[:responsetext.find("<div ")]
    sentiment = sentiment[:sentiment.rfind("</td>")]
    sentiment = sentiment[sentiment.rfind("<td>") + 4:]
    locateinformation = responsetext.find("0x")
    someemojisentiments.write('%s, %s\n' % (unicodeinfo, sentiment))
    
    
