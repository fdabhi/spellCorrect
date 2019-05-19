# -*- coding: utf-8 -*-
"""
Created on Sun May 19 00:35:12 2019

@author: Abhi-Win10
"""

from flask import Flask, request, jsonify, render_template
import os
from symspellpy.symspellpy import SymSpell, Verbosity 
import re

def correction(input_term):

    # create object
    sym_spell = SymSpell()
    # load dictionary
    dictionary_path = os.path.join(os.path.dirname(__file__),
                                   "frequency_dictionary_en_82_765.txt")
    term_index = 0  # column of the term in the dictionary text file
    count_index = 1  # column of the term frequency in the dictionary text file
    if not sym_spell.load_dictionary(dictionary_path, term_index, count_index):
        print("Dictionary file not found")
        return

    max_edit_distance_lookup = 2
    suggestion_verbosity = Verbosity.CLOSEST  # TOP, CLOSEST, ALL
    suggestions = sym_spell.lookup(input_term, suggestion_verbosity,
                                   max_edit_distance_lookup)

    suggestions.extend(sym_spell.lookup_compound(input_term,
                                            max_edit_distance_lookup))

    suggestions = sorted(suggestions, key = lambda x: (x.distance))
    
    #to remove dupicate objects
    import collections
    seen = collections.OrderedDict()
    for obj in suggestions:
        if obj.term not in seen:
           seen[obj.term] = obj
    
    suggestions = list(seen.values())

    #when the no correction is needed
    seen = collections.OrderedDict()
    for obj in suggestions:
        if obj.term != input_term:
           seen[obj.term] = obj
    
    correctWords = list(seen.values())
    if len(correctWords)==0:
        return
    
#    for suggestion in suggestions:
#        print("{}, {}, {}".format(suggestion.term, suggestion.distance,
#                                  suggestion.count))
    return suggestions

def shorten_word(input_term):
    
    pattern = re.compile(r"(.)\1{2,}")
    return pattern.sub(r"\1\1", input_term)


def remove_emoji(string):
    # Emojis pattern
    emoji_pattern = re.compile("["
                    u"\U0001F600-\U0001F64F"  # emoticons
                    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                    u"\U0001F680-\U0001F6FF"  # transport & map symbols
                    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                    u"\U00002702-\U000027B0"
                    u"\U000024C2-\U0001F251"
                    u"\U0001f926-\U0001f937"
                    u'\U00010000-\U0010ffff'
                    u"\u200d"
                    u"\u2640-\u2642"
                    u"\u2600-\u2B55"
                    u"\u23cf"
                    u"\u23e9"
                    u"\u231a"
                    u"\u3030"
                    u"\ufe0f"
        "]+", flags=re.UNICODE)
    
    return emoji_pattern.sub(r'', string)

def spellcheck(input_term):
    #input_term = "home🤗Assignment"
    input_term = remove_emoji(input_term)
    input_term2 = shorten_word(input_term)
    suggestions = correction(input_term2)
    if suggestions is None:
        if input_term2 == input_term:
            #print("No Correction!")
            return []
        else:
            #print(input_term2)
            return [input_term2]
    
    return [s.term for s in suggestions]

app = Flask(__name__)

@app.route('/spellCorrect', methods= ["GET", "POST"])
def homepage():
    if request.method == 'POST':
        word = request.form.get('word')
        if word:
            return jsonify(result=spellcheck(word))
        else:
            return jsonify(result='Input needed')

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)