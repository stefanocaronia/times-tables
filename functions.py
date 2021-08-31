from colorama import init, Fore, Back, Style
from random import randrange, seed
import simpleaudio
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

import vars

#
# FUNCTIONS
#

def play(wavefile):
    wave_obj = simpleaudio.WaveObject.from_wave_file(wavefile)
    play_obj = wave_obj.play()
    # play_obj.wait_done()


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
    return (math.ceil(100 / (elapsed / 2)) if elapsed > 0 else 100) if elapsed < vars.BONUS_MAX_TIME else 0


def cinput(text, color):
    print(color, end='')
    delay_print(text)
    print(Fore.WHITE, end='')
    print(end='')
    return input()


def read_records():
    if not os.path.isfile(vars.SCOREBOARD):
        return {}

    with open(vars.SCOREBOARD) as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        data = {}
        for row in reader:
            if len(row) == 0:
                continue

            vars.playername = row[0]

            first = True
            for field in row:
                if first:
                    vars.playername = field
                    data[vars.playername] = {}
                    first = False
                    continue
                else:
                    score_parts = field.split(":")
                    timetable = score_parts[0]
                    score = score_parts[1]
                    data[vars.playername][timetable] = score
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
    with open(vars.SCOREBOARD, 'w') as csvfile:
        for vars.playername in data:
            line = vars.playername
            for timetable in data[vars.playername]:
                line = line + ";" + timetable + \
                    ":" + str(data[vars.playername][timetable])
            csvfile.write(line + "\n")
    csvfile.close()


def get_played_game():
    if not is_numeric(vars.single) or int(vars.single) < 2:
        return '<=' + str(vars.max)
    else:
        return str(vars.single)


def get_played_game_verbose():
    if is_numeric(vars.single) and int(vars.single) >= 2:
        game = "Times table " + str(vars.single)
    else:
        game = "Times tables up to " + str(vars.max)

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


def screen_clear():
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')


def status(score, lives, questions):
    print(" ")
    print_translate("    - Your score is " + Fore.CYAN + str(score) + Fore.WHITE)
    print_translate("    - You still have " + Fore.CYAN + str(lives) +
          " live" + ('' if lives == 1 else 's') + Fore.WHITE)
    print_translate("    - You are missing " + Fore.CYAN +
          str(questions) + " question" + ('' if questions == 1 else 's') + Fore.WHITE)
    print(" ")


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


def endgame():
    play('sounds/retro.wav')
    records = read_records()
    game = get_played_game()
    if vars.player in records:
        if game in records[vars.player]:
            old_record = int(records[vars.player][game])
        else:
            old_record = 0
            records[vars.player][game] = 0
    else:
        old_record = 0
        records[vars.player] = {}
        records[vars.player][game] = 0

    if (vars.score > old_record):
        records[vars.player][game] = vars.score

    write_records(records)

    print(" ")

    print_translate(Fore.WHITE + "You played: " + Fore.YELLOW + get_played_game_verbose() + Fore.WHITE)
    print_translate("Your score is: " + Fore.CYAN + str(vars.score) + Fore.WHITE)
    if old_record > 0:
        print_translate(Fore.WHITE + "Your previous score was: " + Fore.CYAN + str(old_record) + Fore.WHITE)

    if vars.lives == 0:
        print_translate(Fore.RED + "You ran out of lives" + Fore.WHITE)
    else:
        print_translate(Fore.WHITE + "You have completed the game!" + Fore.WHITE)

    if vars.QUESTIONS == vars.right_answers:
        print_translate(Fore.GREEN + "Well done " + vars.player + "! You have answered all the questions correctly, you are a genius of the multiplication tables!" + Fore.WHITE)
    else:
        if vars.right_answers > 0:
            print_translate(Fore.GREEN + "You answered correctly to " + str(vars.right_answers) + " question" + ('' if vars.right_answers == 1 else 's') + Fore.WHITE)
        print_translate(Fore.RED + "You were wrong in " + str(vars.wrong_answers) + " answer" + ('' if vars.wrong_answers == 1 else 's') + Fore.WHITE)

    if old_record > 0:
        if vars.score > old_record:
            print_translate(Fore.GREEN + vars.player + ", you have improved!!! " + Fore.WHITE)
        elif vars.score == old_record:
            print_translate(Fore.WHITE + vars.player + ", you kept the score from earlier!" + Fore.WHITE)
        elif vars.score < old_record:
            print_translate(Fore.RED + vars.player + ", you got worse." + Fore.WHITE)

    print(" ")


LANGUAGE = read_language(vars.LOCALE)