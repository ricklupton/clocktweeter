
import time
import urllib2
import os
import twitter

def get_clock_state():
    url_root = "http://www.trin.cam.ac.uk/clock/data/"
    path = time.strftime("%Y/%m/clock%Y-%m-%d.txt")
    f = urllib2.urlopen(url_root + path)
    last_line = f.readlines()[-1]
    f.close()

    ts, drift, amp = last_line.split()
    return float(ts), float(drift), float(amp)


CONSUMER_KEY = "WU7FBdk7AfftK14nSgKdA"
CONSUMER_SECRET = "Ab58c909B3UdQkoaruLo0mudUO75SQf3O07s0lkg4r0"
def get_twitter():
    MY_TWITTER_CREDS = os.path.join(os.path.dirname(__file__), '.clocktweeter_credentials')
    if not os.path.exists(MY_TWITTER_CREDS):
        twitter.oauth_dance("Trinity clock tweeter", CONSUMER_KEY,
                            CONSUMER_SECRET, MY_TWITTER_CREDS)

    oauth_token, oauth_secret = twitter.read_token_file(MY_TWITTER_CREDS)

    t = twitter.Twitter(auth=twitter.OAuth(
        oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))
    return t

def tweet_clock_state(maximum_age=12):
    ts, drift, amp = get_clock_state()

    # check the "latest" data isn't too old
    hours_old = (time.time() - ts) / 3600
    if hours_old > maximum_age:
        raise RuntimeError("No up-to-date clock information available")

    fast_slow = "fast" if drift > 0 else "slow"
    message = """The clock is %.1f seconds %s today.
http://www.trin.cam.ac.uk/clock """ % (abs(drift), fast_slow)

    t = get_twitter()
    t.statuses.update(status=message)

if __name__ == "__main__":
    tweet_clock_state()
