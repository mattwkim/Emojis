#Matt Kim
#Printing graph functions
import matplotlib.pyplot as plt
import operator, os

def printemojiinformation(data):
    """Create graphs with top 5 emojis vs each metric as well
        as the top 5 words used next to the top 5 emojis.    """
    metricslist = ['shares','views','comments','likes','count']
    
    #Will print the top 5 emojis used because of there being too many emojis overall
    for metric in metricslist:
        top5emoji = sorted(data.items(), reverse=True,key=lambda t:t[1][metric])
        top5emoji = dict(top5emoji[:5])
        top5emojis = {}
        for emoji in top5emoji.keys():
            top5emojis[emoji] = top5emoji[emoji][metric]
        plt.bar(range(len(top5emojis)),top5emojis.values(),align='center')
        plt.xticks(range(len(top5emojis)),top5emojis.keys(),rotation='vertical')
        plt.title("The top 5 emojis with highest " + metric)
        plt.savefig("Top_5_Emojis_Highest_" + metric + "_Graph.png",bbox_inches="tight")
        plt.close()
        
        #Print out top 5 words used next to emojis with highest counts
        if metric == 'count':
            index = 5
            for emoji in top5emojis:
                top5words = data[emoji]['commonwords']
                top5words = sorted(top5words.items(),key=operator.itemgetter(1), reverse=True)
                top5words = dict(top5words[:5])
                plt.bar(range(len(top5words)),top5words.values(),align='center')
                plt.xticks(range(len(top5words)),top5words.keys(),rotation='vertical')
                plt.title("The top 5 words used next to " + emoji)
                plt.savefig("Top_5_Words_used_Next_to_the_" + str(index) + "_Common_Emoji.png",bbox_inches="tight")
                plt.close()
                index -= 1

def printchannelgraphs(data):
    """Creates Channel vs emojis graph by using data from channelemoji dict
        ChannelEmoji: {Key: Channel, Value: {Key:Emoji, Value:Count}}"""
    for channel in data:
        if channel != 0:
            top5emojisinchannel = dict(sorted(data[channel].items(), reverse=True,key=operator.itemgetter(1))[:5])
            plt.bar(range(len(top5emojisinchannel)),top5emojisinchannel.values(),align='center')
            plt.xticks(range(len(top5emojisinchannel)),top5emojisinchannel.keys(),rotation='vertical')
            plt.title("Top 5 emojis used in" + channel)
            plt.savefig("Top_5_Emojis_Used_In_" + channel + ".png",bbox_inches="tight")
            plt.close()

def printbrandgraphs(data, emojisentiments):
    """Creates brand vs top 5 emojis graphs, brand vs skin tone modifiers graphs,
        and a brands vs sentiment scores graph
        data = brandemojicount {Key: Brand, Value:{Key:Emoji, value:count}}
        emojisentiment = emojiunicodesentimentdict {Key: Emoji, Value:Sentiments}"""
    #Place emoji vs brand graph in separate folder than the skin tone modifiers
    os.makedirs("Skin Tone Modifier vs Brand Graphs")
    os.makedirs("Top 5 Emojis vs Brand Graphs")
    
    for brand in data.keys():
        os.chdir("Top 5 Emojis vs Brand Graphs")
        
        #Because there are so many emojis in each brand, I'll print the top 5 emojis used in each brand
        top5emojisandcounts = sorted(data[brand].items(),reverse=True,key=operator.itemgetter(1))[:5]
        top5emojisandcounts = dict(top5emojisandcounts)
        plt.bar(range(len(top5emojisandcounts)),top5emojisandcounts.values(),align='center')
        plt.xticks(range(len(top5emojisandcounts)),top5emojisandcounts.keys(), rotation='vertical')
        thebrand = unicode(brand, "utf-8")
        plt.title(thebrand)
        plt.savefig("Top_5_Emojis_Used_for_" + thebrand + ".png",bbox_inches="tight")
        plt.close()
        os.chdir("..")
        os.chdir("Skin Tone Modifier vs Brand Graphs")
        skintonemodifiers = {'\U0001f3fb':0, '\U0001f3fc':0,'\U0001f3fd':0,'\U0001f3fe':0,'\U0001f3ff':0}
        for emoji in skintonemodifiers.keys():
            skintonemodifiers[emoji] = data[brand][emoji]       
        plt.bar(range(len(skintonemodifiers)), skintonemodifiers.values(), align='center')
        plt.xticks(range(len(skintonemodifiers)),skintonemodifiers.keys(),rotation='vertical')
        plt.title(thebrand + " skin tone modifiers count")
        plt.savefig("Skin tone modifiers count for " + thebrand, bbox_inches="tight")
        plt.close()
        os.chdir("..")

    #Print brand vs total emoji sentiment score graph
    #Since there are just 19, compared to the tons of emojis used, I'll be printing all brands
    brandsentiment = {}
    for brand in data.keys():
        #Note: Because not all emojis from the full emoji unicode list link appeared in the emoji sentiment link in the google docs,
        #I wouldn't say these graphs are very accurate..
        sentiment = 0
        for emoji in data[brand]:
            index = -8
            for i in range(0, len(emojisentiments['Emoji_Unicode'])):
                if emojisentiments['Emoji_Unicode'][i] == emoji:
                    index = i
            if index != -8:
                sentiment += emojisentiments["Sentiment"][index]
        brand = brand.decode("utf8")
        brandsentiment[brand] = sentiment
    plt.bar(range(len(brandsentiment)), brandsentiment.values(),align='center')
    plt.xticks(range(len(brandsentiment)),brandsentiment.keys(),rotation='vertical')
    plt.title("Brand vs Sentiment")
    plt.savefig("Brand_vs_Sentiment.png",bbox_inches="tight")
    plt.close()

    
