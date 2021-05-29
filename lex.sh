#!/bin/sh

# TODO : Update the wiktionry dump.

rm a.txt b.txt c.txt ;

grep -o "<title>[A-Za-z]\+</title>\|\*.*{{IPA|en|/.\+/}}\|==English" enwiktionary-latest-pages-articles.xml > a.txt ;

sed 's/}[,;]/}/g' a.txt | sed 's/{{enPR|[^}]*}},\? //g' > b.txt ;

cat b.txt | ./clean_redundant_lines.py > c.txt ;


