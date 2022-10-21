# -*- coding: utf-8 -*-
import os

from airtest.core.cv import Template

from Utils.LoadConfig import LoadConfig
from Utils.OtherTools import OT


class GlobalEnumG:
    if not os.path.exists(OT.abspath(f"/Res/配置文件.ini")):
        LoadConfig.init_config()
    Ver = '2.10'
    TestLog = True if LoadConfig.getconf('全局配置', '日志') == '1' else False
    GamePackgeName = r'com.nexon.maplem.global'
    WaitTime = 1
    ExitBtnTime = 2  # 点击退出游戏否按钮等待时长
    FindImgTimeOut = 20  # 查找图片等待超时时间
    TouchDurationTime = 1  # 延时点击
    LoginGameTimeOut = 600  # 登录超时时长
    UiCheckTimeOut = 900  # 界面操作超时时长
    SelectCtrTimeOut = 300  # 操作超时时长
    TouchWaitTime = 2  # 点击后等待时长
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
    TEST = Template(OT.imgpath('21'))
    # UI_CLOSE = [(571, 39, 711, 76), Template(OT.imgpath('关闭界面'))]
    TIP = [(271, 47, 1018, 182), Template(OT.imgpath('引导提示'))]
    UI_CLOSE = [(1060, 24, 1149, 97), Template(OT.imgpath('弹窗'))]
    UI_QR = [(0, 0, 1280, 720), Template(OT.imgpath('确认'))]
    UI_QBLQ = [(0, 0, 1280, 720), Template(OT.imgpath('全部领取'))]
    UI_GM = [(0, 0, 1280, 720), Template(OT.imgpath('购买'))]
    UI_YES = [(277, 92, 989, 637), Template(OT.imgpath('是'))]
    UI_NO = [(277, 92, 989, 637), Template(OT.imgpath('否'))]
    UI_LB = [(1132, 58, 1157, 86), Template(OT.imgpath('推荐礼包'))]
    UI_SET = [(1196, 626, 1278, 708), Template(OT.imgpath('设置'))]
    TIP_ClOSE = [(831, 373, 870, 415), Template(OT.imgpath('提示'))]
    GAME_END = [(567, 151, 709, 198), '结束']  # 游戏结束
    NET_ERR = [(493, 365, 778, 387), '不佳']  # 网络异常
    # 下载更新
    GAME_XZ = [(562, 148, 721, 202), '下']  # 下载警告
    # 活动
    QD = [(956, 631, 1249, 697), Template(OT.imgpath('活动签到'))]
    QD_LQ = [(951, 624, 1264, 703), Template(OT.imgpath('签到奖励'))]
    QD_1 = [(1218, 12, 1265, 55), Template(OT.imgpath('活动签到1'))]
    # 登录相关
    GAME_ICON = [(0, 0, 1280, 720), Template(OT.imgpath('游戏icon'))]
    LOGIN_FLAG = [(973, 485, 1278, 715), Template(OT.imgpath('游戏登陆标志'))]
    LOGIN_FLAG1 = [(0, 0, 1280, 720), Template(OT.imgpath('登录区域'))]  # 20,665,56,701
    START_GAME = [(916, 572, 1234, 660), Template(OT.imgpath('游戏开始'))]  # 963,481,1278,688
    INGAME_FLAG = [(1143, 546, 1276, 692), Template(OT.imgpath('验证登录标记'))]  # 734,9,1253,64
    INGAME_FLAG2 = [(877, 307, 969, 396), Template(OT.imgpath('验证登录标记2'))]
    LOGIN_TIPS = [(1240, 14, 1264, 61), Template(OT.imgpath('登录弹窗'))]
    # 任务相关
    SKIP_OCR = [(1121, 6, 1273, 55), '略']  # 略过
    TASK_ZDFP = [(752, 340, 835, 361), '分']
    JN_ZDFP = [(498, 391, 590, 419), '分']  # 技能自动分配
    TASK_ZB = [(748, 380, 794, 406), '装']  # 任务弹出装备按钮
    ZB_TS = [(722, 144, 1272, 656), Template(OT.imgpath('装备提升'))]  # 装备上绿色小箭头
    ZB_ZB = [(1146, 630, 1207, 660), '装']  # 装备详情-装备
    TASK_CLOSE = [(1198, 31, 1250, 82), Template(OT.imgpath('任务界面'))]
    TASK_TAB = [(0, 0, 1280, 720), Template(OT.imgpath('任务页签'), rgb=True)]
    TASK_POINT = [(69, 181, 119, 403), Template(OT.imgpath('任务点'))]
    TASK_START = [(341, 529, 482, 715), Template(OT.imgpath('任务可开始'))]
    TASK_ARROW = [(1189, 483, 1236, 522), Template(OT.imgpath('任务箭头'))]
    TASK_TAKE = [(1067, 403, 1150, 438), Template(OT.imgpath('任务接受'))]
    TASK_OVER = [(0, 0, 1280, 720), Template(OT.imgpath('任务完成'))]
    TASK_MR_QR = [(0, 0, 1280, 720), Template(OT.imgpath('每日任务确认'))]
    TASK_REWARD = [(595, 630, 685, 659), Template(OT.imgpath('任务奖励'))]
    MOVE_NOW = [(752, 191, 825, 214), Template(OT.imgpath('立刻移动'))]
    # 每日相关
    MR_MENU = [(1225, 25, 1252, 52), Template(OT.imgpath('菜单'))]
    # 活动
    HD_QBLQ = [(698, 628, 807, 661), Template(OT.imgpath('全部领取'), rgb=True)]
    HD_QBLQ2 = [(1124, 645, 1222, 684), Template(OT.imgpath('全部领取2'), rgb=True)]
    KT_QBLQ = [(1138, 650, 1223, 680), Template(OT.imgpath('课题全部领取'))]
    KT_QBLQ2 = [(1133, 645, 1226, 684), Template(OT.imgpath('课题全部领取2'), rgb=True)]
    KT_QBLQ3 = [(1132, 642, 1229, 690), Template(OT.imgpath('课题全部领取3'), rgb=True)]
    HD_XX = [(554, 603, 654, 632), Template(OT.imgpath('休息奖励领取'))]
    HD_CZZY = [(549, 96, 952, 158), '全部的成']  # 全部的成長支拨
    CZZY = [(28, 125, 468, 178), Template(OT.imgpath('成长奖励'))]
    # 背包清理
    BAG_FULL = [(1140, 36, 1195, 64), 'FULL']  # 背包满
    BAG_MAX_IMG = [(1140, 36, 1195, 64), Template(OT.imgpath('背包满'))]
    BAG_SELL = [(1167, 663, 1215, 687), Template(OT.imgpath('贩售'))]
    BAG_FJ = [(1026, 661, 1071, 688), Template(OT.imgpath('分解'))]
    BAG_CS_LIST = [(644, 110, 697, 579), Template(OT.imgpath('出售1'))]
    BAG_SX = [(52, 657, 90, 691), Template(OT.imgpath('筛选'))]
    BAG_SX_TY = [(762, 622, 818, 64), Template(OT.imgpath('套用'))]
    BAG_CS_QR = [(1145, 660, 1193, 688), Template(OT.imgpath('贩售确认'), rgb=True)]
    BAG_CS_QR1 = [(758, 519, 818, 547), Template(OT.imgpath('贩售确认1'))]
    BAG_GOLD = [(858, 19, 1115, 63), Template(OT.imgpath('金币详情'))]
    # 邮件
    MAIL_RQ = [(972, 27, 1006, 49), Template(OT.imgpath('邮件'))]
    MAIL_NULL = [(583, 315, 701, 408), Template(OT.imgpath('无邮件'))]
    # 战斗相关
    XC_OCR = [(1040, 598, 1107, 634), '除']  # 卸除 骑宠没下
    XC_IMG = [(1013, 570, 1133, 653), Template(OT.imgpath('卸除'))]
    TC_XX = [(492, 276, 780, 298), '除休息玩家']  # 踢出休息警告
    AUTO_JG = [(539, 154, 742, 198), '结果']  # 自动战斗结果
    AUTO_BAT_OCR = [(395, 647, 450, 663), '自']  # 自动战斗未开启
    AUTO_BAT = [(379, 622, 469, 688), Template(OT.imgpath('自动战斗'))]
    AUTO_BAT1 = [(379, 622, 469, 688), Template(OT.imgpath('自动战斗1'))]
    AUTO_UI_OCR = [(572, 111, 711, 151), '自']  # 自动战斗界面
    RES_EXIT_TEAM = [(0, 0, 1280, 720), Template(OT.imgpath('休息离队提示'))]
    S_MAP = [(1190, 70, 1272, 140), Template(OT.imgpath('小地图'))]
    PERSON_POS = [(864, 75, 1257, 193), Template(OT.imgpath('人物坐标'))]
    XT_MOVE = [(1133, 648, 1193, 677), Template(OT.imgpath('星图移动'))]
    # 组队相关
    TEMA_ING = [(332, 245, 410, 332), Template(OT.imgpath('组队中'))]
    TEAM_CREAT = [(78, 197, 217, 381), Template(OT.imgpath('创立队伍'))]
    TEAM_AUTO_JION = [(78, 197, 217, 381), Template(OT.imgpath('自动加入'))]
    TEAM_FIND = [(78, 197, 217, 381), Template(OT.imgpath('自动加入'))]
    # 装备
    EQ_JJS = [(734, 155, 1268, 645), Template(OT.imgpath('凝聚力量的结晶石'))]
    EQ_TJP_OCR = [(802, 75, 1259, 623), '匠铺']  # 铁匠铺
    EQ_UP_OCR = [(37, 304, 135, 363), '升']  # 升级
    EQ_QH_OCR = [(158, 316, 248, 350), '力强']  # 星力强化
    EQ_ZBZ_OCR = [(730, 166, 1265, 616), '装']  # 装备中
    EQ_WZB = [(225, 97, 370, 211), Template(OT.imgpath('无装备'))]
    EQ_ZDXZ = [(1002, 597, 1279, 717), Template(OT.imgpath('自动选择'))]
    EQ_ZDXZ_UI_OCR = [(571, 38, 713, 81), '自']  # 自动选择
    EQ_ZDXZ_SD_OCR = [(59, 502, 513, 524), '定']  # 存储自动选择设定
    EQ_UP = [(559, 621, 717, 701), Template(OT.imgpath('升级'), rgb=True)]  # 升级确认按钮
    EQ_UP_QR = [(492, 604, 789, 682), Template(OT.imgpath('升级确认'))]
    # 强化
    EQ_QH_NULL = [(413, 210, 465, 232), '基']  # 强化格子为空
    EQ_QH = [(606, 647, 664, 679), Template(OT.imgpath('强化'))]
    EQ_QH2 = [(603, 536, 678, 564), Template(OT.imgpath('强化2'))]
    # 买药
    CZ_FUHUO = [(267, 472, 525, 585), Template(OT.imgpath('复活'))]
    BUY_NOW_MOVE = [(792, 162, 914, 685), Template(OT.imgpath('立即前往'))]
    BUY_YS_LOGIN = [(792, 162, 914, 685), Template(OT.imgpath('药水登录'))]
    JN_LOGIN_2 = [(790, 305, 912, 382), Template(OT.imgpath('药水登录'))]
    BUY_YS_NUM = [(909, 628, 947, 665), Template(OT.imgpath('药品数量'))]
    HP_NULL_OCR = [(1116, 368, 1184, 387), 'HP']  # HP为空
    MP_NULL_OCR = [(1194, 370, 1263, 388), 'MP']
    YS_GM_QR = [(577, 157, 704, 196), '道具']  # 购买确认
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

    # 买药
    BUY_MP_LOGIN = [(549, 33, 730, 74), '水']  # 登绿MP樂水
    BUY_HP_LOGIN = [(549, 33, 730, 74), '登绿HP樂水']  # 登绿HP樂水
    YS_GM = [(664, 209, 772, 237), '水']  # 药水购买界面
    # Ocr
    TASK_OCR = [(395, 647, 450, 663), '任']  # 自动任务
    BAG_OCR = [(9, 18, 94, 61), '背包']  # 背包
    BAG_CS_OCR = [(13, 18, 92, 61), '贩售']  # 贩售
    BAG_SX_OCR = [(571, 39, 711, 76), '贾']  # 贩卖筛选
    BAG_CS_QR_OCR = [(575, 154, 707, 197), '贩售道具']  # 贩售道具
    BAG_GOLD_OCR = [(574, 155, 705, 195), '持有']  # 持有枫币
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
    BAG_BS = [(664, 209, 780, 235), '珠']
    BAG_DQ = [(771, 626, 848, 663), '丢']
    BAG_DQ1 = [(702, 624, 764, 662), '丢']
    BAG_DQ_QR = [(571, 155, 712, 201), '丢']
    BAG_NULL = [(738, 161, 1266, 644), Template(OT.imgpath('空格子'))]
    # 技能
    MENU_JN = [(798, 73, 1265, 618), '技能']
    JN_ZB_OCR = [(976, 171, 1125, 698), '装']
    JN_XZ = [(172, 164, 507, 476), Template(OT.imgpath('卸载技能'), threshold=0.9)]
    JN_ZB = [(989, 197, 1127, 715), Template(OT.imgpath('装备技能'), rgb=True)]
    # 宠物
    CW_SJJS = [(516, 85, 771, 127), '物剩']  # 宠物剩余时间结束
    MENU_CW = [(798, 73, 1265, 618), '窜物']
    CW_NULL = [(479, 140, 521, 160), 'ACC']  # 未装备宠物
    USE_CW = [(1146, 628, 1203, 661), '装']
    FEVER = [(201, 505, 254, 543), 'Fever']  # 宠物技能
    JN_LOGIN = [(573, 34, 705, 73), '技能登']  # 技能登录
    PET_1 = [(349, 143, 433, 217), Template(OT.imgpath('默认宠物1'))]
    PET_2 = [(349, 143, 433, 217), Template(OT.imgpath('默认宠物2'))]
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
    YM_READY = [(109, 147, 230, 183), 'Y']
    PKJ = [(704, 104, 891, 193), Template(OT.imgpath('皮卡啾'))]
    PKJ_READY = [(757, 152, 855, 179), 'Y']
    NH = [(1048, 103, 1191, 194), Template(OT.imgpath('女皇'))]
    NH_READY = [(1071, 151, 1178, 181), 'Y']
    YM_OVER = [(122, 135, 205, 163), 'L']
    PKJ_OVER = [(750, 138, 862, 169), 'L']
    NH_OVER = [(1029, 111, 1208, 184), 'L']
    BOSS_DJ = [(571, 32, 693, 65), '现道']
    # 每日
    MR_BACK = [(23, 22, 66, 61), Template(OT.imgpath('返回'))]
    MR_BAT_EXIT = [(1202, 251, 1269, 317), Template(OT.imgpath('战斗退出'), threshold=0.9)]
    MR_TIP_CLOSE = [(1209, 12, 1276, 73), Template(OT.imgpath('关闭界面'), threshold=0.8)]  # 关闭菜单界面弹窗
    MR_MENU_KSNR = [(809, 73, 1250, 608), '快速内容']  # 菜单入口
    MR_KSZD = [(1060, 639, 1174, 685), '快速']  # 快速粗际
    MR_AREA = (5, 151, 1271, 712)
    HD_MENU = [(809, 73, 1250, 608), '活勤']
    MR_GWGY_OCR = [(9, 7, 314, 73), '怪物公']  # 怪物公园
    GWGY_FQ = [(357, 491, 445, 553), '放']
    MR_XLZC_OCR = [(9, 7, 314, 73), '星力']  # 星力戟场
    XT_FLAG = [(191, 83, 297, 117), Template(OT.imgpath('星图标记'))]
    XT_MOVE_QR = [(534, 154, 738, 194), '星力']  # 移勤星力戟堤

    MR_JZT_OCR = [(9, 7, 314, 73), '金字塔']  # 奈特的金字塔
    MR_XZD_OCR = [(9, 7, 314, 73), '征']  # 速征际
    MR_GWSLT_OCR = [(9, 7, 314, 73), '怪物狩']  # 怪物狩僧惠
    GWSLT_ZDJL = [(570, 39, 708, 83), '纪']  # 战斗记录
    GWSLT_ZDJS = [(398, 296, 860, 348), '结束']  # 战斗结束 游咸重元结束!2秒俊自勤退出
    MR_MRDC_OCR = [(9, 7, 314, 73), '每日']  # 每日地城
    MR_JYDC_OCR = [(9, 7, 314, 73), '菁英']  # 菁英地城
    MR_MNDC_OCR = [(9, 7, 314, 73), '迷你']  # 迷你地城
    MNDC_JR = [(540, 140, 740, 185), '入迷你地城']  # 进入迷你地城
    MNDC_JS = [(533, 126, 747, 174), '结束迷你地城']
    MNDC_JG = [(576, 79, 705, 118), '结果']  # 最终结果
    MNDC_JSQR = [(747, 543, 819, 573), '结束']
    MNDC_FQ = [(463, 530, 535, 567), '放']  # 放弃之前的地城
    MR_GHDC_OCR = [(99, 19, 250, 63), '曹地']  # 公会地城
    MR_GH_OCR = [(11, 13, 92, 65), '公']  # 公会主界面
    JRGH_OCR = [(569, 406, 708, 448), '速加']  # 加入公会
    JRGH_IMG = [(0, 0, 1280, 720), Template(OT.imgpath('加入公会'))]
    MR_JRGH_OCR = [(99, 19, 178, 66), '公']  # 加入公会
    GH_KSJR = [(653, 667, 736, 698), '快速加入']
    GH_WXDC = [(1121, 362, 1240, 386), '限']  # 无限地城
    MR_RYZ_OCR = [(97, 18, 274, 63), '誉']  # 公会荣誉战
    GH_WXDC_MAP = [(40, 90, 132, 117), '塔']  # 无限地城战斗中
    GH_RYZ = [(1129, 465, 1238, 496), '荣']  # 公会荣誉战-W
    MR_WLDC_OCR = [(9, 7, 314, 73), '武陵道']  # 武陵道堤
    MR_WLDC_PM = [(515, 38, 766, 77), '排名']  # 排名结算
    ZD_KS = [(350, 380, 390, 401), '始']  # 组队 开始
    MR_WLDC_RC = [(1065, 637, 1177, 676), Template(OT.imgpath('入场'), threshold=0.9)]
    MR_WLDC_JR = [(584, 43, 698, 95), '入']  # 进入界面
    MR_JZT_JR = [(593, 153, 682, 193), '入']  # 进入界面
    MR_MRDC_JR = [(601, 39, 680, 81), '入']  # 进入界面
    MR_YDZXD = [(311, 487, 960, 660), '至']  # 移勤至遐革
    MR_MAX = [(984, 249, 1029, 273), Template(OT.imgpath('MAX'))]
    MR_JHXT_OCR = [(9, 7, 314, 73), '化系']  # 淮化系流
    MR_TBB_OCR = [(9, 7, 314, 73), '寳寳的']  # 温寳寳的料
    TBB_CLGW = [(540, 39, 739, 82), '材料怪物']
    TBB_ZDJS = [(588, 525, 701, 561), '碓']  # 确认
    TBB_ZCTZ = [(784, 629, 891, 660), '再次']
    TBB_ZCRC = [(570, 36, 708, 75), '再次入']  # 再次入场
    TBB_QX = [(450, 628, 531, 660), '取消']  # 取消再次入场
    MR_XGT_OCR = [(9, 7, 314, 73), '星光M塔']  # 星光M塔
    MR_XGT_JR = [(550, 156, 739, 194), '星光M塔']
    MR_HD_OCR = [(9, 7, 314, 73), '混沌速']  # 混沌速征际
    YZD_JS = [(464, 324, 804, 362), '元结束']  # 远征队结束
    MR_CYRQ_OCR = [(9, 7, 314, 73), '次元入侵']  # 次元入侵
    # ------
    KT_MENU = [(809, 73, 1250, 608), '课题']

    HD_UI_OCR = [(5, 5, 175, 73), '活勤']  # 活勤
    KT_UI_OCR = [(5, 5, 175, 73), '课题']  # 课题 界面
    JN_UI_OCR = [(5, 5, 175, 73), '技能']  # 技能 界面
    CW_UI_OCR = [(5, 5, 175, 73), '窜物']  # 宠物 界面
    SD_UI_OCR = [(5, 5, 175, 73), '商店']  # 商店 界面
    MR_UI_OCR = [(5, 5, 175, 73), '快速']  # 快速单元 界面
    TJP_UI_OCR = [(5, 5, 175, 73), '匠']  # 藏匠铺 铁匠铺
    MAP_UI_OCR = [(18, 10, 122, 66), '地']  # 地圆 地图
    MAP_MOVE_ERR = [(546, 152, 736, 199), '法瞬']  # 无法瞬间移动
    MAP_DONT_USE = [(576, 152, 707, 201), '法使用']  # 没石头无法使用
    MAP_MOVE_END = [(546, 152, 736, 199), '完成']  # 瞬间移动完成
    MAP_XL = [(592, 310, 665, 339), '目的地']  # 寻路确认框
    MAP_MOVE_NOW = [(530, 280, 677, 308), '移之石']  # 确认瞬间移动
    MAP_XL_OCR = [(495, 188, 583, 217), '接移']  # 寻路中
    MAP_YD = [(938, 648, 1037, 678), '移']  # 瞬间移动按钮

    KT_MRRW_OCR = [(42, 75, 166, 518), '每日任移']  # 每日任务
    KT_MZRW_OCR = [(42, 75, 166, 518), '每遇任移']  # 每周任务
    KT_MRSL_OCR = [(42, 75, 166, 518), '每日狩']  # 每日狩猎
    KT_CJ_OCR = [(42, 75, 166, 518), '成就']  # 成就
    HD_DR_OCR = [(1, 86, 210, 716), '登入']  # 登入挺励
    HD_XX_OCR = [(1, 86, 210, 716), '休息']  # 休息挺励

    # 邮件
    MAIL_UI_OCR = [(606, 39, 685, 82), '信件']  # 邮箱
    MAIL_SOLO_OCR = [(388, 133, 905, 166), '佃人']  # 个人
    # 组队
    TEAM_TAB = [(8, 291, 62, 343), Template(OT.imgpath('组队页签'))]
    TEAM_XZDW = [(86, 333, 215, 381), Template(OT.imgpath('寻找队伍'))]
    TEAM_ZDJR = [(89, 266, 212, 313), Template(OT.imgpath('自动加入'))]
    TEAM_ZDJR_QR = [(1110, 141, 1237, 190), Template(OT.imgpath('自动加入确认'))]
    TEAM_ZDJR_OCR = [(99, 282, 199, 305), '加入中']  # 自动加入中
    TEAM_CLDW = [(86, 197, 214, 248), Template(OT.imgpath('创立队伍'))]
    TEAM_CLDW_OCR = [(547, 39, 735, 82), '立']  # 创立队伍选项
    TEAM_PWD_OCR = [(540, 55, 741, 99), '密']  # 输入密码
    PD_BG = [(1069, 15, 1191, 70), Template(OT.imgpath('频道变更'))]
    PD_BG_OCR = [(574, 40, 710, 80), '更']
    PWD_TEAM = [(897, 189, 964, 533), Template(OT.imgpath('密码队伍'))]
    JION_TEAM_OCR = [(1007, 448, 1140, 473), '不存在']  # 不存在队伍

    EXIT_TEAM = [(290, 187, 328, 446), Template(OT.imgpath('离开队伍'))]
    QUIT_TEAM = [(540, 154, 738, 200), '伍']  # 进入每日时 离开队伍
    TKDK_OCR = [(42, 93, 129, 114), '天空的']
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
              '偏僻泥沼': [[949, 1050, 1212, 148], [921, 1156, 135], [1198, 135], [30, 70, 100], [1250, 1153, 966, 870]],
              '变形的森林': [[982, 1143, 153], [961, 1175, 135], [135], [50, 100, 0], [1250, 1153, 966, 870]],
              '武器库星图': [[933, 1094, 1216, 153], [998, 1060, 135], [135], [50, 50, 0], [1245, 1153, 966, 870]],
              '灰烬之风高原': [[1036, 1060, 153], [1024, 1060, 1119, 135], [135], [50, 50, 0], [1245, 1153, 966, 870]],
              '崎岖的峡谷': [[1022, 1067, 153], [949, 135], [1060, 1171, 135], [50, 100, 30], [1245, 1153, 966, 880]]

              },
        # ----野图
        '4': {
            '露台2': [[961, 1172, 142], [135], [135], [60, 0, 0], [1244, 1153, 966, 874]],
            '忘却之路3': [[975, 1171, 153], [135], [135], [70, 0, 0], [1245, 1153, 966, 870]],
            '神秘森林': [[911, 1193, 135], [904, 1178, 135], [135], [70, 100, 0], [1244, 1153, 966, 874]],
            '武器库': [[933, 1060, 1172, 153], [1001, 1123, 135], [135], [50, 50, 0], [1245, 1153, 966, 870]],
            '崎岖峡谷': [[1023, 1066, 153], [950, 1060, 135], [135], [60, 100, 0], [1245, 1153, 966, 870]],
            '木菇菇林': [[1027, 1112, 153], [135], [135], [30, 0, 0], [1165, 1085, 1050, 960]]
        }

    }
    # 0:识别左上角地图名,1:星图星数
    MAP_OCR = {
        'NULL': [[0, ''], 0],
        '研究所102': [[(42, 103, 156, 123), '研究所'], 40],
        '西边森林': [[(41, 102, 163, 122), '神木村'], 45],
        '冰冷死亡战场': [[(40, 104, 146, 122), '死亡'], 65],
        '龙蛋': [[(42, 87, 114, 104), '80'], 80],
        '爱奥斯塔入口': [[(43, 101, 149, 124), '塔入口'], 90],
        '奥斯塔入口': [[(40, 102, 159, 122), '赫'], 105],
        '天空露台2': [[(40, 87, 114, 104), '110'], 110],
        '机械室': [[(40, 92, 182, 114), '113'], 113],
        '时间漩涡': [[(40, 90, 184, 117), '115'], 115],
        '忘却之路4': [[(40, 93, 192, 116), '之路'], 120],
        '偏僻泥沼': [[(40, 93, 178, 113), '泥沼'], 130],
        '变形的森林': [[(40, 102, 161, 121), '森林'], 136],
        '武器库星图': [[(40, 93, 168, 116), '142'], 142],
        '灰烬之风高原': [[(39, 85, 118, 106), '144'], 144],
        '崎岖的峡谷': [[(39, 90, 192, 118), '147'], 147],
        # ----野图
        '神秘森林': [[(43, 91, 169, 115), '神秘'], '森林', '神秘', 80],
        '露台2': [[(40, 90, 148, 117), '2'], '斯湖', '2', 110],
        '忘却之路3': [[(42, 92, 131, 117), '之路3'], '神殿', '之路3', 120],
        '武器库': [[(41, 92, 98, 116), '武器'], '未来', '武器', 139],
        '崎岖峡谷': [[(42, 93, 129, 114), '的峡谷'], '未来', '的峡谷', 144],
        '木菇菇林': [[(40, 90, 174, 120), '木菇'], '艾', '木菇', 150]
    }
    # 米纳雨森林
    # 路德斯湖
    # 艾霰森林
    # 诗固神殿
    # 武陵桃圆
    # 未来之門
    # 瑞恩村


