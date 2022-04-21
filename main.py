#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pypinyin
import csv

def get_translation(input, dict_path):
    # load dict
    with open(dict_path, "r", encoding='utf-8') as csv_file:
        reader=csv.reader(csv_file)
        word_dict=dict(reader)

    # get tones of words
    tones = pypinyin.pinyin(input, style=pypinyin.TONE)

    # translate
    output = ''
    for tone in tones:
        tone = tone[0]
        if tone in word_dict:
            output += word_dict[tone]
        else: # keep if not in dict
            output += tone
    
    return output

if __name__ == "__main__":
    dict_path = './tool/word_dict.csv'

    str = input('input :')
    res = get_translation(str, dict_path)

    print('output:'+res)