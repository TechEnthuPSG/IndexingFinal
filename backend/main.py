# importing required modules

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import Stemmer
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import pickle, os

# intializing flask app with cors 

app = Flask(__name__)
cors = CORS(app, resources={r"/foo": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

# initialing pystemmer and preparing rootwords for wordsplitting

stemmer = Stemmer.Stemmer('tamil')
rootwords = []
chdf = open('datasetFile.txt','r', encoding='utf8')
for r in chdf.readlines():
        rootwords.append(str(r.strip()))

rootwordsDict = {}
if(os.path.exists('rootwords.pickle')):
    with open('rootwords.pickle', "rb") as f:
        rootwordsDict = pickle.load(f)
        f.close()

# functions for word splitting

def pickleDumper(data):
    with open('rootwords.pickle', "wb") as f:
        pickle.dump(data, f)
        f.close()

def fuzzymatch(string, master = rootwords):
  score1 = 0
  score2 = 0
  arr1 = []
  arr2 = []
  d1 = {}
  d2 = {}
  for (i,j) in process.extract(string, master, limit = 10):
    ratio = fuzz.ratio(i,string)
    if ratio >= 80:
      score1 += 1
      arr1.append(i)
      d1[i] = ratio
    ratio = fuzz.partial_ratio(i,string)
    if ratio >= 85:
      score2 += 1
      arr2.append(i)
      d2[i] = ratio
  return (score1, arr1, d1, score2, d2)

rootwordString = "\n".join(rootwords)

# functions for partial stemming algorithm

def hasQuestionSuffix(word):
  return (word[-1] in ["ா", "ே", "ோ"])

def fixQuestionSuffix(word):
  return word[:-1] + "்" 

def hasConjuctionSuffix(word):
  return (word[-3:] == "ும்")

def fixConjuctionSuffix(word):
  return word[:-3] + "்" 
  #return word[:-2]

def hasPluralSuffix(word):
  return (word[-5:] == "ங்கள்") or (word[-3:] == "கள்") or word[-4:] == "றனர்" or word[-3:] == "னர்" 

def fixPluralSuffix(word):
  if word[-5:] == "ங்கள்":
    return word[:-5] + "ம்"
  elif word[-3:] == "கள்":
    return word[:-3]
  elif word[-4:] == "றனர்":
    return (word[:-3]+ "ு")
  elif word[-3:] == "னர்":
    return word[:-3]

def hasImperativeSuffix(word):
   return (word[-1] in ["ி"])

def fixImperativeSuffix(word):
  #logic changed here
  #return word[:-1]
  return word[:-2]

def hasTenseSuffix(word):
    return (word[-6:] == "கின்றன") or (word[-3:] in ["ேன்"]) or (word[-16:-6]=="கொண்டிருக்")

def fixTenseSuffix(word):
  if (word[-4:]=="வேன்"):  #for future tense
     return word[:-4]
  if (word[-3:] in ["ேன்"]):
    return word[:-5] + "ு"
  if (word[-6:] == "கின்றன"):  # present
     return word[:-6]
  if(word[-16:-6]=="கொண்டிருக்"):
     return word[:-18]
  
def hasCommonWordSuffix(word):
  return  "ில்லாத" in word 

def fixCommonWordSuffix(word):
  return word[:-6]+ "்"

#வேற்றுமை உருப்புகள்
def hasCaseSuffix(word):
  return (word[-4:-2] == word[-2:]) or (word[-6:] in ["த்தில்"]) or (word[-4:] in ["ிடம்", "த்த்"]) or (word[-1]=='ை') or (word[-2:] in ["த்","ந்"]) or  (word[-4:] in ["த்து","ந்து","ந்த"] or word[-3:] in ["ந்த"]) or (word[-3:] == "ின்") or (word[-1:]== "ு")

#வேற்றுமை உருப்புகள்
def fixCaseSuffix(word):
  if(word[-4:-2] == word[-2:]):
    return word[:-2]
  if(word[-1:]== "ு"):
    if(word[-2]==word[-3]):
        return word[:-3]
    else:
        return word[:-2]
  if(word[-6:] in ["த்தில்"]):
    return word[:-6]+"ம்"
  if (word[-4:] in ["த்து","ந்து","ந்த"] or word[-3:] in ["ந்த"]):
    if(word[-3:] in ["ந்த"]):
      return word[:-3]
    return word[:-4]
  if word[-4:] == "த்த்":
    return word[:-4] + "ம்"
  if(word[-4:] == "ிடம்"):
    return word[:-4]+'்'
  if(word[-1]=='ை'):
    return word[:-1]+'்'
  if(word[-2:] in ["த்","ந்"]):  # to remove last extra mei eluthu
    return word[:-2]
  if word[-3:] == "ின்":
    return word[:-3] + '்'
  return word

def stem(word):

  iteration = 0
  temp = word.replace('ஂ', '்')
  
  while temp and len(temp) > 4:

    iteration += 1
    # #print("Beginning of iteration {} : {}".format(iteration, temp))

    if hasQuestionSuffix(temp):
      tempStore = temp
      temp = fixQuestionSuffix(temp)
      if(tempStore == temp):
        break

    elif hasConjuctionSuffix(temp):
      tempStore = temp
      temp = fixConjuctionSuffix(temp)
      if(tempStore == temp):
        break

    elif hasCaseSuffix(temp):
      tempStore = temp
      temp = fixCaseSuffix(temp)
      if(tempStore == temp):
        break

    elif hasPluralSuffix(temp):
      tempStore = temp
      temp = fixPluralSuffix(temp)
      if(tempStore == temp):
        break

    elif hasImperativeSuffix(temp):
      tempStore = temp
      temp = fixImperativeSuffix(temp)
      if(tempStore == temp):
        break

    elif hasTenseSuffix(temp):
      tempStore = temp
      temp = fixTenseSuffix(temp)
      if(tempStore == temp):
        break
      

    elif hasCommonWordSuffix(temp):
      tempStore = temp
      temp = fixCommonWordSuffix(temp)
      if(tempStore == temp):
        break

    else:
      break
    
  return temp

#function for choosing root from snoball stemmer and word splitting

def optimal(word, ratio_dict, part_ratio_dict):
    x = ratio_dict
    y = part_ratio_dict
    print(x, y)
    if y == {} :
        return x
    
    if x == {} :
        return y
    
    if (word in x) and (word in y):
        return {
            word  : x[word]
        }
    elif len(x) == 1 and len(y) == 1:
        return x
    else:
        common_words = [i for i in x if i in y]
        if len(common_words) == 0:
            return x
        d = {}
        for i in common_words:
            if len(i) <= 2:
                d[i] = y[i]
            else:
                d[i] = x[i]
        return d

# flask endpoints

@app.route("/",methods=["GET"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def home():
    return "hello server"

@app.route("/<word>")
@cross_origin(origin='*')
def search(word):
  if (word in rootwordsDict):
    return rootwordsDict[word]
  else:
    pystemer_output = stemmer.stemWord(word)
    pystemer_root = ""
    if pystemer_output == "":
        pystemer_root = stem(word)
    else:
        pystemer_root = pystemer_output
    word_split_output = fuzzymatch(word)
    #print(word_split_output)
    x,y = word_split_output[2], word_split_output[4]
    if fuzz.ratio(pystemer_output, word) >= 50:
        x[pystemer_output] = fuzz.ratio(pystemer_output, word)
    if fuzz.partial_ratio(pystemer_output, word) >= 75:
        y[pystemer_output] = fuzz.partial_ratio(pystemer_output, word)
    optimum = optimal(word, x, y)
    print(optimum)
    out_dict = {
        "word" : str(word),
        "pystemmer" : {pystemer_root : fuzz.ratio(pystemer_root,[word])},
        "word_split" : word_split_output[2],
        "optimum":  optimum  
    }
    
    if (out_dict["pystemmer"] == {} and out_dict["word_split"] == {}):
        out_dict["pystemmer"] = {
            word:100
        }
    if optimum == {}:
        out_dict["optimum"] = out_dict["pystemmer"]
    
    # max = 0 
    # maxKey = ""
    # for x in optimum.keys():
    #     if(optimum[x]>max):
    #         maxKey = x
    #         max = optimum[x]
    out_dict['result'] = out_dict['optimum'] 
    
    rootwordsDict[word] = jsonify(out_dict)
    pickleDumper(rootwordsDict)
    #print(out_dict)
    return jsonify(out_dict)

if __name__=='__main__':
    app.run()