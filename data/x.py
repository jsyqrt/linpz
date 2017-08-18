# coding: utf-8

x = 0
with open("sye.json", "r") as f:
    for line in f:
        x += 1
        print line
        if x==3:
            break
