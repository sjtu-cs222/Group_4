# -*- coding: utf-8 -*-
"""
this is a python file to get the evaluation of lineup
"""

import data
import os


def normalization1(hero_att2):
    """按照同列进行归一化"""
    names = hero_att2.keys()
    for name in names:
        hero_att2[name]['生存'] /= 10
        hero_att2[name]['攻击'] /= 10
        hero_att2[name]['技能'] /= 10
    # print(hero_att2)
    return hero_att2


def normalization2(hero_att2, att):
    values = list(hero_att2.values())
    values.sort(key=lambda x: x[att])
    minimum = values[0][att]
    maximum = values[49][att]
    names = list(hero_att2.keys())
    for name in names:
        hero_att2[name][att] = (hero_att2[name][att]-minimum)/(maximum-minimum)
    return hero_att2


# w 物攻 y 移速 f 攻击范围 g 官方给出的攻击伤害(归一化)
def get_attack(hero_att2):
    hero_attack = {}
    names = list(hero_att2.keys())
    for name in names:
        hero_attack[name] = 0.2*(5/11*hero_att2[name]['物理攻击']+3/11*hero_att2[name]['移速']+3/11*hero_att2[name]['攻击范围'])+0.8*hero_att2[name]['攻击']
    return hero_attack

    # attack = 0.2*(5/11*w+3/11*y+3/11*f)+0.8*g
    # return attack


# wf 物防 ff 法防 s 生命 y 移速 h 官方给出的生存能力(归一化)
def get_survival(hero_att2):  # wf, ff, s, y, h):
    hero_survival = {}
    names = list(hero_att2.keys())
    for name in names:
        hero_survival[name] = 0.2*(0.25*hero_att2[name]['物理防御']+0.15*hero_att2[name]['法术防御']+0.5*hero_att2[name]['最大生命']+0.1*hero_att2[name]['移速'])+0.8*hero_att2[name]['生存']
    return hero_survival
    # survival = 0.2*(0.25*wf+0.15*ff+0.5*s+0.1*y)+0.8*h
    # return survival