# class ColorEnumG:
#     LOGIN_CLOSE = [[(1240, 36, 'FFFFFF'), (1243, 36, 'FFFFFF'), (1245, 33, 'FFFFFF')], '登录弹窗']
#     LOGIN_MAIN = [[(20, 666, 'EAA000'), (1140, 627, '211C21'), (61, 42, 'FFFFFF')], '登录主界面']
#     LOGIN_START = [[(965, 602, '9CBF18'), (1148, 604, '99BC17'), (955, 404, 'F6E7C9')], '游戏开始']
#
#     EXIT_GAME = [[(458, 531, '4C87B0'), (571, 511, '4C87B0'), (761, 513, 'EE7046'),
#                   (635, 346, 'F2F2F2'), (344, 572, 'F2F2F2')], '游戏退出']
#     PET_TIME_END = [
#         [(910, 96, 'F6FAFD'), (910, 98, 'FFFFFF'), (451, 93, '415067'), (511, 302, '404A54'), (524, 419, 'FFFFFF'),
#          (623, 229, 'EA7C61'), (693, 298, '404A54')], '宠物到期']  # 未修正
#     QD_HD_BJBS = [[(1067, 660, 'ECCD00'), (1235, 34, '334B5E'), (799, 653, '3A9FED')], '签到活动-不见不散']
#     QD_HD_BJBS_CLOSE = [[(1236, 34, '334B5E'), (646, 30, 'FFF2CC'), (794, 665, '399EEB')], '关闭-签到不见不散']
#     QD_MY = [[(1226, 41, '415066'), (87, 43, 'FFFFFF'), (96, 72, '415066'), (20, 700, 'F2F2F2'),
#               (1261, 698, 'F2F2F2'), (1136, 112, '617A95'), (97, 167, 'F2F2F2'), (106, 147, '2B3646')], '每月签到']
#     QD_MZ = [[(1144, 60, 'FFFFFF'), (147, 93, '415066'), (816, 677, 'F2F2F2')], '每周签到']
#     HD_LB = [[(1086, 77, 'A5A5A5'), (1117, 668, '363D4A'), (160, 670, 'ECECEC'), (1061, 88, 'FFFFFF'),
#               (644, 74, 'FFFFFF'), (1074, 64, 'A5A5A5'), (1118, 392, 'F1F1F1'), (987, 91, 'FFFFFF')], '推荐礼包']
#     # 背包
#     BAG_MAIN = [[(1243, 57, '415066'), (989, 671, '4C87B0'), (1131, 689, '4C87B0')], '背包主界面']
#     BAG_SELL = [[(1241, 36, 'FFFFFF'), (126, 48, '415066'), (1089, 675, 'EE7046'), (297, 671, 'E9E9E9')], '背包出售']
#     BAG_GOLD = [[(528, 517, 'EE7046'), (398, 200, '415066'), (556, 290, 'D4D4D4')], '背包-持有金币']
#     HB_ENUM = [[(1230, 116, 'FFFFFF'), (923, 187, '464F58'), (924, 233, '2D333B'), (960, 325, '2D333B')], '货币目录']
#     BAG_SX = [[(1224, 57, 'FFFFFF'), (418, 617, '4C87B0'), (665, 616, 'EE7046'), (98, 631, 'F2F2F2')], '背包-筛选']
#     BAG_FJ = [[(388, 543, '4C87B0'), (670, 543, 'EE7046'), (955, 234, 'DFDFDF')], '背包-分解筛选']
#     ZB_CD = [[(1221, 53, 'FFFFFF'), (1126, 623, 'EE7046'), (686, 624, '4C87B0'), (826, 624, 'ED7046')], '装备-详情']
#
#     # 任务
#     TASK_CLOSE = [[(1220, 51, 'F9FFFF')], '任务关闭']  # 未修正
#     # 每日
#     MR_KSDY = [[(1241, 53, '415066'), (967, 103, 'EE7046'), (778, 104, '4C87B0'), (1140, 100, '617A95')], '快速单元界面']
#     # 武林
#     WL_MAIN = [[(15, 25, '344154'), (746, 436, '515F6E'), (105, 382, '4C87B0')], '武林道场-主界面']
#     WL_JR = [[(393, 634, '4C87B0'), (679, 633, 'EE7046'), (928, 573, 'E4E4E4'), (224, 99, '415066')], '武林道场-进入']
#     WL_PM = [[(592, 633, 'EE7046'), (353, 26, '434F69'), (647, 518, 'F2F2F2'), (894, 636, 'F2F2F2')], '武林-排名']  # 未修正
#     # 金字塔
#     JZT_MAIN = [[(26, 19, '344154'), (333, 618, 'DCDEE1'), (88, 521, 'F2F2F2')], '金字塔-主界面']
#     JZT_JR = [[(413, 521, '4C87B0'), (352, 455, 'E9E9E9'), (354, 258, 'FFFFFF')], '金字塔-进入']
#     JZT_END = [[(572, 571, '4C87B0'), (381, 566, '4C87B0'), (763, 571, 'EE7046')], '金字塔-结束']
#     JYDC_MAIN = [[(25, 16, '344154'), (154, 256, 'EE7546'), (1102, 249, '515F6E')], '菁英地城-主界面']
#     JYDC_JR = [[(421, 518, '4C87B0'), (495, 451, 'E9E9E9'), (358, 267, 'FFFFFF')], '菁英地城-进入']
#     JYDC_END = [[(548, 636, '4C87B0'), (273, 638, '4C87B0'), (832, 642, 'EE7046')], '菁英地城-结束']
#     MRDC_MAIN = [[(20, 17, '344154'), (1230, 207, 'F2F2F2'), (12, 204, 'F2F2F2')], '每日地城-主界面']
#     MRDC_MAIN1 = [[(22, 18, '344154'), (278, 618, 'DCDEE1'), (144, 620, 'EE7546')], '每日地城-混沌']
#     MRDC_JR = [[(549, 633, '4C87B0'), (402, 538, 'E4E4E4'), (360, 182, 'E9E9E9')], '每日地城-进入']
#
#     JHXT_MAIN = [[(19, 17, '344154'), (123, 131, '515F6E'), (441, 246, 'E9E9E9'), (50, 622, 'DCDEE1')], '进化系统-主界面']
#     JHXT_JR = [[(415, 637, '4C87B0'), (682, 634, 'EE7046'), (264, 416, 'E6E6E6'), (251, 648, 'F2F2F2')],
#                '进化系统-进入']
#     YZD_MAIN = [[(23, 12, '344154'), (1044, 382, '515F6E'), (1027, 479, 'E4E4E4')], '远征队-主界面']
#     GWSLT_MAIN = [[(25, 19, '344154'), (291, 655, 'E7E7E7'), (200, 489, 'E7E7E7')], '怪物狩猎团-主界面']
#     TBB_MAIN = [[(39, 39, '344154'), (52, 468, '4C87B0'), (164, 464, '4C87B0'), (1068, 127, '515F6E')], '汤宝宝-主界面']
#     TBB_JR = [[(597, 618, '4C87B0'), (405, 618, '4C87B0'), (768, 618, 'EE7046'), (451, 135, 'FFD741')], '汤宝宝-进入']
#     TBB_CLGW = [[(583, 645, 'EE7046')]]
#     TBB_ZCJR = [[(418, 625, '4C87B0'), (673, 626, 'EE7046'), (404, 253, 'EBEBEB'), (602, 131, 'F2F2F2')], '汤宝宝-再次进入']
#     XLZC_MAIN = [[(17, 20, '344154'), (58, 420, '617A95'), (888, 151, 'E7E7E7')], '星力战场-主界面']
#     CYRQ_MAIN = [[(20, 12, '344154'), (122, 550, 'FFFFFF'), (124, 442, 'ECECEC')], '次元入侵-主界面']
#     CYRQ_END_F = [[(562, 332, '4C87B0'), (313, 338, '4C87AF'), (790, 337, 'EE7046')], '次元入侵-失败']  # 未修正
#
#     MNDC_MAIN = [[(15, 11, '344154'), (1001, 374, 'E8E8E8'), (811, 636, '4C87B0')], '迷你地城-主界面']
#     MNDC_JR = [[(404, 626, '4C87B0'), (680, 624, 'EE7046'), (246, 272, 'E4E4E4')], '迷你地城-进入']
#     GWGY_MAIN = [[(18, 19, '344154'), (573, 649, '4C87B0'), (712, 651, '4C87B0'), (374, 41, 'FFFFFF')], '怪物公园-主界面']
#     XGT_MAIN = [[(18, 33, '344154'), (1158, 494, '558FB8'), (855, 487, '558FB8'), (1045, 443, 'F2F2F2')], '星光M塔-主界面']
#     EXIT_TEAM = [[(693, 519, 'EE7046'), (399, 519, '4C87B0'), (638, 352, 'F2F2F2')], '有队伍,是否离开队伍']
#     HDYZD_MAIN = [[(23, 17, '344154'), (714, 647, '4C87B0'), (60, 616, 'DCDEE1'), (14, 614, 'F2F2F2')], '混沌远征队-主界面']
#     GH_MAIN = [[(1242, 42, 'FFFFFF'), (722, 168, '515F6E'), (993, 167, '515F6E'), (662, 116, 'F2F2F2')], '公会-主界面']
#     GH_JRGH = [[(11, 13, '344154'), (925, 662, 'EE7046'), (902, 107, 'FFFFFF')], '公会-加入公会界面']  # 未修正
#     GH_WXDC = [[(14, 42, '344154'), (37, 96, 'EE7546'), (907, 600, 'FFFFFF'), (698, 673, 'F2F2F2')], '公会-无限地城']
#     GH_RYZ_F = [[(865, 645, 'EE7046'), (345, 91, '415067'), (633, 589, 'F2F2F2')], '公会荣誉战斗-失败']  # 未修正
#     GH_RYZ = [[(17, 39, '344154'), (45, 98, 'EE7546'), (919, 698, 'E9E9E9'), (768, 692, 'EFF3EF')], '公会-荣誉战']
#     # ----
#     MAIL_MAIN = [[(1033, 59, 'FFFFFF'), (481, 110, 'F2F2F2'), (237, 689, 'F2F2F2'), (221, 88, '415066')], '邮件-主界面']
#     KT_MAIN = [[(1242, 38, 'FFFFFF'), (118, 41, 'FFFFFF'), (98, 40, '415066'), (101, 693, '2B3646')], '课题-主界面']
#     PET_MAIN = [[(1244, 53, '415066'), (169, 23, '4C87B0'), (669, 105, 'E9E9E9'), (1153, 682, 'F2F2F2')], '宠物-主界面']
#     PET_XQ = [[(1221, 53, 'FFFFFF'), (1125, 621, 'EE7046'), (1051, 642, 'F2F2F2')], '宠物-详情']
#     PET_JN_LOGIN = [[(908, 54, 'FFFFFF'), (505, 122, 'F2F2F2'), (938, 238, 'F2F2F2')], '宠物-技能登录']
#     PET_NULL = [[(390, 171, 'FFFFFF'), (371, 172, 'DCDEE1'), (408, 173, 'DCDEE1'), (388, 195, 'FFFFFF')], '宠物-空']
#     JN_MAIN = [[(1235, 36, 'FFFFFF'), (196, 177, 'EAEAEA'), (310, 508, '515F6E'), (610, 105, '617A95')], '技能-主界面']
#     # 药水
#     YS_LOGIN = [[(906, 53, 'FFFFFF'), (935, 651, 'F2F2F2'), (537, 123, 'F2F2F2'), (357, 82, '415066')], '药水登录界面']
#     YS_SHOP = [[(1239, 40, '8993A0'), (25, 101, 'EE7546'), (1132, 689, 'F2F2F2')], '药水商店界面']
#     YS_XQ = [[(1223, 55, 'FFFFFF'), (1069, 134, '415066'), (1182, 338, 'F2F2F2'), (907, 670, 'DDDEDF')], '药水购买-详情']
#     YS_GM_QR = [[(425, 523, '4C87B0'), (680, 520, 'EE7046'), (382, 266, 'F2F2F2')], '药水购买-确认']
#     # HD
#     SKIP_NEW = [[(551, 534, 'EE7046'), (622, 213, 'FFEFC9')], '新内容开放']  # 未修正
#     HD_CZZY = [[(1242, 48, '415066'), (954, 99, 'FBC475'), (870, 679, 'CD657E')], '成长支援']
#     ROLE_INFO = [[(1241, 39, 'FFFFFF'), (359, 627, '617A95'), (1128, 124, 'EE7046')], '角色信息']
#     MAP_MAIN = [[(1238, 38, 'FFFFFF'), (1090, 26, 'EE7046'), (169, 23, '4C87B0'), (110, 30, '415066')], '地图-主界面']
#     BAT_MAIN = [[(983, 125, 'FFFFFF'), (897, 460, 'DDDDDD'), (548, 581, 'DDDDDD'), (315, 213, 'FFD741')], '自动战斗-主界面']
#     BAT_RES = [[(587, 528, 'EE7046'), (408, 382, 'FFFFEF'), (384, 524, 'F2F2F2'), (407, 174, '415066')], '自动战斗-结果']
#     MENU_MAIN = [[(1231, 34, 'FFFFFF'), (1222, 655, 'FFFFFF'), (841, 659, 'FFFFFF'), (873, 24, 'FFFFFF')], '菜单-主界面']
#     FEVER_BUFF = [[(984, 125, 'FFFFFF'), (631, 582, 'F2F2F2'), (283, 194, 'F2F2F2'), (768, 228, 'FFFFFF')],
#                   'fever_buff']


