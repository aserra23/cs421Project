from Grader import EssayGrader
import os.path
import os
import nltk

# this is placed here so it won't be called multiple times from the Grader module when looping
#nltk.download()

nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('treebank')

if __name__ == '__main__':

    # read all the files names as string store in list
    All_files = os.listdir("../input/testing/essays")

    All_files.sort()

    # open output file
    file_writer = open("../output/result.txt", 'w')

    # iterate through all essays in testing folder
    for file in All_files:
        filepath = "../input/testing/essays/"+file

        # open file and read them as a string
        if os.path.isfile(filepath):

            essayGrader = EssayGrader(filepath, file, file_writer)
            essayGrader.prepare_data()
            essayGrader.determine_sub_and_final_scores()
            essayGrader.determine_classifier()
            essayGrader.write()
            #print(file)
        else:
            print("invalid filename!")
    file_writer.close()
    print('done')