def get_single_power(hero_attack, hero_survival, hero_att, hero_att2):
    mid, sid, sup, jug = data.get_all_roads()
    names = list(hero_att2.keys())
    hero_power = {}
    for name in names:
        hero_power[name] = {}
        if name in mid:
            if hero_att[name]['主定位'] == '坦克'or hero_att[name]['主定位'] == '辅助':
                hero_power[name]['中路'] = 0.5*(((1+hero_survival[name])*(1+hero_att2[name]['技能']))**(1+hero_attack[name]))+0.5*((1 + hero_attack[name]) ** ((1 + hero_att2[name]['技能']) * (1 + hero_survival[name])))
            elif hero_att[name]['主定位'] == '战士':
                hero_power[name]['中路'] = 0.6*((1 + hero_survival[name]) ** ((1 + hero_att2[name]['技能']) * (1 + hero_attack[name])))+0.4*(((1+hero_attack[name])*(1+hero_att2[name]['技能']))**(1+hero_survival[name]))
            else:
                hero_power[name]['中路'] = 0.1*((1 + hero_survival[name]) ** ((1 + hero_att2[name]['技能']) * (1 + hero_attack[name])))+0.9*(((1+hero_attack[name])*(1+hero_att2[name]['技能']))**(1+hero_survival[name]))
        if name in sid:
            if hero_att[name]['主定位'] == '坦克' or hero_att[name]['主定位'] == '辅助':
                hero_power[name]['边路'] = 0.8*(((1+hero_survival[name])*(1+hero_att2[name]['技能']))**(1+hero_attack[name]))+0.2*((1 + hero_attack[name]) ** ((1 + hero_att2[name]['技能']) * (1 + hero_survival[name])))
            elif hero_att[name]['主定位'] == '战士':
                hero_power[name]['边路'] = 0.3*((1 + hero_survival[name]) ** ((1 + hero_att2[name]['技能']) * (1 + hero_attack[name])))+0.7*(((1+hero_attack[name])*(1+hero_att2[name]['技能']))**(1+hero_survival[name]))
            elif hero_att[name]['主定位'] == '刺客':
                hero_power[name]['边路'] = 0.25*((1 + hero_survival[name]) ** ((1 + hero_att2[name]['技能']) * (1 + hero_attack[name])))+0.75*(((1+hero_attack[name])*(1+hero_att2[name]['技能']))**(1+hero_survival[name]))
            else:
                hero_power[name]['边路'] = 0.2*((1 + hero_survival[name]) ** ((1 + hero_att2[name]['技能']) * (1 + hero_attack[name])))+0.8*(((1+hero_attack[name])*(1+hero_att2[name]['技能']))**(1+hero_survival[name]))

        if name in sup:
            hero_power[name]['辅助'] = 0.8*(((1+hero_survival[name])*(1+hero_att2[name]['技能']))**(1+hero_attack[name]))+0.2*((1 + hero_attack[name]) ** ((1 + hero_att2[name]['技能']) * (1 + hero_survival[name])))
        if name in jug:
            if hero_att[name]['主定位'] == '战士':
                hero_power[name]['打野'] = 0.35*((1 + hero_survival[name]) ** ((1 + hero_att2[name]['技能']) * (1 + hero_attack[name])))+0.65*(((1+hero_attack[name])*(1+hero_att2[name]['技能']))**(1+hero_survival[name]))
            elif hero_att[name]['主定位'] == '刺客':
                hero_power[name]['打野'] = 0.2*((1 + hero_survival[name]) ** ((1 + hero_att2[name]['技能']) * (1 + hero_attack[name])))+0.8*(((1+hero_attack[name])*(1+hero_att2[name]['技能']))**(1+hero_survival[name]))
            else:
                hero_power[name]['打野'] = 0.1*((1 + hero_survival[name]) ** ((1 + hero_att2[name]['技能']) * (1 + hero_attack[name])))+0.9*(((1+hero_attack[name])*(1+hero_att2[name]['技能']))**(1+hero_survival[name]))

        """
        hero_power[name] = (1+hero_attack[name])**((1+hero_att2[name]['技能'])*(1+hero_survival[name]))+(1+hero_att2[name]['技能'])**((1+hero_attack[name])*(1+hero_survival[name]))+ (1+hero_survival[name])**((1+hero_attack[name])*(1+hero_att2[name]['技能']))
        hero_power[name] = ((1+hero_attack[name])*(1+hero_att2[name]['技能']))**(1+hero_survival[name])+(1+hero_survival[name])**((1+hero_attack[name])*(1+hero_att2[name]['技能']))
        hero_raw_power[name].extend([((1+hero_attack[name])*(1+hero_att2[name]['技能']))**(1+hero_survival[name]),
                                 ((1+hero_survival[name])*(1+hero_att2[name]['技能']))**(1+hero_attack[name]),
                                 (1 + hero_attack[name]) ** ((1 + hero_att2[name]['技能']) * (1 + hero_survival[name])),
                                 (1 + hero_survival[name]) ** ((1 + hero_att2[name]['技能']) * (1 + hero_attack[name]))])
                                 """

    return hero_power


def normalize_single_road_power(hero_power, road):
    power = []
    raw_power = list(hero_power.values())
    for i in raw_power:
        if road in i:
            power.append(i[road])
    power.sort()
    minimum = power[0]
    maximum = power[-1]
    names = list(hero_power.keys())
    for name in names:
        if road in hero_power[name]:
            hero_power[name][road] = (hero_power[name][road] - minimum) / (maximum - minimum)


def normalize_all_power(hero_power):
    normalize_single_road_power(hero_power, '中路')
    normalize_single_road_power(hero_power, '边路')
    normalize_single_road_power(hero_power, '辅助')
    normalize_single_road_power(hero_power, '打野')


