# -*- coding: utf-8 -*-
"""this is a python file for bp_ai input"""
import random
import data
import eva


def p_choose(ld):
    if isinstance(ld, list):
        length = len(ld)
        value = random.randint(0, length-1)
        return ld[value]
    else:
        k = list(ld.keys())
        v = list(ld.values())
        temp = 0
        for i in v:
            temp += i*i
        value = random.randint(1, int(temp))
        count = 0
        temp = 0
        for j in k:
            temp += v[count]*v[count]
            if value <= temp:
                return k[count]
            count += 1


def judge_system(lineup, hero_to_choose):
    hero_value = data.get_hero_value()
    temp_l = {}
    # 防止错误
    tmp_h = hero_to_choose[0]
    temp_l[tmp_h] = 1
    # first system
    core1 = "大乔"
    if core1 in hero_to_choose:
        tmp = 0
        for i in lineup:
            tmp += hero_value[i]["生存"]
        if len(lineup) == 0 or tmp/len(lineup) >= 4:
            temp_l[core1] = 75
        else:
            temp_l[core1] = 90
    elif core1 in lineup:
        if "老夫子" in hero_to_choose:
            return "老夫子", 80

    hero = p_choose(temp_l)
    return hero, temp_l[hero]


def judge_restrain(lineup, hero_to_choose):
    hero_value = data.get_hero_value()
    temp_l = {}
    # 防止错误
    tmp_h = hero_to_choose[0]
    temp_l[tmp_h] = 1
    # first restrain
    if "张良" in lineup:
        if '武则天' in hero_to_choose:
            temp_l['武则天'] = 90
    # second restrain
    tmp = 0
    for i in lineup:
        if hero_value[i]["射程"] == 1:
            tmp += 1
    if tmp >= 3:
        if "盾山" in hero_to_choose:
            temp_l["盾山"] = 99
    # third restrain
    tmp = 0
    for i in lineup:
        if hero_value[i]["生存"] <= 2:
            tmp += 1
    if tmp >= 3:
        if "阿珂" in hero_to_choose:
            temp_l["阿珂"] = 99
    hero = p_choose(temp_l)
    return hero, temp_l[hero]


def del_list_no_use(ls, ban, pick):
    """去除bp选过的英雄"""
    for i in ban.values():
        if i in ls:
            ls.remove(i)
    for i in pick.values():
        if i in ls:
            ls.remove(i)
    return ls


def del_diy_no_use(dr, ban, pick):
    """去除bp选过的英雄"""
    for i in ban.values():
        if i in dr.keys():
            dr.pop(i)
    for i in pick.values():
        if i in dr.keys():
            dr.pop(i)
    return dr


def get_pick(pick):
    red = []
    blue = []
    blue_pick = 'blue_pick'
    red_pick = 'red_pick'
    pick_node = [1, 5, 9]
    j = 0
    for j in range(1, int(len(pick) / 2) + 1):
        blue.append(pick[blue_pick + str(j)])
        red.append(pick[red_pick + str(j)])
    if len(pick) % 2 != 0:
        if len(pick) in pick_node:
            blue.append(pick[blue_pick + str(j + 1)])
        else:
            red.append(pick[red_pick + str(j + 1)])
    return red, blue


