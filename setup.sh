#!/bin/bash

##################################
#### Database setup (~760 MB) ####
##################################
# 1. Install PostgreSQL
# 2. Move to lastfm_RS and execute: make restore_db
# Done! The database will be created and populated

#############################################
#### Recommendation data setup (~500 MB) ####
#############################################
# > Move to lastfm_RS and execute: make recsys_data
# Done! This extracts the preprocessed dataset into lastfm_RS/backend/research/recbole_research/saved/
# Otherwise, the data needs to be preprocessed, which takes considerable time and memory


# Conda environment name
ENV_NAME='lastfm_venv'

# Spacy model for pos tagging, sentence parsing and tokenization
# Recommended: en_core_web_sm, en_core_web_lg
SPACY_MODEL='en_core_web_lg'

# Setup conda environment with modules and libraries
eval "$(conda shell.bash hook)"
conda env create -f environment.yml -n $ENV_NAME
conda activate $ENV_NAME

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

printf "\nAll done! Activate the environment with: conda activate $ENV_NAME\n"