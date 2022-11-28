# -*- coding: utf-8 -*-
import os
import random

from Utils.LoadConfig import LoadConfig
from Utils.OtherTools import OT


class GlobalEnumG:
    if not os.path.exists(OT.abspath(f"/Res/配置文件.ini")):
        LoadConfig.init_config()
    Ver = '2.26'
    TestLog = True if LoadConfig.getconf('全局配置', '日志') == '1' else False
    TouchWait = int(LoadConfig.getconf('全局配置', '点击延时'))
    GamePackgeName = r'com.nexon.maplem.global'  # r'com.nexon.maplem.japan'  # r'com.nexon.maplem.global'
    WaitTime = 1
    ExitBtnTime = 2  # 点击退出游戏否按钮等待时长
    FindImgTimeOut = 20  # 查找图片等待超时时间
    TouchDurationTime = 1  # 延时点击
    LoginGameTimeOut = 600  # 登录超时时长
    UiCheckTimeOut = 900  # 界面操作超时时长
    SelectCtrTimeOut = 300  # 操作超时时长
    TouchEx = random.randint(0, 2)  # 点击偏移
    TouchEy = random.randint(0, 2)
    if TouchWait != 0:
        TouchWaitTime = TouchWait
    else:
        TouchWaitTime = 3  # 点击后等待时长
    TaskWaitTime = 2  # 任务等待时长
    BackWaitTime = 2  # 按back后等待时长
    TaskCheckTime = 120  # 任务检查等级时间
    CheckRoleTime = 3600  # 检查角色等级,计算金币

    PWD_POS = {
        '0': (805, 478),
        '1': (515, 523),
        '2': (608, 508),
        '3': (674, 515),
        '4': (514, 434),
        '5': (610, 433),
        '6': (710, 437),
        '7': (513, 347),
        '8': (613, 339),
        '9': (663, 324)
    }

    JN_POS = {
        0: (378, 372),
        1: (251, 415),
        2: (248, 298),
        3: (330, 235),
        4: (451, 233)
    }
    Discard_ID = {
        '0': '红宝石',
        '1': '蓝宝石',
        '2': '绿宝石',
        '3': '紫宝石',
        '4': '黄宝石',
        '5': '可疑的武器练成粉袋子',
        '6': '可疑的防具练成粉袋子',
        '7': '进化系统硬币',
        '8': '不灭法老戒指',
        '9': '混沌皮卡啾标志',
        '10': '愤怒的残暴炎魔腰带'

    }
    ZhiYe = {
        "长按技能": "0",
        "短按": "1"
    }
    StatesInfo = {
        'InGame': {'name': "游戏中", 'id': 1},
        'Nothing': {'name': "无任务", 'id': 2},
        'Wait': {'name': "等待任务", 'id': 2},
        'Login': {'name': "登录游戏", 'id': 2},
        'AutoChoose': {'name': "一键托管", 'id': 99},
        'Check': {'name': "检查界面", 'id': -1},
        'BuyY': {'name': "买药", 'id': 4},
        'FuHuo': {'name': "复活", 'id': 3},
        'NetErr': {'name': "网络异常", 'id': 3},
        'BagSell': {'name': "背包出售", 'id': 5},
        'BagClear': {'name': "背包清理", 'id': 5},
        'UpEquip': {'name': "升级装备", 'id': 8},
        'StrongEquip': {'name': "强化装备", 'id': 8},
        'LearnSkill': {'name': "学习技能", 'id': 8},
        'UseSkill': {'name': "摆放技能", 'id': 8},
        'UsePet': {'name': "摆放宠物", 'id': 8},
        'GetReward': {'name': "领取奖励", 'id': 8},
        'CheckXT': {'name': "星图检查", 'id': 8},
        'CheckYT': {'name': "野图检查", 'id': 8},
        'AutoTask': {'name': "自动任务", 'id': 1},
        'AutoMR': {'name': "自动每日", 'id': 2},
        'AutoBat': {'name': "自动挂机", 'id': 3},
        'AutoBoss': {'name': "混BOSS图", 'id': 2},
        'AutoHDboss': {'name': '混沌boss', 'id': 2},
        'CheckRole': {'name': "检查角色", 'id': 5},
        'GetLevelReard': {'name': "领取成长奖励", 'id': 5},
        'CheckGold': {'name': "计算产出", 'id': 6},
        'CheckTeamState': {'name': "检查队伍状态", 'id': 6},
    }
    ExecuteStates = ['AutoTask', 'AutoBat', 'Nothing', 'Wait', 'CheckTeamState']
    SelectStates = ['InGame',
                    'Check',
                    'Login',
                    'FuHuo',
                    'NetErr',
                    'BuyY',
                    'BagSell',
                    'BagClear',
                    'UseSkill',
                    'UsePet',
                    'UpEquip',
                    'StrongEquip',
                    'GetReward',
                    'CheckXT',
                    'CheckYT',
                    'AutoBoss',
                    'AutoHDboss',
                    'AutoMR',
                    'CheckRole',
                    'GetLevelReard',
                    'CheckGold',
                    'AutoChoose']


