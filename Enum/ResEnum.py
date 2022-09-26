# -*- coding: utf-8 -*-
from airtest.core.cv import Template
from transitions import State

from Utils.OtherTools import OT


class GlobalEnumG:
    Ver = '2.0'
    GamePackgeName = r'com.nexon.maplem.global'
    FindImgTimeOut = 20  # 查找图片等待超时时间
    TouchDurationTime = 4  # 延时点击
    LoginGameTimeOut = 600  # 登录超时时长
    UiCheckTimeOut = 600  # 界面操作超时时长
    SelectCtrTimeOut = 300  # 操作超时时长
    TouchWaitTime = 2  # 点击后等待时长

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
    StatesInfo = {
        'InGame': {'name': "游戏中", 'id': 1},
        'Nothing': {'name': "无任务", 'id': 2},
        'Wait': {'name': "等待任务", 'id': 2},
        'Login': {'name': "登录游戏", 'id': 2},
        'Check': {'name': "检查界面", 'id': -1},
        'BuyY': {'name': "买药", 'id': 4},
        'FuHuo': {'name': "复活", 'id': 3},
        'BagSell': {'name': "背包清理", 'id': 5},
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
    }
    ExecuteStates = ['AutoTask', 'AutoMR', 'AutoBat', 'AutoBoss', 'Nothing', 'Wait']
    SelectStates = ['InGame',
                    'Check',
                    'Login',
                    'FuHuo',
                    'BuyY',
                    'BagSell',
                    'UseSkill',
                    'UsePet',
                    'UpEquip',
                    'StrongEquip',
                    'GetReward',
                    'CheckXT',
                    'CheckYT']


