from model_setup import getString
from twitter_access import getTweets
import sys
import easygui
from datetime import datetime


def getRisk(ptype):
    
    very_low=["ISFJ", "ISTJ", "ESFJ", "ESTJ"]
    low=["INFJ", "INTJ", "ENFJ", "ENTJ"]
    high=["ESFP", "ESTP", "ISFP", "ISTP"]
    very_high=["ENFP", "ENTP", "INFP", "INTP"]
    
    if ptype in very_low:
        return (1, "VERY LOW")
    if ptype in low:
        return (2, "LOW")
    if ptype in high:
        return (3, "HIGH")
    if ptype in very_high:
        return (4, "VERY HIGH")
    return (0, "I don't know, not enough information")


def getType(handle):
    print("getting tweets")
    tweets=getTweets(handle)
    print("got tweets")
    
    print("loading and using model")
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    ptype=getString(tweets)
    print("model loaded & used")
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    return ptype

if __name__ =="__main__":
    try:
        handle=sys.argv[1]
        print(handle + " " + str(getRisk(handle)))
    #if there's no arguments
    except:
        image = "image.jpg"
        handle=easygui.enterbox("Input Twitter handle:", image=image)
        ptype=getType(handle)
        risk=getRisk(ptype)
        easygui.msgbox("I think their personality type is:    " +
            ptype +  "\nSo their risk tolerance is:           " + risk[1])
    
