import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import brown
from nltk.tokenize import sent_tokenize
from nltk.corpus import wordnet as wn
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
import os.path
import os



# this line reads all this files in folder 'High' and put them 
# in list
allfiles = os.listdir("../input/training")
for af in allfiles:	
	print(af)





# these lines open a folder to write to 
f=open("../output/result.txt", 'w')
f.write(allfiles[0]) #Can only write string.
f.write(allfiles[1]) 
f.close()


