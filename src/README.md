# Python Development

The main goal of this is to create an application that easily adds notecards/quiz questions for the user that is
converted into the LaTeX that can be processed by ecards. Therefore, a naive file format is used that is kept
for the user to easily modify each notecard's front and back without more advanced LaTeX formatting. 

The user will generate the notecards, which are stored in a dict according to notecard name, then pickled to
a file. A different function will then unpickle the dict, generate the corresponding LaTeX, and attempt to
compile it.
