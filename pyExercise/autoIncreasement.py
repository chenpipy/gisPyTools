#py代码直接拷贝到arcgis的代码块，存在格式错误，记得调整

# arcgis给选中的要素设置自增，从total开始，自增长的值为increment
total=0
def accumulate(increment):
    global total
    if total:
        total+=increment
    else:
        total=1
    return total

for i in range(100):
    print(accumulate(1))