class RgbEnumG:
    EXIT_FOU = [391, 532, '4C87AF']  # 退出游戏-否
    CLOSE_GAME = [433, 543, '4D87AF']  # 关闭游戏-否
    FUHUO_BTN = [293, 522, '4C87AF']  # 复活按钮
    BG_PINDAO = [1083, 55, 'EE7047']  # 地图主界面-变更频道
    MAP_QWPD = [529, 635, 'EE7047']  # 地图-前往频道
    MAP_SJYD = [927, 657, '4C87AF']  # 瞬间移动
    HD_BJBS = [1058, 655, 'EDCE01']  # 活动签到
    HD_BJBS_LQ = [1058, 655, 'EC9C00']

    KSDY = [16, 14, '415067']  # 快速单元
    XLZC = [53, 429, '617B96']  # 星力战场
    XLZC_YD = [1117, 658, 'EE7047']  # 星力战场-移动
    XLZC_YDQR = [699, 523, 'EE7047']  # 星力战场-移动确认
    XLZC_YDOK = [568, 519, 'EE7047']  # 星力战场-移动完成
    YS_LOGIN = [565, 128, 'F2F2F2']  # 药水登录界面
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
    JZT_JR = [999, 646, 'EE7047']  # 金字塔进入
    JZT_JRQR = [659, 514, 'EE7047']  # 金字塔进入确认
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
    CYQR_JR_QR = [346, 272, 'E9E9E9']
    CYQR_JR_QR1 = [682, 549, 'EE7047']
    CYRQ_JR_F = [1055, 656, 'C3C3C3']

    MNDC_XZ = [54, 138, '2B3747']
    MNDC_XZ2 = [78, 214, '2B3747']
    MNDC_XZ3 = [633, 331, 'FFFFFF']
    MNDC_JRQR = [670, 652, 'EE7047']
    MNDC_JR = [1053, 650, 'EE7047']
    MNDC_END = [564, 593, 'EE7047']
    MNDC_JG_QR = [564, 593, 'EE7047']
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
    TEAM_MMDW = [102, 521, '3B759B']  # 密码队伍选项
    TEAM_QRMM = [524, 609, 'EE7047']  # 确认密码

    TEAM_SQJR = [1125, 647, 'EE7047']  # 申请加入
    TEAM_SQJR_F = [1125, 647, 'C3C3C3']  # 无法申请加入

    MAP_XL = [1108, 655, 'EE7047']  # 寻路按钮
    MAP_XLQR = [660, 521, 'EE7047']  # 寻路按钮确认
    MAP_ERR = [520, 520, 'EE7047']  # 无法瞬间移动

    BAG_M = [407, 32, 'EE7047']
    BAG_GOLD_QR = [579, 510, 'EE7047']
    BAG_BS = [1043, 132, 'AAB5CB']  # 宝石栏
    BAG_SP = [954, 129, 'AAB5C7']  # 饰品
    BAG_FJ = [860, 122, 'A9B6C9']  # 防具
    BAG_WQ = [770, 133, 'A4AFC3']  # 武器
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
    HD_CZZY = [240, 280, 'FF8D4F']  # 成长支援
    TC_1 = [1172, 269, '617B94']

    GX_XZ_BACK = [523, 188, 'FF7C52']  # 更新下载完成
    GX_XZ = [536, 528, 'EB7047']  # 有下载
