__author__ = 'tuhung-te'

import re
import os
from Settings import stop_words_FileName
import string

class PreProcessing(object):

    def __init__(self):
        self.stopwordslis =""


    #  getting ride of repetitions of character
    def  removeRepeatingCharacter(self,textstring):
    # (W): any alphanumeric character \1{1,} repeat once
         text = re.sub(r"(.)\1{1,}",r'\1\1', textstring)
         return  text


    def getStopWrods(self,filename):
        return [line.strip() for line in open(filename, 'r')]

    def removeStopWords(self,text):
        featureVector = []
        wordList = text.split()
        stopWordList = self.getStopWrods(os.path.join(os.path.dirname(__file__),stop_words_FileName))

        for word in wordList:
            val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", word)
            if word not in stopWordList and val is not None:
                featureVector.append(word)
        print(' '.join(featureVector))
        return ' '.join(featureVector);



    def processing(self,text):
        # URL  instead of www and http
        text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',str(text).lower())
        # AT_USER instead of @username
        text = re.sub('@[^\s]+','ATUSER',text)
        # get ride of additional white space
        text = re.sub('[\s]+', ' ', text)
        # remove hashtag (#)
        text = re.sub(r'#([^\s]+)', r'\1', text)

        text = text.strip('\'"')
        #remove repeating character
        text = self.removeRepeatingCharacter(text)
        #text = text.strip('\'"?,.')
        exclude = set(string.punctuation)
        text = ''.join(ch for ch in text if ch not in exclude)

        text = self.removeStopWords(text)

        return text


