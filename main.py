import re
import pygame
import sys
from pygame.locals import *
import random
from english_words import english_words_lower_alpha_set
from PyDictionary import PyDictionary

dictionary = PyDictionary()
english_words = list(english_words_lower_alpha_set)
height = 700
width = 1000
white = (255, 255, 255)
black = (0, 0, 0)
yellow = (200, 200, 0)
navyblue = (60, 60, 100)
cyan = (0, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
clock = pygame.time.Clock()
pygame.init()
DISPLAYSURF = pygame.display.set_mode((width, height))
min_len = 0
max_len = 12
score = 0


def draw_line(n):
    x = 100
    y = 100
    global center
    center = []
    for i in range(n):
        pygame.draw.line(DISPLAYSURF, black, (x, y), (x + 50, y), 10)
        center.append((x + 25, y))
        x += 80
    return


def check(s, answer):
    return s in answer


def draw_font(guessed, answer):
    idx = []
    for i in range(len(answer)):
        if answer[i] == guessed:
            idx.append(i)
    for val in idx:
        mytext = pygame.font.Font("freesansbold.ttf", 50)
        textSurface = mytext.render(guessed, True, black)
        textRect = textSurface.get_rect()
        textRect.midbottom = center[val]
        DISPLAYSURF.blit(textSurface, textRect)


def create_text(text, x, y, fontSize=20):
    mytext = pygame.font.Font("freesansbold.ttf", fontSize)
    textSurface = mytext.render(text, True, black)
    textRect = textSurface.get_rect()
    textRect.center = (x, y)
    DISPLAYSURF.blit(textSurface, textRect)


def create_meaning(meaning, x=width // 2, y=200):
    s = ""
    for i in range(len(meaning)):
        s = s + " " + meaning[i]
        if len(s) >= 80:
            create_text(s, x, y)
            y += 50
            s = ""
    create_text(s, x, y)
    return y


def create_button(textMsg, x, y, w, h, color, colorOnHover, action=None):
    global min_len
    global max_len
    myRect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(DISPLAYSURF, color, myRect)
    centerx, centery = myRect.center
    create_text(textMsg, centerx, centery, 30)
    mousex, mousey = pygame.mouse.get_pos()

    if x < mousex < x + w and y < mousey < y + h:
        pygame.draw.rect(DISPLAYSURF, colorOnHover, myRect)
        press = pygame.mouse.get_pressed()
        if press[0] == 1 and action != None:
            if textMsg == "Easy":
                max_len = 6
                action()
            elif textMsg == "Medium":
                min_len = 5
                max_len = 9
                action()
            elif textMsg == "Hard":
                min_len = 8
                action()
            else:
                action()


def create_pictures(totalTries, y):
    img = pygame.image.load("images\hang" + str(10 - totalTries + 1) + '.png')
    imgRect = img.get_rect()
    imgRect.midtop = (width // 2, y + 120)
    DISPLAYSURF.blit(img, imgRect)


def quit_game():
    pygame.quit()
    sys.exit()


def intro():
    img = pygame.image.load('images\hangman1.png')
    while True:
        DISPLAYSURF.fill(white)
        create_text("HANGMAN", width // 2, height // 2 - 200, 100)
        DISPLAYSURF.blit(img, (225, height // 2 - 100))
        create_button("PLAY", 100, 600, 100, 50, blue, navyblue, difficulty)
        create_button("QUIT", 800, 600, 100, 50, red, navyblue, quit_game)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                quit_game()

        pygame.display.update()
        clock.tick(30)


def difficulty():
    while True:
        DISPLAYSURF.fill(white)
        create_button("Easy", width // 2 - 50, 100, 150, 50, green, navyblue, main)
        create_button("Medium", width // 2 - 50, 300, 150, 50, yellow, navyblue, main)
        create_button("Hard", width // 2 - 50, 500, 150, 50, red, navyblue, main)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                quit_game()

        pygame.display.update()
        clock.tick(30)


def main():
    global score
    first = True
    answer = random.choice(english_words)
    while not (min_len < len(answer) < max_len) or len(str(dictionary.meaning(answer))) >= 250 or dictionary.meaning(answer) is None:
        answer = random.choice(english_words)
    correct_guessed = set()
    totalTries = 10
    meaning = str(dictionary.meaning(answer))
    meaning = re.sub("'", "", meaning)
    meaning = re.sub("\\[", "", meaning)
    meaning = re.sub("\\]", "", meaning)
    meaning = re.sub("\\{", "", meaning)
    meaning = re.sub("\\}", "", meaning)
    meaning = re.sub("\\(", "", meaning)
    meaning = re.sub("\\)", "", meaning)
    print(len(meaning))
    meaning = list(map(str, meaning.split()))
    while True:
        DISPLAYSURF.fill(white)

        draw_line(len(answer))

        y = create_meaning(meaning)
        create_text("Total Tries : " + str(totalTries), 850, 30, 30)
        create_text(f"Score : {score}", 100, 30, 30)
        create_pictures(totalTries, y)
        for char in correct_guessed:
            draw_font(char, answer)
        if len(correct_guessed) == len(set(answer)) or totalTries <= 0:
            if len(correct_guessed) == len(set(answer)) and first and totalTries > 0:
                score += 1
                first = False
            else:
                if score > 0 and first:
                    score -= 1
                    first = False
            create_text(answer, width // 2, y + 50, 30)
            create_button("New Game", width // 2 - 100, height - 100, 200, 50, green, blue, main)

        for event in pygame.event.get():
            if event.type == QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN and 97 <= event.key <= 122:
                pressed = chr(event.key)
                if check(pressed, answer) and pressed not in correct_guessed:
                    correct_guessed.add(pressed)
                else:
                    totalTries -= 1
                    if totalTries <= 0:
                        totalTries = 0

        pygame.display.update()
        clock.tick(30)


intro()
