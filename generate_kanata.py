#!/usr/bin/env python3
# -*- coding: utf-8 -*-




from itertools import product

# ========== list_A ==========
list_A = [
    ("q", "q"), ("w", "w"), ("e", "e"), ("r", "r"), ("t", "t"),
    ("e f", "y"), ("e r", "u"), ("w e", "i"), ("w r", "o"), ("q r", "p"),
    ("a", "a"), ("s", "s"), ("d", "d"), ("f", "f"), ("g", "g"),
    ("w f", "h"), ("d f", "j"), ("s d", "k"), ("s f", "l"), ("a f", ";"),
    ("z", "z"), ("x", "x"), ("c", "c"), ("v", "v"), ("b", "b"),
    ("s c", "n"), ("c v", "m"), ("x c", ","), ("x v", "."), ("z v", "/"),
]

# ========== list_B ==========
list_B = [
    ("p", "q"), ("o", "w"), ("i", "e"), ("u", "r"), ("y", "t"),
    ("j i", "y"), ("u i", "u"), ("i o", "i"), ("u o", "o"), ("p u", "p"),
    (";", "a"), ("l", "s"), ("k", "d"), ("j", "f"), ("h", "g"),
    ("j o", "h"), ("j k", "j"), ("k l", "k"), ("j l", "l"), ("j ;", ";"),
    ("/", "z"), (".", "x"), (",", "c"), ("m", "v"), ("n", "b"),
    (", l", "n"), ("m ,", "m"), (", .", ","), ("m .", "."), ("m /", "/"),
]

# 提取第1列、第2列
col1_A = [a for a, _ in list_A]
col2_A = [b for _, b in list_A]
col1_B = [a for a, _ in list_B]
col2_B = [b for _, b in list_B]

# 分别做笛卡尔积
col1_product = list(product(col1_A, col1_B))   # 第1列的笛卡尔积
col2_product = list(product(col2_A, col2_B))   # 第2列的笛卡尔积

# 按位置配对：第1列的第k个组合 与 第2列的第k个组合 对应
paired = list(zip(col1_product, col2_product))

print(f"总配对数: {len(paired)}  (30 × 30 = 900)")
print()

# 输出格式示例
for i, ((c1a, c1b), (c2a, c2b)) in enumerate(paired, 1):
    # print(f"{i:3d}. 第1列积: ({c1a!r}, {c1b!r})  |  第2列积: ({c2a!r}, {c2b!r})")
    print(f" ({c1a} {c1b}  spc )   (  macro   {c2a} {c2b} spc ) ")



print("------------------------------")    
for i, (input, output) in enumerate(list_A, 1):
    print(f" ({input}     spc )   (  macro   {output}  spc ) " )


    
    
