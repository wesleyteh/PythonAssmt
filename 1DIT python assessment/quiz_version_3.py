# Import necessary libraries
import random, pygame ,sys
from pygame.locals import *

# Constants
QUESTION_AMOUNT = 10
WINDOWWIDTH = 1200
WINDOWHEIGHT = 600

# Colours           R    G    B     Colour
BGCOLOUR        = (  0,   0,   0) # Black
BOXCOLOUR       = (127, 127, 127) # Gray
TEXTCOLOUR      = (255, 255, 255) # White
HIGHLIGHTCOLOUR = (  0,   0, 255) # Blue
WRONGCOLOUR     = (255,   0,   0) # Red
CORRECTCOLOUR   = (  0, 255,   0) # Green

# Initialize pygame
pygame.init()
pygame.display.set_caption('Chemistry Quiz')

# Create the game window
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
DISPLAYSURF.fill(BGCOLOUR)

# Create text fonts
HEADER = pygame.font.SysFont(None, 52)
SUBHEADER = pygame.font.SysFont(None, 42)
BODY_TEXT = pygame.font.SysFont(None, 32)
DESCRIPTION = pygame.font.SysFont(None, 18)


# Load the questions from a file and select a subset of questions for the quiz
questions_dict = dict(random.sample(sorted(eval(open("questions.txt").read()).items()), QUESTION_AMOUNT))

# Main function
def main():
    quiz_end = False

    # Load and display image
    img = pygame.transform.scale(pygame.image.load("science_img.jpg").convert(), (400, 400))
    DISPLAYSURF.blit(img, (100, 100))

    # Display title
    displayText(WINDOWWIDTH / 2, WINDOWHEIGHT * 0.1, "CHEMISTRY QUIZ", HEADER)

    # Display photo info
    displayText(300, 510,
        "Photo by Vedrana Filipović on https://unsplash.com",
                DESCRIPTION)
    
    # Display instructions for the quiz
    displayText(WINDOWWIDTH * (3/4), WINDOWHEIGHT * 0.2, "Instructions:", SUBHEADER)
    
    display = lambda x, text: displayText(WINDOWWIDTH * (3/4), WINDOWHEIGHT * x, text, BODY_TEXT)
    display(0.3, "_______________________")
    display(0.43, "- You will be asked 10 multiple")
    display(0.47, "choice chemistry questions.")
    display(0.55, "- Click the box to choose your answer!")
    display(0.7, "Good luck!")

    # Draw the start button
    drawButton(WINDOWWIDTH / 2, WINDOWHEIGHT - 50, "Start")
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and not quiz_end:
                mouse_x, mouse_y = event.pos
                start_button_rect = pygame.Rect(WINDOWWIDTH // 2 - 150, WINDOWHEIGHT - 75, 300, 50)

                # Start the quiz when the start button is clicked
                if start_button_rect.collidepoint(mouse_x, mouse_y):
                    highlightButton(start_button_rect, HIGHLIGHTCOLOUR)
                    quiz()
                    quiz_end = True

            pygame.event.clear()

        pygame.display.update()

# Quiz function
def quiz():
    points = 0
    DISPLAYSURF.fill(BGCOLOUR)

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
            break

        if previous_question != current_question:
            DISPLAYSURF.fill(BGCOLOUR)
            previous_question = current_question
            answers, correct_ans = randomiseAnswers(current_question)
            displayQuestion(current_question, answers)
            displayText(WINDOWWIDTH - 100, 50, f"Score: {points}", SUBHEADER)

        pygame.display.update()

def randomiseAnswers(question_num):
    # Get a random question from the question dictionary
    question, answers = list(questions_dict.items())[question_num]
    correct_answer = answers[0]
    random.shuffle(answers)
    correct_answer_index = answers.index(correct_answer)

    return answers, correct_answer_index

def displayQuestion(question_num, answers):
    # Display the current question and its answers
    question = list(questions_dict.items())[question_num][0]
    displayText(WINDOWWIDTH / 2, 50, f"Question {question_num + 1}/{QUESTION_AMOUNT}", HEADER)
    displayText(WINDOWWIDTH / 2, 125, question, SUBHEADER)

    button_y = 200
    for answer in answers:
        drawButton(WINDOWWIDTH / 2, button_y, answer)
        button_y += 100

def checkAnswer(question_num, x, y, points, answers, correct_answer_index):
    button_y = 200
    for i, answer in enumerate(answers):
        button_rect = pygame.Rect(WINDOWWIDTH / 2 - 150, button_y - 25, 300, 50)

        if button_rect.collidepoint(x, y):
            highlightButton(button_rect, HIGHLIGHTCOLOUR)

            if i == correct_answer_index:
                highlightButton(button_rect, CORRECTCOLOUR)
                points += 1
            else:
                highlightButton(button_rect, WRONGCOLOUR)
                correct_button_rect = pygame.Rect(WINDOWWIDTH / 2 - 150, 200 + (100 * correct_answer_index) - 25,
                                                  300, 50)
                highlightButton(correct_button_rect, CORRECTCOLOUR)

            question_num += 1

        button_y += 100

    return points, question_num

def drawButton(x, y, text):
    # Draw a button with the given text at the specified position
    button_rect = pygame.Rect(x - 150, y - 25, 300, 50)
    pygame.draw.rect(DISPLAYSURF, BOXCOLOUR, button_rect)
    pygame.draw.rect(DISPLAYSURF, BGCOLOUR, button_rect, 2)
    displayText(x, y, text, BODY_TEXT)

def highlightButton(rect, color):
    # Highlight the button by drawing a colored border around it
    pygame.draw.rect(DISPLAYSURF, color, rect, 3)
    pygame.display.update()
    pygame.time.wait(500)

def displayText(x, y, text, font):
    # Display text on the game window at the specified position
    text_surface = font.render(text, True, TEXTCOLOUR)
    text_rect = text_surface.get_rect(center=(x, y))
    DISPLAYSURF.blit(text_surface, text_rect)

def displaySummary(points):
    # Display the summary of the quiz with the total score
    DISPLAYSURF.fill(BGCOLOUR)
    displayText(WINDOWWIDTH / 2, WINDOWHEIGHT * 0.3, "Results:", HEADER)
    
    display = lambda x, text: displayText(WINDOWWIDTH / 2, WINDOWHEIGHT * x, text, SUBHEADER)
    display(0.4, "__________________")
    display(0.5, f"Total questions: {QUESTION_AMOUNT}")
    display(0.575, f"Correct questions: {points}")
    display(0.65, f"Wrong questions: {QUESTION_AMOUNT - points}")

    displayText(WINDOWWIDTH / 2, WINDOWHEIGHT * 0.8, f"{points}/{QUESTION_AMOUNT}", HEADER)
    
    pygame.display.update()

if __name__ == "__main__":
    main()
