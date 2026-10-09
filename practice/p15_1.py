class Zhang:
    def __init__(self, desc, amount):
        self.desc = desc
        self.amount = amount

a = Zhang("早饭",23)
b = Zhang("午饭",60)
c = Zhang("晚饭",25)
# print(a.desc, a.amount)
# print(b.desc,b.amount)
# print("两笔加起来:", a.amount + b.amount)
# print("模具长这样:", Zhang)
# print("造出来的长这样:", a)
S = 0
avc = [a, b, c]
for z in avc:
    S  = S + z.amount
    print(z.desc, z.amount)
print(S)

