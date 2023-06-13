#!/bin/bash

# Spacy model for pos tagging, sentence parsing and tokenization
# Recommended: en_core_web_sm, en_core_web_lg
SPACY_MODEL='en_core_web_lg'

# Setup current environment with modules and libraries
# App modules
pip3 install autopep8 django django-admin dj_database_url psycopg2-binary bs4 nltk spacy spacy_fastlang pylast lyricsgenius \
             whitenoise djLint sqlalchemy wikipedia pyngrok
# Additional modules
pip3 install gunicorn zipp urllib3 typing-extensions toml text-unidecode static3 sqlparse six pytz PyJWT pyflakes pycparser \
             pycodestyle Pillow image flake8 Faker django-debug-toolbar django-crispy-forms django-allauth dj-static coverage
# Use Python to download libraries + Insert required code to lyricsgenius.genius
python3 -c "
import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')

import spacy
if '$SPACY_MODEL' not in spacy.util.get_installed_models():
    spacy.cli.download('$SPACY_MODEL')

import lyricsgenius
insert_code = \"\"\"        # inserted
        else:
            rem = div.find('div', class_=re.compile('Lyrics__Footer'))
            if rem:
                rem.replace_with('')

            header = div.find('h2', class_=re.compile('TextLabel'))
            if header:
                header.replace_with('')

            header2 = div.find('div', class_=re.compile('LyricsHeader'))
            if header2:
                header2.replace_with('')

\"\"\"

already_ins = False
with open(lyricsgenius.genius.__file__, 'r') as f:
    code = f.readlines()
    if '        # inserted\n' not in code:
        code.insert(144, insert_code)
    else:
        already_ins = True

if not already_ins:
    with open(lyricsgenius.genius.__file__, 'w') as f:
        f.writelines(code)
"