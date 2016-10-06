from os import environ
import sys
from random import choice
import twitter


def open_and_read_file(filenames):
    """Given a list of files, open them, read the text, and return one long
        string."""

    body = ""

    for filename in filenames:
        text_file = open(filename)
        body = body + text_file.read()
        text_file.close()

    return body


def make_chains(text_string):
    """Takes input text as string; returns dictionary of markov chains."""

    chains = {}

    words = text_string.split()

    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        value = words[i + 2]

        if key not in chains:
            chains[key] = []

        chains[key].append(value)

        # or we could replace the last three lines with:
        #    chains.setdefault(key, []).append(value)

    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""

    key = choice(chains.keys())
    words = [key[0], key[1]]
    while key in chains:
        # Keep looping until we have a key that isn't in the chains
        # (which would mean it was the end of our original text)
        #
        # Note that for long texts (like a full book), this might mean
        # it would run for a very long time.

        word = choice(chains[key])
        words.append(word)
        key = (key[1], word)

    return " ".join(words)


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""
     
    start_text = choice(chains.keys())
    
    while not start_text[0].istitle():
        start_text = choice(chains.keys())

    master_text = start_text[0] + " " + start_text[1]
    text_split = tuple(master_text.split())

    while text_split[-2:] in chains:
        new_word = choice(chains[text_split[-2:]])
        master_text += (" "+ new_word)
        text_split = tuple(master_text.split())


    print len(master_text)
    return master_text


def tweet(master_text):
    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.
    api = twitter.Api(
        consumer_key=environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=environ['TWITTER_ACCESS_TOKEN_SECRET'])

    # print api.VerifyCredentials()
    tweet_message = master_text[:125] + " #hbgracefall16"
    tweet = api.PostUpdate(tweet_message)
    return tweet

def continue_tweeting():

    keep_going = "y"
    while keep_going != "q":
        filenames = sys.argv[1:]
        text = open_and_read_file(filenames)
        chains = make_chains(text)
        master_text = make_text(chains)
        tweet(master_text)
        keep_going = raw_input("Would you like to tweet again? Type 'y' for yes or 'q' to quit. ").lower()

# Get the filenames from the user through a command line prompt, ex:
# # python markov.py green-eggs.txt shakespeare.txt
# filenames = sys.argv[1:]

# # Open the files and turn them into one long string
# text = open_and_read_file(filenames)

# # Get a Markov chain
# chains = make_chains(text)

# master_text = make_text(chains)

continue_tweeting()


# Your task is to write a new function tweet, that will take chains as input
# print tweet(master_text)
