import argparse
import random
import os
import pickle
import shutil
from subprocess import run


"""
This is the command line interface latexflashcards. It can either generate a
new flashcard set, modify an existing one, or generate the pdf of a file.
"""


def parse_args():
    parser = argparse.ArgumentParser(
        description='Create a LaTeX flashcard stack')
    parser.add_argument('mode', type=str,
                        help='The mode to launch in. Choice of create or edit'
                             '; which will create a new stack or edit an '
                             'existing one.')
    parser.add_argument('folder', type=str,
                        help='The folder to place the generated files in')
    parser.add_argument('-t', '--generate_tex', action='store_true',
                        help='Flag to generate a .tex file when done.')
    parser.add_argument('-g', '--generate_pdf', action='store_true',
                        help='Flag to generate the main.pdf file when done. ')
    parser.add_argument('-d', '--display', action='store_true',
                        help='Flag to determine whether the loaded stack is '
                             'displayed prior to editing.')
    parser.add_argument('-r', '--reorder', action='store_true',
                        help='Flag whether to remove flashcard functionality '
                             'and simply reorder the pdf pages.')
    return parser.parse_args()


def load_stack(file_name):
    """Loads a notecard stack from the given file
    """
    stack = pickle.load(open(file_name, 'rb'))
    for card_name in stack:
        if len(stack[card_name]) == 3:
            stack[card_name].append('')
        if len(stack[card_name]) == 4:
            stack[card_name].append([])
    return stack


def input_stack_q(stack, key, question):
    """Querys the user for an answer about the stack
    and then places their answer in the given key
    """
    stack[key] = input(question + '\n')


def edit_card(stack, card_name):
    """Edits (a possibly new) card with name card_name
    """
    typ = input('\tModifying card ' + card_name + '. Is it a MC? (y/n)\n')
    while typ != 'y' and typ != 'n':
        typ = input('\tError: Not y/n input. Retry input\n')

    if typ == 'y':
        ques = input('\tUsing a MC card. What is the question?\n')
        n_ans = int(input('\tHow many answers are there?\n'))
        ans = []
        ans.append(input('\tEnter the correct answer:\n'))
        for _ in range(1, n_ans):
            ans.append(input('\tEnter an incorrect answer:\n'))
        explanation = input('\tEnter the explanation:\n')
        order = []
        ord_str = input('\tEnter the sequence of the index of answers:\n')
        if len(ord_str) > 0:
            order = [int(idx) for idx in ord_str.split(',')]
        stack[card_name] = [typ == 'y', ques, ans, explanation, order]
    else:
        front = input('\tNot a MC card. What is the front of the card?\n')
        back = input('\tWhat is the back of the card?\n')
        stack[card_name] = [typ == 'y', front, [back], '', []]
    return stack


def edit_logic(stack, save_filename):
    """The editing logic of a particular stack. Called by both create
    and edit modes. Saves the stack at the end of editing.
    """
    card_name = input('Enter the name of the next card you\'d like to edit '
                      'or create:\n')
    if card_name in stack:
        print('\t', card_name, ' already exists and is ', stack[card_name])
        idx = int(input('\tWhich index do you want to modify?\n'))
        if idx == 2:
            idx = int(input('\tWhich answer index do you want to modify?\n'))
            stack[card_name][2][idx] = input('\tEnter the new answer:\n')
        elif idx == 4:
            ord_str = input('\tEnter the new answer order sequence:\n')
            if len(ord_str) == 0:
                stack[card_name][4] = []
            else:
                stack[card_name][4] = [int(idx) for idx in ord_str.split(',')]
        else:
            stack[card_name][idx] = input('\tEnter the new value:\n')
    else:
        stack = edit_card(stack, card_name)
    pickle.dump(stack, open(save_filename, 'wb'))
    return stack


