import argparse
import pickle
import os
import shutil

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
    parser.add_argument('-g', '--generate',
                        help='Flag to generate a .tex file when done.')
    return parser.parse_args()


def load_stack(file_name):
    """Loads a notecard stack from the given file
    """
    return pickle.load(open(file_name, 'rb'))


def input_stack_q(stack, key, question):
    """Querys the user for an answer about the stack
    and then places their answer in the given key
    """
    stack[key] = input(question + '\n')


def add_card(stack, save_filename):
    """Adds a notecard to the given stack and then saves the stack
    """
    raise NotImplementedError()


def edit_card(stack, card_name, save_filename):
    """Edits a card in the given stack and name, then saves the stack
    """
    raise NotImplementedError()


def edit_logic(stack, save_filename):
    """The editing logic of a particular stack. Called by both create
    and edit modes.
    """
    raise NotImplementedError()


def generate_tex(stack, file_name):
    """Generates the tex for the given file and saves it
    """
    raise NotImplementedError()


def main():
    args = parse_args()

    if not os.path.exists(args.folder):
        raise ValueError('The given folder does not exist')
    shutil.copyfile(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                 '..', 'latex', 'template', 'main.tex'),
                    os.path.join(args.folder, 'main.tex'))

    stack = {}
    save_stack_name = os.path.join(args.folder, 'stack.dat')
    save_tex_name = os.path.join(args.folder, 'stack.tex')

    try:
        if args.mode == 'create':
            stack = {}
            input_stack_q(stack, 'title', 'What is the title of this stack?')
            input_stack_q(stack, 'author', 'Who is the author of this stack?')
            pickle.dump(stack, open(save_stack_name, 'wb'))
            print('You have created a new stack. After you create a new card, '
                  'then the stack will save to ', save_stack_name, '. Exit '
                  'at anytime to quit editing the stack.')
            while True:
                edit_logic(stack, save_stack_name)
        elif args.mode == 'edit':
            if not os.path.exists(save_stack_name):
                raise ValueError('The given file does not exist.')
            stack = load_stack(save_stack_name)
            print('You have loaded ', stack['title'], '. After you create a '
                  'new card, then the stack will save to ', save_stack_name,
                  '. Exit at anytime to quit editing the stack.')
            while True:
                edit_logic(stack, save_stack_name)
        else:
            raise ValueError('Expected "create" or "edit" for mode')
    except KeyboardInterrupt:
        print('Exiting program. If you chose to generate latex.')
        if args.generate:
            generate_tex(stack, save_tex_name)


if __name__ == '__main__':
    main()
