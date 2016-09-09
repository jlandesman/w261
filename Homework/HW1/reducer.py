#!/usr/bin/python
import sys
import re
import string
new_dict = {}
totals = ["HAM Doc Count", "SPAM Doc Count","HAM Word Count","SPAM Word Count"] #Total fields

#For all countfiles from the mapper
for f in sys.argv[1:]:
    with open (f, "r") as myfile:
        for line in myfile:
            word,count = line.split(",",1) #Split the text into words and counts
            #Convert counts to integers
            try:
                count = int(count)
            except:
                count = 0
            if word in new_dict: new_dict[word] += count #If the word exists, add the count to the total
            else: new_dict[word] = count #If it's a new word, create a new entry

#Exclude Word and Doc totals.
findwords = []
for x in new_dict:
    if x not in totals:
        y = x.replace("HAM","").replace("SPAM","").strip()
        if y not in findwords: findwords.append(y)
            
           
#Naive bayes classification of emails using the variables derived above for a single, user-defined word
filename = 'enronemail_1h.txt'
PR_Y = float(new_dict['SPAM Doc Count'])/(new_dict['SPAM Doc Count']+new_dict['HAM Doc Count'])
counter = 0
spam_counter = 0
spam_pred_counter = 0
correct_pred=0

print new_dict
#Laplace smoothing coeffecient
alpha = 1
n=len(findwords)
with open (filename, "r") as myfile:
    #For each email in the file
    for line in myfile:
        #Reset probabilities
        PR_X_Y = 1
        PR_X = 1
    
        spam_flag =  line.split("\t")[1] #Classify as Spam or Ham
        text = line.split("\t")[2] + line.split("\t")[3] #Uses only the subject and body of the email
        print line
        for word in findwords:
            if len(word)<=1: continue
            elif word in line:
                word = word.strip(string.punctuation).rstrip().lower() #Remove punctuation and set to lowercase
                try:
                    spam_wc = new_dict['SPAM '+word]
                except:
                    spam_wc = 0
                try:
                    ham_wc = new_dict['HAM '+word]
                except:
                    ham_wc = 0
                
                if (ham_wc+spam_wc)==0: continue
                #Estimate P(X|Y), which is the product of P(X|Y) for each word (in this case only one)
                PR_X_Y = PR_X_Y * float(spam_wc+alpha)/(new_dict['SPAM Word Count']+alpha*n)
                #Estimate P(X), which is the product of P(X) for each word (in this case only one)
                #PR_X = PR_X *float(spam_wc+ham_wc)/(new_dict['SPAM Word Count']+new_dict['HAM Word Count'])
                PR_X = PR_X *float(spam_wc+ham_wc)/(new_dict['SPAM Word Count']+new_dict['HAM Word Count'])
                print word + " " + str(ham_wc+spam_wc) + " " + str(PR_X)
                
        #P(Y|X) for the email
        PR_Y_X = PR_Y * PR_X_Y / PR_X
        #Make a prediction
        if PR_Y_X > 0.5: spam_pred = '1'
        else: spam_pred = '0'
        
        if spam_pred == '1': spam_pred_counter+=1
        if spam_flag == '1': spam_counter+=1            
        if spam_pred==spam_flag: correct_pred += 1
        counter +=1
       
    #Print summary details to output file
print ""
print "Number of emails: %i" %(counter)
print "Number of spam emails: %i" %(spam_counter)
print "Number of emails predicted as spam: %i" %(spam_pred_counter)
print "Number of emails correctly predicted: %i" %(correct_pred)
print "Accuracy: %f" %(float(correct_pred)/counter)