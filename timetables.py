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
# CONSTANTS
#


SCOREBOARD = 'scores.csv'
QUESTIONS = 10
LIVES = 3
PRIZE = 100
BONUS_MAX_TIME = 7
PLAYER_UNKNOWN = 'Pinco Pallino'

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
    print("    - Il tuo punteggio è " + Fore.CYAN + str(score) + Fore.WHITE)
    print("    - Hai ancora " + Fore.CYAN + str(LIVES) +
          " vit" + ('a' if LIVES == 1 else 'e') + Fore.WHITE)
    print("    - Ti manca" + ('' if QUESTIONS == 1 else 'no') + " " + Fore.CYAN +
          str(QUESTIONS) + " domand" + ('a' if QUESTIONS == 1 else 'e') + Fore.WHITE)
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
    print(Fore.YELLOW + "TABELLONE DEI RECORD DI " + player + Fore.WHITE)
    print(Fore.YELLOW + "-------------------------------------" + Fore.WHITE)

    player_records = records[player]

    for game in player_records:
        print(Fore.CYAN + get_played_game_verbose_from_string(game) +
              Fore.GREEN + "\t" + str(player_records[game]) + Fore.WHITE)
    print(" ")


def get_played_game():
    if not is_numeric(single) or int(single) < 2:
        return '<=' + str(max)
    else:
        return str(single)


def get_played_game_verbose():
    if is_numeric(single) and int(single) >= 2:
        game = "Tabellina del " + str(single)
    else:
        game = "Tabelline fino al " + str(max)

    return game


def get_played_game_verbose_from_string(game_string):
    if game_string[0] == '<':
        return "Tabelline fino al " + game_string.lstrip('<=')
    else:
        return "Tabellina del " + game_string + "    "


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

    print(Fore.WHITE + "  " + player + ", hai giocato a: " +
          Fore.YELLOW + get_played_game_verbose() + Fore.WHITE)

    if LIVES == 0:
        print(Fore.RED + "  Hai terminato le LIVES" + Fore.WHITE)
    else:
        print(Fore.WHITE + "  Hai completato il gioco!" + Fore.WHITE)

    print("  Il tuo punteggio è: " + Fore.CYAN + str(score) + Fore.WHITE)

    if QUESTIONS == right_answers:
        print(Fore.GREEN + "  Complimenti " + player +
              "! hai risposto correttamente a tutte le QUESTIONS, sei un genio delle tabelline!" + Fore.WHITE)
    else:
        if right_answers > 0:
            print(Fore.GREEN + "  Hai risposto correttamente a " +
                  str(right_answers) + " domand" + ('a' if right_answers == 1 else 'e') + Fore.WHITE)
        print(Fore.RED + "  Hai sbagliato " +
              str(wrong_answers) + " domand" + ('a' if wrong_answers == 1 else 'e') + Fore.WHITE)

    if old_record > 0:
        print(Fore.WHITE + "  " + player + ", il tuo punteggio precedente era: " +
              Fore.GREEN + str(old_record) + Fore.WHITE)
        if score > old_record:
            print(Fore.GREEN + "  Sei migliorato!!! " + Fore.WHITE)
        elif score == old_record:
            print(Fore.WHITE + "  Hai mantenuto il punteggio di prima!" + Fore.WHITE)
        elif score < old_record:
            print(Fore.RED + "  Sei peggiorato." + Fore.WHITE)

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

indent = '    '
retry = 'S'
player = ''

while retry and (retry.upper()[0] == 'S' or retry.upper()[0] == 'Y'):

    screen_clear()

    print(" " + Fore.CYAN)
    print("* -------------------------- * ")
    print("* IL GIOCO DELLE TABELLINE   * ")
    print("* -------------------------- * ")
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
        player = cinput(
            "Ciao! Come ti chiami" + (" (" + players + ")" if len(players) > 0 else "") + "? ", Fore.WHITE)

    if player == '':
        player = PLAYER_UNKNOWN

    print_records(records, player)

    single = cinput(
        "Con che tabellina vuoi giocare, " + player + " (invio per tutte)? ", Fore.WHITE)

    if not is_numeric(single) or int(single) < 2:
        max = cinput("Fino a quale tabellina hai studiato? ", Fore.WHITE)

    if not is_numeric(max) or int(max) < 2:
        max = 9

    print(" ")
    print(Fore.CYAN + "Iniziamo!!" + Fore.WHITE)
    print(Fore.WHITE + "Hai " + Fore.CYAN + str(QUESTIONS) + Fore.WHITE +
          " domande e " + Fore.CYAN + str(lives) + Fore.WHITE + " vite" + Fore.WHITE)
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
            answer = cinput("Quanto fa " + operation + "? ", Fore.WHITE)

        result = num1 * num2
        operation = str(num1) + " x " + str(num2) + " = " + str(result)

        if int(answer) == result:

            right_answers += 1
            elapsed = math.ceil(time.time() - start)
            bonus = get_bonus(elapsed)
            prize = PRIZE + num1 * 5 + num2 * 5 + bonus
            score += prize

            print(Fore.GREEN + indent + "Bravo! Il risultato è corretto! " +
                  Style.BRIGHT + operation + Fore.WHITE + Style.NORMAL)
            print(Fore.GREEN + indent + "Hai risposto in " +
                  str(elapsed) + " secondi " + Fore.WHITE)
            print(Fore.GREEN + indent + "Hai ottenuto " +
                  str(prize) + " punti " + Fore.WHITE)
            if bonus > 0:
                print(Fore.YELLOW + indent + "Evviva! Hai avuto un bonus di " +
                      str(bonus) + " punti " + Fore.WHITE)
        else:

            wrong_answers += 1
            LIVES -= 1

            print(Fore.RED + indent + "Sbagliato! Il risultato corretto era " +
                  str(result) + Fore.GREEN + "\n    Ricorda: " + Style.BRIGHT + operation + "" + Fore.WHITE + Style.NORMAL)

        answers += 1

        if LIVES > 0 and answers < QUESTIONS:
            status(score, LIVES, QUESTIONS - answers)
            print(indent + "Premi un tasto per la prossima domanda")
            wait()
            print('')

    endgame(score, LIVES, QUESTIONS, right_answers, wrong_answers)

    retry = cinput("Vuoi fare un'altra partita? ", Fore.WHITE)
