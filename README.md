# LaTeX Flash Card Maker

This repo contains source for making Flashcards with LaTeX and the ecards package.

### Setup

Install `texlive-full` and find the `texmf` directory on your drive, then run `./setup.sh <path/to/texmf>`
to install the necessary dependencies to generate electronic flashcards with LaTeX. 

## Use



#### Inner documentation

The structure of the generated tex file is given by `latex/template/main.tex`. Most notably, the actual notecard
stack will be defined inside of `stack.tex` in the form of commands. A list of the required commands are defined
below:


| Command Name | Description |
|--------------|-------------|
| `\stackTitle` | The title of the notecard stack |
| `\stackAuthor` | The author of the notecard stack |
| `\stackContent` | The actual notecards. Will be loaded inside of `document` |
|--------------|-------------|
