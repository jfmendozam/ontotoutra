import nltk
from langdetect import detect
import csv

class Tokenize:
    """ Text tokenizer """

    def __init__(self):
        """ Default constructor """

        self.language       = "es"
        self.workDirectory  = "/home/jf/Documentos/phd/thesis/intership/dev/tourist text mining/datasets/colombia_es/4 tagging/hotel/"
        self.tagFilename    = "honr_o.txt"
        self.wfFilename     = "words_negative_freq_es.csv"
        self.structFilename = "structure_es.csv"
        # http://universaldependencies.org/tagset-conversion/es-conll2009-uposf.html
        self.tagCategories_es = {
                'Adjective'   : ['A'],
                'Adverb'      : ['R'],
                'Conjunction' : ['C'],
                'Determiner'  : ['D'],
                'Interjection': ['I'],
                'Noun'        : ['N', 'W'],
                'Numeral'     : ['Z'],
                'Preposition' : ['S'],
                'Pronoun'     : ['P'],
                'Punctuation' : ['F'],
                'Verb'        : ['V'],
                'X'           : ['X', 'FW', 'LS', 'SYM', 'UH'],
                }
        self.reviews       = []
        self.tokens        = []
        self.words         = []
        self.tags          = []
        self.entities      = []
        self.other         = []


    def getCategory(self, tag):
        """ Get the tag's category """

        for cat in self.tagCategories_es:
            if (tag in self.tagCategories_es[cat]):
                return(cat)
        return("")


    def tokenizing(self):
        """ Text tokenizer """

        self.tokens   = []
        self.tags     = []
        self.entities = []
        self.other    = []

        for review in self.reviews:
            try:
                if (detect(review) == self.language):
                    token = nltk.word_tokenize(review)
                    tag = nltk.pos_tag(token)
                    entity = nltk.chunk.ne_chunk(tag)

                    self.tokens.append(token)
                    self.tags.append(tag)
                    self.entities.append(entity)
                else :
                    self.other.append(review)
            except Exception as e:
                continue

        with open(self.workDirectory + self.tagFilename, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"')

            for tag in self.tags:
                for value in tag:
                    writer.writerow(value)


    def tagFrequencies(self):
        """ Tag Frequencies """

        fr = []
        with open(self.workDirectory + self.tagFilename, 'r') as tagFile:
            for line in tagFile:
                fields = line.split()
                if (len(fields) > 3):
                    found = False
                    for i in range(0, len(fr)):
                        if (fr[i][0] == fields[2][0]):
                            fr[i][1] += 1
                            found = True
                            break
                    if not found:
                        fr.append([fields[2][0], 1])
        self.tags = []
        for freq in fr:
            for key, value in self.tagCategories_es.items():
                if (freq[0] in value):
                    self.tags.append([key, freq[0], freq[1]])
                    break


    def wordFrequencies(self):
        """ Word Frequencies """

        fr = []
        with open(self.workDirectory + self.tagFilename, 'r') as tagFile:
            for line in tagFile:
                fields = line.split()
                if (len(fields) > 3):
                    found = False
                    for i in range(0, len(fr)):
                        if (fr[i][0] == fields[0].lower() and fr[i][2] == fields[2][0]):
                            fr[i][3] += 1
                            found = True
                            break
                    if not found:
                        fr.append([fields[0].lower(), fields[1], fields[2][0], 1])
        self.words = []
        for freq in fr:
            for key, value in self.tagCategories_es.items():
                if (freq[2] in value):
                    self.words.append([freq[0], freq[1], freq[2], key, freq[3]])
                    break

        with open(self.workDirectory + self.wfFilename, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"')
            for w in self.words:
                writer.writerow(w)


    def wordCategory(self):
        """ Word - category """

        cats = []
        for tag in self.tags:
            for key, value in tag:
                cats.append([key, self.getCategory(value)])

        for cat in self.tagCategories_es:
            with open(self.workDirectory + "_" + cat + '.csv', 'w') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quotechar='"')
                for i in cats:
                    if (i[1] == cat):
                        writer.writerow(i)


    def getRules(self):
        """ Get rules """

        rules = []
        for tag in self.tags:
            s = ""
            for w, t in tag:
                s += self.getCategory(t) + " "
                if (t == '.' or t == ','):
                    rules.append(s)
                    s = ""
            if (len(s) > 0):
                rules.append(s)

        with open(self.workDirectory + self.structFilename, 'w') as csvfile:
            for rule in rules:
                csvfile.write("%s\n" % rule)

#from Tokenize import Tokenize
#tk = Tokenize()
#tk.reviews = reviews
#tk.language = "es"
#tk.workDirectory = "/run/media/jf/Datos/Tourist Text Mining/datasets/colombia_es/"
#tk.tagFilename = "location_tags_es.csv"
#tk.wfFilename = "location_words_freq_es.csv"
#tk.structFilename = "location_structure_es.csv"
#tk.tokenizing()