class ImgEnumG:
    """图片数据"""
    TIP = [(271, 47, 1018, 182), '222222', '引导提示']
    UI_CLOSE = [(1060, 24, 1149, 97), '222222', '弹窗']
    UI_QR = [(0, 0, 1280, 720), '222222', '确认']
    UI_QBLQ = [(0, 0, 1280, 720), '222222', '全部领取']
    MOGU = [(162, 10, 1120, 694), '222222', '蘑菇']
    MOGU1 = [(162, 10, 1120, 694), '222222', '蘑菇1']
    JUBAO = [(162, 10, 1120, 694), "222222", r'举报']
    # 活动
    QD_1 = [(1218, 12, 1265, 55), '222222', '活动签到1']
    # 登录相关
    GAME_ICON = [(0, 0, 1280, 720), '111111', '游戏icon']
    LOGIN_FLAG = [(973, 485, 1278, 715), '222222', '游戏登陆标志']
    LOGIN_TIPS = [(1240, 14, 1264, 61), '222222', '登录弹窗']
    # 任务相关
    ZB_TS = [(722, 144, 1272, 656), '222222', '装备提升']  # 装备上绿色小箭头
    TASK_TAB = [(0, 0, 1280, 720), '333333', '任务页签']
    TASK_START = [(341, 529, 482, 715), '222222', '任务可开始']
    TASK_TAKE = [(1067, 403, 1150, 438), '222222', '任务接受']
    TASK_OVER = [(0, 0, 1280, 720), '222222', '任务完成']
    TASK_REWARD = [(595, 630, 685, 659), '222222', '任务奖励']
    CZJL_ICON = [(3, 122, 498, 185), '222222', '成长奖励']
    # 活动
    KT_QBLQ = [(1138, 650, 1223, 680), '222222', '课题全部领取']
    # 背包清理
    BAG_MAX_IMG = [(1140, 36, 1195, 64), '222222', '背包满']
    BAG_GOLD = [(858, 19, 1115, 63), '333333', '金币详情']
    # 组队相关
    TEMA_ING = [(332, 245, 410, 332), '222222', '组队中']

    # 装备
    EQ_WZB = [(225, 97, 370, 211), '111111', '无装备']
    EQ_UP = [(559, 621, 717, 701), '222222', '升级']  # 升级确认按钮
    EQ_UP_QR = [(492, 604, 789, 682), '222222', '升级确认']
    # 买药
    CZ_FUHUO = [(267, 472, 525, 585), '222222', '复活']
    BUY_YS_LOGIN = [(792, 162, 914, 685), '222222', '药水登录']
    JN_LOGIN_2 = [(790, 305, 912, 382), '222222', '药水登录']
    YS_NUM_OCR = {
        '5': [(733, 631, 810, 658), '500'],
        '4': [(733, 631, 810, 658), '400'],
        '3': [(733, 631, 810, 658), '300'],
        '2': [(733, 631, 810, 658), '200'],
        '0': [(733, 631, 810, 658), '100'],
    }
    YS_LEVEL = {
        '4阶药水': (759, 253),
        '5阶药水': (1025, 235),
        '6阶药水': (1210, 244),
        '7阶药水': (318, 445),
        '8阶药水': (490, 448),
        '9阶药水': (594, 445)
    }
    YS_NUM = {
        '0': (1024, 517),
        '1': (739, 317),
        '2': (839, 317),
        '3': (939, 317),
        '4': (739, 417),
        '5': (839, 417),
        '6': (939, 417),
        '7': (739, 517),
        '8': (839, 517),
        '9': (939, 517),
    }

    # 清理背包
    RED_BS = [(738, 161, 1266, 644), '222222', '红宝石']
    G_BS = [(738, 161, 1266, 644), '222222', '绿宝石A']
    Z_BS = [(738, 161, 1266, 644), '222222', '紫宝石A']
    L_BS = [(738, 161, 1266, 644), '222222', '蓝宝石A']
    JZT_DJ = [(738, 161, 1266, 644), '222222', '金字塔产物']
    FJ_HE1 = [(738, 161, 1266, 644), '222222', '防具合成石1']
    FJ_HE2 = [(738, 161, 1266, 644), '222222', '防具合成石2']
    WQ_HE1 = [(738, 161, 1266, 644), '222222', '武器合成石1']
    WQ_HE2 = [(738, 161, 1266, 644), '222222', '武器合成石2']
    BAG_NULL = [(738, 161, 1266, 644), '111111', '空格子']
    YM_YD = [(738, 161, 1266, 644), '050505', '愤怒的残暴炎魔腰带']
    PKJ_FLAG = [(738, 161, 1266, 644), '050505', '混沌皮卡啾标志']

    # 宠物
    PET_1 = [(349, 143, 433, 217), '222222', '默认宠物1']
    PET_2 = [(349, 143, 433, 217), '222222', '默认宠物2']
    CW_TYPE = {
        'A': [[(735, 163, 1268, 651), '222222', '宠物A1'],
              [(735, 163, 1268, 651), '222222', '宠物A2'],
              [(735, 163, 1268, 651), '222222', '宠物A3']],
        'B': [[(735, 163, 1268, 651), '222222', '宠物B1'],
              [(735, 163, 1268, 651), '222222', '宠物B2'],
              [(735, 163, 1268, 651), '222222', '宠物B3']],
        'C': [[(735, 163, 1268, 651), '222222', '宠物C1'],
              [(735, 163, 1268, 651), '222222', '宠物C2'],
              [(735, 163, 1268, 651), '222222', '宠物C3']]
    }
    PET_POS = {
        1: [131, 130, '2b3646', 'ee7546'],
        2: [127, 219, '2b3646', 'ee7546'],
        3: [127, 306, '2b3646', 'ee7546']
    }
    # BOSS
    YM = [(65, 103, 262, 194), '222222', '炎魔']
    PKJ = [(704, 104, 891, 193), '222222', '皮卡啾']
    NH = [(982, 97, 1222, 194), '555555', '女皇']
    # 每日
    MR_BAT_EXIT = [(1202, 251, 1269, 317), '222222', '战斗退出']
    JRGH_IMG = [(0, 0, 1280, 720), '222222', '加入公会']

    # ------

    # 组队
    TEAM_TAB = [(4, 172, 82, 363), '333333', '组队页签']
    TEAM_XZDW = [(86, 333, 215, 381), '222222', '寻找队伍']
    PWD_TEAM = [(897, 189, 964, 533), '111111', '密码队伍']
    EXIT_TEAM = [(290, 187, 328, 446), '222222', '离开队伍']
    SKIP_NEW = [(2, 72, 491, 212), '111111', '新内容']
    JN_TEACH = [(790, 569, 981, 717), '111111', '教学']
    GX_XZ_ING = [(0, 0, 1280, 720), '222222', '数据更新']


