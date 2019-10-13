import json
from nltk.corpus import wordnet as wn
import urllib.request
from nltk.tag import pos_tag


"""
def main():
    down = [(1, 'BOXER'), (2, 'ARENA'), (3, 'AGLET'), (4, 'CAT'), (5, 'IST')]
    across = [(1, 'BAA'), (4, 'CORGI'), (5, 'AXELS'), (6, 'TENET'), (7, 'RAT')]

    new_down_clues, new_across_clues = generate_clues(down, across)
    
    print(new_down_clues)
    print(new_across_clues)
    """

def extract_solutions(cells):
    down = []
    across = []
    
    # Extracting down solutions
    for i in range(5):
        solution = ''
        key = 0
        for j in range(5):
            index = i + 5 * j
            if cells[index]["key"] is not None and key == 0:
                key = cells[index]["key"]
            
            if cells[index]["letter"] is not None:
                solution += cells[index]["letter"]
            
        down.append((key, solution))
        
    # Extracting across solutions
    for i in range(5):
        solution = ''
        key = 0
        for j in range(5):
            index = 5*i + j
            if cells[index]["key"] is not None and key == 0:
                key = cells[index]["key"]
                
            if cells[index]["letter"] is not None:
                solution += cells[index]["letter"]
                
        across.append((key, solution))

    down = sorted(down, key= lambda x: x[0])
    across = sorted(across, key=lambda x: x[0])
    
    return down, across





def generate_clues(down, across):
    new_down_clues = []
    new_across_clues = []
    
    solution_container = down + across
    
    for i in range(len(solution_container)):
        key, solution = solution_container[i]
        new_clue = try_wordnet(solution)
        if new_clue == None:
            new_clue = try_urban_dict(solution)
        
        if new_clue == None:
            new_clue = try_merriam_webster(solution)
        
        if new_clue == None:
            new_clue = try_rhyme(solution)
        
        if new_clue == None:
            new_clue = "Could not generate clue"
        
        if i < 5:
            new_down_clues.append((key, new_clue))
        else:
            new_across_clues.append((key, new_clue))
            
    return new_down_clues, new_across_clues


def try_wordnet(solution):
    print("Searching for new clue for {0} in Wordnet...".format(solution))
    
    synset = wn.synsets(solution)
    if not synset:
        print("Wordnet gave no result...")
        return None
                
    new_clue = synset[0].definition()
    return clean(new_clue, solution)



def try_urban_dict(solution):
    print("Searching for new clue for {0} in Urban Dictinary...".format(solution))
    
    with urllib.request.urlopen("http://api.urbandictionary.com/v0/define?term={" + solution + "}") as url:
        dictAPI = json.loads(url.read().decode())
    
    if not dictAPI['list']:
        print("Urban Dictionary gave no result...")
        return None
    
    new_clue = dictAPI['list'][0]['definition']
    return clean(new_clue, solution)



def try_merriam_webster(solution):
    print("Searching for new clue for {0} in Merriam Webster...".format(solution))
    link = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/" + solution + "?key=3d58f945-743a-4611-8c3c-229dde491cb3"
    with urllib.request.urlopen(link) as url:
        dictAPI = json.loads(url.read().decode())
    
    if not isinstance(dictAPI[0], dict):
        print("Merriam Webster gave no result...")
        return None

    new_clue = dictAPI[0]['shortdef'][0]
    
    return clean(new_clue, solution)

def try_rhyme(solution):
    print("Finding a rhyming word...")
    
    with urllib.request.urlopen("https://api.datamuse.com/words?rel_rhy=" + solution) as url:
        dictAPI = json.loads(url.read().decode())
    
    if not dictAPI:
        print("Rhyming failed...")
        return None
    
    tag = pos_tag(solution.split())[0][1] 
    new_clue = word_type(tag) + ",  rhymes with " + dictAPI[0]['word']
    return new_clue



def clean(new_clue, solution):
    new_clue = new_clue.rstrip()
    new_clue = new_clue.replace('\n', ' ').replace('\r', '')
    
    while True:    
        index = new_clue.find("(")
        if index >= 0:
            subs = new_clue[index:new_clue.find(")") + 1]
            new_clue = new_clue.replace(subs, "")
        else: 
            index = new_clue.find(")")
            if index >= 0:
                new_clue = new_clue[index+1:]
            else:
                break
    
    started = False
    while not started:
        if not new_clue[0].isalpha():
            new_clue = new_clue[1:len(new_clue)]
        else:
            started = True
    
    index = new_clue.find(";")
    if index > 0:
        new_clue = new_clue[:index]
    
    index = new_clue.find(".")
    if index >= 0:
        if len(new_clue)-1 > index and new_clue[index+1] == "\"":
            new_clue = new_clue[0:index+1]
        else:
            new_clue = new_clue[0:index]

    """index = new_clue.find("which")
    if index >= 0:
        new_clue = new_clue[0:index]"""
         
        
    new_clue = new_clue.replace("[", "")
    new_clue = new_clue.replace("]", "")
    new_clue = new_clue.replace(solution, "___")
    
    if len(new_clue) > 140:
        index = new_clue.rfind(",", 0, 140)
        if index > 0:
            new_clue = new_clue[:index]
        else:
            index = new_clue.rfind(" ", 0, 140)
            new_clue = new_clue[:index]
    
    return new_clue.capitalize()

def word_type(tag):
    tagset = {
            'CC': 'coordinating conjunction',
            'CD': 'cardinal digit',
            'DT': 'determiner',
            'EX': 'existential there',
            'FW': 'foreign word',
            'IN': 'preposition/subordinating conjunction',
            'JJ': 'adjective',
            'JJR': 'adjective, comparative',
            'JJS':	'adjective, superlative',
            'LS': 'list marker',
            'MD': 'modal',
            'NN': 'noun, singular',
            'NNS': 'noun plural',
            'NNP': 'proper noun, singular',
            'NNPS': 'proper noun, plural',
            'PDT': 'predeterminer',
            'POS': 'possessive ending',
            'PRP': 'personal pronoun',
            'PRP$': 'possessive pronoun',
            'RB': 'adverb',
            'RBR': 'adverb, comparative',
            'RBS': 'adverb, superlative',
            'RP': 'particle',
            'TO': 'to',	
            'UH': 'interjection',
            'VB': 'verb, base form',
            'VBD':	'verb, past tense',
            'VBG':	'verb, gerund/present participle',
            'VBN': 'verb, past participle',
            'VBP': 'verb',
            'VBZ': 'verb',
            'WDT': 'wh-determiner',
            'WP': 'wh-pronoun',
            'WP$': 'possessive wh-pronoun',
            'WRB':	'wh-abverb'
            }
    
    return tagset[tag].capitalize()

"""
if __name__ == "__main__":
    main()
    """
