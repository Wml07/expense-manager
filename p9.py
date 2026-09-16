
dc = {"早饭":23, "午饭":60}
print(dc.items())

for cate in dc:
    print(f"{cate}:{dc[cate]}元")


for C,M in dc.items():
    print(f"{C}:{M}元")