class ImgEnumG:
    """图片数据"""
    TEST = Template(OT.imgpath('21'))
    # UI_CLOSE = [(571, 39, 711, 76), Template(OT.imgpath('关闭界面'))]
    UI_CLOSE = [(1060, 24, 1149, 97), Template(OT.imgpath('弹窗'))]
    UI_QR = [(0, 0, 1280, 720), Template(OT.imgpath('确认'))]
    UI_QBLQ = [(0, 0, 1280, 720), Template(OT.imgpath('全部领取'))]
    UI_GM = [(0, 0, 1280, 720), Template(OT.imgpath('购买'))]
    UI_YES = [(277, 92, 989, 637), Template(OT.imgpath('是'))]
    UI_NO = [(277, 92, 989, 637), Template(OT.imgpath('否'))]
    UI_LB = [(1132, 58, 1157, 86), Template(OT.imgpath('推荐礼包'))]
    UI_SET = [(1196, 626, 1278, 708), Template(OT.imgpath('设置'))]
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
    LOGIN_FLAG = [(1014, 538, 1271, 703), Template(OT.imgpath('游戏登陆标志'))]
    LOGIN_FLAG1 = [(20, 665, 56, 701), Template(OT.imgpath('登录区域'))]  # 20,665,56,701
    START_GAME = [(963, 481, 1278, 688), Template(OT.imgpath('游戏开始'))]  # 963,481,1278,688
    INGAME_FLAG = [(734, 9, 1253, 64), Template(OT.imgpath('验证登录标记'))]  # 734,9,1253,64
    INGAME_FLAG2 = [(904, 336, 939, 372), Template(OT.imgpath('验证登录标记2'))]
    LOGIN_TIPS = [(1240, 14, 1264, 61), Template(OT.imgpath('登录弹窗'))]
    # 任务相关
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
    # 背包清理
    BAG_FULL = [(1140, 36, 1195, 64), 'FULL']  # 背包满
    BAG_SELL = [(1167, 663, 1215, 687), Template(OT.imgpath('贩售'))]
    BAG_FJ = [(1026, 661, 1071, 688), Template(OT.imgpath('分解'))]
    BAG_CS_LIST = [(644, 110, 697, 579), Template(OT.imgpath('出售1'))]
    BAG_SX = [(52, 657, 90, 691), Template(OT.imgpath('筛选'))]
    BAG_SX_TY = [(762, 622, 818, 64), Template(OT.imgpath('套用'))]
    BAG_CS_QR = [(1145, 660, 1193, 688), Template(OT.imgpath('贩售确认'), rgb=True)]
    BAG_CS_QR1 = [(758, 519, 818, 547), Template(OT.imgpath('贩售确认1'))]
    BAG_GOLD = [(917, 4, 1134, 82), Template(OT.imgpath('金币详情'))]
    # 邮件
    MAIL_RQ = [(972, 27, 1006, 49), Template(OT.imgpath('邮件'))]
    MAIL_NULL = [(583, 315, 701, 408), Template(OT.imgpath('无邮件'))]
    # 战斗相关
    AUTO_JG = [(539, 154, 742, 198), '结果']  # 自动战斗结果
    AUTO_BAT_OCR = [(395, 647, 450, 663), '自']  # 自动战斗未开启
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
    EQ_QH_OCR = [(158, 316, 248, 350), '星力']  # 星力强化
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
        '0': (845, 581),
        '2': (845, 540),
        '3': (845, 488),
        '4': (845, 440),
        '5': (845, 391)
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
    # 技能
    MENU_JN = [(798, 73, 1265, 618), '技能']
    JN_ZB_OCR = [(976, 171, 1125, 698), '装']
    JN_XZ = [(172, 164, 507, 476), Template(OT.imgpath('卸载技能'), threshold=0.9)]
    JN_ZB = [(976, 171, 1125, 698), Template(OT.imgpath('装备技能'), rgb=True)]
    # 宠物
    MENU_CW = [(798, 73, 1265, 618), '窜物']
    CW_NULL = [(479, 140, 521, 160), 'ACC']  # 未装备宠物
    USE_CW = [(1146, 628, 1203, 661), '装']
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
    YM_READY=[(74,110,286,187),Template(OT.imgpath('炎魔'))]
    PKJ_READY = [(717,116,915,184), Template(OT.imgpath('皮卡啾'))]
    NH_READY = [(1039,118,1222,185), Template(OT.imgpath('女皇'))]
    # 每日
    MR_BACK = [(23, 22, 66, 61), Template(OT.imgpath('返回'))]
    MR_BAT_EXIT = [(1202, 251, 1269, 317), Template(OT.imgpath('战斗退出'), threshold=0.8)]
    MR_TIP_CLOSE = [(1209, 12, 1276, 73), Template(OT.imgpath('关闭界面'), threshold=0.8)]  # 关闭菜单界面弹窗
    MR_MENU_KSNR = [(809, 73, 1250, 608), '快速内容']  # 菜单入口
    MR_KSZD = [(1060, 639, 1174, 685), '快速']  # 快速粗际
    MR_AREA = (5, 151, 1271, 712)
    HD_MENU = [(809, 73, 1250, 608), '活勤']
    MR_GWGY_OCR = [(9, 7, 314, 73), '怪物公']  # 怪物公园
    GWGY_FQ=[(357,491,445,553),'放']
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
    MNDC_JS=[(533,126,747,174),'结束迷你地城']
    MNDC_JSQR=[(747,543,819,573),'结束']
    MNDC_FQ=[(463,530,535,567),'放']#放弃之前的地城
    MR_GH_OCR = [(9, 7, 314, 73), '公曾']  # 公会
    MR_WLDC_OCR = [(9, 7, 314, 73), '武陵道']  # 武陵道堤
    MR_WLDC_PM = [(515, 38, 766, 77), '排名']  # 排名结算
    ZD_KS = [(350, 380, 390, 401), '始']  # 组队 开始
    MR_WLDC_RC = [(1065, 637, 1177, 676), Template(OT.imgpath('入场'), threshold=0.9)]
    MR_WLDC_JR = [(584, 43, 698, 95), '入']  # 进入界面
    MR_JZT_JR = [(593, 153, 682, 193), '入']  # 进入界面
    MR_MRDC_JR = [(601, 39, 680, 81), '入']  # 进入界面
    MR_YDZXD = [(311, 487, 960, 660), '移勤至']  # 移勤至遐革
    MR_MAX = [(984, 249, 1029, 273), Template(OT.imgpath('MAX'))]
    MR_JHXT_OCR = [(9, 7, 314, 73), '化系']  # 淮化系流
    MR_TBB_OCR = [(9, 7, 314, 73), '寳寳的']  # 温寳寳的料
    TBB_CLGW = [(540, 39, 739, 82), '材料怪物']
    TBB_ZDJS = [(588, 525, 701, 561), '碓']  # 确认
    TBB_ZCTZ = [(784, 629, 891, 660), '再次']
    TBB_ZCRC = [(570, 36, 708, 75), '再次入']  # 再次入场
    TBB_QX = [(450, 628, 531, 660), '取消']  # 取消再次入场
    MR_XGT_OCR = [(9, 7, 314, 73), '星光M塔']  # 星光M塔
    MR_HD_OCR = [(9, 7, 314, 73), '混沌速']  # 混沌速征际
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
    MAP_MOV_OCR = [(546, 152, 736, 199), '移']  # 无法瞬间移动
    MAP_XL_OCR = [(495, 188, 583, 217), '接移']  # 寻路中

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
    TEAM_TAB = [(8, 291, 62, 343), Template(OT.imgpath('组队页签'), rgb=True)]
    TEAM_XZDW = [(86, 333, 215, 381), Template(OT.imgpath('寻找队伍'), rgb=True)]
    TEAM_ZDJR = [(89, 266, 212, 313), Template(OT.imgpath('自动加入'), rgb=True)]
    TEAM_ZDJR_QR = [(1110, 141, 1237, 190), Template(OT.imgpath('自动加入确认'))]
    TEAM_ZDJR_OCR = [(99, 282, 199, 305), '加入中']  # 自动加入中
    TEAM_CLDW = [(86, 197, 214, 248), Template(OT.imgpath('创立队伍'), rgb=True)]
    TEAM_CLDW_OCR = [(547, 39, 735, 82), '立']  # 创立队伍选项
    TEAM_PWD_OCR = [(540, 55, 741, 99), '密']  # 输入密码
    PD_BG = [(1069, 15, 1191, 70), Template(OT.imgpath('频道变更'))]
    PD_BG_OCR = [(574, 40, 710, 80), '更']
    PWD_TEAM = [(897, 189, 964, 533), Template(OT.imgpath('密码队伍'))]
    JION_TEAM_OCR = [(1007, 448, 1140, 473), '不存在']  # 不存在队伍

    EXIT_TEAM = [(290, 187, 328, 446), Template(OT.imgpath('离开队伍'))]


