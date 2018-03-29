### LaTeX Flash Card Maker

This repo contains source for making Flashcards with LaTeX and the ecards package.

#### Notes to Self

Navigate to local `texmf` folder.

```
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
cd ..
```
