
class BinaryBWT:
    def __init__(self, str):
        self.str=str


    def DNA2binary(self, s):
        bString = ''
        for ch in s :
            if ch == 'A':
                bString += '00';
            elif ch == 'C':
                bString += '01';
            elif ch == 'G':
                bString += '10';
            elif ch == 'T':
                bString += '11';
            else:
                print("Wrong Letter!")
        return bString

    def binary2DNA(self, bString):
        s = ''
        # a = [['00','01', '10', '11'],['A','C', 'G', 'T']]
        pointer = 0
        while pointer < len(bString) - 1:
            if bString[pointer] == '0' and bString[pointer + 1] == '0':
                s += 'A'
            elif bString[pointer] == '0' and bString[pointer + 1] == '1':
                s += 'C'
            elif bString[pointer] == '1' and bString[pointer + 1] == '0':
                s += 'G'
            elif bString[pointer] == '1' and bString[pointer + 1] == '1':
                s += 'T'
            pointer += 2
        return s

    def rank(self, char, int, list):  # takes a char, a number and a list und counts frequency of chars upto this number in the list
        counter = 0
        if int < 0:
            int = 0
        if int >= len(list):
            int = len(list) - 1
        for i in range(0, int + 1):
            if char == list[i]:
                counter += 1
        return counter

    def count(self, char, rank, list):  # takes a char, the rank and a list and returns the position in the list in which the number of chars=rank
        counter = 0
        for i in range(0, len(list)):
            if list[i] == char:
                counter += 1
                if counter == rank:
                    return i
                    break

    def bin2BWTs(self, binaryInput):  # takes a binaryInput and creates the two BWTs and returns the start/end position
        E1 = binaryInput
        RotationBWT1 = [binaryInput]  # rotation list for BWT1 with the binaryInput in index 0
        RotationBWT2 = []  # rotation list for BWT2
        for i in range(1, len(binaryInput)):
            binaryInput = binaryInput[1:] + binaryInput[0]  # create next rotatation
            if i % 2 == 0:
                RotationBWT1.append(binaryInput)  # add even rotations to BWT1
            else:
                RotationBWT2.append(binaryInput)  # add odd rotations to BWT2

        RotationBWT1.sort()  # sort them
        RotationBWT2.sort()  # sort them
        binaryInput = binaryInput[1:] + binaryInput[0]  # recreate the binary input
        for i in range(0, len(
                RotationBWT1)):  # find the binary input in Rotations BWT1(is needed to find the start/end position)
            if RotationBWT1[i] == binaryInput:
                E1 = i
                break
        BWT1 = []  # list for just the last char of RotationBWT1
        BWT2 = []  # list for just the last char of RotationBWT2
        for i in RotationBWT1:
            BWT1.append(i[len(i) - 1])
        for i in RotationBWT2:
            BWT2.append(i[len(i) - 1])
        print(type(BWT1))
        print(BWT2)
        return [E1, BWT1, BWT2]

    def BWTs2bin(self, E1, BWT1, BWT2):  # takes start posotion and two BWTs and creates the binary DNA string
        print(type(BWT1))
        BWT1First = BWT2.copy()  # create new list for First column of BWT1(because first column of BWT1 is sorted BWT2)
        BWT2First = BWT1.copy()  # create new list for First column of BWT2(vice versa)
        BWT1First.sort()
        BWT2First.sort()
        print(E1)

        position = E1
        currentChar = BWT1[E1]
        word = BWT1[E1]  # add first character
        for i in range(1, (len(BWT1) + len(BWT2))):
            if i % 2 == 0:
                number = rank(currentChar, position, BWT2)
                position = count(currentChar, number, BWT1First)
                currentChar = BWT1[position]
                word += currentChar
            else:
                number = rank(currentChar, position, BWT1)
                position = count(currentChar, number, BWT2First)
                currentChar = BWT2[position]
                word += currentChar
        return word[::-1]

    """def main():
        s = "GTAT"
        print("Input string:", s)
        print("To DNA:", DNA2binary(s))
        BWT1 = list(DNA2binary(s)[1])
        BWT2 = list(DNA2binary(s)[2])
        E1 = int(DNA2binary(s)[0])

        print("BWT1: ", BWT1, "BWT2: ", BWT2, "e1: ", E1)
        print(bin2BWTs(DNA2binary(s)))
        # BWTs2bin(E1, BWT1, BWT2)

    if __name__ == "__main__":
        main()"""