class UiEnumG:
    BAG_UI = [(59, 11, '415066'), (645, 32, '415066'), (557, 123, 'ffffff'),
              (467, 124, '2b3646'), (997, 675, '4c87b0'), (1148, 686, '4c87b0'), (59, 120, 'ee7546')]  # 背包主界面


class BatEnumG:
    TASK_ID = {
        '登录游戏': {'id': '0', 'state': 'Login'},
        '自动任务': {'id': '1', 'state': 'AutoTask'},
        '自动每日': {'id': '2', 'state': 'AutoMR'},
        '混Boss图': {'id': '5', 'state': 'AutoBoss'},
        '装备技能': {'id': '6', 'state': 'UseSkill'},
        '穿戴新手宠物': {'id': '7', 'state': 'UsePet'},
        '默认设置': {'id': '8', 'state': 'Login'},
        '开箱子': {'id': '9', 'state': 'Login'},
        '强化装备': {'id': '10', 'state': 'Login'},
        '升级装备': {'id': '11', 'state': 'Login'},
        '自定义一': {'id': '11', 'state': 'Login'},
        '自定义二': {'id': '12', 'state': 'Login'},
    }
    MAP_DATA = {
        '1': {'NULL': []},
        '2': {'NULL': []},
        '3': {'死亡战场': '0',
              '爱奥斯塔入口': [[1000, 1088, 148], [956, 1139, 135], [1060, 1162, 135], [30, 70, 100], [1250, 1153, 966, 870]],
              '天空露台2': '2',
              '西边森林': '3',
              '龙蛋': '4',
              '忘却4': '5',
              '武器库星图': '6',
              '偏僻泥沼': '7',
              '机械室': '8',
              '变形的森林': '9',
              '灰烬之风高原': '10',
              '时间漩涡': '11',
              },
        # ----野图
        '4': {
            '露台2': '0',
            '忘却之路3': '1',
            '神秘森林': '2',
            '骑士之殿': '3',
            '武器库': '4',
            '崎岖的荒野': '5'
        }

    }
    # 0:识别左上角地图名,1:星图星数
    MAP_OCR = {
        'NULL': [[0, ''], 0],
        '偏僻泥沼': [[(40, 93, 178, 113), '泥沼'], 130],
        # ----野图
        '露台2': [[(40, 90, 148, 117), '彩露'], '斯湖', '彩露', 110]
    }
    # 米纳雨森林
    # 路德斯湖
    # 艾霰森林
    # 诗固神殿
    # 武陵桃圆
    # 未来之門
    # 瑞恩村
