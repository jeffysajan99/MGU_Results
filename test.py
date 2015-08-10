# a = ["aaa", "bbb", "ccc"]
# b = [
#     ["1", "1", "1"],
#     ["2", "2", "2"],
#     ["3", "3", "3"]
# ]
# c = zip(a, b)
# print c
# for i in range(len(b)):
#     b[i].insert(0, a[i])
#
# print b

# print ", ".join(zip(a, [", ".join(i) for i in b]))

data = [u'11012368', u'SAYOOJ K. C.', u'RAJAGIRI SCHOOL OF ENGINEERING AND TECHNOLOGY', u'COMPUTER SCIENCE AND ENGINEERING', u'High Performance Computing, 32, 30, -, Artificial Intelligence, 32, 27, -, Security in Computing, 31, 53, 84, E-commerce, 35, 53, 88, Advanced Mathematics, 38, 77, 115, Computer Graphics Lab, 35, 40, 75, Project, 72, -, 72, Viva Voce, -, 42, 42', u'-', u'-']

raw = data[0:4] + [str(i).strip() for i in data[4].split(",")] + data[5:]
raw = [int(i) if i.isdigit() else i for i in raw]
data = [0 if i=='-' else i for i in raw]
for i in data:
    print data.index(i), i

