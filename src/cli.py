import argparse
import pickle
import os


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
    parser.add_argument('file', type=str,
                        help='The file to edit/create WITHOUT extension')
    parser.add_argument('-g', '--generate',
                        help='Flag to generate a .tex file when done.')
    return parser.parse_args()


def load_stack(file_name):
    """Loads a notecard stack from the given file
    """
    return pickle.load(open(file_name, 'rb'))


def add_card(stack):
    """Adds a notecard to the given stack
    """
    raise NotImplementedError()


def edit_card(stack, card_name):
    """Edits a card in the given stack and name
    """
    raise NotImplementedError()


def generate_tex(stack, file_name):
    """Generates the tex for the given file and saves it
    """
    raise NotImplementedError()


def main():
    args = parse_args()

    stack = {}

    if args.mode == 'create':
        stack = {}

    elif args.mode == 'edit':
        if not os.path.exists(args.file + '.dat'):
            raise ValueError('The given file does not exist.')
        stack = load_stack(args.file + '.dat')

    else:
        raise ValueError('Expected "create" or "edit" for mode')

    pickle.dump(stack, open(args.file + '.dat', 'wb'))
    if args.generate:
        generate_tex(stack, args.file + '.tex')


if __name__ == '__main__':
    main()
