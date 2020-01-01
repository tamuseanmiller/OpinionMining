# -*- coding: utf-8 -*-

# Sample Python code for youtube.commentThreads.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

posWords = set()
negWords = set()


def create():
    cnt = 0
    file = open('negative-words.txt', 'r', encoding='ISO-8859-1')
    for line in file:
        cnt += 1
        if cnt >= 32:
            line = line.replace('\n', '')
            negWords.add(line)
    cnt = 0
    file.close()
    file = open('positive-words.txt', 'r', encoding='ISO-8859-1')
    for line in file:
        cnt += 1
        if cnt >= 31:
            line = line.replace('\n', '')
            posWords.add(line)


# Method that parses through every line of file made from main method
# and assigns a score to every comment, then returns a total score
def parse(score=0):
    # Puts all lines of file into the list 'lines'
    with open('info.txt', 'r', encoding='ISO-8859-1') as f:
        lines = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        lines = [x.strip() for x in lines]

    # Reads every line from document
    for l in lines:

        # Splits by whitespace
        j = l.split()
        comment_score = 0
        for i in j:

            # Checks for if the word is contained in pos or neg sets and sets a unique comment score
            if i in posWords:
                comment_score += 1
            elif i in negWords:
                comment_score -= 1

        # For debug, prints each comment that has an assigned score, and also tallies the total score
        if comment_score > 0:
            print("Positive Score: +" + str(comment_score) + " --> " + l)
            score += 1
        elif comment_score < 0:
            print("Negative: " + str(comment_score) + " --> " + l)
            score -= 1

    return score


# Method that calls Youtube API v3 to return at most 100 comments for a particular channel
def getComments(api_service_name, api_version, client_secrets_file, developer_key, channel_id, page_token=None):

    # Get credentials and create an API client
    # flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    #     client_secrets_file, scopes)
    # credentials = flow.run_console()

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=developer_key)

    # Checks to see if a nextPageToken value was passed
    if page_token is not None:
        response = youtube.commentThreads().list(
            part="snippet,replies",
            allThreadsRelatedToChannelId=channel_id,
            maxResults=100,
            order="time",
            textFormat="html",
            pageToken=page_token
        ).execute()
    else:
        response = youtube.commentThreads().list(
            part="snippet,replies",
            allThreadsRelatedToChannelId=channel_id,
            maxResults=100,
            order="time",
            textFormat="html"
        ).execute()

    return response


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret_765965354761-eu1neqo2lommuqc2tqh8fi1vtvkfr66i.apps.googleusercontent.com.json"
    developer_key = 'AIzaSyC2BquPeqcoHl8RQs_m7wUVnJfO84fKCRw'
    channel_id = input("Channel ID --> ")

    response = getComments(api_service_name, api_version, client_secrets_file, developer_key, channel_id)

    # Opens file to write all comments
    file = open('info.txt', 'w', encoding='utf-8')

    # The sample size for loop
    for resp in range(1):

        # for loop to iterate through every comments information
        for block in response['items']:
            block = block['snippet']
            block = block['topLevelComment']
            block = block['snippet']
            block = block['textOriginal']
            block = block.replace('\n', '')
            file.write(block + '\n')

            # Reads the comments again to get over the max limit of 100
            response = getComments(api_service_name, api_version, developer_key, client_secrets_file, channel_id,
                                   response['nextPageToken'])

    file.close()
    create()
    score = parse()

    print("Score:", score)


if __name__ == "__main__":
    main()
