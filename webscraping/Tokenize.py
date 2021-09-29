import nltk
from langdetect import detect
import csv

class Tokenize:
    """ Text tokenizer """

    def __init__(self):
        """ Default constructor """

        self.language       = "en"
        self.workDirectory  = "/run/media/jf/Datos/Tourist Text Mining/datasets/colombia_en/"
        self.tagFilename    = "tags_en.csv"
        self.wfFilename     = "words_freq_en.csv"
        self.structFilename = "structure_en.csv"
        # http://www.lrec-conf.org/proceedings/lrec2012/pdf/274_Paper.pdf
        self.tagCategories_en = {
                'Adjective'   : ['ADJ', 'JJ', 'JJR', 'JJS'],
                'Adverb'      : ['ADV', 'RB', 'RBR', 'RBS', 'WRB'],
                'Conjunction' : ['CONJ', 'CC'],
                'Determiner'  : ['DET', 'DT', 'EX', 'PDT', 'WDT'],
                'Noun'        : ['NOUN', 'NN', 'NNP', 'NNPS', 'NNS'],
                'Numeral'     : ['NUM', 'CD'],
                'Particle'    : ['PRT', 'POS', 'RP', 'TO'],
                'Preposition' : ['ADP', 'IN'],
                'Pronoun'     : ['PRON', 'PRP', 'PRP$', 'WP', 'WP$'],
                'Punctuation' : ['.', '#', '$', "''", '”', '``', ',', '.', ':', "''", '(', ')', '-LRB-', '-RRB-'],
                'Verb'        : ['VERB', 'MD', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'],
                'X'           : ['X', 'FW', 'LS', 'SYM', 'UH'],
                }
        self.reviews       = []
        self.tokens        = []
        self.tags          = []
        self.entities      = []
        self.other         = []


    def getCategory(self, tag):
        """ Get the tag's category """

        for cat in self.tagCategories_en:
            if (tag in self.tagCategories_en[cat]):
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
        for tag in self.tags:
            for key, value in tag:
                found = False
                for i in range(0, len(fr)):
                    if (fr[i][0] == value):
                        fr[i][1] += 1
                        found = True
                        break
                if not found:
                    fr.append([value, 1])


    def wordFrequencies(self):
        """ Word Frequencies """

        wd = []
        for tag in self.tags:
            for key, value in tag:
                found = False
                for i in range(0, len(wd)):
                    if (wd[i][0].lower() == key.lower()):
                        wd[i][1] += 1
                        found = True
                        break
                if not found:
                    wd.append([key, 1])

        with open(self.workDirectory + self.wfFilename, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"')
            for w in wd:
                writer.writerow(w)


    def wordCategory(self):
        """ Word - category """

        cats = []
        for tag in self.tags:
            for key, value in tag:
                cats.append([key, self.getCategory(value)])

        for cat in self.tagCategories_en:
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