def generate_cards_tex(stack, folder_name):
    """Generates the tex for the cards in the stack
    """
    content_tex = """\documentclass{standalone}

\\begin{document}
                  """
    for card_name, card_content in stack.items():
        if card_name[:2] == 'M:':
            continue

        if not card_content[0]:
            card_tex = """\\begin{{card}}
  {0}
  \\begin{{response}}
    \\begin{{answer}}
      {1}
    \\end{{answer}}
  \\end{{response}}
\\end{{card}}
                       """.format(card_content[1], card_content[2][0])

            content_tex += '\n' + card_tex

        else:
            full_q = card_content[1] + '\n\\hspace{1cm}\n' + \
                     '\\begin{multiChoice}{' + \
                     str(len(card_content[2])) + '}\n'
            perm = list(range(len(card_content[2])))
            if len(card_content[4]) == 0:
                random.shuffle(perm)
            else:
                perm = card_content[4]
            for i in perm:
                full_q += '\Ans{0} {1} & '.format(str(int(i == 0)),
                                                  card_content[2][i])
            full_q = full_q[:-2] + '\n\\end{multiChoice}\n'

            card_tex = """\\begin{{card}}
  {0}
  \\begin{{response}}
    \\begin{{answer}}
      {1}
    \\end{{answer}}
  \\end{{response}}
\\end{{card}}
                       """.format(full_q, card_content[2][0] + '. ' +
                                  card_content[3])

            content_tex += '\n' + card_tex

        content_tex += '\n'
    content_tex += "\\end{document}"
    with open(os.path.join(folder_name, "stack.tex"), "w") as tex_file:
        tex_file.write(content_tex)


def generate_tex(stack, folder_name):
    """Generates the tex for the given file and saves it
    """
    if not os.path.exists(os.path.join(folder_name, 'preamble.tex')):
        with open(os.path.join(folder_name, 'preamble.tex'), 'w') as tex_file:
            tex_file.write('\\newcommand\\stackTitle{' +
                           stack['M:title'] + '}\n\n')
            tex_file.write('\\newcommand\\stackAuthor{' +
                           stack['M:author'] + '}\n\n')
    generate_cards_tex(stack, folder_name)


def generate_pdf(stack, folder_name):
    """Generates the pdf and reorders it for a tex
    """
    run('pdflatex {0}main.tex'.format(folder_name), shell=True)
    run('pdflatex {0}printable.tex'.format(folder_name), shell=True)

def display_stack(stack):
    """Displays the stack in a nice way
    """
    for card_name, card_content in stack.items():
        print(card_name, ':\n\t', card_content)


def main():
    args = parse_args()

    if not os.path.exists(args.folder):
        raise ValueError('The given folder does not exist')
    shutil.copyfile(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                 '..', 'latex', 'template', 'main.tex'),
                    os.path.join(args.folder, 'main.tex'))
    shutil.copyfile(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                 '..', 'latex', 'template', 'printable.tex'),
                    os.path.join(args.folder, 'printable.tex'))

    stack = {}
    save_stack_name = os.path.join(args.folder, 'stack.dat')

    try:
        if args.mode == 'create':
            stack = {}
            input_stack_q(stack, 'M:title', 'What is the title of the stack?')
            input_stack_q(stack, 'M:author', 'Who is the author of the stack?')
            pickle.dump(stack, open(save_stack_name, 'wb'))
            print('You have created a new stack. After you create a new card, '
                  'then the stack will save to ', save_stack_name, '. Exit '
                  'at anytime to quit editing the stack.')
            while True:
                stack = edit_logic(stack, save_stack_name)
        elif args.mode == 'edit':
            if not os.path.exists(save_stack_name):
                raise ValueError('The given file does not exist.')
            stack = load_stack(save_stack_name)
            if args.display:
                display_stack(stack)
            print('You have loaded ', stack['M:title'], '. After you create a '
                  'new card, then the stack will save to ', save_stack_name,
                  '. Exit at anytime to quit editing the stack.')
            while True:
                stack = edit_logic(stack, save_stack_name)
        else:
            raise ValueError('Expected "create" or "edit" for mode')
    except KeyboardInterrupt:
        print('Exiting program.')
        if args.generate_tex:
            generate_tex(stack, args.folder)
        if args.generate_pdf:
            generate_tex(stack, args.folder)
            generate_pdf(stack, args.folder)
        if args.reorder:
            n_questions = len(stack.keys()) - 2
            page_order = '1 ' + ' '.join([str(2 + i) + ' ' 
                                          + str(2 + i + n_questions)
                                          for i in range(n_questions)])
            run('pdftk {0}main.pdf cat {1} output {0}printable_main.pdf'
                 .format(args.folder, page_order), shell=True)

if __name__ == '__main__':
    main()
