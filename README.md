# Spelling Correction Flask app

Creating a spelling correction app using the Flask web framework and Python port of SymSpell.

It takes input as a word (with a spelling mistake) and shows a list of correct words.

It corrects words that are merged (eg: "aboutthat", "quick🤗Assignment"), repetitive letters (eg: "awwwesome"), words separated by space or '-'.

## Dependencies

* SymSpell: (https://github.com/mammothb/symspellpy)
* Flask: (http://flask.pocoo.org/)

## Install guide

##### Clone the repo

```bash
git clone https://github.com/fdabhi/spellCorrect.git
```

##### Install dependencies
```bash
pip install -r requirements.txt
```

##### Demo
Heroku app - [SpellCorrect](https://spellcorrecttest.herokuapp.com/spellCorrect)
