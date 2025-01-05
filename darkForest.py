import random

# 参数设置
POINT_FIGHT = 0.2
POINT_FIGHTWIN = 1.5
POINT_FIGHTLOSE = 1.0
POINT_COOPERATION = 1.2

class Civilization:
    """文明类：描述文明的基本属性和状态"""
    def __init__(self, mark, attitude, isPositive):
        self.mark = mark  # 文明分数
        self.state = 1  # 0：死亡，1：存活
        self.attitude = attitude  # 0：友善，1：中立，2：好斗
        self.isPositive = isPositive  # 1：积极探索，0：消极保守

def analyzeList(uniList):
    """统计文明的态度和积极性分布"""
    n0, n1, n2, nPos, nNeg, nTotal = 0, 0, 0, 0, 0, 0
    for cv in uniList:
        if cv.state == 1:  # 只统计存活文明
            nTotal += 1
            if cv.attitude == 0:
                n0 += 1
            elif cv.attitude == 1:
                n1 += 1
            elif cv.attitude == 2:
                n2 += 1
            if cv.isPositive == 1:
                nPos += 1
            else:
                nNeg += 1
    print(f'nTotal: {nTotal} n0: {n0} n1: {n1} n2: {n2} nPos: {nPos} nNeg: {nNeg}')

def activeCv(cv1, cv2):
    """两个文明之间的互动"""
    if cv1.attitude == 2 or cv2.attitude == 2:  # 任意一方好斗
        n = (cv1.mark + cv2.mark) * POINT_FIGHTWIN
        if cv1.mark > cv2.mark:  # cv1胜利
            cv1.mark += n * POINT_FIGHTWIN
            cv2.mark -= n * POINT_FIGHTLOSE
        else:  # cv2胜利
            cv2.mark += n * POINT_FIGHTWIN
            cv1.mark -= n * POINT_FIGHTLOSE
    elif cv1.attitude == 0 or cv2.attitude == 0:  # 至少一方友善
        n = (cv1.mark + cv2.mark) * POINT_COOPERATION
        cv1.mark += n
        cv2.mark += n
    return [cv1, cv2]

def checkDead(cv):
    """检查文明是否死亡"""
    if cv.mark <= 0:
        cv.state = 0
    return cv

def getPositiveCvs(uniList):
    """获取宇宙中积极探索的文明"""
    return [cv for cv in uniList if cv.isPositive == 1 and cv.state == 1]

def findOther(cv, uniList):
    """随机寻找另一个互动文明"""
    while True:
        target = random.choice(uniList)
        if target != cv and target.state == 1:  # 目标需存活且非自身
            return target

def isAllDead(uniList):
    """是否仅剩一个文明存活"""
    alive_count = sum(1 for cv in uniList if cv.state == 1)
    return alive_count <= 1

def initUniverse():
    """初始化宇宙文明并开始模拟"""
    originList = [
        Civilization(
            mark=random.randint(8000, 12000),
            attitude=random.randint(0, 2),
            isPositive=random.randint(0, 1)
        ) for _ in range(200)
    ]

    print('-' * 40)
    print('Origin Universe:')
    analyzeList(originList)
    print('-' * 40)

    roundList = originList

    while True:
        posList = getPositiveCvs(roundList)  # 获取积极探索的文明
        fightList = [findOther(cv, roundList) for cv in posList]  # 找到互动目标

        reList = []
        for i in range(len(posList)):
            activedCvs = activeCv(posList[i], fightList[i])  # 文明互动
            reList.extend(activedCvs)

        # 检查死亡状态
        for cv in reList:
            checkDead(cv)

        # 更新轮次的文明列表
        roundList = list({cv for cv in reList if cv.state == 1})

        # 打印统计结果
        analyzeList(roundList)
        highest = max(cv.mark for cv in roundList if cv.state == 1)
        lowest = min(cv.mark for cv in roundList if cv.state == 1 and cv.mark > 0)
        print(f'high: {highest} low: {lowest}')

        # 检查是否仅剩一个文明存活
        if isAllDead(roundList):
            break

# 开始模拟
initUniverse()
