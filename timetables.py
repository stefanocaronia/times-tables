from colorama import init, Fore, Back, Style
from random import randrange, seed
import sys
import time
import os
import re
import math
try:
    import getch as m
except ImportError:
    import msvcrt as m

#
# FUNCTIONS
#

def wait():
    m.getch()

#!/usr/bin/env python

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
    return (math.ceil(100 / (elapsed / 2)) if elapsed > 0 else 100) if elapsed < 4 else 0


def cinput(text, color):
    print(color, end='')
    delay_print(text)
    print(Fore.WHITE, end='')
    print(end='')
    return input()


def status(punteggio, vite, domande):
    print(" ")
    print("    - Il tuo punteggio è " + Fore.CYAN + str(punteggio) + Fore.WHITE)
    print("    - Hai ancora " + Fore.CYAN + str(vite) + " vit" + ('a' if vite == 1 else 'e') + Fore.WHITE)
    print("    - Ti manca" + ('' if domande == 1 else 'no') + " " + Fore.CYAN + str(domande) + " domand" + ('a' if domande == 1 else 'e') + Fore.WHITE)
    print(" ")


def endgame(punteggio, vite, domande, risposte_giuste, risposte_sbagliate):
    print(" ")
    print(Fore.WHITE + "* ----------------------------------------------------------------------------------------- *" + Fore.WHITE)
    if vite == 0:
        print(Fore.RED + "  Hai terminato le vite" + Fore.WHITE)
    else:
        print(Fore.WHITE + "  Hai completato il gioco!" + Fore.WHITE)

    print("  Il tuo punteggio è: " + Fore.CYAN + str(punteggio) + Fore.WHITE)

    if domande == risposte_giuste:
        print(Fore.GREEN + "  Complimenti! hai risposto correttamente a tutte le domande, sei un genio delle tabelline!" + Fore.WHITE)
    else:
        if risposte_giuste > 0:
            print(Fore.GREEN + "  Hai risposto correttamente a " +
                  str(risposte_giuste) + " domand" + ('a' if risposte_giuste == 1 else 'e') + Fore.WHITE)
        print(Fore.RED + "  Hai sbagliato " +
              str(risposte_sbagliate) + " domand" + ('a' if risposte_sbagliate == 1 else 'e') + Fore.WHITE)

    print(Fore.WHITE + "* ----------------------------------------------------------------------------------------- *" + Fore.WHITE)
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

while retry and (retry.upper()[0] == 'S' or retry.upper()[0] == 'Y'):

    screen_clear()

    print(" " + Fore.CYAN)
    print("* -------------------------- * ")
    print("* IL GIOCO DELLE TABELLINE   * ")
    print("* -------------------------- * ")
    print(Fore.WHITE)

    risposte = 0
    risposte_giuste = 0
    risposte_sbagliate = 0
    punteggio = 0
    max = ''
    single = ''
    premio = 100
    vite = 3
    domande = 10

    already = [[0, 0]]
    last = [0, 0]

    single = cinput(
        "Con che tabellina vuoi giocare (invio per tutte)? ", Fore.WHITE)

    if not is_numeric(single) or int(single) < 2:
        max = cinput("Fino a quale tabellina hai studiato? ", Fore.WHITE)

    if not is_numeric(max) or int(max) < 2:
        max = 9

    print(" ")
    print(Fore.CYAN + "Iniziamo!!" + Fore.WHITE)
    print(Fore.WHITE + "Hai " + Fore.CYAN + str(domande) + Fore.WHITE +
          " domande e " + Fore.CYAN + str(vite) + Fore.WHITE + " vite" + Fore.WHITE)
    print(" ")

    last = [0, 0]

    while (risposte < domande and vite > 0):
        num1 = num2 = 0

        tries = 0
        while ([num1, num2] in already or [num2, num1] == last or [num2, num1] in already) and tries < 10:
            num1 = int(single) if is_numeric (single) else get_random_number(int(max))
            num2 = get_random_number(9)
            tries += 1

        last = [num1, num2]
        already.append(last)

        risposta = ''
        operation = str(num1) + " x " + str(num2)

        start = time.time()

        while risposta == '':
            print(Fore.CYAN + str(risposte + 1).zfill(2) + ". ", end='')
            risposta = cinput("Quanto fa " + operation + "? ", Fore.WHITE)

        result = num1 * num2
        operation = str(num1) + " x " + str(num2) + " = " + str(result)

        if int(risposta) == result:

            risposte_giuste += 1
            elapsed = math.ceil(time.time() - start)
            bonus = get_bonus(elapsed)
            punti = premio + num1 * 5 + num2 * 5 + bonus
            punteggio += punti

            print(Fore.GREEN + indent + "Bravo! Il risultato è corretto! " +
                  Style.BRIGHT + operation + Fore.WHITE + Style.NORMAL)
            print(Fore.GREEN + indent + "Hai risposto in " +
                  str(elapsed) + " secondi " + Fore.WHITE)
            print(Fore.GREEN + indent + "Hai ottenuto " +
                  str(punti) + " punti " + Fore.WHITE)
            if bonus > 0:
                print(Fore.YELLOW + indent + "Evviva! Hai avuto un bonus di " +
                      str(bonus) + " punti " + Fore.WHITE)
        else:

            risposte_sbagliate += 1
            vite -= 1

            print(Fore.RED + indent + "Sbagliato! Il risultato corretto era " +
                  str(result) + Fore.GREEN + "\n    Ricorda: " + Style.BRIGHT + operation + "" + Fore.WHITE + Style.NORMAL)

        risposte += 1

        if vite > 0 and risposte < domande:
            status(punteggio, vite, domande - risposte)
            print(indent + "Premi un tasto per la prossima domanda")
            wait()
            print('')

    endgame(punteggio, vite, domande, risposte_giuste, risposte_sbagliate)

    retry = cinput(
        "Vuoi fare un'altra partita? ", Fore.WHITE)
