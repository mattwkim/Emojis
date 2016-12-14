#Matt Kim
import math, pandas, sys, string, os, re
from GraphCreator import printchannelgraphs, printbrandgraphs, printemojiinformation

#Read files 
#Replace empty spaces with 0 instead of nan (pandas assigns nan automatically)
brandsfile = pandas.read_csv("brands_mentioned.csv", skiprows=1, names=['uniq_id','brand_name'])
postsfile = pandas.read_csv("posts.csv",skiprows=1,names=['uniq_id','channel','media_outlet_link','post_link','post_message','shares','views','comments','likes'])
emojiunicode = pandas.read_csv("EmojiUnicodeList.csv", skiprows=1, names = ["Emoji_Unicode"])
emojisentiment = pandas.read_csv("EmojiSentimentList.csv",skiprows=1,names=["Emoji_Unicode","Sentiment"])
postsfile = postsfile.fillna(0)
brandsfile = brandsfile.fillna(0)

messagescontainer = postsfile['post_message']

#Contains all of the emojis with their counts in each brand
brandemojicount = {}

#Emoji to the sum of each of their metrics as well as their count
emojimetricscount = {}

#Emojis and their counts within each channel
channelemoji = {}
metrics = ['shares','views','comments','likes']

#Grab data for each dictionary I made above
for i in range(0,len(messagescontainer)):
    #Avoid empty messages
    if messagescontainer[i] != 0:
        message = messagescontainer[i]
        message = unicode(message, 'utf8')
        message = message.encode("unicode_escape")

        #Find all emojis using regular expression
        #Re statement below misses the \, so add it back manually
        emojisinmessage = re.findall(r"(?=(" + '|'.join(emojiunicode['Emoji_Unicode'])+r"))",message)
        emojisinmessage = [chr(92) + myunicode for myunicode in emojisinmessage]

        #Create brand/channel keys in their respective dictionaries
        brand = brandsfile['brand_name'][i]
        if brand not in brandemojicount:
            brandemojicount[brand] = {}
        channel = postsfile['channel'][i]
        if channel not in channelemoji:
            channelemoji[channel] = {}

        #Add data to the containers
        for emoji in emojisinmessage:
            #Channel to emoji count dictionary
            if emoji not in channelemoji[channel]:
                channelemoji[channel][emoji] = 1
            else:
                channelemoji[channel][emoji] += 1
                
            #create emoji to engagement metrics dictionary
            if emoji not in emojimetricscount:
                emojiinfo = {}
                for metric in metrics:
                    emojiinfo[metric] = postsfile[metric][i]
                emojiinfo['count'] = 1
                emojimetricscount[emoji] = emojiinfo
                
            #Concatenate previous information with new ones in emojimetrics dict
            else:
                for metric in metrics:
                    emojimetricscount[emoji][metric] = emojimetricscount[emoji][metric] + postsfile[metric][i]
                emojimetricscount[emoji]['count'] = emojimetricscount[emoji]['count'] + 1

            #Grab words left and right of the emojis
            leftright = []
            index = message.find(emoji)
            parsedmessage = message[:index].strip()
            leftspace = parsedmessage.rfind(" ")
            
            #Covers a bug
            #Example: "\ufe0f\u2022"
            #If the emoji is \u2022, there is no space, so leftword = 'f'
            if leftspace == -1:
                leftword = parsedmessage
            else:
                leftword = parsedmessage[leftspace:].strip()
                
            leftright.append(leftword)
            message = message[index + len(emoji):].strip()
            rightspace = message.find(" ")

            #Covers a bug
            #Example: "\u2600\u2000"
            #If the emoji is \u2600, there is no space, so rightword = '\u260'
            if rightspace == -1:
                rightword = message
            else:
                rightword = message[:rightspace].strip()
            leftright.append(rightword)
            for word in leftright:
                #For some emojis that aren't utf-16 according to the unicode site, shows up as utf-16 in python, i.e. the sun emoji(\u2600\ufe0f)
                #Gonna get rid of parts that don't show up on unicode.org
                #Python acts up if I say "\u" since it thinks it's an incomplete unicode char
                #chr(92) + 'u' is an alternative
                if chr(92) + 'u' in word:
                    indices = [i for i in range(0, len(word) - 1) if word[i] + word[i + 1] == chr(92) + 'u']
                    offset = 0
                    for index in indices:
                        if word[index - offset + 2].isalpha():
                            word = word[:index - offset] + word[index + 6 - offset:]
                            offset += 6
                            
                if "\n" in word or "\\n" in word:
                        word = word.replace("\n","")
                        word = word.replace("\\n","")
                if word != '':
                    if 'commonwords' not in emojimetricscount[emoji]:
                        emojimetricscount[emoji]['commonwords'] = {}
                    if word not in emojimetricscount[emoji]['commonwords']:
                        emojimetricscount[emoji]['commonwords'][word] = 1
                    else:
                        emojimetricscount[emoji]['commonwords'][word] += 1
                        
            #Create brand with associated emojis dictionary   
            if emoji not in brandemojicount[brand]:
                brandemojicount[brand][emoji] = 1
            else:
                brandemojicount[brand][emoji] += 1

#Save all images into a new folder
os.makedirs("MattKimBarGraphs")
os.chdir("MattKimBarGraphs")

#Print top 5 emoji vs metrics graphs as well as top 5 emojis used graph
os.makedirs("EmojiMetrics")
os.chdir("EmojiMetrics")
printemojiinformation(emojimetricscount)

#Print top 5 emojis used per channel graphs in new folder
os.chdir("..")
os.makedirs("ChannelVsEmojis")
os.chdir("ChannelVsEmojis")
printchannelgraphs(channelemoji)
    
#Save all brand related graphs in new folder
os.chdir("..")
os.makedirs("Brand Graphs")
os.chdir("Brand Graphs")
printbrandgraphs(brandemojicount, emojisentiment)




        
