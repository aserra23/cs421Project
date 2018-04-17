import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import brown
from nltk.tokenize import sent_tokenize
from nltk.corpus import wordnet as wn
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
import os.path
import os
#from nltk.corpus import treebank




rules = {"NP VP": "S", "V PN": "VP", 'Det Nominal': 'NP',   'Nominal PP' : 'Nominal' , 'Adj Nominal' : 'Nominal', 'Prep NP' : 'PP'     }
terminal = {'NN' : 'NP', 'PN' : "NP" } # this will not work if there are 2 same keys


verb_tags = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"] # all the verb tages
subject_tags_P = ['NNS', 'NNPS']
subject_tags_S = ['NN', 'NNP']
PRP_words = ['you', 'You', 'we', 'We', 'they', 'They', 'I', 'i']

wrong_verb_combo =['TO VBD', 'TO VBG', 'TO VBN', 'TO VBZ', 'MD VBD', 'MD VBG', 'MD VBN', 'MD VBZ', 'VBZ VB', 'VBZ VBD', 'VBZ VBP', 'VBZ VBZ', 'VBP VB', 'VBP VBD', 'VBP VBP', 'VBP VBZ'] 
               
wrong_sub_v_combo = ['NN VB', 'NN VBP', 'NNS VBZ', 'NNP VB', 'NNP VBP', 'NNPS VBZ','PRPP VBZ', 'PRPS VB', 'PRPS VBP']


#text = ("I had killed the tiger.")

#tokens = word_tokenize(text)
#tagged_tokens = pos_tag(tokens)

#print(tagged_tokens)


def CKY(Tag_List):
    #set up table
    word =[]
    word = word+Tag_List # add an empty string to shift the list to fit the CKY codes
    table = []
    temp=""
    for x in range (0, len(word)):
        table.append([])
        for y in range(0, len(word)):
            table[x].append([])

    # filling CKY table
    for j in range (1,len(word)):
        table[j-1][j].append(word[j]) # fill with the Tag 
        for t in terminal.keys():      #check if the tag is a terminal of others, fill in if so. 
            if t == word[j]:
                table[j-1][j].append(terminal[t])

        i=j-1 
        while i>=0:
            for k in range(i+1, j):   # use j means last one k <= j-1
                for x in table[i][k]:
                    for y in table[k][j]:                           
                        temp = x + " " + y
                        if temp in rules:
                            table[i][j].append(rules[temp])
                        temp = ""  # rest temp for next rule check

            i=i-1   # decrease i by 1 for next cell
                    
    return table         # sent back the filled table


#function to count total verbs from a Tag_List
def CountVerbs(Tag_List):
    total_verb =0
    for t in Tag_List:
        if t in verb_tags:
            total_verb+=1
    return total_verb



# function to check if there is any spelling error
def CountSpelling(Essay_str):
    Spelling_Count=0
    word_count=0

    #Dict = set(wn.words())   # this one didn't have so many words: ex with, this, that... same as using wn.synset(). 
    Dict = set(brown.words())
    tokens = word_tokenize(Essay_str)
   # print("---", tokens)
    for word in tokens:
        word_count+=1
        check= word in Dict
        if check == False and word != "n't":
            Spelling_Count += 1
            #print(word)                       # print the mispelled word -- TODO can delete later

    return int(word_count/(Spelling_Count+0.0001))



#function to check if the subject and verb are matching (singular/plural)
def check_sub_verb(Tag_List, Word_List):
    count = 0
    i=0
    #sub_que = []
    temp=""

    for i in range(0, len(Tag_List)-1):
        if Tag_List[i] == "PRP": 
            if Word_List[i] in PRP_words:
                temp = "PRPP" + " " + Tag_List[i+1]
            else:
                temp = "PRPS" + " " + Tag_List[i+1]
        else:
            temp = Tag_List[i] + " "+ Tag_List[i+1]
        
        if temp in wrong_sub_v_combo:
            count = count+1
            #print("WWWWWwrong tag: ",temp, "words are: ", Word_List[i], Word_List[i+1])
    #print("count of wrong sub verb: ", count)
    return count





