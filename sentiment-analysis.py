# Import argparse a standard library which will accept filenames as arguements
# Importing Google cloud language library
import csv
import json
import os
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

def print_result(annotations):
    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude

    for index, sentence in enumerate(annotations.sentences):
        sentence_sentiment = sentence.sentiment.score
        print('Sentence {} has a sentiment score of {}'. format(index, sentence_sentiment))

    print('Overall Sentiment: score of {} with magnitude of {}'.format(score, magnitude))

    return 0

def save_results_to_csv(ids, tweets, dates, sentiments, magnitudes, directory, resultsName):
    with open(directory + '/' + resultsName + '.csv', 'w') as resultsFile:
        print("Saving Results to CSV")
        i = 1
        while i < len(ids):
            print(ids[i])
            resultsFile.writelines(str(ids[i]) + ',' + str(tweets[i]) + ',' + str(dates[i]) + ',' + str(sentiments[i]) + ',' + str(magnitudes[i]) + '\n')
            i += 1
    resultsFile.close()

def analyze(filename):
    #run sentiment analysis on text
    client = language.LanguageServiceClient()

    # Lists containing CSV raw data
    ids = []
    tweets = []
    dates = []
    sentiments = []
    magnitudes = []

    with open(filename, 'r') as review_file:
        content = csv.reader(review_file)
        for row in content:
            # Iterate through the content and split it into individual lines
            ids.append(row[0])
            tweets.append(row[1])
            dates.append(row[2])

    for tweet in tweets:
        print(tweet)
        tweetObject = types.Document(
            content = tweet,
            type = enums.Document.Type.PLAIN_TEXT)

        annotations = client.analyze_sentiment(tweetObject)

        # score = annotations.document_sentiment.score
        # magnitude = annotations.document_sentiment.magnitude

        for index, sentence in enumerate(annotations.sentences):

            sentiments.append((sentence.sentiment.score))
            magnitudes.append((sentence.sentiment.magnitude))

    save_results_to_csv(ids, tweets, dates, sentiments, magnitudes, "results", "ResultsTest")

analyze("TestData.csv")