def create_all_normalized_power():
    hero_att = data.get_hero_att()
    hero_att2 = data.get_hero_att2()
    hero_att2 = normalization1(hero_att2)
    hero_att2 = normalization2(hero_att2, '最大生命')
    hero_att2 = normalization2(hero_att2, '物理攻击')
    hero_att2 = normalization2(hero_att2, '物理防御')
    hero_att2 = normalization2(hero_att2, '移速')
    names = list(hero_att2.keys())
    for name in names:
        hero_att2[name]['法术防御'] = 0.4
    hero_attack = get_attack(hero_att2)
    hero_survival = get_survival(hero_att2)
    hero_power = get_single_power(hero_attack, hero_survival, hero_att, hero_att2)
    normalize_all_power(hero_power)
    data.store_json('hero_power', hero_power)


def get_hero_power():
    if not os.path.exists('hero_power.json'):
        create_all_normalized_power()
    hero_power = data.load_json('hero_power')
    return hero_power


def get_the_value(rl):
    hero_power = get_hero_power()
    length = len(rl)
    values = []
    for i in rl.keys():
        if i in hero_power.keys():
            values.append(hero_power[i][rl[i]])
        else:
            values.append(0)
    value = 0
    total_v = 1
    for j in range(length):
        total_v *= (1 + values[j])
    for k in range(length):
        local_k = 1 + values[k]
        value += (local_k**(total_v/local_k))
    return value


def get_all_roads_pro(lineup):
    hero_att = data.get_hero_att()
    hero_roads = {}
    roads = ["中路", "边路", "边路", "辅助", "打野"]
    r_lineup = []
    lup = {}
    tmp_lineup = lineup.copy()
    for i in lineup:
        if i == "庄周":
            local_r = ["辅助", "中路", "边路"]
            hero_roads["庄周"] = []
            for j in local_r:
                if j in roads:
                    hero_roads["庄周"].append(j)
        elif hero_att[i]["次分路"]:
            hero_roads[i] = list([hero_att[i]["主分路"], hero_att[i]["次分路"]])
        else:
            hero_roads[i] = list([hero_att[i]["主分路"]])
    for r1 in hero_roads[tmp_lineup[0]]:
        roads_1 = roads.copy()
        lup_1 = lup.copy()
        roads_1.remove(r1)
        lup_1[tmp_lineup[0]] = r1
        if len(tmp_lineup) == 1:
            r_lineup.append(lup_1)
        else:
            for r2 in hero_roads[tmp_lineup[1]]:
                roads_2 = roads_1.copy()
                lup_2 = lup_1.copy()
                if r2 in roads_2:
                    roads_2.remove(r2)
                    lup_2[tmp_lineup[1]] = r2
                    if len(tmp_lineup) == 2:
                        r_lineup.append(lup_2)
                    else:
                        for r3 in hero_roads[tmp_lineup[2]]:
                            roads_3 = roads_2.copy()
                            lup_3 = lup_2.copy()
                            if r3 in roads_3:
                                roads_3.remove(r3)
                                lup_3[tmp_lineup[2]] = r3
                                if len(tmp_lineup) == 3:
                                    r_lineup.append(lup_3)
                                else:
                                    for r4 in hero_roads[tmp_lineup[3]]:
                                        roads_4 = roads_3.copy()
                                        lup_4 = lup_3.copy()
                                        if r4 in roads_4:
                                            roads_4.remove(r4)
                                            lup_4[tmp_lineup[3]] = r4
                                            if len(tmp_lineup) == 4:
                                                r_lineup.append(lup_4)
                                            else:
                                                for r5 in hero_roads[tmp_lineup[4]]:
                                                    roads_5 = roads_4.copy()
                                                    lup_5 = lup_4.copy()
                                                    if r5 in roads_5:
                                                        roads_5.remove(r5)
                                                        lup_5[tmp_lineup[4]] = r5
                                                        if len(tmp_lineup) == 5:
                                                            r_lineup.append(lup_5)
    return r_lineup


def evaluate(lineup):
    r_lineup = get_all_roads_pro(lineup)
    m = 0
    for rlp in r_lineup:
        local_v = get_the_value(rlp)
        if local_v > m:
            m = local_v
    return m


if __name__ == "__main__":
    create_all_normalized_power()
    lineup = ["庄周", "张飞", "项羽", "百里守约", "程咬金"]
    for rl in get_all_roads_pro(lineup):
        print(rl, ": ", get_the_value(rl))
    print(evaluate(lineup))