# function to check if the sentece has at least 1 verb
def Check_Missing_Verb(Tag_List):
    C_V=0
    for t in Tag_List:
        if t in verb_tags:
            C_V +=1
    if C_V ==0:
        return 1
    else:
        return 0

#function to check if there are any wrong combo verbs  
def Check_Wrong_Combo(Tag_List, sen):
    count=0
    for i in range(0, len(Tag_List)-1):
        temp = Tag_List[i] + " "+ Tag_List[i+1]
        if temp in wrong_verb_combo:
            count = count+1
            #print("wrong tag: ",temp,"wrong sent: ", sen)
    return count



#function breaking essay into sentences and spli each sentence into word and tags 
def Check_Sub_verb(Essay_str, filename, fw):
    sentences = sent_tokenize(Essay_str)
    #print("total word: ",len(Essay_str))
    Tag_List = []
    Word_List = []
    temp = ""
    result = ""
    Tag_combine = []
    rule = []
    count_verb = 0
    count_word=0
    wrong_combo =0
    missing_V =0
    Sub_verb_match =0
    #print(sentences)
    #POS tag each sentence 1 by 1
    for sentence in sentences:
       tokens = word_tokenize(sentence)  # make each sentence into tokens 
       tagged_tokens = pos_tag(tokens)
       #print(tagged_tokens)
       #break word and tag into 2 lists (can't use dictionary because 'key' is not unique
       for W_T_pair in tagged_tokens:
          # result += '[' + W_T_pair[0] + '/' + W_T_pair[1] + '] '
           Tag_List += [W_T_pair[1]]                          # This will put the whole essay tags into 1 list. LOST the purpose to do sentence 1 by 1
           Word_List += [W_T_pair[0]]
          
          # TODO: should do something for this sentece before he end of this loop then reset all those 3 for next sentence
      
       count_verb = count_verb + CountVerbs(Tag_List)  # count the total verb we have in 1 essay
       count_word += len(Tag_List)
       
       Sub_verb_match += check_sub_verb(Tag_List, Word_List) #count the total subject verb mismatch in 1 essay
     
       
       missing_V = missing_V + Check_Missing_Verb(Tag_List)  # count sentences that has no verb
      
       
       wrong_combo = wrong_combo + Check_Wrong_Combo(Tag_List, sentence) # wrong tense, wrong combo verbs 





       CKY_Table = CKY(Tag_List) # TODO change it back to pass Tag_list

       #for tb in CKY_Table:
        #   print(tb)

   
       Tag_List=[]       # reset tag for next sentence
       Word_List=[]      # reset word for next sentence
    
    # useing average 3 verbs per sentence
    #print(count_verb/3) 
    Essay_Len = int(((count_verb/3) + len(sentences)))/2
    # TOCheck later assign score 1 to 5 for essay length:  11- = 1, 12-14 = 2, 15-17=3, 17-20 = 4, 20+ = 5 ?
    if Essay_Len <=11:
        Essay_Len_score = 1
    elif Essay_Len <=14:
        Essay_Len_score =2
    elif Essay_Len <=16:
        Essay_Len_score = 3
    elif Essay_Len <= 18:
        Essay_Len_score =4
    else:
        Essay_Len_score=5





    Spelling = CountSpelling(Essay_str)
    
    # TODO set score for spelling 0-4. 10- =4, 11-20 = 3, 21-30=2, 31-40=1, 41+ =0 
    if Spelling >=30:
        Spelling_reduce = 0
    elif Spelling >=24:
        Spelling_reduce =1
    elif Spelling >= 20:
        Spelling_reduce = 2
    elif Spelling >= 16:
        Spelling_reduce =3
    else:
        Spelling_reduce =4

    

    
    verb_per_mismatch =  count_verb / (Sub_verb_match+0.0001)

    #TODO: set score by verb per mismatch ratio. low = 25.2 high = 42.7,  16- = 1, 17-26 =2, 27-35 = 3, 36-44=4, 45+ = 5
    if verb_per_mismatch <=16:
        Sub_Verb_score = 1
    elif verb_per_mismatch <=26:
        Sub_Verb_score = 2
    elif verb_per_mismatch <=35:
        Sub_Verb_score = 3
    elif verb_per_mismatch <= 44:
        Sub_Verb_score = 4
    else:
        Sub_Verb_score = 5

    
        
    #TODO count the wrong verb combo and need to assign the scores 14- = 1, 15-50 =2, 51-85=3 86-110=4, 110+=5
    Missing_verb = missing_V + wrong_combo
    if(Missing_verb==0):
        Missing_verb_Ratio = 1000
    else:
        Missing_verb_Ratio = count_verb/Missing_verb


    if Missing_verb_Ratio <=14:
        Missing_Verb_score = 1
    elif Missing_verb_Ratio <=50:
        Missing_Verb_score = 2
    elif Missing_verb_Ratio <=85:
        Missing_Verb_score = 3
    elif Missing_verb_Ratio <= 110:
        Missing_Verb_score = 4
    else:
        Missing_Verb_score = 5
    


    Sub_Verb_score = Sub_Verb_score* (count_word / 280)*(count_verb/45)
	


    Missing_Verb_score= Missing_Verb_score* (count_word/280)* (count_verb/45)
    

    if Sub_Verb_score >5:
        Sub_Verb_score =5

    if Missing_Verb_score >5:
        Missing_Verb_score =5
  
    #print("missing verb ration: ", count_verb, Missing_verb_Ratio)

    #print("Ratio: ", verb_per_mismatch)


    #print("This essay has ", Sub_verb_match, "mismatch")
    #print("Essay length: ", Essay_Len, "score =", Essay_Len_score)

    print("total verb compare: ",count_verb, "  ", count_word )
    #print("words per spelling mistake: ", Spelling, "Spelling error reduce= ", Spelling_reduce)

    

    #print("total missing verb: ", missing_V)  # good to check if there is no verb at all in a sentence
    #print("Wrong Combo verb: ", wrong_combo) 

    

   # Final_Score = 2* len(easy) - (spelling) + sbu-verb aggreement(singular/plural) + verb tense/missingverb/extraverb  
       #print(Tag_List)
    Final_Score = 2* Essay_Len_score - Spelling_reduce + int(Sub_Verb_score)  + int(Missing_Verb_score)  # + Sent_form_score + Semantic_score 
    if Essay_Len <10:
        Essay_grade = "LOW"
    elif Final_Score >=12:
        Essay_grade ="HIGH"
    else:
        Essay_grade = "LOW"
      
    
    #write to output folder result.txt
    
    fw.write(filename+"; "+str(Essay_Len_score)+"; "+str(Spelling_reduce)+"; "+str(int(Sub_Verb_score))+"; "+str(int(Missing_Verb_score))+"; 0; 0; 0; "+str(Final_Score)+"; Unknown\n" )
    
    

    #fw.write(str(Essay_Len_score)+"; " )
    
    
    print("Final score is: ", Final_Score)
    print("This essay is graded: ", Essay_grade)

def Main():
    
    #read all teh files names as string store in list
    All_files = os.listdir("../input/testing")	
	
    file_write = open("../output/result.txt", 'w')
        


    #Number_Sentences=0
    # ask/read the input of the file name
   

    for f in All_files:
        filename = "../input/testing/"+f
    # open file and read them as a string  
        if os.path.isfile(filename) :
           file = open (filename, "r")
           #print("open")
           text=file.read()         # read the whole essay into 1 string
               
           Check_Sub_verb(text, f, file_write)


        else:
           print("invalid filename!")
        
    file.close
    file_write.close

Main()


print("\nThank you for using!\n")