class BatEnumG:
    TASK_ID = {
        '一键托管': {'id': '99', 'state': 'AutoChoose'},
        '自动任务': {'id': '1', 'state': 'AutoTask'},
        '自动每日': {'id': '2', 'state': 'AutoMR'},
        '混Boss图': {'id': '5', 'state': 'AutoBoss'},
        '装备技能': {'id': '6', 'state': 'UseSkill'},
        '穿戴新手宠物': {'id': '7', 'state': 'UsePet'},
        '默认设置': {'id': '8', 'state': 'Login'},
        '开箱子': {'id': '9', 'state': 'Login'},
        '强化装备': {'id': '10', 'state': 'StrongEquip'},
        '升级装备': {'id': '11', 'state': 'UpEquip'},
        '背包出售': {'id': '11', 'state': 'BagSell'},
        '背包清理': {'id': '12', 'state': 'BagClear'},
        '奖励领取': {'id': '13', 'state': 'GetReward'},
    }
    MAP_DATA = {
        '1': {'NULL': []},
        '2': {'NULL': []},
        '3': {'研究所102': [[898, 1211, 161], [138], [138], [50, 0, 0], [1252, 1153, 966, 870]],
              '西边森林': [[972, 1148, 134], [134], [134], [80, 100, 50], [1252, 1153, 966, 870]],
              '冰冷死亡战场': [[924, 1210, 141], [1059, 134], [134], [50, 30, 100], [1252, 1153, 966, 870]],
              '龙蛋': [[1000, 1105, 147], [1019, 1072, 134], [1059, 134], [50, 50, 10], [1154, 1100, 1050, 970]],
              '爱奥斯塔入口': [[997, 1086, 147], [953, 1135, 134], [1158, 134], [30, 70, 100], [1252, 1153, 966, 870]],
              '奥斯塔入口': [[1043, 147], [986, 134], [948, 134], [70, 100, 100], [1252, 1153, 966, 870]],
              '天空露台2': [[910, 987, 1092, 1227, 142], [134], [134], [30, 0, 0], [1252, 1153, 966, 870]],  # 987 x1 1092x2
              '机械室': [[901, 1082, 153], [1096, 134], [1114, 134], [50, 100, 100], [1252, 1153, 966, 870]],
              '时间漩涡': [[1012, 1086, 147], [1038, 1113, 134], [1077, 134], [50, 50, 100], [1252, 1153, 1000, 970]],
              '忘却之路4': [[1024, 1101, 153], [1149, 134], [1210, 134], [30, 70, 100], [1252, 1153, 966, 873]],  # 1101 x2
              '偏僻泥沼': [[947, 1210, 147], [920, 1154, 134], [1199, 134], [30, 70, 100], [1252, 1153, 966, 860]],
              '变形的森林': [[982, 1141, 153], [961, 1176, 134], [134], [50, 100, 0], [1252, 1103, 966, 860]],
              '武器库星图': [[929, 1092, 1214, 153], [997, 134], [134], [50, 50, 0], [1252, 1153, 966, 870]],
              '灰烬之风高原': [[1035, 1060, 153], [1024, 1060, 1119, 134], [134], [50, 50, 0], [1252, 1153, 966, 870]],
              '崎岖的峡谷': [[1020, 1065, 153], [948, 1170, 134], [1060, 134], [50, 100, 30], [1252, 1153, 966, 860]]

              },
        # ----野图
        '4': {
            '露台2': [[958, 1170, 141], [134], [134], [60, 0, 0], [1252, 1153, 966, 870]],
            '忘却之路3': [[974, 1169, 153], [134], [134], [70, 0, 0], [1252, 1153, 966, 870]],  # 1169x2
            '神秘森林': [[909, 1193, 134], [905, 1176, 134], [134], [70, 100, 0], [1252, 1153, 966, 870]],
            '武器库': [[931, 1169, 153], [998, 1121, 134], [134], [50, 50, 0], [1252, 1153, 966, 870]],
            '崎岖峡谷': [[1020, 1065, 153], [948, 1170, 134], [1060, 134], [60, 100, 0], [1252, 1153, 966, 870]],
            '木菇菇林': [[1027, 1111, 153], [134], [134], [30, 0, 0], [1165, 1085, 1050, 960]]
        }

    }
    # 0:识别左上角地图名,1:星图星数
    MAP_OCR = {
        'NULL': [[0, ''], 0],
        '研究所102': ['40'],
        '西边森林': ['45'],
        '冰冷死亡战场': ['65'],
        '龙蛋': ['80'],
        '爱奥斯塔入口': ['90'],
        '奥斯塔入口': ['105'],
        '天空露台2': ['110'],
        '机械室': ['113'],
        '时间漩涡': ['115'],
        '忘却之路4': ['120'],
        '偏僻泥沼': ['130'],
        '变形的森林': ['136'],
        '武器库星图': ['142'],
        '灰烬之风高原': ['144'],
        '崎岖的峡谷': ['147'],
        # ----野图
        '神秘森林': ['80', 'mnesl', 'sm'],
        '露台2': ['110', 'ldsh', 'lt'],
        '忘却之路3': ['120', 'sjsd', 'wq'],
        '武器库': ['139', 'wlzm', 'wqk'],
        '崎岖峡谷': ['144', 'wlzm', 'qqxg'],
        '木菇菇林': ['150', 'alsl', 'mggl'],
    }
    # 米纳雨森林
    # 路德斯湖
    # 艾霰森林
    # 诗固神殿
    # 武陵桃圆
    # 未来之門


