import emoji

class Emoticon:


    def __init__(self):
        self.freq = []


    def frequency(self, character, text):
        found = False
        for index in range(0, len(self.freq)):
            if (character == self.freq[index][0]):
                found = True
                self.freq[index][2] += 1
        if not found:
            self.freq.append([character, text, 1])


    def replaceEmoji(self, inputFilename, outputFilename):
        with open(outputFilename, 'w') as outputFile, open(inputFilename, 'r') as inputFile:
            for inputLine in inputFile:
                outputLine = ""
                for character in inputLine:
                    if (outputLine == "") :
                        character = character.upper()
                    if character in emoji.UNICODE_EMOJI:
                        outputLine += " (EMOJI " + emoji.demojize(character).upper() + ")"
                        self.frequency(character, emoji.demojize(character))
                    else:
                        outputLine += character
                if (outputLine[len(outputLine) - 2] != "."):
                    outputLine = outputLine[ : -1] + "."
                    outputLine += "\n"
                outputFile.write(outputLine)