def get_in_road_choose(hero_to_choose, pick_dire):
    """仅可过滤部分情况"""
    mid, sid, sup, jug = data.get_all_roads()
    hero_att = data.get_hero_att()
    roads = ["中路", "边路", "边路", "辅助", "打野"]
    tmp_pick_dire = pick_dire.copy()

    # 排除已确定的情况
    for i in pick_dire:
        if not hero_att[i]["次分路"]:
            roads.remove(hero_att[i]["主分路"])
            tmp_pick_dire.remove(i)
    pick_dire = tmp_pick_dire.copy()
    flag = True
    while flag:
        flag = False
        for i in pick_dire:
            if hero_att[i]["次分路"] and i != "庄周":
                if hero_att[i]["次分路"] not in roads:
                    roads.remove(hero_att[i]["主分路"])
                    tmp_pick_dire.remove(i)
                    flag = True
                elif hero_att[i]["主分路"] not in roads:
                    roads.remove(hero_att[i]["次分路"])
                    tmp_pick_dire.remove(i)
                    flag = True
            if i == "庄周":
                local_r = ["辅助", "中路", "边路"]
                local_c = 0
                for j in local_r:
                    if j in roads:
                        local_c += 1
                        local_t = j
                if local_c == 1:
                    roads.remove(local_t)
                    if "庄周" in tmp_pick_dire:
                        tmp_pick_dire.remove("庄周")
                    flag = True
        pick_dire = tmp_pick_dire.copy()

    new_hero_to_choose = []
    for i in roads:
        if i == "中路":
            for j in mid:
                if j in hero_to_choose and j not in new_hero_to_choose:
                    new_hero_to_choose.append(j)
        elif i == "边路":
            for j in sid:
                if j in hero_to_choose and j not in new_hero_to_choose:
                    new_hero_to_choose.append(j)
        elif i == "辅助":
            for j in sup:
                if j in hero_to_choose and j not in new_hero_to_choose:
                    new_hero_to_choose.append(j)
        elif i == "打野":
            for j in jug:
                if j in hero_to_choose and j not in new_hero_to_choose:
                    new_hero_to_choose.append(j)
    return new_hero_to_choose


def judge_eva1(my_pick, el_pick, hero_to_use):
    hero_power = eva.get_hero_power()
    hero_my_choose = get_in_road_choose(hero_to_use, my_pick)
    tmp = 0
    for i in hero_my_choose:
        l_my1 = my_pick.copy()
        l_my1.append(i)
        evaluation = eva.evaluate(l_my1)
        if evaluation > tmp:
            tmp = evaluation
            hero = i
    power = 0
    for i in list(hero_power[hero].values()):
        if i > power:
            power = i
    return hero, int(power * 100)


def judge_eva2(my_pick, el_pick, hero_to_use):
    hero_power = eva.get_hero_power()
    hero_my_choose = get_in_road_choose(hero_to_use, my_pick)
    hero_el_choose = get_in_road_choose(hero_to_use, el_pick)
    tmp = -100
    for i in hero_my_choose:
        l_my1 = my_pick.copy()
        l_my1.append(i)
        for j in hero_el_choose:
            l_el1 = el_pick.copy()
            l_el1.append(j)
            evaluation = eva.evaluate(l_my1) - eva.evaluate(l_el1)
            if evaluation > tmp:
                tmp = evaluation
                hero = i
    power = 0
    for i in list(hero_power[hero].values()):
        if i > power:
            power = i
    return hero, int(power * 100)


def judge_eva3(my_pick, el_pick, hero_to_use):
    hero_power = eva.get_hero_power()
    hero_my_choose = get_in_road_choose(hero_to_use, my_pick)
    hero_el_choose = get_in_road_choose(hero_to_use, el_pick)
    tmp = -100
    for i in hero_my_choose:
        l_my1 = my_pick.copy()
        l_my1.append(i)
        c_my1 = get_in_road_choose(hero_my_choose, l_my1)
        for k in c_my1:
            l_my2 = l_my1.copy()
            l_my2.append(k)
            for j in hero_el_choose:
                l_el1 = el_pick.copy()
                l_el1.append(j)
                evaluation = eva.evaluate(l_my2) - eva.evaluate(l_el1)
                if evaluation > tmp:
                    tmp = evaluation
                    hero = i
    power = 0
    for i in list(hero_power[hero].values()):
        if i > power:
            power = i
    return hero, int(power * 100)


def judge_eva4(my_pick, el_pick, hero_to_use):
    hero_power = eva.get_hero_power()
    hero_my_choose = get_in_road_choose(hero_to_use, my_pick)
    hero_el_choose = get_in_road_choose(hero_to_use, el_pick)
    tmp = -100
    for i in hero_my_choose:
        l_my1 = my_pick.copy()
        l_my1.append(i)
        c_my1 = get_in_road_choose(hero_my_choose, l_my1)
        for j in hero_el_choose:
            l_el1 = el_pick.copy()
            l_el1.append(j)
            c_el1 = get_in_road_choose(hero_el_choose, l_el1)
            for l in c_el1:
                l_el2 = l_el1.copy()
                l_el2.append(l)
                for k in c_my1:
                    l_my2 = l_my1.copy()
                    l_my2.append(k)
                    evaluation = eva.evaluate(l_my2) - eva.evaluate(l_el2)
                    if evaluation > tmp:
                        tmp = evaluation
                        hero = i
    power = 0
    for i in list(hero_power[hero].values()):
        if i > power:
            power = i
    return hero, int(power * 100)


