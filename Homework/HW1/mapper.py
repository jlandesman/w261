#!/usr/bin/python
import sys
import re
import string
filename = sys.argv[1] #Takes a data chunk as an input
findwords = sys.argv[2].lower() #List of words (in this case, a single word)
new_dict = {}
word_count = 0
doc_count = 0

#Searches each email (line) in the file for the user-specified word
with open (filename, "r") as myfile:
    for line in myfile:
        #Creates a text field for SPAM/HAM from the binary field
        if line.split("\t")[1] == '1': spam_flag = "SPAM"
        else: spam_flag = "HAM"
            
        text = line.split("\t")[2] + line.split("\t")[3] #Uses only the subject and body of the email
        for word in text.split(" "):
            word = word.strip(string.punctuation).rstrip().lower() #Remove punctuation and set to lowercase
            if word in new_dict: new_dict[word] += 1 #If the word exists, add the count to the total
            else: new_dict[word] = 1 #If it's a new word, create a new entry
            word_count+=1 #Running count of words
        doc_count+=1 #Running count of documents
        
for i in new_dict:  
    print spam_flag + " " + i + ", " + str(new_dict[i]) #Word and count
print spam_flag + " Word Count, " + str(word_count)  #Total word count for the file
print spam_flag + " Doc Count, " + str(doc_count) #Total doc count for the file