class RgbEnumG:
    ENUM_BTN = [1222, 52, 'ffffff']  # 菜单按钮
    EXIT_FOU = [391, 532, '4c87b0']  # 退出游戏-否
    CLOSE_GAME = [433, 543, '4c87b0']  # 关闭游戏-否
    FUHUO_BTN = [293, 522, '4c87b0']  # 复活按钮
    BG_PINDAO = [1083, 55, 'ee7046']  # 地图主界面-变更频道
    MAP_QWPD = [529, 635, 'ee7046']  # 地图-前往频道
    MAP_SJYD = [927, 657, '4c87b0']  # 瞬间移动
    HD_BJBS = [1058, 655, 'EDCE01']  # 活动签到
    HD_BJBS_LQ = [1058, 655, 'EC9C00']

    KSDY = [971, 109, 'ee7046']  # [16, 14, '415066']  # 快速单元
    XLZC = [53, 429, '617a95']  # 星力战场
    XLZC_YD = [1117, 658, 'ee7046']  # 星力战场-移动
    XLZC_YDQR = [699, 523, 'ee7046']  # 星力战场-移动确认
    XLZC_YDOK = [568, 519, 'ee7046']  # 星力战场-移动完成
    YS_LOGIN = [612, 124, 'f2f2f2']  # [565, 128, 'f2f2f2']  # 药水登录界面
    YS_SHOP = [925, 544, 'f2f2f2']  # 药水商店
    YS_XQ = [1040, 648, 'ee7046']  # 药水详情
    YS_GMQR = [686, 523, 'ee7046']  # 药水购买确认
    BACK = [16, 10, '344154']  # 左上角返回
    JR = [1012, 645, 'ee7046']  # 进入按钮
    MR_EXIT_TEAM = [678, 517, 'ee7046']  # 进入副本提示有队伍
    TEAM_KS = [398, 389, '5a5531']  # 组队进入
    EXIT_TEAM_QR = [714, 525, 'ee7046']
    WL_PM = [592, 633, 'ee7046']  # 武林排名界面
    WL_M = [16, 10, '344154']  # 武林界面
    WL_JR = [1068, 650, 'ee7046']  # 武林进入
    WL_JRQR = [669, 630, 'ee7046']  # 武林进入确认
    WL_QX = [406, 635, '4c87b0']  # 武林入场取消
    JZT_JR = [999, 646, 'ee7046']  # 金字塔进入
    JZT_JRQR = [714, 525, 'ee7046']  # 金字塔进入确认
    JZT_END = [566, 574, '4c87b0']
    JYDC_END = [273, 638, '4c87b0']  # 菁英地城结束
    JYDC_MAX = [825, 439, '617a95']  # 菁英地城max

    MRDC_JR = [1012, 645, 'ee7046']  # 每日地城进入
    MRDC_JRQR = [661, 625, 'ee7046']  # 每日地城进入确认
    MRDC_HD = [143, 620, 'ee7546']  # 混沌模式

    GWSL_END = [283, 206, 'f2f2f2']

    TBB_JR = [768, 618, 'ee7046']
    TBB_QR = [567, 523, 'ee7046']

    JHXT_JRQR = [734, 640, 'ee7046']
    JHXT_END = [556, 616, '4c87b0']

    CYRQ_END = [376, 517, '4c87b0']
    CYRQ_JR = [1055, 656, 'ee7046']
    CYQR_JR_QR = [908, 446, 'e9e9e9']
    CYQR_JR_QR1 = [682, 549, 'ee7046']
    CYRQ_JR_F = [1055, 656, 'c3c3c3']

    MNDC_XZ = [57, 138, '2b3646']
    MNDC_XZ2 = [78, 214, '2b3646']
    MNDC_XZ3 = [633, 331, 'ffffff']
    MNDC_JRQR = [670, 652, 'ee7046']
    MNDC_JR = [1053, 650, 'ee7046']
    MNDC_END = [564, 593, 'ee7046']
    MNDC_JG_QR = [564, 593, 'ee7046']  # 最终结果-离开
    MNDC_JG = [384, 598, '4c87b0']  # 迷你地城结果-移动
    MNDC_JG_LK = [523, 604, 'ee7046']
    BAT_JG = [540, 524, 'ee7046']  # 自动战斗结果
    BAT_AUTO_QR = [733, 563, 'ee7046']  # 自动战斗确认
    BAT_AUTO_M = [505, 543, 'dddddd']  # 自动战斗界面

    AUTO_FREE = [897, 391, '617a95']
    AUTO_10 = [709, 344, 'ffd741']
    AUTO_30 = [840, 336, 'ffd741']
    AUTO_60 = [908, 338, 'ffd741']

    XGT_JR = [1167, 642, 'ee7046']
    XGT_ZCJR = [983, 621, 'ee7046']
    XGT_JR_F = [1167, 642, 'c3c3c3']

    GWGY_JR = [1084, 656, 'ee7046']
    GWGY_JR_F = [1084, 656, 'c3c3c3']
    GWGY_JRQR = [749, 633, 'ee7046']

    YZD_KN = [156, 339, '2b3646']
    YZD_PT = [159, 259, '2b3646']
    YZD_JR = [1055, 651, 'ee7046']
    YZD_JR_F = [1052, 648, 'c3c3c3']

    GH_M = [549, 104, 'eaeaea']
    GH_JR = [692, 515, 'ee7046']
    GH_XJR = [925, 662, 'ee7046']  # 加入新公会
    GH_JRQR = [840, 528, 'ee7046']
    GH_RYZ = [709, 668, 'eff3ef']
    GH_RYZ_JR = [433, 666, 'ee7046']
    GH_RYZ_JR_F = [433, 666, 'c3c3c3']
    GH_WXDC = [709, 668, 'f2f2f2']
    GH_WXDC_JR = [449, 653, 'ee7046']
    GH_WXDC_JR_F = [449, 653, 'c3c3c3']

    EXIT_TEAM = [669, 534, 'ee7046']  # 离队确认
    TEAM_ZDJR = [99, 277, 'ee7046']  # 自动加入
    TEAM_ZDJR_QR = [1126, 162, '617a95']  # 自动加入-确认
    TEAM_CLDW = [99, 214, '4c87b0']  # 创立队伍按钮
    TEAM_CLDW_M = [53, 671, 'f2f2f2']  # 创立队伍界面
    TEAM_XZDW = [102, 350, '50b65d']
    TEAM_CLQR = [536, 642, 'ee7046']
    TEAM_MMDW = [102, 521, '3b78a2']  # 密码队伍选项
    TEAM_QRMM = [524, 609, 'ee7046']  # 确认密码
    TEAM_CXZL = [927, 651, '4c87b0']

    TEAM_SQJR = [1125, 647, 'ee7046']  # 申请加入
    TEAM_SQJR_F = [1125, 647, 'c3c3c3']  # 无法申请加入

    MAP_XL = [1108, 655, 'ee7046']  # 寻路按钮
    MAP_XLQR = [660, 521, 'ee7046']  # 寻路按钮确认
    MAP_ERR = [520, 520, 'ee7046']  # 无法瞬间移动
    MAP_SJYD_QR = [747, 529, '4c87b0']  # 瞬间移动确认

    BAG_M = [407, 32, 'ee7046']  # 背包界面-奖励优惠保管箱
    BAG_GOLD_QR = [579, 510, 'ee7046']
    BAG_BS = [1043, 132, 'aab6c8']  # 宝石栏
    BAG_SP = [954, 129, 'aab6c8']  # 饰品
    BAG_FJ = [860, 122, 'aab6c8']  # 防具
    BAG_WQ = [770, 133, 'aab6c8']  # 武器
    BAG_DQ = [685, 637, '4c87b0']  # 丢弃
    BAG_DQQR = [670, 523, 'ee7046']

    ZB_XQ = [1188, 106, '415066']
    ZB_JD = [1062, 626, 'ed7046']  # 鉴定
    ZB_JDQR = [725, 516, 'ee7046']  # 鉴定确认
    ZB_CD = [1211, 625, 'ee7046']  # 穿戴

    BAG_SX = [374, 624, '4c87b0']  # 出售筛选
    BAG_SX_TY = [855, 636, 'ee7046']  # 套用
    SX_SP = [782, 375, 'adb7c1']
    SX_SP2 = [698, 451, 'adb7c1']
    SX_SP3 = [586, 537, 'adb7c1']
    BAG_FJSX = [374, 533, '4c87b0']  # 分解筛选
    FJ_SX = [627, 307, 'adb7c1']
    FJ_SX2 = [498, 385, 'adb7c1']
    FJ_TY = [690, 545, 'ee7046']  # 套用
    CSFJ_M = [693, 688, 'e9e9e9']  # 出售分解界面
    CS_QR = [1120, 671, 'ee7046']  # 贩售/分解
    CS_NULL = [599, 132, 'ffffff']  # 出售不为空
    FJ_NULL = [88, 152, 'e9e9e9']  # 分解栏空
    FJ_END = [711, 645, 'ee7046']
    SX_BTN = [79, 673, 'ffffff']  # 筛选按钮位置
    QR = [676, 521, 'ee7046']
    FJ = [1009, 667, '4c87b0']  # 分解
    CS = [1138, 675, '4c87b0']  # 出售

    RE_LQJL = [679, 634, 'ee7046']
    RE_LQJL1 = [518, 616, 'ee7046']
    KT_M = [61, 681, '2b3646']
    KT_CJ = [155, 490, 'ee7546']
    KT_MRSL = [169, 309, 'ee7546']
    KT_MZRW = [48, 207, 'ee7546']
    KT_MRRW = [175, 128, 'ee7546']
    KT_F = [1148, 643, 'c3c3c3']  # 课题领取按钮灰置

    MAIL_M = [614, 666, 'f2f2f2']
    MAIL_LQ = [890, 630, 'ee7046']
    MAIL_LQ_F = [890, 630, 'c3c3c3']
    MAIL_GR = [922, 160, 'ee7546']  # 个人栏
    MAIL_GR_F = [922, 160, '2b3646']

    SKIP_BTN = [374, 528, '4C87']
    SKIP_NEW = [551, 534, 'ee7046']
    SKIP_NEW1 = [622, 213, 'FFE']
    FEVER_BUFF = [582, 191, 'f2f2f2']

    PET_END = [576, 314, '404A54']  # 宠物到期 908，97
    PET_M = [162, 32, '4c87b0']
    PET_NULL = [487, 221, '636c79']
    PET_JN = [612, 133, 'f2f2f2']
    PET_JN_LOGIN1 = [821, 205, 'ee7046']
    PET_JN_LOGIN2 = [821, 325, 'ee7046']
    PET_FEVER_JN = [248, 543, 'dcdee1']  # 点开Ferver技能槽

    ROLE_INFO = [1126, 131, 'ee7046']

    SKILL_M = [299, 504, '515f6e']
    SKILL_CJN = [125, 491, 'ee7546']  # 超级能栏

    TJP_QH_M = [992, 121, 'ffffff']
    TJP_QH_BTN = [580, 645, 'ee7046']
    TJP_QH_BTN_F = [580, 645, 'c3c3c3']

    QH_XYJ = [206, 552, 'dcdee1']
    QH_DP = [287, 553, 'dcdee1']
    QH_BH = [369, 553, 'dcdee1']
    QH_JG = [760, 656, 'ee7046']
    QH_BTN = [571, 548, 'ee7046']
    TJP_SJ_M = [260, 639, 'dcdee1']
    TJP_SJ_BTN = [579, 646, 'ee7046']
    TJP_SJ_BTN_F = [579, 646, 'c3c3c3']
    TJP_SJXZ_BTN = [1125, 643, 'ee7046']
    TJP_SJXZ_BTN_F = [1132, 638, 'c3c3c3']
    TJP_SJ_XZ = [697, 639, 'ee7046']  # 自动选择确认
    HD_M = [286, 41, '415066']
    HD_CZZY = [240, 280, 'ff8d4f']  # 成长支援
    HC_CZZY_LQ = [1238, 655, 'adadad']  # 成长支援领取
    TC_1 = [1172, 269, '617B94']

    GX_XZ_BACK = [523, 188, 'FF7C52']  # 更新下载完成
    GX_XZ = [548, 527, 'ef714a']  # 有下载EB7047


