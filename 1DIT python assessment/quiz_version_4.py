# Import modules
import pygame, sys, random
from pygame.locals import *

# Constants
QUESTION_AMOUNT = 10
WINDOWWIDTH = 1200
WINDOWHEIGHT = 600
BUTTONWIDTH = 400
BUTTONHEIGHT = 50
BUTTONSPACING = 75
SUBJECT = "Chemistry"

# Colours           R    G    B
BGCOLOUR        = ( 31,  48,  71)  # Navy
BOXCOLOUR       = ( 90,  90,  90)  # Gray
TEXTCOLOUR      = (255, 255, 255)  # White
HIGHLIGHTCOLOUR = (  0, 153, 153)  # Teal
WRONGCOLOUR     = (255,  51,  51)  # Red
CORRECTCOLOUR   = (102, 204,   0)  # Green

# Initialize pygame
pygame.init()
pygame.display.set_caption(f'{SUBJECT.capitalize()} Quiz')
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

# Load fonts
HEADER = pygame.font.Font("quicksand.ttf", 45)
SUBHEADER = pygame.font.Font("quicksand.ttf", 35)
QUESTION = pygame.font.Font("quicksand.ttf", 30)
BODY_TEXT = pygame.font.Font("quicksand.ttf", 25)

# Load background image
background_image = pygame.transform.scale(pygame.image.load("background.jpg").convert_alpha(), (WINDOWWIDTH, WINDOWHEIGHT))
transparent = darken = 128
background_image.fill((darken, darken, darken, transparent), special_flags=pygame.BLEND_RGBA_MULT) 

# Dictionary of what questions are given at your level
questions_filter = { # Make sure all the numbers in each list add up to the QUESTION_AMOUNT!
# difc: 1, 2, 3, 4, 5, 6
    0: [2, 2, 2, 2, 2, 0],
    1: [7, 2, 1, 0, 0, 0],
    2: [2, 5, 2, 1, 0, 0],
    3: [0, 2, 5, 2, 1, 0],
    4: [0, 0, 2, 6, 2, 0],
    5: [0, 0, 0, 2, 7, 1],
    6: [0, 0, 0, 1, 5, 4]
    }

