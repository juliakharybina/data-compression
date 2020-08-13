import random


class RandomText:
    def __init__(self, file_name):
        self.file_name=file_name

    def makeRandomText(self,i):
        f = open(self.file_name, 'r')
        s = f.read()
        rnd = random.randint(1, len(s) - (i * 100))
        s = s[rnd:(rnd + i * 100)]
        return s

    #main - myText = makeRandomText(2)
    #print(myText)