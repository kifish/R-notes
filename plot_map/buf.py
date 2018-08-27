
import re

def strQ2B(ustring):
    """全角转半角"""
    ustring = str(ustring)
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:  # 全角空格直接转换
            inside_code = 32
        elif (inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化
            inside_code -= 65248
        rstring += chr(inside_code)
    return rstring




pattern1 = re.compile(r'混合[性型].{0,5}癌',re.M)
pattern2 = re.compile(r'小细胞癌',re.M)
pattern3 = re.compile(r'大细胞癌|大细胞神经内分泌癌',re.M)
pattern4 = re.compile(r'鳞癌|鳞状细胞癌',re.M)
pattern5 = re.compile(r'腺癌',re.M)
pattern_fq = re.compile(r'(.*?)([^\u4E00-\u9FA5]*[期]*)',re.M)
pattern_chinese = re.compile(r'[\u4E00-\u9FA5]+',re.M)
pattern_fq2 = re.compile(r'([^a-zA-Z0-9]*)([^\u4E00-\u9FA5]*[期]*)',re.M)


def judge2(text):
    text = strQ2B(text)
    seqs = text.split(',')
    if len(seqs) >= 2:
        if pattern_chinese.search(seqs[0]):
            seqs = seqs[1:]
    text = ''.join(seqs)
    text = strQ2B(text)
    res = '未知'
    if pattern_fq.search(text):
        res = pattern_fq.search(text).group()
        if res == '' or res == 'nan':
            res = '未知'

    return res



test_str = '混合性癌（小细胞癌，鳞癌）T3N0MO.IIa期'
print(judge2(test_str))
print(pattern_fq.search(test_str).group(0))
print(pattern_fq.search(test_str))
print(pattern_fq2.search(test_str))
print(pattern_fq2.search(test_str).group(2))