def ban_ai_input(dire, ban, pick):
    """ai在此过程中的禁用"""
    # 下为所需的材料建立
    if True:
        hero_name = data.get_hero_name()
        mid, sid, sup, jug = data.get_all_roads()
        powerful = data.get_powerful()
        hero_to_choose = del_list_no_use(hero_name, ban, pick)
        powerful = del_diy_no_use(powerful, ban, pick)
        hero = p_choose(hero_to_choose)

        red_pick, blue_pick = get_pick(pick)
        hero_blue_choose = get_in_road_choose(hero_to_choose, blue_pick)
        hero_red_choose = get_in_road_choose(hero_to_choose, red_pick)

    def remove_most_powerful():
        nonlocal powerful
        tmp = 0
        for i in powerful.keys():
            if powerful[i] > tmp:
                tmp = powerful[i]
                tmp_i = i
        powerful.pop(tmp_i)
        return

    # 下为蓝方禁用函数
    if True:
        def ban_blue1():
            nonlocal hero
            temp_l = {}
            # 第一候选人
            remove_most_powerful()
            remove_most_powerful()
            temp1 = p_choose(powerful)
            coef1 = powerful[temp1]
            temp_l[temp1] = coef1
            # 第二候选人
            temp2, coef2 = judge_system([], hero_to_choose)
            if temp2 in temp_l.keys():
                temp_l[temp2] += int(coef2*0.4)
            else:
                temp_l[temp2] = int(coef2*0.4)
            # 候选人竞选
            hero = p_choose(temp_l)
            return

        def ban_blue2():
            nonlocal hero
            temp_l = {}
            # 第一候选人
            remove_most_powerful()
            temp1 = p_choose(powerful)
            coef1 = powerful[temp1]
            temp_l[temp1] = coef1
            # 第二候选人
            temp2, coef2 = judge_system([], hero_to_choose)
            if temp2 in temp_l.keys():
                temp_l[temp2] += int(coef2*0.4)
            else:
                temp_l[temp2] = int(coef2*0.4)
            # 候选人竞选
            hero = p_choose(temp_l)
            return

        def ban_blue3():
            nonlocal hero
            temp_l = {}
            # 第一候选人
            temp1 = p_choose(powerful)
            coef1 = powerful[temp1]
            temp_l[temp1] = int(coef1*0.3)
            # 第二候选人
            temp2, coef2 = judge_system(red_pick, hero_to_choose)
            if temp2 in temp_l.keys():
                temp_l[temp2] += int(coef2 * 0.5)
            else:
                temp_l[temp2] = int(coef2 * 0.5)
            # 第三候选人
            temp3, coef3 = judge_restrain(blue_pick, hero_to_choose)
            if temp3 in temp_l.keys():
                temp_l[temp3] += int(coef3 * 0.75)
            else:
                temp_l[temp3] = int(coef3 * 0.75)
            # 第四候选人
            temp4, coef4 = judge_eva1(red_pick, blue_pick, hero_to_choose)
            if temp4 in temp_l.keys():
                temp_l[temp4] += int(coef4 * 0.5)
            else:
                temp_l[temp4] = int(coef4 * 0.5)
            # 候选人竞选
            hero = p_choose(temp_l)
            return

        def ban_blue4():
            nonlocal hero
            temp_l = {}
            # 第一候选人
            temp1 = p_choose(powerful)
            coef1 = powerful[temp1]
            temp_l[temp1] = int(coef1 * 0.3)
            # 第二候选人
            temp2, coef2 = judge_system(red_pick, hero_to_choose)
            if temp2 in temp_l.keys():
                temp_l[temp2] += int(coef2 * 0.5)
            else:
                temp_l[temp2] = int(coef2 * 0.5)
            # 第三候选人
            temp3, coef3 = judge_restrain(blue_pick, hero_to_choose)
            if temp3 in temp_l.keys():
                temp_l[temp3] += int(coef3 * 0.75)
            else:
                temp_l[temp3] = int(coef3 * 0.75)
            # 第四候选人
            temp4, coef4 = judge_eva1(red_pick, blue_pick, hero_to_choose)
            if temp4 in temp_l.keys():
                temp_l[temp4] += int(coef4 * 0.5)
            else:
                temp_l[temp4] = int(coef4 * 0.5)
            # 候选人竞选
            hero = p_choose(temp_l)
            return hero

    # 下为红方禁用函数
    if True:
        def ban_red1():
            nonlocal hero
            temp_l = {}
            # 第一候选人
            temp1 = p_choose(powerful)
            coef1 = powerful[temp1]
            temp_l[temp1] = coef1
            # 第二候选人
            temp2, coef2 = judge_system([], hero_to_choose)
            if temp2 in temp_l.keys():
                temp_l[temp2] += int(coef2 * 0.5)
            else:
                temp_l[temp2] = int(coef2 * 0.5)
            # 候选人竞选
            hero = p_choose(temp_l)
            return

        def ban_red2():
            nonlocal hero
            temp_l = {}
            # 第一候选人
            remove_most_powerful()
            remove_most_powerful()
            temp1 = p_choose(powerful)
            coef1 = powerful[temp1]
            temp_l[temp1] = coef1
            # 第二候选人
            temp2, coef2 = judge_system([], hero_to_choose)
            if temp2 in temp_l.keys():
                temp_l[temp2] += int(coef2 * 0.5)
            else:
                temp_l[temp2] = int(coef2 * 0.5)
            # 候选人竞选
            hero = p_choose(temp_l)
            return

        def ban_red3():
            nonlocal hero
            temp_l = {}
            # 第一候选人
            temp1 = p_choose(powerful)
            coef1 = powerful[temp1]
            temp_l[temp1] = int(coef1 * 0.3)
            # 第二候选人
            temp2, coef2 = judge_system(blue_pick, hero_to_choose)
            if temp2 in temp_l.keys():
                temp_l[temp2] += int(coef2 * 0.5)
            else:
                temp_l[temp2] = int(coef2 * 0.5)
            # 第三候选人
            temp3, coef3 = judge_restrain(red_pick, hero_to_choose)
            if temp3 in temp_l.keys():
                temp_l[temp3] += int(coef3 * 0.75)
            else:
                temp_l[temp3] = int(coef3 * 0.75)
            # 第四候选人
            temp4, coef4 = judge_eva1(blue_pick, red_pick, hero_to_choose)
            if temp4 in temp_l.keys():
                temp_l[temp4] += int(coef4 * 0.5)
            else:
                temp_l[temp4] = int(coef4 * 0.5)
            # 候选人竞选
            hero = p_choose(temp_l)
            return

        def ban_red4():
            nonlocal hero
            temp_l = {}
            # 第一候选人
            temp1 = p_choose(powerful)
            coef1 = powerful[temp1]
            temp_l[temp1] = int(coef1 * 0.3)
            # 第二候选人
            temp2, coef2 = judge_system(red_pick, hero_to_choose)
            if temp2 in temp_l.keys():
                temp_l[temp2] += int(coef2 * 0.5)
            else:
                temp_l[temp2] = int(coef2 * 0.5)
            # 第三候选人
            temp3, coef3 = judge_restrain(blue_pick, hero_to_choose)
            if temp3 in temp_l.keys():
                temp_l[temp3] += int(coef3 * 0.75)
            else:
                temp_l[temp3] = int(coef3 * 0.75)
            # 第四候选人
            temp4, coef4 = judge_eva1(blue_pick, red_pick, hero_to_choose)
            if temp4 in temp_l.keys():
                temp_l[temp4] += int(coef4 * 0.5)
            else:
                temp_l[temp4] = int(coef4 * 0.5)
            # 候选人竞选
            hero = p_choose(temp_l)
            return hero

    # 下为蓝方禁用
    if True:
        if len(ban) == 0:
            """蓝方第一ban"""
            ban_blue1()
        elif len(ban) == 2:
            """蓝方第二ban"""
            ban_blue2()
        elif len(ban) == 5:
            """蓝方第三ban"""
            ban_blue3()
        elif len(ban) == 7:
            """蓝方第四ban"""
            ban_blue4()
    # 下为红方禁用
    if True:
        if len(ban) == 1:
            """红方第一ban"""
            ban_red1()
        elif len(ban) == 3:
            """红方第二ban"""
            ban_red2()
        elif len(ban) == 4:
            """红方第三ban"""
            ban_red3()
        elif len(ban) == 6:
            """红方第四ban"""
            ban_red4()

    return hero


