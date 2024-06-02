#encoding=utf-8

'''
@射擊    @益智    @動作    @模擬    @RPG
@戰略    @冒險    ^平台    @獨立    ^RTS
@競技    @恐怖    @體育    @駕駛    @大型電玩
@格鬥    ?免費    ^18禁
'''
def Category_change(type):
    types = set()
    if '射擊' in type:
        types.add('射擊')
    if '角色扮演' or 'RPG' in type:
        types.add('RPG')
    # if 'RPG' in type:
    #     types.add('RPG')
    if '動作' in type:
        types.add('動作')
    if '獨立' in type:
        types.add('獨立')
    if '街機' in type:
        types.add('大型電玩')
    if '冒險' in type:
        types.add('冒險')
    if '模擬' in type:
        types.add('模擬')
    if '運動' in type:
        types.add('體育')
    if '策略' or '戰略' in type:
        types.add('戰略')
    if '競速' in type:
        types.add('駕駛')
    # if '戰略' in type:
    #     types.add('戰略')
    if '解謎' in type:
        types.add('益智')
    if '競' or '對戰' in type:
        types.add('競技')
    # if '對戰' in type:
    #     types.add('競技')
    if '恐怖' in type:
        types.add('恐怖')
    if '格鬥' in type:
        types.add('格鬥')
    # if '免費' in type:
    #     types.add('免費')

    return [t for t in types]

# -----------------------------------

# Test
if __name__ == '__main__':
    L = ['街機和節奏', '射擊', '第一人稱射擊', '動作', '動作角色扮演', '模擬策略', '街機', '運動競速', '免費遊玩', '休閒', '科幻']
    for i in L:
        for j in Category_change(i):
            print(j)
        