import codecs

class BWT:
    def __init__(self, s):
        self.s=s


    def transform(self):
        s= self.s
        assert "$" not in s
        s = s + "$"
        table = sorted(s[i:] + s[:i] for i in range(len(s)))  # table of roations
        last_column = [row[-1] for row in table]  # last character of each row
        return "".join(last_column)  # converting to string


    def ibwt(self, bwt):
        table = [""] * len(bwt)
        for i in range(len(bwt)):
            table = sorted([bwt[i] + table[i] for i in range(len(bwt))])
        i_bwt = [row for row in table if row.endswith("$")][0]  # finding the correct row ending with $
        i_bwt = i_bwt.rstrip("$")
        return i_bwt


    def rle_encode(self, data):
        encoding = ''
        p_char = ''  # previos char
        count = 1
        if not data: return ''
        for char in data:
            if char != p_char:
                if p_char:
                    encoding += str(count) + p_char
                count = 1
                p_char = char
            else:
                count += 1
        else:
            encoding += str(count) + p_char
            return encoding


    def rle_decode(self, data):
        decode = ''
        count = ''
        for char in data:
            if char.isdigit():  # if char is numerical
                count += char  # мы используем += чтоб если двойное чило то оно запислось а не только первая цифра
            else:  # otherwide we've seen a non-numerical
                decode += char * int(count)
                count = ''
        return decode


    #def first(self):
        #transform_bwt = transform(self.s)
        #transform_rle = rle_encode(transform_bwt)
        #length_out = len(transform_rle)
        #return transform_bwt, transform_rle, length_out