def pick_ai_input(dire, ban, pick):
    """ai在此bp过程中的选用"""
    # 下为所需的材料建立
    if True:
        hero_name = data.get_hero_name()
        powerful = data.get_powerful()
        hero_to_choose = del_list_no_use(hero_name, ban, pick)
        powerful = del_diy_no_use(powerful, ban, pick)
        hero_power = eva.get_hero_power()
        hero = p_choose(hero_to_choose)

        red_pick, blue_pick = get_pick(pick)
        hero_blue_choose = get_in_road_choose(hero_to_choose, blue_pick)
        hero_red_choose = get_in_road_choose(hero_to_choose, red_pick)

    def get_most_powerful():
        tmp = 0
        for i in powerful.keys():
            if powerful[i] > tmp:
                tmp = powerful[i]
                tmp_i = i
        return tmp_i, powerful[tmp_i]

    # 下为蓝方选用函数
    if True:
        def pick_blue1():
            nonlocal hero
            temp_l = {}
            # 第一候选人
            temp1, coef1 = judge_eva1(blue_pick, red_pick, hero_to_choose)
            temp_l[temp1] = coef1
            # 第二候选人
            temp2, coef2 = get_most_powerful()
            if temp2 in temp_l.keys():
                temp_l[temp2] += int(coef2)
            else:
                temp_l[temp2] = int(coef2)
            # 第三候选人
            temp3, coef3 = judge_system(blue_pick, hero_to_choose)
            if temp3 in temp_l.keys():
                temp_l[temp3] += int(coef3)
            else:
                temp_l[temp3] = int(coef3)
            # 第四候选人
            temp4, coef4 = judge_restrain(red_pick, hero_to_choose)
            if temp4 in temp_l.keys():
                temp_l[temp4] += int(coef4)
            else:
                temp_l[temp4] = int(coef4)
            # 候选人竞选
            hero = p_choose(temp_l)
            return

        def pick_blue2():
            nonlocal hero
            temp_l = {}
            # 第一候选人
            temp1, coef1 = judge_eva1(blue_pick, red_pick, hero_to_choose)
            temp_l[temp1] = coef1
            # 第二候选人
            temp2, coef2 = get_most_powerful()
            if temp2 in temp_l.keys():
                temp_l[temp2] += int(coef2 * 0.9)
            else:
                temp_l[temp2] = int(coef2 * 0.9)
            # 第三候选人
            temp3, coef3 = judge_system(blue_pick, hero_to_choose)
            if temp3 in temp_l.keys():
                temp_l[temp3] += int(coef3)
            else:
                temp_l[temp3] = int(coef3)
            # 第四候选人
            temp4, coef4 = judge_restrain(red_pick, hero_to_choose)
            if temp4 in temp_l.keys():
                temp_l[temp4] += int(coef4)
            else:
                temp_l[temp4] = int(coef4)
            # 候选人竞选
            hero = p_choose(temp_l)
            return

        def pick_blue3():
            nonlocal hero
            temp_l = {}
            # 第一候选人
            temp1, coef1 = judge_eva1(blue_pick, red_pick, hero_to_choose)
            temp_l[temp1] = coef1
            # 第二候选人
            temp2, coef2 = get_most_powerful()
            if temp2 in temp_l.keys():
                temp_l[temp2] += int(coef2 * 0.8)
            else:
                temp_l[temp2] = int(coef2 * 0.8)
            # 第三候选人
            temp3, coef3 = judge_system(blue_pick, hero_to_choose)
            if temp3 in temp_l.keys():
                temp_l[temp3] += int(coef3)
            else:
                temp_l[temp3] = int(coef3)
            # 第四候选人
            temp4, coef4 = judge_restrain(red_pick, hero_to_choose)
            if temp4 in temp_l.keys():
                temp_l[temp4] += int(coef4)
            else:
                temp_l[temp4] = int(coef4)
            # 候选人竞选
            hero = p_choose(temp_l)
            return

        def pick_blue4():
            nonlocal hero
            temp_l = {}
            # 第一候选人
            temp1, coef1 = judge_eva1(blue_pick, red_pick, hero_to_choose)
            temp_l[temp1] = coef1
            # 第一候选人
            temp2, coef2 = get_most_powerful()
            if temp2 in temp_l.keys():
                temp_l[temp2] += int(coef2 * 0.6)
            else:
                temp_l[temp2] = int(coef2 * 0.6)
            # 第三候选人
            temp3, coef3 = judge_system(blue_pick, hero_to_choose)
            if temp3 in temp_l.keys():
                temp_l[temp3] += int(coef3)
            else:
                temp_l[temp3] = int(coef3)
            # 第四候选人
            temp4, coef4 = judge_restrain(red_pick, hero_to_choose)
            if temp4 in temp_l.keys():
                temp_l[temp4] += int(coef4)
            else:
                temp_l[temp4] = int(coef4)
            # 候选人竞选
            hero = p_choose(temp_l)
            return

        def pick_blue5():
            nonlocal hero
            temp_l = {}
            # 第一候选人
            temp1, coef1 = judge_eva1(blue_pick, red_pick, hero_to_choose)
            temp_l[temp1] = coef1
            # 第二候选人
            temp2, coef2 = get_most_powerful()
            if temp2 in temp_l.keys():
                temp_l[temp2] += int(coef2 * 0.5)
            else:
                temp_l[temp2] = int(coef2 * 0.5)
            # 第三候选人
            temp3, coef3 = judge_system(blue_pick, hero_to_choose)
            if temp3 in temp_l.keys():
                temp_l[temp3] += int(coef3)
            else:
                temp_l[temp3] = int(coef3)
            # 第四候选人
            temp4, coef4 = judge_restrain(red_pick, hero_to_choose)
            if temp4 in temp_l.keys():
                temp_l[temp4] += int(coef4)
            else:
                temp_l[temp4] = int(coef4)
            # 候选人竞选
            hero = p_choose(temp_l)
            return

    # 下为红方选用函数
    if True:
        def pick_red1():
            nonlocal hero
            temp_l = {}
            # 第一候选人
            temp1, coef1 = judge_eva1(red_pick, blue_pick, hero_to_choose)
            temp_l[temp1] = coef1
            # 第二候选人
            temp2, coef2 = get_most_powerful()
            if temp2 in temp_l.keys():
                temp_l[temp2] += int(coef2)
            else:
                temp_l[temp2] = int(coef2)
            # 第三候选人
            temp3, coef3 = judge_system(red_pick, hero_to_choose)
            if temp3 in temp_l.keys():
                temp_l[temp3] += int(coef3)
            else:
                temp_l[temp3] = int(coef3)
            # 第四候选人
            temp4, coef4 = judge_restrain(blue_pick, hero_to_choose)
            if temp4 in temp_l.keys():
                temp_l[temp4] += int(coef4)
            else:
                temp_l[temp4] = int(coef4)
            # 候选人竞选
            hero = p_choose(temp_l)
            return

        def pick_red2():
            nonlocal hero
            temp_l = {}
            # 第一候选人
            temp1, coef1 = judge_eva2(red_pick, blue_pick, hero_to_choose)
            temp_l[temp1] = coef1
            # 第二候选人
            temp2, coef2 = get_most_powerful()
            if temp2 in temp_l.keys():
                temp_l[temp2] += int(coef2 * 0.9)
            else:
                temp_l[temp2] = int(coef2 * 0.9)
            # 第三候选人
            temp3, coef3 = judge_system(red_pick, hero_to_choose)
            if temp3 in temp_l.keys():
                temp_l[temp3] += int(coef3)
            else:
                temp_l[temp3] = int(coef3)
            # 第四候选人
            temp4, coef4 = judge_restrain(blue_pick, hero_to_choose)
            if temp4 in temp_l.keys():
                temp_l[temp4] += int(coef4)
            else:
                temp_l[temp4] = int(coef4)
            # 候选人竞选
            hero = p_choose(temp_l)
            return

        def pick_red3():
            nonlocal hero
            temp_l = {}
            # 第一候选人
            temp1, coef1 = judge_eva1(red_pick, blue_pick, hero_to_choose)
            temp_l[temp1] = coef1
            # 第二候选人
            temp2, coef2 = get_most_powerful()
            if temp2 in temp_l.keys():
                temp_l[temp2] += int(coef2 * 0.8)
            else:
                temp_l[temp2] = int(coef2 * 0.8)
            # 第三候选人
            temp3, coef3 = judge_system(red_pick, hero_to_choose)
            if temp3 in temp_l.keys():
                temp_l[temp3] += int(coef3)
            else:
                temp_l[temp3] = int(coef3)
            # 第四候选人
            temp4, coef4 = judge_restrain(blue_pick, hero_to_choose)
            if temp4 in temp_l.keys():
                temp_l[temp4] += int(coef4)
            else:
                temp_l[temp4] = int(coef4)
            # 候选人竞选
            hero = p_choose(temp_l)
            return

        def pick_red4():
            nonlocal hero
            temp_l = {}
            # 第一候选人
            temp1, coef1 = judge_eva2(red_pick, blue_pick, hero_to_choose)
            temp_l[temp1] = coef1
            # 第二候选人
            temp2, coef2 = get_most_powerful()
            if temp2 in temp_l.keys():
                temp_l[temp2] += int(coef2 * 0.5)
            else:
                temp_l[temp2] = int(coef2 * 0.5)
            # 第三候选人
            temp3, coef3 = judge_system(red_pick, hero_to_choose)
            if temp3 in temp_l.keys():
                temp_l[temp3] += int(coef3)
            else:
                temp_l[temp3] = int(coef3)
            # 第四候选人
            temp4, coef4 = judge_restrain(blue_pick, hero_to_choose)
            if temp4 in temp_l.keys():
                temp_l[temp4] += int(coef4)
            else:
                temp_l[temp4] = int(coef4)
            # 候选人竞选
            hero = p_choose(temp_l)
            return

        def pick_red5():
            nonlocal hero
            temp_l = {}
            # 第一候选人
            temp1, coef1 = judge_eva1(red_pick, blue_pick, hero_to_choose)
            temp_l[temp1] = coef1
            # 第二候选人
            temp2, coef2 = get_most_powerful()
            if temp2 in temp_l.keys():
                temp_l[temp2] += int(coef2 * 0.5)
            else:
                temp_l[temp2] = int(coef2 * 0.5)
            # 第三候选人
            temp3, coef3 = judge_system(red_pick, hero_to_choose)
            if temp3 in temp_l.keys():
                temp_l[temp3] += int(coef3)
            else:
                temp_l[temp3] = int(coef3)
            # 第四候选人
            temp4, coef4 = judge_restrain(blue_pick, hero_to_choose)
            if temp4 in temp_l.keys():
                temp_l[temp4] += int(coef4)
            else:
                temp_l[temp4] = int(coef4)
            # 候选人竞选
            hero = p_choose(temp_l)
            return

    # 下为蓝方选用
    if True:
        if len(pick) == 0:
            """蓝方第一选"""
            pick_blue1()
        elif len(pick) == 3:
            """蓝方第二选,需与第三选关联"""
            pick_blue2()
        elif len(pick) == 4:
            """蓝方第三选,需与第二选关联"""
            pick_blue3()
        elif len(pick) == 7:
            """蓝方第四选,需与第五选关联"""
            pick_blue4()
        elif len(pick) == 8:
            """蓝方第五选,需与第四选关联"""
            pick_blue5()
    # 下为红方选用
    if True:
        if len(pick) == 1:
            """红方第一选,需与第二选关联"""
            pick_red1()
        elif len(pick) == 2:
            """红方第二选,需与第一选关联"""
            pick_red2()
        elif len(pick) == 5:
            """红方第三选,counter_pick"""
            pick_red3()
        elif len(pick) == 6:
            """红方第四选"""
            pick_red4()
        elif len(pick) == 9:
            """红方第五选,counter_pick"""
            pick_red5()
    return hero


