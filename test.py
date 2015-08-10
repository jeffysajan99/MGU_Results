a = ["aaa", "bbb", "ccc"]
b = [
    ["1", "1", "1"],
    ["2", "2", "2"],
    ["3", "3", "3"]
]
c = zip(a, b)
print c
for i in range(len(b)):
    b[i].insert(0, a[i])

print b

# print ", ".join(zip(a, [", ".join(i) for i in b]))