class MulColorEnumG:
    INGAME_FLAG = [897, 329, 948, 379, "E9E9EA-030404",
                   "-5|-4|ECEDEE,-5|-18|E3E4E5-090909,-5|-24|3F454D-000001,-11|1|41454E-000100,-18|1|ECEDEE,"
                   "-23|1|41454E-000100,-3|13|ECEDED,-3|18|42464E,11|-2|D9DADC-131312,17|-2|41454E",
                   0.9, 0, '登录标记']
    SET_BTN = [1213, 641, 1254, 681, "FFFFFF", "-11|8|FFFFFF,-11|20|FFFFFF,1|26|FFFFFF,11|20|FFFFFF,11|8|FFFFFF", 0.9,
               0, '菜单设置']

    S_MAP = [1210, 77, 1254, 123, "FFFFFF", "0|15|FFFFFF,0|20|FFFFFF,-10|26|FFFFFF,0|31|FFFFFF,11|25|FFFFFF", 0.9, 0,
             '小地图']

    HD_TIP = [1154, 156, 1193, 200, "617A95",
              "-2|12|FEFEFE-010101,4|6|FFFFFF,-6|6|FEFEFE-010101,-6|15|FFFFFF,3|15|FFFFFF,12|11|617A95,"
              "-18|11|607A95-010000,0|20|617A95",
              0.9, 0, '活动tip']

    LB_TIP = [1107, 34, 1191, 107, "A5A5A5",
              "-17|-4|FFFFFF,-2|-14|FFFFFF,7|-11|A3A3A3-010101,-11|-10|A5A5A5,-6|5|A3A3A3-010101", 0.9, 0, '礼包推荐']

    XT_STAR = [171, 64, 386, 138, "FF2305-000C05",
               "-5|-1|FFFFFF,-11|0|FF2D0E-00180E,-6|4|FF2A04-000E05,-6|-8|FEA380-014467,-3|-6|FE5510-013111,"
               "-8|-6|FF8408-001709",
               0.9, 0, '星力标记']
    COIN_ENUM = [1201, 87, 1259, 150, "FEFEFE-010101",
                 "7|-8|FEFEFE-010101,-11|-13|FFFFFF,-6|8|565A61-292826,18|4|2D333B,-13|1|2D333B,0|-12|2D333B", 0.9, 0,
                 '货币目录']
    TASK_CLOSE = [1181, 10, 1267, 82, "FEFEFE-010101",
                  "-12|-12|F3F4F5-0C0B0A,9|-10|FEFEFE-010101,14|3|344154,-15|11|344154,-4|16|344154,10|10|FEFEFE-010101",
                  0.9, 0, '任务关闭']
    TASK_POINT = [74, 178, 124, 434, "09AC62-000202",
                  "1|-5|09AB61,1|-9|D1EBDE-2E1421,5|-7|BBE5D1-441A2E,8|0|DCF0E7-230F18,2|6|DCF1E7-230E18,-4|5|FFFFFF",
                  0.9, 0, '任务绿点']
    GAME_LOGIN = [7, 650, 72, 712, "EAA000",
                  "-13|4|FFFEFD,-6|0|FFFDF9,-6|-19|EAA000,16|-2|EAA000,14|16|EAA000,-1|12|FFFEFD", 0.9, 0, '登录界面区域按钮']
    GAME_START = [930, 579, 1219, 654, "92B915", "-74|-16|A3C319,-143|-1|93B915,-74|19|8DB414", 0.9, 0, '游戏开始']
    ZB_TS = [738, 161, 1266, 644, "73F349",
             "-7|0|73F349,-4|0|75FF4B,-4|-4|75FF4A,-4|-5|70F547,-3|-3|75FF4A,-5|-3|74FC49", 0.9, 0, '装备提升']

    # 道具清理
    BS_BLUE = [738, 161, 1266, 644, "5EEEFF", "-2|12|ADF6FF,16|2|866DF4,-16|1|05FFD9", 0.8, 0, '蓝宝石']
    BS_GREE = [738, 161, 1266, 644, "CBFFEE", "-15|2|00FF91,17|2|09A6A2,3|15|00DFB1", 0.8, 0, '绿宝石']
    BS_RED = [738, 161, 1266, 644, "BB0121", "-4|18|FF2068,-16|10|FF7FAA,-32|19|FE28B5,-34|-9|FFFFFF", 0.8, 0, '红宝石']
    BS_Z = [738, 161, 1266, 644, "A877FF", "12|-2|7B2FFF,-2|15|7729FF,-19|4|7424FF", 0.8, 0, '紫宝石']
    BS_H = [738, 161, 1266, 644, "FFFFA3", "12|6|FF8808,6|16|FF8B09,-4|14|FFDC24,-18|12|FFF545", 0.8, 0, '黄宝石']
    WQ_DZ = [738, 161, 1266, 644, "881177", "-3|19|A79487,4|19|626262,-1|30|626262", 0.8, 0, '武器材料袋子']
    FJ_DZ = [738, 161, 1266, 644, "88DCEE", "2|18|676767,-1|27|626262,-13|26|626262", 0.8, 0, '防具材料袋子']
    JH_COIN = [738, 161, 1266, 644, "BB8800",
               "13|-4|BB8800,9|9|BB9900,-6|10|BB8800,-12|-7|FFFFAA,1|-22|FFFFFF,24|0|FFFFFF,2|23|DDDDDD", 0.8, 0,
               '进化系统硬币']

    JZT_BMFLJZ = [738, 161, 1266, 644, "FFDDEE", "-2|-6|FF0033,-1|-8|FF0033,-20|11|F64B38,-16|17|F64B38,6|11|FFFFFF",
                  0.8, 0, '不灭法老戒指']

    # find color
    IGAME = [12, 0, 112, 47, 'FFD800-000000']
    BOSS_DROP = [495, 237, 794, 344, 'EB8D6B-0B2229']  # boss掉落
    BOSS_FUHUO = [399, 459, 941, 617, 'C6481E-000000']  # boss战死亡
    XT_FLAG = [196, 69, 390, 141, 'FF3303-001203']


