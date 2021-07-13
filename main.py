from random import seed
from random import random
import os
import sys
import time


nucleotide = ('A', 'C', 'G', 'T')

# Classe che si occupa della generazione casuale di valori
class RandomGenerator():

    def __init__(self, distribuzione: tuple, g_value: float):
        self.boundaries = [0.0, 0.0, 0.0, 1.0]
        self.g_value = g_value
        tot = 0
        for i in range(3):
            tot = tot + distribuzione[i]
            self.boundaries[i] = tot

    def getNextBase(self):
        seed(time.time() / 1000)
        random_value = random()

        if random_value < self.boundaries[0]:
            return  0
        elif random_value < self.boundaries[1]:
            return  1
        elif random_value < self.boundaries[2]:
            return 2
        elif random_value < self.boundaries[3]:
            return 3

    def getNextBernulliValue(self):
        random_value = random()
        if random_value < self.g_value:
            return True
        else:
            return False


def buildDatasetUsingDistribution(outputPath: str, numeroSequenze: int, lunghezzaSequenza: int, distribuzione: tuple, prefisso):
    rg = RandomGenerator(distribuzione, 0.25)
    sequenza_riferimento = ''

    for j in range(lunghezzaSequenza):
        valore_base = rg.getNextBase()
        sequenza_riferimento = sequenza_riferimento + nucleotide[valore_base]

    saveSequence(prefisso +"-riferimento", sequenza_riferimento, outputPath)

    for i in range(numeroSequenze):

        sequenza_generata = ''
        rg = RandomGenerator(distribuzione, 0.25)
        for j in range(lunghezzaSequenza):
            valore_base = rg.getNextBase()
            sequenza_generata = sequenza_generata + nucleotide[valore_base]


        saveSequence(prefisso + "-sequenza" + str(i), sequenza_generata, outputPath+"/individui")


def buildDatasetPatternTransfer(lunghezzaSequenza: int, probSostituzione: float, inputPath: str):
    random_generator = RandomGenerator((0, 0, 0, 1), probSostituzione)
    file_sequenza_riferimento = open(inputPath+"/Null-Model-riferimento.fa", "r")
    sequenza_riferimento = list(file_sequenza_riferimento.read().split("\n")[1])



    nomi_file_sequenze = os.listdir(inputPath+"/individui")

    for i, nome_file in enumerate(sorted(nomi_file_sequenze)):
        nuova_sequenza_individuo = ""
        file_sequenza_individuo = open(inputPath+"/individui/"+nome_file, "r")
        sequenza_individuo = list(file_sequenza_individuo.read().split("\n")[1])
        nuova_sequenza_individuo = nuova_sequenza_individuo.join(patternTransfer(sequenza_riferimento, sequenza_individuo, lunghezzaSequenza, random_generator))

        saveSequence("PatternTransfer-sequenza" + str(i), nuova_sequenza_individuo, inputPath + "/individui-patternTransfer")





def patternTransfer(seqRiferimento:list, sequenzaAlternativa:list, lunghezzaPattern: int, rg: RandomGenerator):
    testina = 0
    contatore_sottosequenza = 0

    while testina < (len(sequenzaAlternativa) - lunghezzaPattern):
        bd = rg.getNextBernulliValue()
        if(bd):
            for k in range(lunghezzaPattern):
                sequenzaAlternativa[testina] = seqRiferimento[testina]
                testina = testina + 1
            contatore_sottosequenza = contatore_sottosequenza + 1

        else:
            testina = testina + 1

    return sequenzaAlternativa

def saveSequence(nomeSequenza: str, sequenza: str, outputPath: str):
    if not os.path.exists(outputPath):
        os.mkdir(outputPath)
    file = open(outputPath+"/"+nomeSequenza+".fa", 'w')
    file.write(">" + nomeSequenza + '\n' + sequenza)


if __name__ == "__main__":

    args = sys.argv

    if len(args) < 3:
        print("Usage:", "main.py numero_sequenze lunghezza_sequenza output_path")
        exit()

    buildDatasetUsingDistribution(args[3], int(args[1]), int(args[2]), (0.25, 0.25, 0.25, 0.25), "Null-Model")
    buildDatasetPatternTransfer(4, 0.5, ".")