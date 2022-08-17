#! /usr/bin/env bash

LOCALE_DIR=./app/locales

for f in ${LOCALE_DIR}/*; do
    if [ -d "$f" ]; then
        lang="${f##*/}"
        echo "Compile $lang locale"
        msgfmt -o ${LOCALE_DIR}/${lang}/LC_MESSAGES/base.mo ${LOCALE_DIR}/${lang}/LC_MESSAGES/base
    fi
done
