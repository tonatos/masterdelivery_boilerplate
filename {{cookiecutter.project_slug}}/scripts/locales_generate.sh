#! /usr/bin/env bash


export $(grep -v '^#' .env | xargs -0)
LOCALE_DIR=./app/locales

for i in ${ACCEPT_LANGUAGES//,/ }
do
    # call your procedure/other scripts here below
    mkdir -p ${LOCALE_DIR}/${i}
    mkdir -p ${LOCALE_DIR}/${i}/LC_MESSAGES
    msginit --no-translator -i ${LOCALE_DIR}/${GETTEXT_DOMAIN}.pot --locale=${i} -o ${LOCALE_DIR}/${i}/LC_MESSAGES/${GETTEXT_DOMAIN}.po
done