# Main function
def main():
    # Load questions from external file
    all_questions = eval(open("questions.txt").read())
    level, progress = 0, 0
    
    while True: # Quiz loop
        DISPLAYSURF.fill(BGCOLOUR)
        DISPLAYSURF.blit(background_image, (0, 0))

        # Check for level up
        if progress >= 100 and level != 6:
            progress -= 100
            level += 1

        displayText(WINDOWWIDTH / 2, WINDOWHEIGHT * 0.1, f"{SUBJECT.upper()} QUIZ", HEADER) # Display title
        displayText(175, WINDOWHEIGHT * 0.1, f"Level: {level}", SUBHEADER) # Display level

        if level == 0: # Beginning test to check their skill
            displayText(175, WINDOWHEIGHT * 0.175, f"Initialising level...", BODY_TEXT)
        elif level == 6:
            displayText(175, WINDOWHEIGHT * 0.175, f"MAX LEVEL", BODY_TEXT) # Tell them they are at the maximum level
        else:
            displayText(175, WINDOWHEIGHT * 0.175, f"{progress}% to next level", BODY_TEXT) # Display how much progress to level up
    
        # Display instructions for the quiz
        displayText(WINDOWWIDTH / 2, WINDOWHEIGHT * 0.25, "Instructions:", SUBHEADER) 
        displayText(WINDOWWIDTH / 2, WINDOWHEIGHT * 0.3, "_______________________", BODY_TEXT)
        displayText(WINDOWWIDTH / 2, WINDOWHEIGHT * 0.43, f"- You will be asked {QUESTION_AMOUNT} multiple", BODY_TEXT)
        displayText(WINDOWWIDTH / 2, WINDOWHEIGHT * 0.47, f"choice {SUBJECT.lower()} questions.", BODY_TEXT)
        displayText(WINDOWWIDTH / 2, WINDOWHEIGHT * 0.55, "- Click the box to choose your answer!", BODY_TEXT)
        displayText(WINDOWWIDTH / 2, WINDOWHEIGHT * 0.7 , "Good luck!", BODY_TEXT)
        displayText(WINDOWWIDTH / 2, WINDOWHEIGHT * 0.3, "_______________________", BODY_TEXT)

        # Draw the start button
        drawButton(WINDOWWIDTH / 2, WINDOWHEIGHT - 50, "Start")
        pygame.display.update()

        game = True
        
        while game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    start_button_rect = pygame.Rect(WINDOWWIDTH // 2 - BUTTONWIDTH/2, WINDOWHEIGHT - 75, BUTTONWIDTH, BUTTONHEIGHT)

                    # Start the quiz when the start button is clicked
                    if start_button_rect.collidepoint(mouse_x, mouse_y):
                        highlightButton(start_button_rect, HIGHLIGHTCOLOUR)
                        filtered_questions = filtering(level, all_questions)

                        # Check for level up progress
                        result = quiz(filtered_questions) # Returns a percent
                        if level == 0: # Set level according to how well they did
                            level = 1 if (int(result / 20)==0) else int(result / 20)
                        else:
                            progress += int((result - 50) * 2)
                        
                        game = False # Stop game loop

                pygame.event.clear()

            pygame.display.update()

# Filtering function
def filtering(level, questions):
    questions = list(questions.items())
    random.shuffle(questions)
    filtered_questions = {}
    calibrated_filter = questions_filter[level]

    for index, num in enumerate(calibrated_filter):
        i = 0
        
        for question, info in questions:
            if i == num:
                break

            if int(info['difficulty']) == index + 1:
                filtered_questions[question] = info
                i += 1

    return filtered_questions

    
    
# Quiz function
def quiz(questions_dict):
    points = 0
    DISPLAYSURF.fill(BGCOLOUR)
    DISPLAYSURF.blit(background_image, (0, 0))

    current_question, previous_question = 0, -1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                points, current_question = checkAnswer(current_question, mouse_x, mouse_y, points, answers, correct_ans)

            pygame.event.clear()

        if current_question > QUESTION_AMOUNT - 1:
            displaySummary(points)
            return points * 100 / QUESTION_AMOUNT # Returns it as a percent out of 100

        if previous_question != current_question:
            # Question answered (wait for next button to be pressed)
            drawButton(WINDOWWIDTH / 2, WINDOWHEIGHT - 50, "Next")
            pygame.display.update()
            
            wait_for_next_question = False if (current_question==0) else True
            while wait_for_next_question:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = event.pos
                        next_button_rect = pygame.Rect(WINDOWWIDTH // 2 - BUTTONWIDTH/2, WINDOWHEIGHT - 75, BUTTONWIDTH, BUTTONHEIGHT)

                        # Move to next question when next button clicked (break loop)
                        if next_button_rect.collidepoint(mouse_x, mouse_y):
                            highlightButton(next_button_rect, HIGHLIGHTCOLOUR)
                            wait_for_next_question = False
                
                pygame.event.clear

            DISPLAYSURF.fill(BGCOLOUR)
            DISPLAYSURF.blit(background_image, (0, 0))
            previous_question = current_question
            answers, correct_ans = randomiseAnswers(questions_dict, current_question)
            displayQuestion(questions_dict, current_question, answers)
            displayText(WINDOWWIDTH - 100, 50, f"Score: {points}", SUBHEADER)

        pygame.display.update()

        
def randomiseAnswers(questions_dict, question_num):
    # Get a random question from the question dictionary
    question, ans_and_diff = list(questions_dict.items())[question_num]
    answers = ans_and_diff['answers']
    correct_answer = answers[0]
    random.shuffle(answers)
    correct_answer_index = answers.index(correct_answer)

    return answers, correct_answer_index

def displayQuestion(questions_dict, question_num, answers):
    # Display current question and answers
    question = list(questions_dict.items())[question_num][0]
    displayText(WINDOWWIDTH / 2, 50, f"Question {question_num + 1}/{QUESTION_AMOUNT}", SUBHEADER)
    if len(question) >= 76:
        for num, i in enumerate(question[38:76]):
            if i == " ":
                boundary = num + 38
                break
        displayText(WINDOWWIDTH / 2, 110, question[:boundary], QUESTION)
        displayText(WINDOWWIDTH / 2, 140, question[boundary:], QUESTION)
    else:
        displayText(WINDOWWIDTH / 2, 125, question, QUESTION)

    button_y = 200
    for answer in answers:
        drawButton(WINDOWWIDTH / 2, button_y, answer)
        button_y += BUTTONSPACING

def checkAnswer(question_num, x, y, points, answers, correct_answer_index):
    button_y = 200
    for i, answer in enumerate(answers):
        button_rect = pygame.Rect(WINDOWWIDTH / 2 - BUTTONWIDTH/2, button_y - BUTTONHEIGHT/2, BUTTONWIDTH, BUTTONHEIGHT)

        if button_rect.collidepoint(x, y):
            highlightButton(button_rect, HIGHLIGHTCOLOUR)

            if i == correct_answer_index:
                highlightButton(button_rect, CORRECTCOLOUR)
                points += 1
            else:
                highlightButton(button_rect, WRONGCOLOUR)
                correct_button_rect = pygame.Rect(WINDOWWIDTH / 2 - BUTTONWIDTH/2, 200 + (BUTTONSPACING * correct_answer_index) - BUTTONHEIGHT/2,
                                                  BUTTONWIDTH, BUTTONHEIGHT)
                highlightButton(correct_button_rect, CORRECTCOLOUR)

            question_num += 1

        button_y += BUTTONSPACING

    return points, question_num

def drawButton(x, y, text):
    # Draw a button with the given text
    button_rect = pygame.Rect(x - BUTTONWIDTH/2, y - BUTTONHEIGHT/2, BUTTONWIDTH, BUTTONHEIGHT)
    pygame.draw.rect(DISPLAYSURF, BOXCOLOUR, button_rect)
    pygame.draw.rect(DISPLAYSURF, BGCOLOUR, button_rect, 2)
    displayText(x, y, text, BODY_TEXT)

def highlightButton(rect, color):
    # Highlight button by drawing a colored border around it
    pygame.draw.rect(DISPLAYSURF, color, rect, 3)
    pygame.display.update()
    pygame.time.wait(500)

def displayText(x, y, text, font):
    # Display text
    text_surface = font.render(text, True, TEXTCOLOUR)
    text_rect = text_surface.get_rect(center=(x, y))
    DISPLAYSURF.blit(text_surface, text_rect)

def displaySummary(points):
    # Display summary of quiz with total score
    DISPLAYSURF.fill(BGCOLOUR)
    DISPLAYSURF.blit(background_image, (0, 0))
    
    displayText(WINDOWWIDTH / 2, WINDOWHEIGHT * 0.3, "Results:", HEADER)
    displayText(WINDOWWIDTH / 2, WINDOWHEIGHT * 0.4, "__________________", SUBHEADER)
    displayText(WINDOWWIDTH / 2, WINDOWHEIGHT * 0.5, f"Total questions: {QUESTION_AMOUNT}", SUBHEADER)
    displayText(WINDOWWIDTH / 2, WINDOWHEIGHT * 0.575, f"Correct questions: {points}", SUBHEADER)
    displayText(WINDOWWIDTH / 2, WINDOWHEIGHT * 0.65, f"Wrong questions: {QUESTION_AMOUNT - points}", SUBHEADER)
    displayText(WINDOWWIDTH / 2, WINDOWHEIGHT * 0.8, f"{points}/{QUESTION_AMOUNT}", HEADER)

    # Draw the back button
    drawButton(WINDOWWIDTH / 2, WINDOWHEIGHT - 50, "Back")
    pygame.display.update()

    while True: # Check if back button is clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                back_button_rect = pygame.Rect(WINDOWWIDTH // 2 - BUTTONWIDTH/2, WINDOWHEIGHT - 75, BUTTONWIDTH, BUTTONHEIGHT)

                # Go back to title screen when back button is clicked
                if back_button_rect.collidepoint(mouse_x, mouse_y):
                    highlightButton(back_button_rect, HIGHLIGHTCOLOUR)
                    pygame.event.clear()
                    return

        pygame.event.clear()
    

if __name__ == "__main__":
    main()