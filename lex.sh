#!/bin/sh

# TODO : Update the wiktionry dump.

rm a.txt b.txt c.txt 2> /dev/null ;

grep -o "<title>[A-Za-z]\+</title>\|^\*.*{{IPA|en|/.\+/}}\|^==English" \
enwiktionary-latest-pages-articles.xml > a.txt ;

cat a.txt | sed 's/^\*\+/\*/' | sed 's/{{[^aI][^|]*|[^}]*}},\?\s*//g' | \
sed 's/}}\s\?[^\s]\+\s\?{{/}} {{/g' | sed 's/^*\+\s\+[A-Za-z]\+.*{{/* {{/' | \
sed 's/}}[^{]\+$/}}/' | sed 's/IPAchar/IPA/' | sed 's/IPA|\//IPA|en|\//' > b.txt ;

cat b.txt | ./clean_redundant_lines.py > c.txt ;

cat c.txt | ./build_json.py > ipa_dictionary.json ;

rm a.txt b.txt c.txt 2> /dev/null ;

