
import re
from collections import defaultdict

#define dictionaries that used in calate prob
cnt_2_seque = defaultdict(dict)
cnt_3_seque = defaultdict(lambda: defaultdict(dict))
prob_3_seque = defaultdict(lambda: defaultdict(dict))
prob_2_seque = defaultdict(lambda: defaultdict(dict))
cnt_1_seque = defaultdict(dict)
#hold all unique words
words = []

def readFile(filename):
    f = open(filename, encoding='utf-8')
    lines = f.read()
    str = ""
    for s in lines:
        if s[0] != '<' and s[0] != '>':
            str = str + s
    return str

# calculates count
def calculateCount(str):
    # gets rid of commas and stuff
    str = re.split('; |, |\*|\n|\s| ', str)
    global words, cnt_1_seque
    # remove repeated words
    words = set(str)
    words = list(words)

    # initializes the dictionaries first
    for i in range(len(str) - 2):
        cnt_3_seque[str[i]][str[i + 1]][str[i + 2]] = 0
        cnt_2_seque[str[i]][str[i + 1]] = 0
        cnt_1_seque[str[i]] = 0

    cnt_1_seque[str[len(str) - 1]] = 1
    cnt_1_seque[str[len(str) - 2]] = 1
    cnt_2_seque[str[len(str) - 2]][str[len(str) - 1]] = 1

    # then whenever a sentence is found, increases its count
    for i in range(len(str) - 2):
        cnt_3_seque[str[i]][str[i + 1]][str[i + 2]] = cnt_3_seque[str[i]][str[i + 1]][str[i + 2]] + 1
        cnt_2_seque[str[i]][str[i + 1]] = cnt_2_seque[str[i]][str[i + 1]] + 1
        cnt_1_seque[str[i]] = cnt_1_seque[str[i]] + 1

    # then calculates probability according to markov trigram assumption, p(z|x,y) = c(x,y,z) / c(x,y)
    for i in range(len(str) - 2):
        prob_3_seque[str[i]][str[i + 1]][str[i + 2]] = cnt_3_seque[str[i]][str[i + 1]][str[i + 2]] / cnt_2_seque[str[i]][str[i + 1]]
    # p(y|x) = c(x,y) / c(x)
    for i in range(len(str) - 1):
        prob_2_seque[str[i]][str[i + 1]] = cnt_2_seque[str[i]][str[i + 1]] / cnt_1_seque[str[i]]

# predict word using trigram
def TrigramPredictWord(sentence):
    # splits sentence
    arr = sentence.split()
    #print(len(arr))
    res = defaultdict(dict)
    if(len(arr)==2):
        
        for third in cnt_3_seque[arr[0]][arr[1]]:
            res[third] = prob_3_seque[arr[0]][arr[1]][third]

    else :
        for third in cnt_2_seque[arr[0]]:
            res[third] = prob_2_seque[arr[0]][third]
    
    
    # sort the dictionary by probs value
    s = [(k, res[k]) for k in sorted(res, key=res.get, reverse=False)]
    res = []

    for key, value in s:
        res.append(key)
            
    # returns first 10 trigram predictions with highest probability
    return res[0:10]

def getPrediction(sentence):
    res = TrigramPredictWord(sentence)
    res = [sentence + " " + s for s in res]
    return res


"""     main     """
doc = readFile("corpus.txt")
calculateCount(doc)
while True :
    query = input("enter word")
    result = getPrediction(query)
    for word in result:
        print(word)
#print(cnt_1_seque)
#print(cnt_2_seque)
#print(cnt_3_seque)