class WorldEnumG:
    NEXON = [0, 11, 3, 341, 125, 'NEXON', 'DADAD8-252527', 0.9]
    ZB_SJ = [0, 48, 314, 254, 355, '升级', 'C5C6C7-3A3938', 0.9]
    ZB_QH = [0, 48, 314, 254, 355, '星力强化', 'C5C6C7-3A3938', 0.9]
    SET_BTN = [0, 1207, 634, 1262, 689, '设置按钮', 'D7D7D7-282828', 0.9]
    YM_READY = [0, 108, 144, 232, 182, 'READY', 'EAEBEA-151415', 0.9]
    PKJ_READY = [0, 745, 146, 864, 182, 'READY', 'EAEBEA-151415', 0.9]
    NH_READY = [0, 1072, 151, 1176, 179, 'READY', 'EAEBEA-151415', 0.9]
    BAT_ENDY = [0, 431, 318, 630, 363, '游戏单元结束', 'D4D3D3-2B2C2C', 0.9]
    NET_ERR = [0, 495, 309, 781, 355, '自动连线中', 'C2A904-3D3504', 0.8]
    BACN_KSDY = [0, 223, 36, 1135, 705, '移动至选单', 'D5E3EC-2A1C13', 0.9]
    QR_BTN = [0, 228, 73, 1014, 665, '确认', 'F8C5B4-073A4B', 0.9]
    EXIT_TEAM = [0, 288, 174, 328, 499, '退出队伍', 'DADBDC-252423', 0.9]
    AUTO_JION = [0, 88, 198, 210, 382, '自动加入中', 'CCCACC-333233', 0.9]
    LOGIN_REWARD = [0, 16, 87, 201, 713, '登入奖励', 'BBBEC3-44413C', 0.9]
    SLEEP_REWARD = [0, 16, 87, 201, 713, '休息奖励', 'BBBEC3-44413C', 0.9]
    HD_CZZY = [0, 16, 87, 201, 713, '成长支援', 'BBBEC3-44413C', 0.9]
    TASK_ARROW = [0, 1152, 472, 1266, 533, '任务箭头', 'DADADA-252525', 0.9]
    TASK_AUTO = [0, 381, 625, 468, 676, '自动任务', 'D6D6D5-29292A', 0.8]
    BAT_AUTO = [0, 388, 638, 458, 669, '自动战斗', 'C4C3C2-3B3C3D', 0.8]
    BAT_XC = [0, 1037, 593, 1115, 641, '卸除', 'D7D7D7-282828', 0.9]
    SKIP = [0, 1165, 11, 1250, 46, '略过', 'B5B5B5-4A4A4A', 0.9]
    SJ_SET = [0, 837, 411, 1009, 488, '升级设定', '6D757E-2C2926', 0.9]
    YS_DL = [0, 789, 159, 918, 688, '登录', 'D7DED7-282128', 0.9]
    YS_LJQW = [0, 789, 159, 918, 688, '立即前往', 'D7DED7-282128', 0.9]
    TEAM_NULL = [0, 972, 433, 1196, 501, '无队伍', '717982-2F2C29', 0.9]
    EXIT_TEAM_TIP = [0, 377, 174, 874, 421, '离队提示', 'D7C548-282716', 0.9]
    DATA_UP=[0,536,150,749,197,'数据更新','D7D9DE-282621',0.9]
    # mr
