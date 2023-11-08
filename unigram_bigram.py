"""
Date created: 11/5/2023
Author: Trevor Hitchcock
Description: This program reads in a file and displays unigrams and bigrams for it
"""
import re

# this method removes special characters, changes all numbers to <\n>, replaces punctuation with <\p>
#     and lowercases string
# method is called after loading in text file and when the user inputs a string
def text_processing(text):
    # extra lines for readability
    
    # removes characters besides alphabet, numbers, space, and break
    no_spec = re.sub(r'[^A-Za-z0-9.!? \n]', '', text)
    
    # replace numbers
    no_nums = re.sub(r'\d+', ' </n>', no_spec)
    
    # replace puncuation
    no_punc_or_nums = re.sub(r'[!?\.]', ' </p>', no_nums)
    
    # lowercase
    no_spec_lower = no_punc_or_nums.lower()
    
    return no_spec_lower

# this method loads in a file at the start of the program
# it is also able to be called again to load a different file
def load_file():
    txt = input("Enter the name of the file you'd like to read from: ")
    
    with open(txt, "r", encoding="utf-8", errors="ignore") as file:
        str_words = file.read()
    
    post_processing = text_processing(str_words)
    # split into array to easily put into dictionary
    words_list = post_processing.split()

    # fills unigram dictionary. key is word, value is amount
    unigram_count = {}
    for word in words_list:
        if word not in unigram_count:
            unigram_count[word] = 1
        else:
            unigram_count[word] += 1
    print("Unigrams created successfully")
    
    # fills bigram dictionary. key is bigram, value is amount
    bigram_count = {}
    for i in range(len(words_list)-1):
        bigram = words_list[i] + " " + words_list[i+1]
        if bigram not in bigram_count:
            bigram_count[bigram] = 1
        else:
            bigram_count[bigram] += 1
    print("Bigrams created successfully")

    return unigram_count, bigram_count

# this method shows the count of every unigram
# and every bigram that it appears in
def unigram(unigram_count, bigram_count):
    user_word = input("\nWhich unigram would you like to search for: ").lower()
    
    word = text_processing(user_word)
    
    print("\nThe unigram '"+ word +"' appears",unigram_count[word],"times.\n")
    
    print(word.capitalize(),"at the begining:") # capitalize for printing
    for key,_ in bigram_count.items():
        if word == key.split()[0]: # 0 first index
            print(key)
    
    print("\n" + word.capitalize(),"at the end:") # capitalize for printing
    for key,_ in bigram_count.items():
        if word == key.split()[1]: # 1 second indiex
            print(key)

# this method shows the probability of a user entered bigram
def bigram(unigram_count, bigram_count):
    user_bigram = input("\nWhich bigram would you like to search for: ").lower()
    
    bigram = text_processing(user_bigram)
    
    try:
        print("\nThe bigram '"+ bigram +"' appears",bigram_count[bigram],"times.\n")
        bi_count = bigram_count[bigram]
        second = bigram.split()
        second =" ".join(second[1:]) # grabs the second word
        second_count = unigram_count[second] # grabs count
        print("The probability of '"+bigram+"' is " + str(round(bi_count/second_count,10)))
        
    except KeyError:
        print("Bigram not found")

# this method shows the probability of a user entered sentence
def sentence_probability(unigram_count, bigram_count):
    sentence = input("Enter a sentence to check the probability of: ")
    
    # lowercase because dictionary is lowercase
    processed_sentence = text_processing(sentence)
    
    # create bigrams of inputted sentence
    sentence_arr = processed_sentence.split()
    
    if(len(sentence_arr) > 6):
        print("Sentence must be 6 unigrams or less")
        return # exits functions
    
    # creates dictionary of bigrams of user inputted sentence
    sentence_count = {}
    for i in range(len(sentence_arr)-1):
        bigram = sentence_arr[i] + " " + sentence_arr[i+1]
        if bigram not in sentence_count:
            sentence_count[bigram] = 1
        else:
            sentence_count[bigram] += 1
    
    # multiplies user inputted bigrams 
    total_prob = 1
    for bigram,count in sentence_count.items():
        if bigram in bigram_count:
            second = bigram.split()
            second =" ".join(second[1:]) # grabs the second word
            second_count = unigram_count[second] # grabs count
            total_prob *= bigram_count.get(bigram)/second_count
        else: # bigram not found in file, probability = 0
            total_prob = 0
            break
    print("The probability of the sentence '"+str(sentence)+"' appearing is "+str(total_prob))
    
def main():
    
    unigram_count,bigram_count = load_file()
    choice = "init"
    
    while choice == "init" or choice != 5 :
        print("\nWelcome to unigram/bigram reader!")
        print("1. Search for unigram")
        print("2. Search for bigram")
        print("3. Sentence probability")
        print("4. Load a new file")
        print("5. Exit")
        
        try:
            choice = int(input("Pick an option: "))
            
            if choice == 1:
                unigram(unigram_count, bigram_count)
            elif choice == 2:
                bigram(unigram_count, bigram_count)
            elif choice == 3:
                sentence_probability(unigram_count,bigram_count)
            elif choice == 4:
                unigram_count,bigram_count = load_file()
            elif choice == 5:
                print("Exiting file...")
        except ValueError:
            print("Enter a valid input")

if __name__ == "__main__":
    main()