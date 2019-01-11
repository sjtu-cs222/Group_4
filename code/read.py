# -*- coding: utf-8 -*-

import xlrd

def read_hero_attr(file_name):
    # 打开文件
    workbook = xlrd.open_workbook(file_name,"utf-8")
    sheet1 = workbook.sheet_by_index(0)
    att = sheet1.row_values(1)
    hero_att = {}
    for i in range(2,88):
        val = sheet1.row_values(i)
        hero_att[val[0]] = {}
        for j in range(1,10):
            hero_att[val[0]][att[j]] = val[j]
    return hero_att


def read_train_linup_attr(file_name):
    hero_att = read_hero_attr('hero_att.xlsx')
    workbook = xlrd.open_workbook(file_name, "utf-8")
    sheet = workbook.sheet_by_index(0)
    x_list = []
    y_list = []
    for i in range(20):
        val = sheet.row_values(i)
        temp1 = []
        temp2 = []
        for j in range(12):
            if j == 10 or j == 11:
                temp2.append(round(val[j], 3))
            else:
                temp1.extend([hero_att[val[j]]['生存'], hero_att[val[j]]['输出'], hero_att[val[j]]['位移'], hero_att[val[j]]['控制'], hero_att[val[j]]['推进']])
        x_list.append(temp1)
        y_list.append(temp2)
    return x_list, y_list

def get_input_tensor(lineup):
    hero_att = read_hero_attr('hero_att.xlsx')
    #workbook = xlrd.open_workbook(file_name, "utf-8")
    #sheet = workbook.sheet_by_index(0)
    raw_heroes = list(lineup.values())
    heroes = raw_heroes[0] + raw_heroes[1]
    x_list = []
    temp = []
    for j in range(10):
        temp.extend([hero_att[heroes[j]]['生存'], hero_att[heroes[j]]['输出'], hero_att[heroes[j]]['位移'], hero_att[heroes[j]]['控制'], hero_att[heroes[j]]['推进']])
    x_list.append(temp)
    return x_list

if __name__ == '__main__':
    read_train_linup_attr('train.xlsx')