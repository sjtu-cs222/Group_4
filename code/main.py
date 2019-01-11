# -*- coding: utf-8 -*-
"""this is a python file which contains main function"""
import bp
import data
import eva
import predict

if __name__ == '__main__':
    data.create_all()
    match = bp.bp_pve()
    predict.get_winning_rate(match)

