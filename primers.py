from Bio.Seq import Seq
from Bio.SeqUtils import GC, MeltingTemp
from Bio.Alphabet import IUPAC, _verify_alphabet


class Primers():
    def __init__(self):
        self.primerMinLength = 17
        self.primerMaxLength = 25
        self.primerMinMeltTemp = 55
        self.primerMaxMeltTemp = 60
        self.primerMinGC = 50
        self.primerMaxGC = 60
        self.__sequence = ''

    def getSequence(self):
        return self.__sequence

    def setSequence(self, sequence):
        sequence = sequence.replace("\n", "")
        self.__sequence = Seq(sequence.upper(), IUPAC.unambiguous_dna)

    def checkInput(self):
        if not _verify_alphabet(self.__sequence):
            raise ValueError("De input mag alleen uit A, T, C of G bestaan.")

    def selectAnnealingArea(self, sequence, positionStart, positionEnd):
        """ Selects the annealing area and splits the sequence in 3 parts
            Annealingarea, 5end and 3 end
        Args:
            sequence (str) -- sequence to select annealing area on (revComp)DNA
            positionStart (int) -- start position of annealing area
            positionEnd (int) -- end position of annealing area
        Return: (tuple)
            sequence5end (str) -- first part of sequence - for finding primers
            sequence3end (str) -- last part of sequence - for finding primers
        """
        sequence5end = sequence[:positionStart + self.primerMaxLength]
        sequence3end = sequence[positionEnd:]
        sequenceAnnealingArea = sequence[positionStart:positionEnd]
        return sequence5end, sequence3end, sequenceAnnealingArea

    def findPrimers(self, sequence):
        """ Finds all primers based on length, GC content and melting Temp
        Args:
            sequence (str) -- 5'to'3 sequence
        Return:
            primers (list) -- list contains [primer sequence, melting temp, GC]
        """
        print("\n" + sequence)
        print("\n" + sequence.complement())
        primers = []

        for primerLength in range(self.primerMaxLength,
                                  self.primerMinLength-1,
                                  -1):
            """ Outer loop: loops through primer lengths.
                Decrements from 25 to 17 """

            for x in range(len(sequence)-primerLength):
                """ Inner loop: loops through sequence.
                    Increments position each iteration with 1 """
                possiblePrimer = sequence[0+x:primerLength+x]
                if self.primerMinMeltTemp\
                        <= MeltingTemp.Tm_Wallace(possiblePrimer)\
                        <= self.primerMaxMeltTemp:

                    if self.primerMinGC <= GC(possiblePrimer)\
                            <= self.primerMaxGC:

                        primers.append([possiblePrimer,
                                        MeltingTemp.Tm_Wallace(possiblePrimer),
                                        GC(possiblePrimer), primerLength, x])
            sequence = sequence[:-1]
        return primers
