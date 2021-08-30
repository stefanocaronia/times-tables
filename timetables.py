#!/usr/bin/env python3

from colorama import init, Fore, Back, Style
from random import randrange, seed
import sys
import time
import os
import re
import math
import csv
import os.path

try:
    import getch as m
except ImportError:
    import msvcrt as m

#
# CONFIGURATION
#


QUESTIONS = 10
LIVES = 3
PRIZE = 100
BONUS_MAX_TIME = 7
PLAYER_UNKNOWN = 'Pinco Pallino'
LOCALE = 'en'


#
# FUNCTIONS
#


def wait():
    m.getch()


def delay_print(s):
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.01)


def is_numeric(string):
    return string != '' and re.search('\d', string)


def get_random_number(max):
    seed()
    num = 0
    while num < 2:
        num = randrange(1, max)
    return num


def get_bonus(elapsed):
    return (math.ceil(100 / (elapsed / 2)) if elapsed > 0 else 100) if elapsed < BONUS_MAX_TIME else 0


def cinput(text, color):
    print(color, end='')
    delay_print(text)
    print(Fore.WHITE, end='')
    print(end='')
    return input()


def status(score, LIVES, QUESTIONS):
    print(" ")
    print_translate("    - Your score is " + Fore.CYAN + str(score) + Fore.WHITE)
    print_translate("    - You still have " + Fore.CYAN + str(LIVES) +
          " live" + ('' if LIVES == 1 else 's') + Fore.WHITE)
    print_translate("    - You are missing " + Fore.CYAN +
          str(QUESTIONS) + " question" + ('' if QUESTIONS == 1 else 's') + Fore.WHITE)
    print(" ")


def read_records():
    if not os.path.isfile(SCOREBOARD):
        return {}

    with open(SCOREBOARD) as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        data = {}
        for row in reader:
            if len(row) == 0:
                continue

            playername = row[0]

            first = True
            for field in row:
                if first:
                    playername = field
                    data[playername] = {}
                    first = False
                    continue
                else:
                    score_parts = field.split(":")
                    timetable = score_parts[0]
                    score = score_parts[1]
                    data[playername][timetable] = score
    csvfile.close()
    return data


def read_language(locale):
    filename = locale + '.lang'
    data = {}
    if not os.path.isfile(filename):
        return {}
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter="=")
        data = {}
        for row in reader:
            data[row[0].strip()] = row[1].strip()
    csvfile.close()
    return data


def write_records(data):
    with open(SCOREBOARD, 'w') as csvfile:
        for playername in data:
            line = playername
            for timetable in data[playername]:
                line = line + ";" + timetable + \
                    ":" + str(data[playername][timetable])
            csvfile.write(line + "\n")
    csvfile.close()


def print_records(records, player):
    if player not in records:
        return

    print(" ")
    print_translate(Fore.YELLOW + "SCOREBOARD OF " + player + Fore.WHITE)
    print(Fore.YELLOW + "-------------------------------------" + Fore.WHITE)

    player_records = records[player]

    for game in player_records:
        print_translate(Fore.CYAN + get_played_game_verbose_from_string(game) +
              Fore.GREEN + "\t" + str(player_records[game]) + Fore.WHITE)
    print(" ")


def get_played_game():
    if not is_numeric(single) or int(single) < 2:
        return '<=' + str(max)
    else:
        return str(single)


def get_played_game_verbose():
    if is_numeric(single) and int(single) >= 2:
        game = "Times table " + str(single)
    else:
        game = "Times tables up to " + str(max)

    return game


def get_played_game_verbose_from_string(game_string):
    if game_string[0] == '<':
        return "Times tables up to " + game_string.lstrip('<=')
    else:
        return "Times table " + game_string + "    "


def translate(text):
    for key in LANGUAGE.keys():
        text = text.replace(key, LANGUAGE[key])
    text = text.replace('Ã¨', 'è')
    return text


def print_translate(text):
    text = translate(text)
    print(text)
    return len(text)

def cinput_translate(text, color):
    text = translate(text)
    return cinput(text, color)


def endgame(score, LIVES, QUESTIONS, right_answers, wrong_answers):

    records = read_records()
    game = get_played_game()
    if player in records:
        if game in records[player]:
            old_record = int(records[player][game])
        else:
            old_record = 0
            records[player][game] = 0
    else:
        old_record = 0
        records[player] = {}
        records[player][game] = 0

    if (score > old_record):
        records[player][game] = score

    write_records(records)

    print(" ")
    print(Fore.YELLOW + "* ----------------------------------------------------------------------------------------- *" + Fore.WHITE)

    print_translate(Fore.WHITE + "  " + player + ", You played: " +
          Fore.YELLOW + get_played_game_verbose() + Fore.WHITE)

    if LIVES == 0:
        print_translate(Fore.RED + "  You ran out of lives" + Fore.WHITE)
    else:
        print_translate(Fore.WHITE + "  You have completed the game!" + Fore.WHITE)

    print_translate("  Your score is: " + Fore.CYAN + str(score) + Fore.WHITE)

    if QUESTIONS == right_answers:
        print_translate(Fore.GREEN + "  Well done " + player +
              "! You have answered all the questions correctly, you are a genius of the multiplication tables!" + Fore.WHITE)
    else:
        if right_answers > 0:
            print_translate(Fore.GREEN + "  You answered correctly to " +
                  str(right_answers) + " question" + ('' if right_answers == 1 else 's') + Fore.WHITE)
        print_translate(Fore.RED + "  You were wrong in " +
              str(wrong_answers) + " answer" + ('' if wrong_answers == 1 else 's') + Fore.WHITE)

    if old_record > 0:
        print_translate(Fore.WHITE + "  " + player + ", your previous score was: " +
              Fore.CYAN + str(old_record) + Fore.WHITE)
        if score > old_record:
            print_translate(Fore.GREEN + "  You have improved!!! " + Fore.WHITE)
        elif score == old_record:
            print_translate(Fore.WHITE + "  You kept the score from earlier!" + Fore.WHITE)
        elif score < old_record:
            print_translate(Fore.RED + "  You got worse." + Fore.WHITE)

    print(Fore.YELLOW + "* ----------------------------------------------------------------------------------------- *" + Fore.WHITE)

    print(" ")


