# Chemistry quiz Iteration 2

import random # For random.shuffle()

points = 0 # Establish points variable
QUESTION_AMOUNT = 10 # Set how many questions to be asked

# Obtain an amount of question from a set of even more questions from dictionary from external file
questions_dict = dict(random.sample(sorted(eval(open("questions.txt").read()).items()), QUESTION_AMOUNT))

print(f"Hello! Welcome to chemistry quiz!\nThere are {QUESTION_AMOUNT} multiple choice questions.\nGood luck!\n")# Greet user

for num, question_answer_pair in enumerate(questions_dict.items()): # Loop through every question & answers pair
    question, answers = question_answer_pair # Assign question string and answer list
    print(f"\nQuestion {num+1}:\n{question}") # Display question number and question
    correct_answer = answers[0] # Stores correct answer (the external dict has correct answer in index 0)
    random.shuffle(answers) # Shuffles the answers so the correct answer is in a random spot
    correct_answer_index = answers.index(correct_answer) # Gets the index of the correct answer after shuffle
    print(f"\na. {answers[0]}\nb. {answers[1]}\nc. {answers[2]}\nd. {answers[3]}") # Prints the multiple choice

    # Loop until user answers correctly (a, b, c or d)
    while True: 
        answer = input("\nAnswer: ").lower() # Ask for answer
        if answer in ['a', 'b', 'c', 'd']: # Check if they answered correctly
            break # Break out of the loop
        else: # Print out that answer was invalid
            print("Invalid Input! Reply must be a, b, c or d")

    # Check if answer is correct
    if answer == ['a', 'b', 'c', 'd'][correct_answer_index]:
        print("Well done!")
        points += 1 # Add a point
    else: # Print out correct answer if they were wrong
        print("Wrong answer! The answer was:", ['a', 'b', 'c', 'd'][correct_answer_index]+".",correct_answer)

# Display score when completed
print("\nYour score is:", points,"/",len(questions_dict))

