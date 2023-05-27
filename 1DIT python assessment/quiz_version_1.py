# Chemistry quiz Iteration 1

points = 0 # Establish points variable
questions_dict = {
    "What are the 3 states of matter?": ["solid", "liquid", "gas"],
    "What is the element which symbol is 'Na'?": ["sodium"],
    "What is the center of an atom called?": ["nucleus"]
    } # Dictionary to store questions and answers

# Loop through every question & answer pair
for num, question in enumerate(questions_dict):
    # Gets question index number and question from the questions dictionary
    print(f"\nQuestion {num+1}:\n{question}")

    answer = input("\nAnswer: ") # Ask for answer

    correct = True # Set correct variable to True by default

    # Check if every answer in the questions dictionary is present
    for correct_answers in questions_dict[question]:
        if correct_answers not in answer.lower(): # If there is an answer not present
            correct = False # Change the correct variable to False
            break # Stop the loop

    # Check if they answered correctly
    if correct:
        print("Well done!")
        points += 1 # Add a point
    else:
        # Print out correct answer if they were wrong
        print("Wrong answer! The answer was:", ', '.join(questions_dict[question]))

# Display score when completed
print("\nYour score is:", points,"/",len(questions_dict))
