from collections import Counter, namedtuple #how many times equivalent values are added
class Node(namedtuple("Node", ["left", "right"])):
    def walk(self, code,
             acc):  # acc - второй аргумент префекс кода который мы накопили спускаясь от корня до данноо узла
        self.left.walk(code, acc + "0")
        #print(code)
        #print(acc)
        self.right.walk(code, acc + "1")
        #print(code)
        #print(acc)


class Leaf(namedtuple("Leaf", ["char"])):
    def walk(self, code, acc):
        code[self.char] = acc or "0"  # записываем настроенный код данного символа