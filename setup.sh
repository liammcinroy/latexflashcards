if [$# == 0 || $# > 1]; then
    echo "Description: Setup the dependencies necessary for latexflashcards"
    echo "Usage: $0 texmf-loc"
    echo "texmf-loc: The location of the texmf directory used by latex"
    exit 1
fi

home=pwd
cd $1
wget http://mirrors.ctan.org/macros/latex/contrib/conv-xkv.zip
unzip conv-xkv.zip && rm conv-xkv.zip
cd conv-xkv/ && pdflatex conv-xkv.ins
cd ..
wget http://mirrors.ctan.org/macros/latex/contrib/ecards.zip
unzip ecards.zip && rm ecards.zip
cd ecards/ && pdflatex ecards.ins
cd ..
wget http://mirrors.ctan.org/macros/latex/contrib/acrotex.zip
unzip acrotex.zip && rm acrotex.zip
cd acrotex/ && pdflatex acrotex.ins
cd $home
