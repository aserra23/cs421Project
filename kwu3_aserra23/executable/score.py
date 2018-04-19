
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
allfiles = os.listdir("input\training")
print(allfiles)

# these lines open a folder to write to 
f=open("output\result.txt", 'w')
f.write(allfiles[0]) #Can only write string.
f.close()



'''
# this is how to create a report.txt in folder
f = open('report.txt', 'w')

#this is how to open the folder in the same directory and read #all this file names in it
for file_Names in os.listdir(os.getcwd()):
	
	#this is how to write the stuff in the file we opened
	f.write(file_Names)
	f.write('\n') # to new line

#close the file, here report.txt once we finish all.
#Note, don't close it b4 end or the next open/write will delete #the old work.

f.close()

'''



'''



verb=['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
PRP_words = ['you', 'You', 'we', 'We', 'they', 'They', 'I', 'i']
wrong_verb_combo =['TO VBD', 'TO VBG', 'TO VBN', 'TO VBZ', 'MD VBD', 'MD VBG', 'MD VBN', 'MD VBZ', 'VBZ VB', 'VBZ VBD', 'VBZ VBP', 'VBZ VBZ', 'VBP VB', 'VBP VBD', 'VBP VBP', 'VBP VBZ'] 
wrong_sub_v_combo=['NN VB', 'NN VBP', 'NNS VBZ', 'NNP VB', 'NNP VBP', 'NNPS VBZ','PRPP VBZ', 'PRPS VB', 'PRPS VBP']

Dict = set(brown.words())

s_count=0
ct=0
cv=0
cm=0
tw=0
ft =""
tag = []
wd=[]
mismatch =0 
total_combo_c=0
total_mis_v =0
total_essay_score =0

def sv(Tag_List, Word_List):
	count =0
	i=0
	temp = ""
	for i in range (0, len(Tag_List)-1):
		
		if Tag_List[i] == "PRP":
			if Word_List[i] in PRP_words:
				temp = "PRPP" + " " + Tag_List[i+1]
			else:
				temp = "PRPS" + " " + Tag_List[i+1]
		else:
			temp = Tag_List[i] + " " + Tag_List[i+1]
		
		if temp in wrong_sub_v_combo:
			count +=1
			print("Sub verb mismatch: ",temp, Tag_List[i], Tag_List[i+1], Word_List[i], Word_List[i+1])
	return count




def wrong_combo(Tag_List):
	count=0
	for i in range(0, len(Tag_List)-1):
		temp = Tag_List[i] + " " + Tag_List[i+1]
		if temp in wrong_verb_combo:
			count+=1


	return count



def count_missing(Tag_List):
	count=0
	for t in Tag_List:
		if t in verb:
			count+=1
	if count == 0:
		return 1
	else:
		return 0	



for x in range(1, 51):
	one_essay_verb =0
	misP = 0
	word_count =0
	sen_mis =0
	combo_c=0
	mis_v=0

	ft ="H" + str(x)+ ".txt"
	ct+=1
	print("\n\n          File Name: ", ft)
	
	E_file = open(ft,"r")
	text = E_file.read()
	
	sentences = sent_tokenize(text) # sentence list of essay
	print("length of sentence: ",len(sentences))
	s_count += len(sentences)
	
	for s in sentences:              # s is 1 sent in an essay
		tokens = word_tokenize(s)
		tagged_tokens = pos_tag(tokens)
		for W_T_pair in tagged_tokens:
			tag += [W_T_pair[1]]
			wd  += [W_T_pair[0]]
		for tg in tag:
			word_count +=1
			if tg in verb:
				cv+=1
				one_essay_verb +=1
				
		
		
		for w in wd:
			tw += 1
			check = w in Dict
			if check == False and w != "n't":
				misP += 1
				cm+=1
		
		sen_mis += sv(tag, wd)
		
		combo_c += wrong_combo(tag)
		mis_v += count_missing(tag)
		
		tag=[]
		wd=[]	  

		
		
	total_combo_c += combo_c
	mismatch += sen_mis
	total_mis_v += mis_v
	ft=""  # reset for nest file name
	
	print("Total Verb In an Essay: ", one_essay_verb)
	print ("missing verb in essay: ", mis_v)
	print("Sent in 1 essay by verbs: ", one_essay_verb/3)
	print ("total spelling error: ", misP)
	print ("total word in 1 essay: ", word_count) 
	print("word per mispell: ", word_count/misP)
	print("each sent mismatch: ", sen_mis, "total: ", mismatch)
	
	print("wrong combo this essay: ", combo_c)

	
	Essay_Len = (one_essay_verb/3 + len(sentences))/2
	if Essay_Len <=11:
        	Essay_Len_score = 1
	elif Essay_Len <=14:
		Essay_Len_score =2
	elif Essay_Len <= 16:
		Essay_Len_score =3
	elif Essay_Len <= 18:
		Essay_Len_score =4
	else:
		Essay_Len_score = 5
    	    	
	print("Len score: ", Essay_Len_score)

	
	misp_ratio = word_count /(misP+0.0001)
	if misp_ratio >= 30:
		spelling = 0
	elif misp_ratio >= 24:
		spelling = 1
	elif misp_ratio >= 20:
		spelling = 2
	elif misp_ratio >= 16:
		spelling = 3
	else:
		spelling = 4
	
	print ("spelling reduce: ", spelling)



	sv_ratio = one_essay_verb / (sen_mis +0.0001)
	
	if sv_ratio <=16:
		sv_score =1
	elif sv_ratio <= 26:
		sv_score = 2
	elif sv_ratio <=35:
		sv_score = 3
	elif sv_ratio <=44:
		sv_score = 4
	else:
		sv_score = 5

	print("word to mis_sv: ", word_count/(sen_mis+0.0001))
	print("sub verb score: ", sv_score)

	wv_ratio = one_essay_verb / (mis_v + combo_c +0.00001)

	
	if wv_ratio <=14:
		wv_score = 1
	elif wv_ratio <= 50:
		wv_score = 2
	elif wv_ratio <= 85:
		wv_score = 3
	elif wv_ratio <= 110:
		wv_score = 4
	else:
		wv_score = 5
	
	print("missing verb score:", wv_score)

	missing_score = wv_score *(one_essay_verb/45)*(word_count/280)
	if missing_score >5:
		missing_score=5

	sv_mismatch_score = sv_score *(one_essay_verb/45)*(word_count/280)
	if sv_mismatch_score >5:
		sv_mismatch_score =5
	
	print("Essay_len= ", 2*Essay_Len_score, "spelling= ", spelling, "sv = ", sv_mismatch_score, "missing_score", missing_score)
	essay_score = 2*Essay_Len_score -spelling + int(sv_mismatch_score) + int(missing_score)
	
	total_essay_score += essay_score
	print("FFFFFFFFFFFFFFFFFF  THIS ESSAY SCORED: ", essay_score)
	
	if Essay_Len <10:
		grade = "LOW"
	elif essay_score >=12:
		grade = "High"
	else:
		grade = "LOW"
	print("GGGGGGGGGGGrade of this essay: ", grade)

print("WWWWWWWWWWWWWWWWWWWWW  all 50 score: ", total_essay_score)
print("AAAAAAAAAAAAAAAAvg score: ", total_essay_score/50)
print("Toatl missing verb: ", total_mis_v)
print ("Total wrong combo: ", total_combo_c)
print ("S/V mismatch: ", mismatch)
print("total sentense =  ", s_count)
print ("File sampled = ", ct)
print ("avg sentense: ", s_count/ct)
print ("total verb: " , cv)
print ("Verb per sentense: ", cv/s_count)
print ("3 verbs per sentence, there are: ", cv/150, " sentence")
print("Total spelling error: ", cm, "with avg: ", cm/50)
print("Avg word per mispell: ", tw/cm)  
print("total word of all 50 essay= ", tw)


# conclude: High = 1011 total sentense with avg = 20.22
#High 3374 verbs with 3.337 verbs per sentense
#if 3 verb/sent, high has avg 22.5 sent per essay
#if 2.5 , 27 sent/essay
# 1 mispell in 35.4 words
# total s/v mismatch is 79 with avg 79/50 verb/mismatch: 42.7
#sent:mis: 1068/79 = 13.5
#26 total wrong combo
#



#conclude: Low = 435 sentences with avg 8.7, 
#Low: 1689 verbs avg 3.882 verbs per sentence

#if 3 verbs/ sentense, low has avg 11.3 sentences per essay
#if 2.5 it will be 13.5
# there is 1 mispell in every 11.2 words
# total s/v mismatch is 67 with avg 67/50 V/Mis: 25.2
#sent/mis: 499/67=7,45
#total wrong combo 45
#total score = 250 with current seting( with negective score)
#avg = 5 points

'''

'''
s_count=0
for f in file_name_tokens:
	E_file = open (f, "r")
	sentences = sent_tokenize(E_file)
	s_count += len(sentences)
print("total sentense =  ", s_count)
'''

