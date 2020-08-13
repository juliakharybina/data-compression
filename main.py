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
    global data
    data=""#global variable
    def __init__(self):
        super().__init__()
        self.setupUi(self) #инициализация нашего дизайна
        self.pushButton.clicked.connect(self.openFileNameDialog)
        self.pushButton_2.clicked.connect(self.combo_select)
        self.pushButton_3.clicked.connect(self.draw_charts)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options = QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                               "All Files (*);;Python Files (*.py)", options=options)
        fileName = fileName[0]
        fname = open(fileName)
        global data
        data = fname.read()
        self.textBrowser.setText(data)
        fname.close()

    def evaluate(self, data1, s, d):
        vals=[]
        if s == 'bwt':
            sum = 0
            vals_bwt = []
            for i in range(1, 21):
                rnd_txt = RandomText(data1)
                data = rnd_txt.makeRandomText(i)
                pre_text = self.textBrowser.toPlainText()
                self.textBrowser.setText(pre_text+"  "+str(i)+": "+data+ " \n \n")
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
            pre_text = self.textBrowser_3.toPlainText()
            self.textBrowser_3.setText(pre_text  + 'Sum for bwt: '+str(sum)+ "\n")
            pre_text2 = self.textBrowser_2.toPlainText()
            self.textBrowser_2.setText(pre_text2  + "; length of the compressed text: " + str(len(transform_rle)) + ";  initial length: " + str(len(data))+ "\n")
            #rb = xlrd.open_workbook('sheet.xls', formatting_info=True)
            #sheet = rb.sheet_by_index(0)
            #vals_bwt = pre_text.split()
            vals.append(vals_bwt)
            #print(vals_bwt)
            """for i in range(0, len(vals_bwt)):
                vals_bwt[i]=int(vals_bwt[i])
            print("after int")"""
            """wb = xlwt.Workbook()
            ws = wb.add_sheet('Test', cell_overwrite_ok=True)
            for i in range(0, len(vals_bwt)):
                el = vals_bwt[i]
                print(el)
                ws.write(i, 0, el)
            wb.save('sheet_w.xls')"""

        elif s=='huffman':
            sum=0
            vals_h = []
            for i in range(1, 21):
                rnd_txt = RandomText(data1)
                data = rnd_txt.makeRandomText(i)
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
            pre_text = self.textBrowser_3.toPlainText()
            self.textBrowser_3.setText(pre_text  + 'Sum for Huffman: ' + str(sum)+ "\n")
            self.textBrowser_2.setText(pre_text2  +"length of Huffmancode: " + str(len(huffmanCode)) + ";  initial length: " + str(len(data))+ "\n")
            #print(vals_h)
            vals.append(vals_h)
            """wb = xlwt.Workbook()
            ws = wb.add_sheet('Test', cell_overwrite_ok=True)
            for i in range(0, len(vals_h)):
                el = vals_h[i]
                print(el)
                ws.write(i, 1, el)
            wb.save('sheet_w.xls')"""

        elif s=='repair':
            sum = 0
            vals_r=[]
            for i in range(1, 21):
                rnd_txt = RandomText(data1)
                data = rnd_txt.makeRandomText(i)
                pre_text = self.textBrowser.toPlainText()
                self.textBrowser.setText(pre_text + " " + str(i) + ": " + data + " \n \n")
                t1_start = time.perf_counter_ns()
                repair = RePair(data)
                ch = 'A'
                rules = {}
                rules, s = repair.repair(data, ch, rules)
                #decomp_string=repair.decomp(rules,s)
                decomp_string=""
                t1_stop = time.perf_counter_ns()
                vals_r.append(t1_stop - t1_start)
                pre_text2 = self.textBrowser_2.toPlainText()
                self.textBrowser_2.setText(pre_text2 + "Rules: " + str(rules) + "; s: " + s +"Decomp string: "+decomp_string)
                pre_text = self.textBrowser_3.toPlainText()
                self.textBrowser_3.setText(pre_text  + str(t1_stop - t1_start)+ "\n")
                sum = sum + (t1_stop - t1_start)
            pre_text = self.textBrowser_3.toPlainText()
            self.textBrowser_3.setText(pre_text  + 'Sum for RePair: ' + str(sum)+ "\n")
            pre_text2 = self.textBrowser_2.toPlainText()
            self.textBrowser_2.setText(pre_text2 + ' initial length: ' + str(len(data)) + 'len(RePair): ' + str(len(s)))
            #print(vals_r)
            vals.append(vals_r)
            """wb = xlwt.Workbook()
            ws = wb.add_sheet('Test', cell_overwrite_ok=True)
            for i in range(0, len(vals_r)):
                el = vals_r[i]
                print(el)
                ws.write(i, 2, el)
            wb.save('sheet_w.xls')"""
        print("before excel")
        if count(vals)>3:
            wb = xlwt.Workbook()
            ws = wb.add_sheet('Test', cell_overwrite_ok=True)
            print("vals: ",len(vals))
            for j in range(0, len(vals)):
                for i in range(0, len(vals)):
                    print("j: "+j)
                    #el = vals[j[i]]
                    #print(el)
                    #ws.write(i, j, el)
           # wb.save('sheet_w.xls')



    def combo_select(self):
        global data
        # if data == "":
        if self.checkBox.isChecked():
            print("checked")
            file_name = 'rle.txt'
        else:
            file_name = 'alice.txt'
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
        """rb = xlrd.open_workbook('sheet.xls', formatting_info=True)
        sheet = rb.sheet_by_index(0)
        wb = xlwt.Workbook()
        ws = wb.add_sheet('Test', cell_overwrite_ok=True)
        vals = {1, 2, 3, 4, 5, 6, 10, 12, 13}
        for i in range(1, 9):
            row = sheet.row_values(0)
            for c_el in row:
                el = vals.pop()
                ws.write(i, 0, el)
                print(el)
        wb.save('xl_rec2.xls')"""
        table = pd.read_excel('sheet_w.xls')
        x = table.values[:, 0]
        y = table.values[:, 1]
        z = table.values[:, 2]
        plt.figure(figsize=(100, 100))
        plt.plot(x)
        plt.plot(y)
        plt.plot(z)
        plt.show()


def main():
    app = QtWidgets.QApplication(sys.argv) #новый экземпляр QApplication
    window = AppCompression() #cоздаем обьект класса ЕxampleApp
    window.show() #Показываем окно
    app.exec_()#запускаем приложение


if __name__ == '__main__':
    main()