def screen_clear():
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')

#
# GAME
#


init()
LANGUAGE = read_language(LOCALE)

SCOREBOARD = 'scores.csv'

indent = '    '
retry = 'S'
player = ''

while retry and (retry.upper()[0] == 'S' or retry.upper()[0] == 'Y'):

    screen_clear()

    print(" " + Fore.CYAN)
    l = print_translate("* TIMETABLES GAME *")
    print("* " + ('-' * (l - 4) )+" * ")
    print(Fore.WHITE)

    answers = 0
    right_answers = 0
    wrong_answers = 0
    score = 0
    max = ''
    single = ''
    lives = LIVES

    already = [[0, 0]]
    last = [0, 0]

    records = read_records()
    names = list(records.keys())

    if PLAYER_UNKNOWN in names:
        names.remove(PLAYER_UNKNOWN)
    players = ', '.join(names)
    if player == '':
        player = cinput_translate("Hello! Who are you" + (" (" + players + ")" if len(players) > 0 else "") + "? ", Fore.WHITE)

    if player == '':
        player = PLAYER_UNKNOWN

    print_records(records, player)

    single = cinput_translate("With which timetable do you want to play, " + player + " (return for all)? ", Fore.WHITE)

    if not is_numeric(single) or int(single) < 2:
        max = cinput_translate("Up to which times table did you study (return for 9)? ", Fore.WHITE)

    if not is_numeric(max) or int(max) < 2:
        max = 9

    print(" ")
    print_translate(Fore.CYAN + "Let's start!!" + Fore.WHITE)
    print_translate(Fore.WHITE + "You have " + Fore.CYAN + str(QUESTIONS) + Fore.WHITE +
          " questions and " + Fore.CYAN + str(lives) + Fore.WHITE + " lives" + Fore.WHITE)
    print(" ")

    last = [0, 0]

    while (answers < QUESTIONS and lives > 0):
        num1 = num2 = 0

        tries = 0
        while ([num1, num2] in already or [num2, num1] == last or [num2, num1] in already) and tries < 10:
            num1 = int(single) if is_numeric(
                single) else get_random_number(int(max))
            num2 = get_random_number(9)
            tries += 1

        last = [num1, num2]
        already.append(last)

        answer = ''
        operation = str(num1) + " x " + str(num2)

        start = time.time()

        while answer == '':
            print(Fore.CYAN + str(answers + 1).zfill(2) + ". ", end='')
            answer = cinput_translate("How much is " + operation + "? ", Fore.WHITE)

        result = num1 * num2
        operation = str(num1) + " x " + str(num2) + " = " + str(result)

        if int(answer) == result:

            right_answers += 1
            elapsed = math.ceil(time.time() - start)
            bonus = get_bonus(elapsed)
            prize = PRIZE + num1 * 5 + num2 * 5 + bonus
            score += prize

            print_translate(Fore.GREEN + indent + "Good! The result is correct! " +
                  Style.BRIGHT + operation + Fore.WHITE + Style.NORMAL)
            print_translate(Fore.GREEN + indent + "You answered in " +
                  str(elapsed) + " seconds " + Fore.WHITE)
            print_translate(Fore.GREEN + indent + "You got " +
                  str(prize) + " points " + Fore.WHITE)
            if bonus > 0:
                print_translate(Fore.YELLOW + indent + "Hurray! You had a bonus of " +
                      str(bonus) + " points " + Fore.WHITE)
        else:

            wrong_answers += 1
            lives -= 1

            print_translate(Fore.RED + indent + "Wrong! Correct result was " +
                  str(result) + Fore.GREEN + "\n    Remember: " + Style.BRIGHT + operation + "" + Fore.WHITE + Style.NORMAL)

        answers += 1

        if lives > 0 and answers < QUESTIONS:
            status(score, lives, QUESTIONS - answers)
            print_translate(indent + "Press a key for the next question")
            wait()
            print('')

    endgame(score, lives, QUESTIONS, right_answers, wrong_answers)

    retry = cinput_translate("Do you want to play another game? ", Fore.WHITE)
