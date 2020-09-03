import sys
import os
import design
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
import BWT
from BWT import BWT
import huffman
from huffman import Huffman
import repair
from repair import RePair
import random_text
from random_text import RandomText
import binaryBWT
from binaryBWT import BinaryBWT
from time import process_time_ns
import time
import xlrd, xlwt
from xlwt.Workbook import *
from xlwt.Style import *
from xlrd import open_workbook
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')

class AppCompression(QtWidgets.QMainWindow, design.Ui_Dialog):
    global file_name
    file_name=''
    global data
    #global vals
    global vals_d
    global size
    size=20
    vals=[]
    vals_d = {}
    data=""#global variable
    global count_bwt, count_h, count_r
    count_bwt = 0
    count_h = 0
    count_r = 0
    def __init__(self):
        super().__init__()
        self.setupUi(self) #инициализация нашего дизайна
        self.pushButton.clicked.connect(self.openFileNameDialog)
        self.pushButton_2.clicked.connect(self.combo_select)
        self.pushButton_3.clicked.connect(self.draw_charts)
        self.pushButton_4.clicked.connect(self.clear_btn)
        self.horizontalSlider.valueChanged[int].connect(self.changeValue)


    def changeValue(self,value):
        print(value)
        global size
        size=value

    def openFileNameDialog(self):
        global file_name
        options = QFileDialog.Options()
        options = QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                               "All Files (*);;Python Files (*.py)", options=options)
        print(fileName)
        if str(fileName)=='(\'\', \'\')': #pроверка если файл не выбран
            file_name=""
        else:
            fileName = fileName[0]
            file_name = fileName
            fname = open(fileName)
            data = fname.read()
            self.textBrowser.setText(data)
            fname.close()
        print("file_name", file_name)


    def evaluate(self, data1, s, d):
        global size
        print("size: ", size)
        #size=20
        #global vals
        global vals_d
        if s == 'bwt':
            global count_bwt
            count_bwt+=1
            sum = 0
            vals_bwt = []
            for i in range(1, size+1):
                rnd_txt = RandomText(data1)
                data = rnd_txt.makeRandomText(i)
                pre_text = self.textBrowser.toPlainText()
                self.textBrowser.setText(pre_text+"  "+str(i)+": "+data+ " \n \n")
                initial_len =len(data)
                t1_start = time.perf_counter_ns()
                bwt = BWT(data)
                transform_bwt = bwt.transform()
                transform_rle = bwt.rle_encode(transform_bwt)
                decode_rle = bwt.rle_decode(transform_rle)
                #decode_bwt = bwt.ibwt(decode_rle)
                t1_stop = time.perf_counter_ns()
                pre_text = self.textBrowser_3.toPlainText()
                self.textBrowser_3.setText(pre_text  + str(t1_stop - t1_start)+ "\n")
                sum = sum+ (t1_stop - t1_start)
                vals_bwt.append(t1_stop - t1_start)
                pre_text2 = self.textBrowser_2.toPlainText()
                self.textBrowser_2.setText(pre_text2+str(i)+ "BWT: "+transform_bwt+" RLE: "+transform_rle+" RLE-DECODE: "+decode_rle+" \n")
                #print("len of transform_rle:", len(transform_rle))
                #print("koef = "+str(initial_len/len(transform_rle)))
            key = "".join(s+str(count_bwt))
            vals_d[s]=vals_bwt
            pre_text = self.textBrowser_3.toPlainText()
            self.textBrowser_3.setText(pre_text  + 'Sum for bwt: '+str(sum)+ "\n")
            pre_text2 = self.textBrowser_2.toPlainText()
            self.textBrowser_2.setText(pre_text2  + "; length of the compressed text: " + str(len(transform_rle)) + ";  initial length: " + str(len(data))+ "\n")

        elif s=='huffman':
            global count_h
            count_h+=1
            sum=0
            vals_h = []
            for i in range(1, size+1):
                rnd_txt = RandomText(data1)
                data = rnd_txt.makeRandomText(i)
                initial_len = len(data)
                pre_text = self.textBrowser.toPlainText()
                self.textBrowser.setText(pre_text + " " + str(i) + ": " + data+ " \n \n")
                t1_start = time.perf_counter_ns()
                huffman = Huffman(data)
                frequencyTable = huffman.computeFrequencies(data)
                codeTable = huffman.huffman_code(frequencyTable)
                huffmanCode = huffman.encode(codeTable)
                encoded = "".join(huffmanCode[ch] for ch in data)
                decoded_str=huffman.huffman_decode(encoded, huffmanCode)
                t1_stop = time.perf_counter_ns()
                vals_h.append(t1_stop - t1_start)
                pre_text = self.textBrowser_3.toPlainText()
                self.textBrowser_3.setText(pre_text +str(t1_stop - t1_start)+ "\n")
                pre_text2 = self.textBrowser_2.toPlainText()
                self.textBrowser_2.setText(pre_text2  +"encoded: " + encoded+ "Decoded-string: "+decoded_str+"\n")
                sum = sum + (t1_stop - t1_start)
                #print("len of transform_rle:", len(huffmanCode))
                #print("koef = " + str(initial_len / len(huffmanCode)))
            key = "".join(s + str(count_h))
            vals_d[key] = vals_h
            pre_text = self.textBrowser_3.toPlainText()
            self.textBrowser_3.setText(pre_text  + 'Sum for Huffman: ' + str(sum)+ "\n")
            self.textBrowser_2.setText(pre_text2  +"length of Huffmancode: " + str(len(huffmanCode)) + ";  initial length: " + str(len(data))+ "\n")

        elif s=='repair':
            sum = 0
            vals_r=[]
            global count_r
            count_r+=1
            for i in range(1, size+1):
                rnd_txt = RandomText(data1)
                data = rnd_txt.makeRandomText(i)
                initial_len = len(data)
                pre_text = self.textBrowser.toPlainText()
                self.textBrowser.setText(pre_text + " " + str(i) + ": " + data + " \n \n")
                t1_start = time.perf_counter_ns()
                repair = RePair(data)
                ch = 'A'
                rules = {}
                rules, s1 = repair.repair(data, ch, rules)
                #decomp_string=repair.decomp(rules,s)
                decomp_string=""
                t1_stop = time.perf_counter_ns()
                vals_r.append(t1_stop - t1_start)
                pre_text2 = self.textBrowser_2.toPlainText()
                self.textBrowser_2.setText(pre_text2 + "Rules: " + str(rules) + "; s: " + s1 +"Decomp string: "+decomp_string)
                pre_text = self.textBrowser_3.toPlainText()
                self.textBrowser_3.setText(pre_text  + str(t1_stop - t1_start)+ "\n")
                sum = sum + (t1_stop - t1_start)
                #print("len of transform_rle:", len(s1))
                #print("koef = " + str(initial_len / len(s1)))
            key = "".join(s + str(count_r))
            vals_d[key] = vals_r
            pre_text = self.textBrowser_3.toPlainText()
            self.textBrowser_3.setText(pre_text  + 'Sum for RePair: ' + str(sum)+ "\n")
            pre_text2 = self.textBrowser_2.toPlainText()
            self.textBrowser_2.setText(pre_text2 + ' initial length: ' + str(len(data)) + 'len(RePair): ' + str(len(s)))
        self.write_to_excel()

    def write_to_excel(self):
        global vals_d
        wb = xlwt.Workbook()
        ws = wb.add_sheet('Test', cell_overwrite_ok=True)
        print("vals_d: ", vals_d)
        count = 0
        for i in vals_d:
            vals_arr = vals_d.get(i)
            # print(str(i))
            ws.write(0, count, i)
            for j in range(0, len(vals_arr)):
                el = vals_arr[j]
                print(str(el))
                ws.write(j + 1, count, el)
            count += 1
        wb.save('sheet_w.xls')
    def clear_btn(self):
        self.textBrowser.setText("");
        self.textBrowser_2.setText("");
        self.textBrowser_3.setText("");

    def combo_select(self):
        global data
        global file_name
        # if data == "":
        #print("file_name",file_name)
        if file_name == "":
            if self.checkBox.isChecked():
                print("checked")
                file_name = 'rle.txt'
            else:
                file_name = 'alice.txt'
        #else:
            #file_name

        content = self.comboBox.currentText() # finding the content of current item in combo box
        if content == "BWT+RLE":
            self.evaluate(file_name,'bwt',1)
            # BWT+RLE
        elif content == "Huffman":
            self.evaluate(file_name, 'huffman', 20)
        elif content == "RePair":
            self.evaluate(file_name, 'repair', 1)
        elif content == "DNA":
            f = open('DNA.txt', 'r')
            data = f.read()
            self.textBrowser.setText(data)
            bBWT=BinaryBWT(data)
            binary = bBWT.DNA2binary(data)
            result = bBWT.bin2BWTs(binary)
            self.textBrowser_2.setText("Result: "+str(binary)+" "+str(result))
            f.close()

    def draw_charts(self):
        table = pd.read_excel('sheet_w.xls')
        plt.figure(figsize=(100, 100))
        plt.title("Wykres działania ałgorytmów")
        tab_len = len(table.columns.ravel())
        for i in range(0, tab_len):
            el = table.values[:, i]
            plt.plot(el,label=table.columns.ravel()[i])
        legend = plt.legend(loc='upper left', shadow=True, fontsize='x-large')
        #plt.axis.set_xlabel('X')
        plt.ylabel('Сzas działania algorytmu')
        plt.xlabel('Rozmiar przetwarzanych danych')
        plt.show()


def main():
    app = QtWidgets.QApplication(sys.argv) #новый экземпляр QApplication
    window = AppCompression() #cоздаем обьект класса ЕxampleApp
    window.show() #Показываем окно
    app.exec_()#запускаем приложение


if __name__ == '__main__':
    main()