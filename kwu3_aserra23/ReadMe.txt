Project 1 for CS421 – University of Illinois at Chicago
Name 1: kwu3@uic.edu
Name 2: aserra23@uic.edu

--------------------------------Setup--------------------------------
In the execution folder, give the following command on your command prompt terminal (Linux):
yourComputerName$ ./run.sh

Alternatively, you can give the following command (in either Windows or Linux):
Please install required libraries using the following commands:
pip3 install nltk
pip3 install numpy

Navigate to the execution folder, give the following command on your command prompt(on linux systems you need to include the ./):
python3 ./cs421Project.py


				*** 
A Window will pop up to ask which files to install and just select on All packages->Download and then exit window from NLTK Downloader 
				***

------------------------------Technique------------------------------
Break the string into sentences. use nltk to get tags on each word and split the sentences into a word list and a tag list. Use the brown corpus to do spelling check on all words. Use the tag list to perform the other parts of grading. Make combinations of the verb-verb tags and subject-verb tags.  If there is no verb in a sentence, it missed a verb. If the verbs tag combo is on the list created for improper combinations then, it is a mistake. Also, if the pronoun, proper noun and/or noun to verb singular/plural rule do not match then, it is mistake.  Also, the number of words and verbs of the essay are considered too because the less of those, the less chance to make mistake. On the other hand, the ratio of a mistake is higher if there is less word.
