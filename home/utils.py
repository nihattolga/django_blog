from math import log

def best(upvote, downvote, item_hour_age, gravity=1.8):
    return ((upvote-downvote) - 1) / pow((item_hour_age+2), gravity)

def hot(A, B, upvote, downvote):
    ts = (A - B).total_seconds()
    x = upvote - downvote
    y = 1 if x > 0 else -1 if x < 0 else 0
    z = 1 if abs(x)<1 else abs(x)
    return (log(z, 10) + (y*ts)/45000)