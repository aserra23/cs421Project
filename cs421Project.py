import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import brown
from nltk.tokenize import sent_tokenize
from nltk.corpus import wordnet as wn
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
import os.path




def CountSentence(Essay_str):
    #break them into sentences
    sentences = sent_tokenize(Essay_str)

    #return total elements in sentences. TODO add this result to other chekcs
    return len(sentences)



def CountSpelling(Essay_str):
    Spelling_Count=0
    #Dict = set(wn.words())   # this one didn't have so many words: ex with, this, that... same as using wn.synset(). 
    Dict = set(brown.words())
    tokens = word_tokenize(Essay_str)
   # print("---", tokens)
    for word in tokens:
        check= word in Dict
        if check == False and word != "n't":
            Spelling_Count += 1
            print(word)

    return Spelling_Count




def Check_Sub_verb(Essay_str):
    sentences = sent_tokenize(Essay_str)
    Tag_List = []
    Word_List = []
    temp = []
    result = ""
    Tag_combine = []
    rule = []
    #print(sentences)
    #POS tag each sentence 1 by 1
    for sentence in sentences:
       tokens = word_tokenize(sentence)  # make each sentence into tokens 
       tagged_tokens = pos_tag(tokens)
       #print(tagged_tokens)
       #break word and tag into 2 lists (can't use dictionary because 'key' is not unique
       for W_T_pair in tagged_tokens:
           result += '[' + W_T_pair[0] + '/' + W_T_pair[1] + '] '
           Tag_List += [W_T_pair[1]]
           Word_List += [W_T_pair[0]]

       print(Tag_List)
       
"""
       result = ""
Tag_List=[]
word_list =[]
temp =[]
Tag_combine =[]
rule = [['PRP', 'CBZ'], ['NNS' , 'VBP']]
for token in tagged_tokens:
    result += '[' + token[0] + '/' + token[1] + '] '
    Tag_List += [token[1]]
    word_list += [token[0]]
    
print(result)
for i in range (0, len(Tag_List)-1):
    temp = [Tag_List[i]] + [Tag_List[i+1]]
    Tag_combine += [temp]
    #if temp in rule:        # this works to find the tag but need to set rule
        #print("\nkkkkkkkkkkkkkkkkkkkkkkkkk\n")
  
    
"""


def Main():
    #Number_Sentences=0
    # ask/read the input of the file name
    while True:
        filename = input("Please enter the file name or Q to quit:    ") 
    # open file and read them as a string  
        if filename== "Q" or filename =="q":
            break
    
        else:
            if os.path.isfile(filename) :
                file = open (filename, "r")
                print("open")
                text=file.read()         # read the whole essay into 1 string
                
                Number_Sentences = CountSentence(text)
                print("total sentencese:", Number_Sentences)

                Number_Spelling_Error = CountSpelling(text) 
                print("Total mispell: ", Number_Spelling_Error)

                Check_Sub_verb(text)


            else:
                print("invalid filename!")
        
        

#text=file.read()




Main()


print("\nThank you for using!\n")







"""
text = ("Pierre Vinken, 61 years old, will join the board as a nonexecutive director Nov. 29. " +
"Mr. Vinken is chairman of Elsevier N.V., the Dutch publishing group. " +
"Rudolph Agnew, 55 years old and former chairman of Consolidated Gold Fields PLC, " +
"was named a director of this British industrial conglomerate.")

tokens = word_tokenize(text)
result = ""
for token in tokens:
	result += "[" + token + "] "
print(result)
print("\n=========================1111============================\n")

## this counts number of sentences in the essay 
sentences = sent_tokenize(text)
print("No. of sentence", len(sentences))  
##  end find number sentence


result = ""
for sentence in sentences:
	result += "[" + sentence + "] "
print(result)
print("\n=========================22222============================\n")

"""
"""
tagged_tokens = pos_tag(tokens)
result = ""
for token in tagged_tokens:
	result += '[' + token[0] + '/' + token[1] + '] '
print(result)
print("\n========================3333=============================\n")


lemmatizer = WordNetLemmatizer()

result = ""
for token in tokens:
	result += '[' + lemmatizer.lemmatize(token) + '] '
print(result)
print("\n======================4444===============================\n")

tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary = False)

"""

"""
for sentence in chunked_sentences:
	str_sentence =' '.join(str(sentence).split())
	str_sentence = str_sentence.replace('(','[')
	str_sentence = str_sentence.replace(')',']')
	print(str_sentence)
print("\n======================5555===============================\n")

"""

"""

# ask/read the input of the file name
filename = input("Please enter the file name:    ") 
# open file and read them as a string  
file = open (filename, "r")
text=file.read()
#print(len(text))                                                       
tokens = word_tokenize(text)

print("Number of words: ", len(tokens))                                                 #this is good to count the words of essay
"""
"""
#count=0
#result = ""
for token in tokens:
    count+=1
    result += "[" + token + "]"
#print(result)
#print(count)
#print (len(result))
"""

"""
print("\n==========================================\n")
dictionary = set( brown.words())
mispell =0
for word in tokens:
    spell_check = word in dictionary
    if(spell_check == False):
            if(word != "n't"):
                mispell=mispell +1
                print(word)
print("Total spell error: ", mispell)

# Split tags into a list and words to another

tagged_tokens = pos_tag(tokens)
#print(tagged_tokens)
#print("type of tokens ", type(tagged_tokens))
result = ""
Tag_List=[]
word_list =[]
temp =[]
Tag_combine =[]
rule = [['PRP', 'CBZ'], ['NNS' , 'VBP']]
for token in tagged_tokens:
    result += '[' + token[0] + '/' + token[1] + '] '
    Tag_List += [token[1]]
    word_list += [token[0]]
    
print(result)
for i in range (0, len(Tag_List)-1):
    temp = [Tag_List[i]] + [Tag_List[i+1]]
    Tag_combine += [temp]
    #if temp in rule:        # this works to find the tag but need to set rule
        #print("\nkkkkkkkkkkkkkkkkkkkkkkkkk\n")
    
#g=[result]
#print("GGGGGGG ", Tag_combine)
print("\n========================333=============================\n")

"""