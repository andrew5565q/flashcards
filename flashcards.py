from random import choice
from io import StringIO
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--import_from')
parser.add_argument('--export_to')

memory_file = StringIO()

dict_main = dict()
dict_hard = dict()


def input_log(phrase_i):
    a = input(phrase_i)
    memory_file.write(phrase_i)
    memory_file.write(a+'\n')
    return a


def print_log(phrase_p):
    print(phrase_p)
    memory_file.write(phrase_p+'\n')


def add():
    term = input_log('The card:\n')
    while True:
        if term in dict_main.keys():
            term = input_log(f'The term "{term}" already exists. Try again:\n')
        else:
            break

    definition = input_log('The definition of the card:\n')
    while True:
        if definition in dict_main.values():
            definition = input_log(f'The definition "{definition}" already exists. Try again:\n')
        else:
            break

    dict_main[term] = definition
    dict_hard[term] = 0

    first = list(dict_main.keys())[-1]
    second = dict_main[list(dict_main.keys())[-1]]
    print_log(f'The pair ("{first}":"{second}") has been added')


def remove():
    re_move = input_log('Which card?\n')
    if re_move in dict_main.keys():
        del dict_main[re_move]
        print_log("The card has been removed.")
    else:
        print_log(f'''Can't remove "{re_move}": there is no such card.''')


def import_func():
    name = input_log('File name:\n')
    try:
        with open(name, 'r') as opened_file:
            count = 0
            k = opened_file.readlines()
            for i in k:
                i = i.split(': ')
                dict_main[i[0]] = i[1].split('\n')[0]
                try:
                    dict_hard[i[0]] = i[2]
                except IndexError:
                    dict_hard[i[0]] = 0
                count += 1

            print_log(str(count) + ' cards have been loaded.')
    except FileNotFoundError:
        print_log('File not found.')


def export():
    name = input_log('File name:\n')
    with open(name, 'w') as f:
        for x, defn in dict_main.items():
            f.write(str(x) + ': ' + defn + ': ' + str(dict_hard[x]) + '\n')

        print_log(str(len(dict_main.keys())) + ' cards have been saved')


def ask():
    times = int(input_log('How many times to ask?\n'))
    times += 1
    for i in range(times-1):
        asker = choice(list(dict_main.keys()))
        answer = input_log(f'Print the definition of "{asker}":\n')
        if dict_main[asker] == answer:
            print_log('Correct!')
        elif answer in dict_main.values():
            long = list(x for x, y in dict_main.items() if y == answer)[0]
            print_log(f'Wrong. The right answer is "{dict_main[asker]}", but your definition is correct for "{long}".')
            dict_hard[asker] += 1
        else:
            print_log(f'Wrong. The right answer is "{dict_main[asker]}".')
            dict_hard[asker] += 1


def exit_func():
    print_log('Bye bye!')
    export_to()
    exit()


def log():
    a = input_log('File name:')
    with open(a, 'w') as file:
        memory_file.seek(0)
        for i in memory_file.read().split('\n'):
            file.write(i+'\n')
        print_log('The log has been saved.')


def hardest_card():
    mistakes = dict_hard.values()
    try:
        max_errors = max(mistakes)
        hardest_keys = list(x for x, y in dict_hard.items() if y == max_errors)

        if max_errors == 0:
            print_log('There are no cards with errors.')

        elif len(hardest_keys) == 1:
            print_log(f'The hardest card is "{hardest_keys[0]}". You have {max_errors} errors answering it.')

        else:
            fin_str = ''
            for i in range(len(hardest_keys)):
                fin_str += f'"{hardest_keys[i]}", '
            fin_str = fin_str[:-2]
            print_log(f'The hardest cards are {fin_str}')
    except ValueError:
        print_log('There are no cards with errors.')


def reset_stats():
    for i in list(dict_hard.keys()):
        dict_hard[i] = 0
    print_log('Card statistics have been reset.')


args = parser.parse_args()


def import_start():
    if args.import_from is not None:
        with open(args.import_from, 'r') as opened_file:
            count = 0
            k = opened_file.readlines()
            for i in k:
                i = i.split(': ')
                dict_main[i[0]] = i[1].split('\n')[0]
                dict_hard[i[0]] = 0
                count += 1

            print_log(str(count) + ' cards have been loaded.')
    else:
        return


def export_to():
    if args.export_to is not None:
        with open(args.export_to, 'w') as f:
            for x, defn in dict_main.items():
                f.write(str(x) + ': ' + defn + '\n')
            print_log(str(len(dict_main.keys())) + ' cards have been saved')
    else:
        return


import_start()

while True:
    action = input_log('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n')
    if action == 'add':
        add()
    if action == 'remove':
        remove()
    if action == 'import':
        import_func()
    if action == 'export':
        export()
    if action == 'ask':
        ask()
    if action == 'exit':
        exit_func()
    if action == 'log':
        log()
    if action == 'hardest card':
        hardest_card()
    if action == 'reset stats':
        reset_stats()
