#!/usr/bin/env python3
# -*- coding: utf-8 -*-

with open('aut-num.txt', 'r', encoding='utf-8') as fin:
    s = fin.read()

l = s.strip().split('\n')
l = [x.strip().replace('AS424242', '') for x in l]
# print(l)

free_list = []
for i in range(4000):
    n = str(i).rjust(4, '0')
    if n not in l:
        print(n)
        free_list.append(n)

print('========')
print(free_list)
print(len(free_list))

with open('aut-num_free.txt', 'w', encoding='utf-8') as fout:
    fout.write(str(free_list))


for i in free_list:
    if i[1] == i[2]:
        print(i)

for i in free_list:
    if int(i[2]) == int(i[1]) + 1 and int(i[3]) == int(i[2]) + 1:
        print(i)

for i in free_list:
    if int(i[2]) == int(i[1]) + 2 and int(i[3]) == int(i[2]) + 2:
        print(i)

for i in free_list:
    if i[2] == '8' and i[3] == '8':
        print(i)
