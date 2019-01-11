# -*- coding: utf-8 -*-
"""
this is a python file for ban-pick simulation
"""
import ai
import data


def ban_input(dire, ban, pick):
    """玩家在bp过程中的选用"""
    hero_att = data.get_hero_att()
    hero = input('请'+dire+"方禁用英雄：")
    while hero in ban.values() or hero in pick.values() or hero not in hero_att.keys():
        hero = input('请'+dire+"方重新禁用英雄：")
    return hero


def pick_input(dire, ban, pick):
    """玩家在bp过程中的选用"""
    hero_att = data.get_hero_att()
    hero = input('请' + dire + "方选择英雄：")
    while hero in ban.values() or hero in pick.values() or hero not in hero_att.keys():
        hero = input('请' + dire + "方重新选择英雄：")
    return hero


def bp_output(ban, pick):
    """输出bp结果"""
    blue_ban = 'blue_ban'
    red_ban = 'red_ban'
    blue_pick = 'blue_pick'
    red_pick = 'red_pick'
    whitespace = "       "
    pick_node = [1, 5, 9]
    print("{0:9}\t{1}".format("蓝方禁用：", "红方禁用：", chr(12288)))
    i = 0
    for i in range(1, int(len(ban)/2)+1):
        print("{0:11}\t{1}".format(ban[blue_ban+str(i)], ban[red_ban+str(i)], chr(12288)))
    if len(ban) % 2 != 0:
        if len(ban) < 4:
            print("{0:11}".format(ban[blue_ban+str(i+1)], chr(12288)))
        elif len(ban) > 4:
            print("{0:13}\t{1}".format(whitespace, ban[red_ban+str(i+1)], chr(12288)))

    print("{0:9}\t{1}".format("蓝方选用：", "红方选用：", chr(12288)))
    j = 0
    for j in range(1, int(len(pick)/2)+1):
        print("{0:11}\t{1}".format(pick[blue_pick+str(j)], pick[red_pick+str(j)], chr(12288)))
    if len(pick) % 2 != 0:
        if len(pick) in pick_node:
            print("{0:11}".format(pick[blue_pick + str(j+1)], chr(12288)))
        else:
            print("{0:13}\t{1}".format(whitespace, pick[red_pick + str(j+1)], chr(12288)))
    return


def bp_simulation(banb, banr, pickb, pickr):
    """此函数用于模拟bp过程
    ：banb： 蓝色方禁用的输入函数
    ：banr： 红色方禁用的输入函数
    ：pickb： 蓝色方选用的输入函数
    ：pickr： 红色方选用的输入函数
    ：return： 无
    """
    ex = 1
    blue_ban = 'blue_ban'
    red_ban = 'red_ban'
    blue_pick = 'blue_pick'
    red_pick = 'red_pick'
    pick_node = [1, 4, 5, 8, 9]
    while ex:
        print("开始ban-pick！")
        ban = {}
        pick = {}
        # 4bans
        ban_count = 0
        for i in range(2):
            ban_count += 1
            ban[blue_ban + str(ban_count)] = banb('蓝色', ban, pick)
            ban[red_ban + str(ban_count)] = banr('红色', ban, pick)
        # 6picks
        pick_count = 0
        bp_count = 0
        rp_count = 0
        for i in range(6):
            pick_count += 1
            if pick_count in pick_node:
                bp_count += 1
                pick[blue_pick + str(bp_count)] = pickb('蓝色', ban, pick)
            else:
                rp_count += 1
                pick[red_pick + str(rp_count)] = pickr('红色', ban, pick)
        # 4bans
        for i in range(2):
            ban_count += 1
            ban[red_ban + str(ban_count)] = banr('红色', ban, pick)
            ban[blue_ban + str(ban_count)] = banb('蓝色', ban, pick)
        # 4picks
        for i in range(4):
            pick_count += 1
            if pick_count in pick_node:
                bp_count += 1
                pick[blue_pick + str(bp_count)] = pickb('蓝色', ban, pick)
            else:
                rp_count += 1
                pick[red_pick + str(rp_count)] = pickr('红色', ban, pick)
        print("ban-pick结束！")
        bp_output(ban, pick)
        red, blue = ai.get_pick(pick)
        match = {"red": red, "blue": blue}
        """
        rate_predict = int(input("请选择是否评估阵容胜率(0:no,1:yes):"))
        if rate_predict:
            predict(match)
        """
        ex = int(input("请选择是否重新开始ban-pick(0:no,1:yes):"))
    return match


def bp_test_simulation(banb, banr, pickb, pickr):
    """此函数用于模拟bp过程
    ：banb： 蓝色方禁用的输入函数
    ：banr： 红色方禁用的输入函数
    ：pickb： 蓝色方选用的输入函数
    ：pickr： 红色方选用的输入函数
    ：return： 无
    """
    ex = 1
    blue_ban = 'blue_ban'
    red_ban = 'red_ban'
    blue_pick = 'blue_pick'
    red_pick = 'red_pick'
    pick_node = [1, 4, 5, 8, 9]
    while ex:
        print("开始ban-pick！")
        ban = {}
        pick = {}
        # 4bans
        ban_count = 0
        for i in range(2):
            ban_count += 1
            ban[blue_ban + str(ban_count)] = banb('蓝色', ban, pick)
            bp_output(ban, pick)
            ban[red_ban + str(ban_count)] = banr('红色', ban, pick)
        # 6picks
        pick_count = 0
        bp_count = 0
        rp_count = 0
        for i in range(6):
            pick_count += 1
            if pick_count in pick_node:
                bp_count += 1
                pick[blue_pick + str(bp_count)] = pickb('蓝色', ban, pick)
                bp_output(ban, pick)
            else:
                rp_count += 1
                pick[red_pick + str(rp_count)] = pickr('红色', ban, pick)
        # 4bans
        for i in range(2):
            ban_count += 1
            ban[red_ban + str(ban_count)] = banr('红色', ban, pick)
            ban[blue_ban + str(ban_count)] = banb('蓝色', ban, pick)
            bp_output(ban, pick)
        # 4picks
        for i in range(4):
            pick_count += 1
            if pick_count in pick_node:
                bp_count += 1
                pick[blue_pick + str(bp_count)] = pickb('蓝色', ban, pick)
                bp_output(ban, pick)
            else:
                rp_count += 1
                pick[red_pick + str(rp_count)] = pickr('红色', ban, pick)
        print("ban-pick结束！")
        bp_output(ban, pick)
        bp_output(ban, pick)
        red, blue = ai.get_pick(pick)
        match = {"red": red, "blue": blue}
        ex = int(input("请选择是否重新开始ban-pick(0:no,1:yes):"))
    return match


def bp_pvp():
    bp_test_simulation(ban_input, ban_input, pick_input, pick_input)
    return


def bp_test_pve():
    match = bp_test_simulation(ai.ban_ai_input, ban_input, ai.pick_ai_input, pick_input)
    # bp_test_simulation(ai.ban_input, ban_ai_input, ai.pick_input, pick_ai_input)
    return match


def bp_pve():
    dire = int(input("欢迎来到人机对抗模式，请选择你的阵容方(0:red, 1:blue)"))
    if not dire:
        match = bp_test_simulation(ai.ban_ai_input, ban_input, ai.pick_ai_input, pick_input)
    else:
        match = bp_test_simulation(ban_input, ai.ban_ai_input, pick_input, ai.pick_ai_input)
    return match


def bp_eve():
    return bp_test_simulation(ai.ban_ai_input, ai.ban_ai_input, ai.pick_ai_input, ai.pick_ai_input)
