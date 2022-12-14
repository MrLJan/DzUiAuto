# -*- coding: utf-8 -*-
import os

from airtest.core.cv import Template

from Utils.LoadConfig import LoadConfig
from Utils.OtherTools import OT


class GlobalEnumG:
    if not os.path.exists(OT.abspath(f"/Res/配置文件.ini")):
        LoadConfig.init_config()
    Ver = '2.21'
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
    TasKId = {

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
        'NetErr': {'name': "复活", 'id': 3},
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
    TIP = [(271, 47, 1018, 182), Template(OT.imgpath('引导提示'))]
    UI_CLOSE = [(1060, 24, 1149, 97), Template(OT.imgpath('弹窗'))]
    UI_QR = [(0, 0, 1280, 720), Template(OT.imgpath('确认'))]
    UI_QBLQ = [(0, 0, 1280, 720), Template(OT.imgpath('全部领取'))]
    # 活动
    QD_1 = [(1218, 12, 1265, 55), Template(OT.imgpath('活动签到1'))]
    # 登录相关
    GAME_ICON = [(0, 0, 1280, 720), Template(OT.imgpath('游戏icon'))]
    LOGIN_FLAG = [(973, 485, 1278, 715), Template(OT.imgpath('游戏登陆标志'))]
    INGAME_FLAG = [(877, 307, 969, 396), Template(OT.imgpath('验证登录标记2'))]  # 734,9,1253,64
    LOGIN_TIPS = [(1240, 14, 1264, 61), Template(OT.imgpath('登录弹窗'))]
    # 任务相关
    TASK_POINT = [(70, 179, 121, 414), Template(OT.imgpath('任务点'))]
    ZB_TS = [(722, 144, 1272, 656), Template(OT.imgpath('装备提升'))]  # 装备上绿色小箭头
    TASK_TAB = [(0, 0, 1280, 720), Template(OT.imgpath('任务页签'), rgb=True)]
    TASK_START = [(341, 529, 482, 715), Template(OT.imgpath('任务可开始'))]
    TASK_TAKE = [(1067, 403, 1150, 438), Template(OT.imgpath('任务接受'))]
    TASK_OVER = [(0, 0, 1280, 720), Template(OT.imgpath('任务完成'))]
    TASK_REWARD = [(595, 630, 685, 659), Template(OT.imgpath('任务奖励'))]
    CZJL_ICON = [(3, 122, 498, 185), Template(OT.imgpath('成长奖励'))]
    # 活动
    KT_QBLQ = [(1138, 650, 1223, 680), Template(OT.imgpath('课题全部领取'))]
    # 背包清理
    BAG_MAX_IMG = [(1140, 36, 1195, 64), Template(OT.imgpath('背包满'))]
    BAG_GOLD = [(858, 19, 1115, 63), Template(OT.imgpath('金币详情'))]
    # 邮件
    MAIL_RQ = [(972, 27, 1006, 49), Template(OT.imgpath('邮件'))]
    # 战斗相关
    AUTO_BAT = [(379, 622, 469, 688), Template(OT.imgpath('自动战斗'))]
    RES_EXIT_TEAM = [(0, 0, 1280, 720), Template(OT.imgpath('休息离队提示'))]
    S_MAP = [(1190, 70, 1272, 140), Template(OT.imgpath('小地图'))]
    PERSON_POS = [(864, 75, 1257, 193), Template(OT.imgpath('人物坐标'))]
    # 组队相关
    TEMA_ING = [(332, 245, 410, 332), Template(OT.imgpath('组队中'))]

    # 装备
    EQ_WZB = [(225, 97, 370, 211), Template(OT.imgpath('无装备'))]
    EQ_UP = [(559, 621, 717, 701), Template(OT.imgpath('升级'), rgb=True)]  # 升级确认按钮
    EQ_UP_QR = [(492, 604, 789, 682), Template(OT.imgpath('升级确认'))]
    # 买药
    CZ_FUHUO = [(267, 472, 525, 585), Template(OT.imgpath('复活'))]
    BUY_YS_LOGIN = [(792, 162, 914, 685), Template(OT.imgpath('药水登录'))]
    JN_LOGIN_2 = [(790, 305, 912, 382), Template(OT.imgpath('药水登录'))]
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
    RED_BS = [(738, 161, 1266, 644), Template(OT.imgpath('红宝石'))]
    G_BS = [(738, 161, 1266, 644), Template(OT.imgpath('绿宝石A'))]
    Z_BS = [(738, 161, 1266, 644), Template(OT.imgpath('紫宝石A'))]
    L_BS = [(738, 161, 1266, 644), Template(OT.imgpath('蓝宝石A'))]
    JZT_DJ = [(738, 161, 1266, 644), Template(OT.imgpath('金字塔产物'))]
    FJ_HE1 = [(738, 161, 1266, 644), Template(OT.imgpath('防具合成石1'))]
    FJ_HE2 = [(738, 161, 1266, 644), Template(OT.imgpath('防具合成石2'))]
    WQ_HE1 = [(738, 161, 1266, 644), Template(OT.imgpath('武器合成石1'))]
    WQ_HE2 = [(738, 161, 1266, 644), Template(OT.imgpath('武器合成石2'))]
    BAG_NULL = [(738, 161, 1266, 644), Template(OT.imgpath('空格子'))]
    # 宠物
    PET_1 = [(349, 143, 433, 217), Template(OT.imgpath('默认宠物1'), threshold=0.9)]
    PET_2 = [(349, 143, 433, 217), Template(OT.imgpath('默认宠物2'), threshold=0.9)]
    CW_TYPE = {
        'A': [[(735, 163, 1268, 651), Template(OT.imgpath('宠物A1'))],
              [(735, 163, 1268, 651), Template(OT.imgpath('宠物A2'))],
              [(735, 163, 1268, 651), Template(OT.imgpath('宠物A3'))]],
        'B': [[(735, 163, 1268, 651), Template(OT.imgpath('宠物B1'))],
              [(735, 163, 1268, 651), Template(OT.imgpath('宠物B2'))],
              [(735, 163, 1268, 651), Template(OT.imgpath('宠物B3'))]],
        'C': [[(735, 163, 1268, 651), Template(OT.imgpath('宠物C1'))],
              [(735, 163, 1268, 651), Template(OT.imgpath('宠物C2'))],
              [(735, 163, 1268, 651), Template(OT.imgpath('宠物C3'))]]
    }
    PET_POS = {
        1: [131, 130, '2B3747', 'EE7546'],
        2: [127, 219, '2B3747', 'EE7546'],
        3: [127, 306, '2B3747', 'EE7546']
    }
    # BOSS
    YM = [(65, 103, 262, 194), Template(OT.imgpath('炎魔'))]
    PKJ = [(704, 104, 891, 193), Template(OT.imgpath('皮卡啾'))]
    NH = [(1048, 103, 1191, 194), Template(OT.imgpath('女皇'))]
    # 每日
    MR_BACK = [(23, 22, 66, 61), Template(OT.imgpath('返回'))]
    MR_BAT_EXIT = [(1202, 251, 1269, 317), Template(OT.imgpath('战斗退出'), threshold=0.9)]
    JRGH_IMG = [(0, 0, 1280, 720), Template(OT.imgpath('加入公会'))]

    # ------

    # 组队
    TEAM_TAB = [(8, 291, 62, 343), Template(OT.imgpath('组队页签'))]
    TEAM_XZDW = [(86, 333, 215, 381), Template(OT.imgpath('寻找队伍'))]
    TEAM_CLDW = [(86, 197, 214, 248), Template(OT.imgpath('创立队伍'))]
    PWD_TEAM = [(897, 189, 964, 533), Template(OT.imgpath('密码队伍'))]
    EXIT_TEAM = [(290, 187, 328, 446), Template(OT.imgpath('离开队伍'))]
    SKIP_NEW = [(2, 72, 491, 212), Template(OT.imgpath('新内容'))]
    JN_TEACH = [(790, 569, 981, 717), Template(OT.imgpath('教学'))]
    GX_XZ_ING = [(0, 0, 1280, 720), Template(OT.imgpath('数据更新'))]


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
    }
    MAP_DATA = {
        '1': {'NULL': []},
        '2': {'NULL': []},
        '3': {'研究所102': [[898, 1211, 159], [135], [135], [50, 0, 0], [1250, 1153, 966, 870]],
              '西边森林': [[928, 1213, 142], [1060, 135], [135], [80, 100, 50], [1250, 1153, 966, 870]],
              '冰冷死亡战场': [[928, 1213, 142], [1060, 135], [135], [50, 30, 100], [1250, 1153, 966, 870]],
              '龙蛋': [[1005, 1106, 148], [1020, 1073, 135], [1060, 135], [50, 100, 10], [1154, 1100, 1050, 970]],
              '爱奥斯塔入口': [[1000, 1088, 148], [956, 1139, 135], [1060, 1162, 135], [30, 70, 100], [1250, 1153, 966, 870]],
              '奥斯塔入口': [[1046, 148], [988, 135], [950, 135], [70, 100, 100], [1250, 1153, 966, 870]],
              '天空露台2': [[910, 989, 1096, 1229, 142], [135], [135], [30, 0, 0], [1250, 1153, 966, 870]],
              '机械室': [[902, 1084, 153], [1098, 135], [1114, 135], [50, 100, 100], [1250, 1153, 966, 870]],
              '时间漩涡': [[1015, 1084, 148], [1037, 1111, 135], [1060, 1078, 135], [50, 50, 100], [1250, 1153, 1000, 970]],
              '忘却之路4': [[1027, 1100, 153], [1151, 135], [1212, 135], [30, 70, 100], [1250, 1153, 966, 873]],
              '偏僻泥沼': [[949, 1050, 1212, 148], [921, 1156, 135], [1198, 135], [30, 70, 100], [1350, 1153, 966, 870]],
              '变形的森林': [[982, 1143, 153], [961, 1175, 135], [135], [50, 100, 0], [1350, 1153, 966, 870]],
              '武器库星图': [[933, 1094, 1216, 153], [998, 1060, 135], [135], [50, 50, 0], [1350, 1153, 966, 870]],
              '灰烬之风高原': [[1036, 1060, 153], [1024, 1060, 1119, 135], [135], [50, 50, 0], [1350, 1153, 966, 870]],
              '崎岖的峡谷': [[1022, 1067, 153], [949, 135], [1060, 1171, 135], [50, 100, 30], [1260, 1153, 966, 880]]

              },
        # ----野图
        '4': {
            '露台2': [[961, 1172, 142], [135], [135], [60, 0, 0], [1244, 1153, 966, 874]],
            '忘却之路3': [[975, 1171, 153], [135], [135], [70, 0, 0], [1245, 1153, 966, 870]],
            '神秘森林': [[911, 1193, 135], [904, 1178, 135], [135], [70, 100, 0], [1244, 1153, 966, 874]],
            '武器库': [[933, 1060, 1172, 153], [1001, 1123, 135], [135], [50, 50, 0], [1245, 1153, 966, 870]],
            '崎岖峡谷': [[1022, 1067, 153], [950, 1060, 135], [135], [60, 100, 0], [1245, 1153, 966, 870]],
            '木菇菇林': [[1027, 1112, 153], [135], [135], [30, 0, 0], [1165, 1085, 1050, 960]]
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
        '神秘森林': ['80''mnesl', 'sm'],
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
    EXIT_FOU = [391, 532, '4C87AF']  # 退出游戏-否
    CLOSE_GAME = [433, 543, '4D87AF']  # 关闭游戏-否
    FUHUO_BTN = [293, 522, '4C87AF']  # 复活按钮
    BG_PINDAO = [1083, 55, 'EE7']  # 地图主界面-变更频道
    MAP_QWPD = [529, 635, 'EE7047']  # 地图-前往频道
    MAP_SJYD = [927, 657, '4C87AF']  # 瞬间移动
    HD_BJBS = [1058, 655, 'EDCE01']  # 活动签到
    HD_BJBS_LQ = [1058, 655, 'EC9C00']

    KSDY = [16, 14, '415067']  # 快速单元
    XLZC = [53, 429, '617B96']  # 星力战场
    XLZC_YD = [1117, 658, 'EE7047']  # 星力战场-移动
    XLZC_YDQR = [699, 523, 'EE7047']  # 星力战场-移动确认
    XLZC_YDOK = [568, 519, 'EE7047']  # 星力战场-移动完成
    YS_LOGIN = [612, 124, 'F2F2F2']  # [565, 128, 'F2F2F2']  # 药水登录界面
    YS_SHOP = [925, 544, 'F2F2F2']  # 药水商店
    YS_XQ = [1040, 648, 'EE7047']  # 药水详情
    YS_GMQR = [686, 523, 'EE7047']  # 药水购买确认
    BACK = [16, 10, '344154']  # 左上角返回
    JR = [1012, 645, 'EE7047']  # 进入按钮
    MR_EXIT_TEAM = [678, 517, 'EE7047']  # 进入副本提示有队伍
    TEAM_KS = [398, 389, '5E5536']  # 组队进入
    EXIT_TEAM_QR = [714, 525, 'EE7047']
    WL_PM = [592, 633, 'EE7047']  # 武林排名界面
    WL_M = [16, 10, '344154']  # 武林界面
    WL_JR = [1068, 650, 'EE7047']  # 武林进入
    WL_JRQR = [669, 630, 'EE7047']  # 武林进入确认
    WL_QX = [406, 635, '4C87AF']  # 武林入场取消
    JZT_JR = [999, 646, 'EE7047']  # 金字塔进入
    JZT_JRQR = [714, 525, 'EE7047']  # 金字塔进入确认
    JZT_END = [566, 574, '4C87AF']
    JYDC_END = [273, 638, '4C87AF']  # 菁英地城结束
    JYDC_MAX = [825, 439, '607B96']  # 菁英地城max

    MRDC_JR = [1012, 645, 'EE7047']  # 每日地城进入
    MRDC_JRQR = [661, 625, 'EE7047']  # 每日地城进入确认
    MRDC_HD = [143, 620, 'EE7546']  # 混沌模式

    GWSL_END = [283, 206, 'F2F2F2']

    TBB_JR = [768, 618, 'EE7047']
    TBB_QR = [567, 523, 'EE7047']

    JHXT_JRQR = [734, 640, 'EE7047']
    JHXT_END = [556, 616, '4C87AF']

    CYRQ_END = [376, 517, '4C87AF']
    CYRQ_JR = [1055, 656, 'EE7047']
    CYQR_JR_QR = [908, 446, 'E9E9E9']
    CYQR_JR_QR1 = [682, 549, 'EE7047']
    CYRQ_JR_F = [1055, 656, 'C3C3C3']

    MNDC_XZ = [57, 138, '2B3747']
    MNDC_XZ2 = [78, 214, '2B3747']
    MNDC_XZ3 = [633, 331, 'FFFFFF']
    MNDC_JRQR = [670, 652, 'EE7047']
    MNDC_JR = [1053, 650, 'EE7047']
    MNDC_END = [564, 593, 'EE7047']
    MNDC_JG_QR = [564, 593, 'EE7047']  # 最终结果-离开
    MNDC_JG = [384, 598, '4C87AF']  # 迷你地城结果-移动
    MNDC_JG_LK = [523, 604, 'EE7047']
    BAT_JG = [540, 524, 'EE7047']  # 自动战斗结果
    BAT_AUTO_QR = [733, 563, 'EE7047']  # 自动战斗确认
    BAT_AUTO_M = [505, 543, 'DDDDDD']  # 自动战斗界面

    AUTO_TIME = [447, 268, '519DF1']
    AUTO_FREE = [897, 391, '617B96']
    AUTO_10 = [709, 344, 'FFD741']
    AUTO_30 = [840, 336, 'FFD741']
    AUTO_60 = [908, 338, 'FFD741']

    XGT_JR = [1167, 642, 'EE7047']
    XGT_ZCJR = [983, 621, 'EE7047']
    XGT_JR_F = [1167, 642, 'C3C3C3']

    GWGY_JR = [1084, 656, 'EE7047']
    GWGY_JR_F = [1084, 656, 'C3C3C3']
    GWGY_JRQR = [749, 633, 'EE7047']

    YZD_KN = [156, 339, '2B3747']
    YZD_PT = [159, 259, '2B3747']
    YZD_JR = [1055, 651, 'EE7047']
    YZD_JR_F = [1052, 648, 'C3C3C3']

    GH_M = [549, 104, 'EAEAEA']
    GH_JR = [692, 515, 'EE7047']
    GH_XJR = [925, 662, 'EE7047']  # 加入新公会
    GH_JRQR = [840, 528, 'EE7047']
    GH_RYZ = [709, 668, 'F1F1F1']
    GH_RYZ_JR = [433, 666, 'EE7047']
    GH_RYZ_JR_F = [433, 666, 'C3C3C3']
    GH_WXDC = [709, 668, 'F2F2F2']
    GH_WXDC_JR = [449, 653, 'EE7047']
    GH_WXDC_JR_F = [449, 653, 'C3C3C3']

    EXIT_TEAM = [669, 534, 'EE7047']  # 离队确认
    TEAM_ZDJR = [99, 277, 'EE7047']  # 自动加入
    TEAM_ZDJR_QR = [1126, 162, '617B96']  # 自动加入-确认

    TEAM_CLDW_M = [53, 671, 'F2F2F2']  # 创立队伍界面
    TEAM_CLQR = [536, 642, 'EE7047']
    TEAM_MMDW = [102, 521, '41799E']  # 密码队伍选项
    TEAM_QRMM = [524, 609, 'EE7047']  # 确认密码

    TEAM_SQJR = [1125, 647, 'EE7047']  # 申请加入
    TEAM_SQJR_F = [1125, 647, 'C3C3C3']  # 无法申请加入

    MAP_XL = [1108, 655, 'EE7047']  # 寻路按钮
    MAP_XLQR = [660, 521, 'EE7047']  # 寻路按钮确认
    MAP_ERR = [520, 520, 'EE7047']  # 无法瞬间移动

    BAG_M = [407, 32, 'EE7']  # 背包界面-奖励优惠保管箱
    BAG_GOLD_QR = [579, 510, 'EE7047']
    BAG_BS = [1043, 132, 'AAB']  # 宝石栏
    BAG_SP = [954, 129, 'A6B7']  # 饰品
    BAG_FJ = [860, 122, 'ACB4C']  # 防具
    BAG_WQ = [770, 133, 'A9B5']  # 武器
    BAG_DQ = [685, 637, '4C87AF']  # 丢弃
    BAG_DQQR = [670, 523, 'EE7047']

    ZB_XQ = [1188, 106, '415067']
    ZB_JD = [1062, 626, 'EE7047']  # 鉴定
    ZB_JDQR = [725, 516, 'EE7047']  # 鉴定确认
    ZB_CD = [1211, 625, 'EE7047']  # 穿戴

    BAG_SX = [374, 624, '4C87AF']  # 出售筛选
    BAG_SX_TY = [855, 636, 'EE7047']  # 套用
    SX_SP = [782, 375, 'ADB7C1']
    SX_SP2 = [698, 451, 'ADB7C1']
    SX_SP3 = [586, 537, 'ADB7C1']
    BAG_FJSX = [374, 533, '4C87AF']  # 分解筛选
    FJ_SX = [627, 307, 'ADB7C1']
    FJ_SX2 = [498, 385, 'ADB7C1']
    FJ_TY = [690, 545, 'EE7047']  # 套用
    CSFJ_M = [1120, 671, 'EE7047']  # 出售分解界面
    CS_QR = [1120, 671, 'EE7047']  # 贩售/分解
    CS_NULL = [599, 132, 'FFFFFF']  # 出售不为空
    FJ_NULL = [88, 152, 'E9E9E9']  # 分解栏空
    FJ_END = [711, 645, 'EE7047']
    QR = [676, 521, 'EE7047']
    FJ = [1009, 667, '4C87AF']  # 分解
    CS = [1138, 675, '4C87AF']  # 出售

    RE_LQJL = [679, 634, 'EE7047']
    RE_LQJL1 = [518, 616, 'EE7047']
    KT_M = [61, 681, '2B3747']
    KT_CJ = [155, 490, 'EE7546']
    KT_MRSL = [169, 309, 'EE7546']
    KT_MZRW = [48, 207, 'EE7546']
    KT_MRRW = [175, 128, 'EE7546']
    KT_F = [1148, 643, 'C3C3C3']  # 课题领取按钮灰置

    MAIL_M = [614, 666, 'F2F2F2']
    MAIL_LQ = [890, 630, 'EE7047']
    MAIL_LQ_F = [890, 630, 'C3C3C3']
    MAIL_GR = [922, 160, 'EE7546']  # 个人栏
    MAIL_GR_F = [922, 160, '2B3747']

    SKIP_BTN = [374, 528, '4C87']
    SKIP_NEW = [551, 534, 'EE7047']
    SKIP_NEW1 = [622, 213, 'FFE']
    FEVER_BUFF = [582, 191, 'F2F2F2']

    PET_END = [576, 314, '404A54']  # 宠物到期 908，97
    PET_M = [162, 32, '4C87AF']
    PET_NULL = [487, 188, '636D79']
    PET_JN = [612, 133, 'F2F2F2']
    PET_JN_LOGIN1 = [821, 205, 'EE7047']
    PET_JN_LOGIN2 = [821, 325, 'EE7047']
    PET_FEVER_JN = [248, 543, 'DDDEE2']  # 点开Ferver技能槽

    ROLE_INFO = [1126, 131, 'EE7047']

    SKILL_M = [299, 504, '525F6F']
    SKILL_CJN = [125, 491, 'EE7546']  # 超级能栏

    TJP_QH_M = [992, 121, 'FFFFFF']
    TJP_QH_BTN = [580, 645, 'EE7047']
    TJP_QH_BTN_F = [580, 645, 'C3C3C3']

    QH_XYJ = [206, 552, 'DEDFE3']
    QH_DP = [287, 553, 'DEDFE3']
    QH_BH = [369, 553, 'DEDFE3']
    QH_JG = [760, 656, 'EE7047']
    QH_BTN = [571, 548, 'EE7047']
    TJP_SJ_M = [260, 639, 'DDDEE2']
    TJP_SJ_BTN = [579, 646, 'EE7047']
    TJP_SJ_BTN_F = [579, 646, 'C3C3C3']
    TJP_SJXZ_BTN = [1125, 643, 'EE7047']
    TJP_SJXZ_BTN_F = [1132, 638, 'C3C3C3']
    TJP_SJ_XZ = [697, 639, 'EE7047']  # 自动选择确认
    HD_M = [286, 41, '415067']
    HD_CZZY = [240, 280, 'FF8D']  # 成长支援
    TC_1 = [1172, 269, '617B94']

    GX_XZ_BACK = [523, 188, 'FF7C52']  # 更新下载完成
    GX_XZ = [536, 528, 'EF714B']  # 有下载EB7047


class OpenCvEnumG:
    STAR_NUM = {
        OT.npypath('p0'): '0',
        OT.npypath('p1'): '1',
        OT.npypath('p2'): '2',
        OT.npypath('p3'): '3',
        OT.npypath('p4'): '4',
        OT.npypath('p5'): '5',
        OT.npypath('p6'): '6',
        OT.npypath('p7'): '7',
        OT.npypath('p8'): '8',
        OT.npypath('p9'): '9',
    }
    YS_NUM = {
        '0': OT.npypath('y0'),
        '1': OT.npypath('y1'),
        '2': OT.npypath('y2'),
        '3': OT.npypath('y3'),
        '4': OT.npypath('y4'),
        '5': OT.npypath('y5'),
        '6': OT.npypath('y6'),
        '7': OT.npypath('y7'),
        '8': OT.npypath('y8'),
        '9': OT.npypath('y9'),
    }

    GOLD_NUM = {
        '0': OT.npypath('g0'),
        '1': OT.npypath('g1'),
        '2': OT.npypath('g2'),
        '3': OT.npypath('g3'),
        '4': OT.npypath('g4'),
        '5': OT.npypath('g5'),
        '6': OT.npypath('g6'),
        '7': OT.npypath('g7'),
        '8': OT.npypath('g8'),
        '9': OT.npypath('g9'),
    }
    HP_MP = {
        'HP': OT.npypath('hp'),
        'MP': OT.npypath('mp'),
    }
    XT_MAP = {
        '40': 'xt_40',
        '45': 'xt_45',
        '65': 'xt_65',
        '80': 'xt_80',
        '90': 'xt_90',
        '105': 'xt_105',
        '113': 'xt_113',
        '115': 'xt_115',
        '120': 'xt_120',
        '130': 'xt_130',
        '136': 'xt_136',
        '142': 'xt_142',
        '144': 'xt_144',
        '147': 'xt_147',
    }
    XT_MAP_EX = {
        '40': 'xt_40_e',
        '45': 'xt_45_e',
        '65': 'xt_65_e',
        '80': 'xt_80_e',
        '90': 'xt_90_e',
        '105': 'xt_105_e',
        '113': 'xt_113_e',
        '115': 'xt_115_e',
        '120': 'xt_120_e',
        '130': 'xt_130_e',
        '136': 'xt_136_e',
        '142': 'xt_142_e',
        '144': 'xt_144_e',
        '147': 'xt_147_e',
    }
    TEAM_FLAG = {
        'ZZZ': [(6, 344, 59, 384), (5, 1, 20, 10)],  # 休息踢出
        'EXP': [(6, 344, 59, 384), (5, 1, 20, 10)],  # 经验队伍
    }
    FIND_INFO = {
        'team_zdjr': [(88, 198, 210, 382), (100, 1, 50, 0), (20, 240, 6, 1, 0, 0.7)],
        # 自动加入中
        'zb_qh': [(48, 314, 254, 355), (100, 1, 20, 15), (20, 240, 0, 1, 0, 0.8)],  # 装备强化
        'zb_sj': [(48, 314, 254, 355), (100, 1, 20, 15), (20, 240, 0, 1, 0, 0.8)],  # 装备升级
        'bat_xc': [(1026, 590, 1122, 645), (5, 1, 20, 10), (20, 240, 0, 1, 0, 0.8)],  # 卸除按钮
        'bat_auto': [(392, 642, 453, 665), (100, 1, 5, 0), (5, 250, 0, 0, 1, 0.39)],  # 自动战斗
        'team_null': [(994, 443, 1156, 478), (5, 1, 20, 10), (20, 240, 0, 1, 0, 0.8)],  # 组队目录无队伍
        'zb_sjset': [(342, 492, 615, 593), (10, 1, 100, 10), (5, 240, 5, 0, 0, 0.8)],  # 存储升级设定 347,497,547,534
        'gh_wxdc': [(1114, 360, 1247, 493), (10, 1, 50, 0), (5, 240, 5, 0, 0, 0.8)],  # 无限地城
        'gh_ryz': [(1114, 360, 1247, 493), (10, 1, 50, 0), (5, 240, 5, 0, 0, 0.8)],  # 荣誉战
        'hd_dljl': [(1, 86, 209, 716), (10, 1, 50, 0), (5, 240, 5, 0, 0, 0.8)],  # 登录奖励
        'hd_xxjl': [(1, 86, 209, 716), (10, 1, 50, 0), (5, 240, 5, 0, 0, 0.8)],  # 休息奖励
        'hd_czzy': [(1, 86, 209, 716), (10, 1, 50, 0), (5, 240, 5, 0, 0, 0.8)],  # 成长支援
        'task_arrow': [(1103, 455, 1276, 545), (2, 1, 10, 0), (5, 250, 0, 0, 1, 0.4)],  # 任务箭头
        'task_close': [(1179, 13, 1265, 82), (2, 0.5, 10, 0), (5, 240, 5, 0, 0, 0.8)],  # 任务对话关闭
        'coin_enum': [(1204, 89, 1260, 145), (3, 0.5, 5, 0), (5, 240, 5, 1, 0, 0.69)],  # 金币目录
        'LB_close': [(1117, 47, 1172, 98), (2, 0.5, 10, 0), (5, 240, 5, 0, 0, 0.8)],  # 礼包弹窗
        'task_point': [(69, 178, 121, 417), (1.1, 0.8, 20, 0), (5, 240, 0, 0, 0, 0.8)],  # 任务绿点
        'ingame_flag2': [(891, 327, 949, 379), (1.05, 0.5, 20, 0), (5, 240, 5, 0, 1, 0.8)],  # 在主界面标志
        'ingame_flag1': [(1153, 556, 1263, 679), (1.5, 0.5, 40, 0), (5, 240, 5, 0, 1, 0.8)],  # 在主界面跳跃
        'game_login': [(926, 569, 1222, 654), (4, 1, 50, 0), (5, 240, 5, 0, 0, 0.8)],  # 游戏登录
        'ui_set': [(1204, 634, 1267, 696), (1, 0.5, 20, 0), (20, 240, 0, 1, 0, 0.8)],  # 菜单设置按钮
        'ui_enum': [(1206, 8, 1271, 64), (10, 3, 30, 0), (5, 250, 0, 0, 1, 0.4)],  # 菜单设置按钮
        'xt_flag': [(187, 83, 360, 130), (2, 0.5, 15, 0), (8, 240, 0, 0, 0, 0.67)],  # 星图标记
        'xl_lkyd': [(638, 176, 870, 230), (5, 3, 50, 0), (5, 240, 5, 0, 1, 0.8)],  # 寻路-立刻移动
        'czjl': [(3, 122, 498, 185), (2, 1, 20, 0), (3, 250, 5, 1, 0, 0.5)],  # 成长奖励入口按钮
        'mr_boss_end': [(457, 323, 838, 367), (15, 9, 200, 0), (8, 240, 6, 0, 1, 0.7)],  # BOSS战斗结束
        'skip': [(1159, 13, 1269, 46), (10, 1, 5, 0), (15, 240, 0, 0, 0, 0.69)],  # 跳过
        'sell': [(10, 15, 92, 67), (10, 1, 10, 0), (20, 240, 0, 1, 0, 0.8)],  # 道具出售界面
        'dec': [(10, 15, 92, 67), (10, 1, 10, 0), (20, 240, 0, 1, 0, 0.8)],  # 道具分解界面
        'team_tip_exit': [(454, 261, 833, 326), (5, 3, 50, 0), (8, 240, 0, 0, 0, 0.69)],  # 离队提示
        'team_xzdw': [(86,192,215,393), (5, 3, 50, 0), (8, 240, 0, 0, 0, 0.79)],  # 寻找队伍
        'team_cldw': [(86,192,215,393), (5, 3, 50, 0), (8, 240, 0, 0, 0, 0.79)],  # 创立队伍
    }
