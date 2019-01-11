# -*- coding: utf-8 -*-
"""
this is a python file to get the data set
"""
import os
import xlrd
import json
import pickle
import eva


def store_json(name, ld):
    """将字典或者列表保存到json文件中"""
    json_name = json.dumps(ld)
    with open(name+'.json', 'w') as json_file:
        json_file.write(json_name)
    return


def load_json(name):
    """将字典或者列表从json文件中取出"""
    if os.path.exists(name+'.json'):
        json_name = open(name+'.json', 'r')
        n = json.load(json_name)
        return n


def create_hero_att():
    """创建保存所有英雄信息的字典，保存于json文件中"""
    workbook = xlrd.open_workbook(r'hero_att.xlsx', "utf-8")
    sheet1 = workbook.sheet_by_index(0)
    att = sheet1.row_values(1)
    hero_att = {}
    for i in range(2, 89):
        val = sheet1.row_values(i)
        hero_att[val[0]] = {}
        # 读取英雄所有数据
        for j in range(1, len(att)):
            hero_att[val[0]][att[j]] = val[j]
    store_json('hero_att', hero_att)
    return


def get_hero_att():
    """获取所有信息的字典"""
    if not os.path.exists('hero_att.json'):
        create_hero_att()
    hero_att = load_json('hero_att')
    return hero_att


def create_hero_att2():
    """创建第二个英雄信息字典"""
    workbook = xlrd.open_workbook(r'hero_att.xlsx', "utf-8")
    sheet1 = workbook.sheet_by_index(1)
    att = sheet1.row_values(1)
    hero_att2 = {}
    for i in range(2, 52):
        val = sheet1.row_values(i)
        hero_att2[val[0]] = {}
        # 读取英雄所有数据
        for j in range(1, len(att)):
            hero_att2[val[0]][att[j]] = val[j]
    store_json('hero_att2', hero_att2)
    return


def get_hero_att2():
    """获取第二个英雄信息字典"""
    if not os.path.exists('hero_att2.json'):
        create_hero_att2()
    hero_att2 = load_json('hero_att2')
    return hero_att2


def create_road(name):
    """创建某条分路的列表，保存到json中"""
    hero_att = get_hero_att()
    road = []
    for hero_name in hero_att.keys():
        r = hero_att[hero_name]['主分路']+' '+hero_att[hero_name]['次分路']
        if name in r:
            road.append(hero_name)
    store_json(name, road)
    return


def create_all_roads():
    """创建所有分路信息"""
    roads = ['中路', '边路', '打野', '辅助']
    for i in roads:
        create_road(i)


def get_all_roads():
    """获取已经建立好的分路信息，用于ai的选取"""
    mid = load_json('中路')
    sid = load_json('边路')
    sup = load_json('辅助')
    jug = load_json('打野')
    return mid, sid, sup, jug


def create_all_lineup():
    """共有40080104个阵容情况,不易于使用"""
    def all_dif(a, b, c, d, e):
        if a != b and a != c and a != d and a != e and b != c and b != d and b != e and c != d and c != e and d != e:
            return 1
        else:
            return 0
    middle = '中路'
    side = '边路'
    support = '辅助'
    jungle = '打野'
    create_all_roads()
    mid, sid, sup, jug = get_all_roads()
    lineup = []
    total = len(mid)*len(sid)*len(sid)*len(sup)*len(jug)
    count = 0
    for m in mid:
        for s1 in sid:
            for s2 in sid:
                for p in sup:
                    for j in jug:
                        count += 1
                        if all_dif(m, s1, s2, p, j):
                            lp = dir()
                            lp[middle] = m
                            lp[side] = s1+' '+s2
                            lp[support] = p
                            lp[jungle] = j
                            lineup.append(lp)
                            print(total - count, ':', lp)
                        else:
                            print(total - count)
    print(len(lineup), " loading...")
    lpfile = open('阵容情况.pickle', 'wb')
    pickle.dump(lineup, lpfile)
    lpfile.close()
    return


def get_all_lineup():
    """获取所有阵容组合的情况，运行时间较长"""
    lpfile = open('阵容情况.pickle', 'rb')
    lineup = pickle.load(lpfile)
    return lineup


def create_hero_name():
    """建立角色名列表"""
    hero_data = load_json("qiujisai")
    hero_names = list(hero_data.keys())
    for i in hero_names:
        num = float(hero_data[i]['ban_cnt']) + float(hero_data[i]['pick_cnt'])
        if num <= 16:
            hero_data.pop(i)
    hero_name = []
    for i in hero_data.keys():
        hero_name.append(i)
    store_json("hero_name", hero_name)
    """
    当前所有英雄的名称
    hero_att = get_hero_att()
    hero_name = list()
    for n in hero_att.keys():
        hero_name.append(n)
    store_json("hero_name", hero_name)
    """
    return


def get_hero_name():
    """获取所有英雄名称的列表"""
    if not os.path.exists('hero_name.json'):
        create_hero_name()
    hero_name = load_json('hero_name')
    return hero_name


def create_hero_value():
    """建立英雄的参数值列表"""
    workbook = xlrd.open_workbook(r'hero_att.xlsx', "utf-8")
    sheet1 = workbook.sheet_by_index(0)
    att = sheet1.row_values(1)
    hero_value = {}
    for i in range(2, 88):
        val = sheet1.row_values(i)
        hero_value[val[0]] = {}
        # 读取英雄所有数据
        for j in range(5, len(att)):
            hero_value[val[0]][att[j]] = val[j]
    store_json('hero_value', hero_value)
    return


def get_hero_value():
    """获取所有英雄参数的字典"""
    if not os.path.exists('hero_value.json'):
        create_hero_value()
    hero_value = load_json('hero_value')
    return hero_value


def create_powerful():
    """建立强势英雄的字典"""
    hero_data = load_json("qiujisai")
    temp = {}
    for i in hero_data.keys():
        temp[i] = int(float(hero_data[i]['ban_rate'])*100)
    choose_time = 8
    i = 0
    powerful = {}
    while i < choose_time:
        i += 1
        tmp = 0
        for j in temp.keys():
            if temp[j] > tmp:
                tmp = temp[j]
                tem_j = j
        powerful[tem_j] = tmp
        temp.pop(tem_j)

    store_json('powerful', powerful)
    return


def get_powerful():
    """获取强势英雄的字典"""
    if not os.path.exists('powerful.json'):
        create_powerful()
    powerful = load_json('powerful')
    return powerful


def create_all():
    create_powerful()
    create_hero_att()
    create_hero_att2()
    create_all_roads()
    create_hero_name()
    create_hero_value()
    eva.create_all_normalized_power()
    return


if __name__ == '__main__':
    create_all()