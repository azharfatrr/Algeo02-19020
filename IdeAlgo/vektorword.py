class wordTuple:
    def __init__(self):
        self.vektor = []
    
    def push(self, string):
        temp = data()
        if (len(self.vektor) == 0):
            temp.word = string
            temp.freq = 1
            self.vektor.append(temp)
            return
        found = False
        for i in range(len(self.vektor)):
            if (self.vektor[i].word == string):
                self.vektor[i].freq += 1
                found = True
        if (not found):
            temp.word = string
            temp.freq = 1
            self.vektor.append(temp)    
    def show(self):
        print("[", end="")
        for i in range(len(self.vektor)):
            if (i != len(self.vektor)-1):
                print(self.vektor[i].word + " " + str(self.vektor[i].freq), end=",")
            else:
                print(self.vektor[i].word + " " + str(self.vektor[i].freq),end="]")
        
        print()

class data:
    def __init__(self):
        self.word =""
        self.freq = 0

words = input()
word = words.split()
tempe = wordTuple()
for i in range(len(word)):
    print(word[i])
    tempe.push(word[i])

tempe.show()