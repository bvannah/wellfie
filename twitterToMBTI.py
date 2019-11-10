from newBackend import getString
from twitterSentiment import getTweets
import sys
import easygui

def getRisk(ptype):
    
    very_low=["ISFJ", "ISTJ", "ESFJ", "ESTJ"]
    low=["INFJ", "INTJ", "ENFJ", "ENTJ"]
    high=["ESFP", "ESTP", "ISFP", "ISTP"]
    very_high=["ENFP", "ENTP", "INFP", "INTP"]
    
    if ptype in very_low:
        return 1
    if ptype in low:
        return 2
    if ptype in high:
        return 3
    if ptype in very_high:
        return 4
    #not enough information
    return 0


def getType(handle):
    tweets=getTweets(handle)
    ptype=getString(tweets)
    return ptype

if __name__ =="__main__":
    try:
        handle=sys.argv[1]
        print(handle + " " + str(getRisk(handle)))
    #if there's no arguments
    except:
        getType()
        image = "image.jpg"
        handle=easygui.enterbox("Input Twitter handle:", image=image)
        easygui.msgbox("I think their personality type is " + ptype)
    
