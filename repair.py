from collections import Counter
class RePair:
    def __init__(self, str):
        self.str=str

    def findMFD(self, s):
        words = s.split(' ')  # string to words
        bigrams = zip(s, s[1:])  # making digrams
        counts = Counter(bigrams)  # counting digrams
        res = counts.most_common()[0]
        t = ''.join(res[0])  # from tuple to string
        return str(t)

    def replaceMFD(self, digram, s, nonT):  # replaces all occurrences of a given most frequent digram by a nonterminal
        return s.replace(digram, nonT)

    def repair(self, s, ch, d):
        while True:  # repeat until no pair occurs>1 time
            #words = s.split(' ')  # string to words
            bigrams = zip(s, s[1:])  # making bigrams

            counts = Counter(bigrams)  # counting bigrams
            res = counts.most_common()[0]  # Return a list of the n most common elements and their counts
            digram = ''.join(res[0])

            s = s.replace(digram, ch)  # replace digram to nonTerminal

            d[ch] = digram  # put digram with nonterminal symbol to dictionary
            # print(res[1])
            if res[1] == 1:  # when our first element occurs only once in the list we go out
                return d, s
                break
            else:
                ch = chr(ord(ch) + 1)  # changing nonterminals
                # repair(s,ch, d) #when there are digrams to replace, we again call the function

        # print(res[2])
        # s.replace(digram, nonT)

    def encode(self, rules, symb):
        if symb.islower():
            return symb
        else:
            symb = rules[symb] + encode(rules, rules[symb])

    def func(self, s):
        for i in s:
            if (i.isupper()):
                return True
        return False

    def decomp(self, rules, s):
        sNew = ''
        while func(s):  # repeat this until all the letters are small
            # print(s);
            for i in s:
                if i.isupper():
                    sNew = sNew + rules[i]
                if i.islower():
                    sNew = sNew + i
            s = sNew
            sNew = ''
        return s