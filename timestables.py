#!/usr/bin/env python3

from colorama import init, Fore, Style
from random import randrange, seed
import time
import math

import vars
import functions

init()

indent = '    '
retry = 'S'
vars.player = ''

#
# GAME
#

while retry and (retry.upper()[0] == 'S' or retry.upper()[0] == 'Y'):

    functions.screen_clear()

    l = functions.print_translate(Fore.CYAN + "* TIMES-TABLES GAME *")
    print("* " + ('-' * (l - 9))+" * ")
    print(Fore.WHITE)

    vars.answers = 0
    vars.right_answers = 0
    vars.wrong_answers = 0
    vars.score = 0
    vars.max = ''
    vars.single = ''
    vars.lives = vars.LIVES

    already = [[0, 0]]
    last = [0, 0]

    records = functions.read_records()
    names = list(records.keys())

    if vars.PLAYER_UNKNOWN in names:
        names.remove(vars.PLAYER_UNKNOWN)
    players = ', '.join(names)
    if vars.player == '':
        vars.player = functions.cinput_translate(
            "Hello! Who are you" + (" (" + players + ")" if len(players) > 0 else "") + "? ", Fore.WHITE)

    if vars.player == '':
        vars.player = vars.PLAYER_UNKNOWN

    functions.print_records(records, vars.player)

    vars.single = functions.cinput_translate(
        "With which timetable do you want to play, " + vars.player + " (return for all)? ", Fore.WHITE)

    if not functions.is_numeric(vars.single) or int(vars.single) < 2:
        vars.max = functions.cinput_translate(
            "Up to which times table did you study (return for 9)? ", Fore.WHITE)

    if not functions.is_numeric(vars.max) or int(vars.max) < 2:
        vars.max = 9

    print(" ")
    functions.print_translate(Fore.CYAN + "Let's start!!" + Fore.WHITE)
    functions.print_translate(Fore.WHITE + "You have " + Fore.CYAN + str(vars.QUESTIONS) + Fore.WHITE +
                              " questions and " + Fore.CYAN + str(vars.lives) + Fore.WHITE + " lives" + Fore.WHITE)
    print(" ")

    last = [0, 0]

    while (vars.answers < vars.QUESTIONS and vars.lives > 0):
        num1 = num2 = 0

        tries = 0
        while ([num1, num2] in already or [num2, num1] == last or [num2, num1] in already) and tries < 10:
            num1 = int(vars.single) if functions.is_numeric(
                vars.single) else functions.get_random_number(int(vars.max))
            num2 = functions.get_random_number(9)
            tries += 1

        last = [num1, num2]
        already.append(last)

        answer = ''
        operation = str(num1) + " x " + str(num2)

        start = time.time()

        while answer == '':
            print(Fore.CYAN + str(vars.answers + 1).zfill(2) + ". ", end='')
            functions.play('sounds/ding.wav')
            functions.read("How much is " + operation + "? ")
            answer = functions.cinput_translate(
                "How much is " + operation + "? ", Fore.WHITE)

        result = num1 * num2
        operation = str(num1) + " x " + str(num2) + " = " + str(result)

        if int(answer) == result:

            vars.right_answers += 1
            elapsed = math.ceil(time.time() - start)
            bonus = functions.get_bonus(elapsed)
            prize = vars.PRIZE + num1 * 5 + num2 * 5 + bonus
            vars.score += prize
            functions.print_translate(Fore.GREEN + indent + "Good! The result is correct! " +
                                      Style.BRIGHT + operation + Fore.WHITE + Style.NORMAL)
            functions.print_translate(
                Fore.GREEN + indent + "You answered in " + str(elapsed) + " seconds " + Fore.WHITE)
            functions.print_translate(
                Fore.GREEN + indent + "You got " + str(prize) + " points " + Fore.WHITE)
            if bonus > 0:
                functions.play('sounds/applause.wav')
                functions.print_translate(
                    Fore.YELLOW + indent + "Hurray! You had a bonus of " + str(bonus) + " points " + Fore.WHITE)
            else:
                functions.play('sounds/chimes.wav')

            functions.read("Good! The result is correct! " + operation)
            functions.read("Hurray! You had a bonus of " +
                           str(bonus) + " points ")

        else:
            functions.play('sounds/buzz.wav')

            vars.wrong_answers += 1
            vars.lives -= 1

            functions.print_translate(Fore.RED + indent + "Wrong! Correct result was " +
                                      str(result) + Fore.GREEN + "\n    Remember: " + Style.BRIGHT + operation + "" + Fore.WHITE + Style.NORMAL)

            functions.read("Wrong! Correct result was " +
                           str(result) + ', ' + operation)

        vars.answers += 1

        if vars.lives > 0 and vars.answers < vars.QUESTIONS:
            functions.status(vars.score, vars.lives,
                             vars.QUESTIONS - vars.answers)
            functions.print_translate(
                indent + "Press a key for the next question")
            functions.wait()
            print('')

    functions.endgame()

    retry = functions.cinput_translate(
        "Do you want to play another game? ", Fore.WHITE)
