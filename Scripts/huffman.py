class Huffman:
    def __init__(self, s):
        self.s=s

        print("constructor")

    class Node(namedtuple("Node", ["left", "right"])):
        def walk(self, code,
                 acc):  # acc - второй аргумент префекс кода который мы накопили спускаясь от корня до данноо узла
            self.left.walk(code, acc + "0")
            print(code)
            print(acc)
            self.right.walk(code, acc + "1")
            print(code)
            print(acc)

    class Leaf(namedtuple("Leaf", ["char"])):
        def walk(self, code, acc):
            code[self.char] = acc or "0"  # записываем настроенный код данного символа

    def huffman_code(h):
        heapq.heapify(h)
        count = len(h)
        while len(h) > 1:  # до того пока не осталось два элемента
            freq1, _count1, left = heapq.heappop(h)  # Remove the node of lowest priority twice to get two nodes.
            print(freq1, _count1, left)
            freq2, _count2, right = heapq.heappop(h)
            print(freq2, _count2, right)
            heapq.heappush(h, (freq1 + freq2, count, Node(left,
                                                          right)))  # Add the new node to the queue. добавляем новый внутренний узел, у котрого потомки лейт и райт
            count += 1
        return h

    def computeFrequencies(s):
        h = []  # create a list(была проблема при сравнении листа и узла)
        for ch, freq in Counter(s).items():
            h.append((freq, len(h), Leaf(ch)))  # method adds an item to the end of the list why len?
            # print("{} {} {}".format(freq, len(h), Leaf(ch)))
        return h

    def encode(h):
        [(_freq, _count,
          root)] = h  # в очереди с приоритетами будет один элемент приоритет которого нам не важен а сам элемент это корень построенного дерева
        code = {}
        root.walk(code, "")  # обходим дерево, начиная с корня и заполняем словарь коде
        return code

    def huffman_decode(enStr, code):
        pointer = 0
        encoded_str = ''
        while pointer < len(enStr):
            for ch in code.keys():
                if enStr.startswith(code[ch], pointer):
                    encoded_str += ch
                    pointer += len(code[ch])
        return encoded_str
