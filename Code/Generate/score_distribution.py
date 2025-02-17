import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ----------------------------------------------------------------------------------------
# 经常修改的参数
# 标题
title = "HDU 2023 计算机学/专硕 复试/录取情况"
# 标签
csv_file_1_label = '081200 计算机学硕 复试'
csv_file_2_label = '085404 计算机专硕 复试'
not_admission_label = '进入复试但未录取'
# csv 复试数据
csv_file_1_reexamine = 'csv_data/2023/2023_081200_reexamine.csv'
csv_file_2_reexamine = 'csv_data/2023/2023_085404_reexamine.csv'
# csv 录取数据
csv_file_1_admission = 'csv_data/2023/2023_081200_admission.csv'
csv_file_2_admission = 'csv_data/2023/2023_085404_admission.csv'
# 保存图片文件名
save_file_name = "2023分数分布.png"
# ----------------------------------------------------------------------------------------

def get_min_max_score(csv_file_1, csv_file_2):
    """
    获取csv中总分最小/最大值
    :param csv_file_1: 文件1
    :param csv_file_2: 文件2
    :return: 最小值, 最大值
    """
    # 读取复试 csv数据
    academic_degree_df = pd.read_csv(csv_file_1)
    professional_degree_df = pd.read_csv(csv_file_2)
    # 读取总分列数据
    academic_total_score = academic_degree_df['Total Points']
    professional_total_score = professional_degree_df['Total Points']

    min_score = min(academic_total_score.min(), professional_total_score.min())
    max_score = max(academic_total_score.max(), professional_total_score.max())
    return min_score, max_score


def create_tick_label(min_score, max_score, step_size):
    """
    生成x轴的标签
    :param min_score: 最低分
    :param max_score: 最高分
    :param step_size: 步长
    :return: x轴标签数组
    """
    # 记录x标签的数组
    tick_label = []
    # 起始标签为 最低分减1
    down = min_score - 1
    up = down + step_size
    while down <= max_score:
        # x标签
        range_label = '({}, {}]'.format(down, up)
        tick_label.append(range_label)
        # MOVE A STEP_SIZE
        down += step_size
        up += step_size
    return tick_label

def count_number(csv_file_1, csv_file_2, min_score, max_score, step_size):
    """
    统计每个分数段的数据
    :param csv_file_1: 文件1
    :param csv_file_2: 文件2
    :param min_score: 最低分
    :param max_score: 最高分
    :param step_size: 步长
    :return: 文件1的统计数据, 文件2的统计数据
    """
    # 读取 csv数据
    data_1_df = pd.read_csv(csv_file_1)
    data_2_df = pd.read_csv(csv_file_2)
    # 读取总分列数据
    data_1_total_points = data_1_df['Total Points']
    data_2_total_points = data_2_df['Total Points']

    # Sort Asc 升序
    data_1_total_points = data_1_total_points.sort_values().reset_index(drop=True)
    data_2_total_points = data_2_total_points.sort_values().reset_index(drop=True)

    # down为范围下限, up为范围上限
    down = min_score - 1
    up = down + step_size

    # 记录当前指针位置
    curr_pointer_data_1 = 0
    curr_pointer_data_2 = 0

    # 1号文件的柱状数据
    data_1_bar = []
    # 2号文件的柱状数据
    data_2_bar = []

    # 生成统计数据
    while down <= max_score:
        # 范围计数
        count_data_1 = count_data_2 = 0
        # data1 统计
        while curr_pointer_data_1 < len(data_1_total_points) and data_1_total_points[curr_pointer_data_1] <= up:
            count_data_1 += 1
            curr_pointer_data_1 += 1
        # data2 统计
        while curr_pointer_data_2 < len(data_2_total_points) and data_2_total_points[curr_pointer_data_2] <= up:
            count_data_2 += 1
            curr_pointer_data_2 += 1
        # 将数据存在数组中
        data_1_bar.append(count_data_1)
        data_2_bar.append(count_data_2)
        # 走一步长
        down += step_size
        up += step_size
    return data_1_bar, data_2_bar


def draw_pic(data_1_reexamine_bar, data_2_reexamine_bar, data_1_admission_bar, data_2_admission_bar, save_file_name):
    """
    画图
    :param data_1_reexamine_bar: 文件1复试柱状数据
    :param data_2_reexamine_bar: 文件2复试柱状数据
    :param data_1_admission_bar: 文件1录取柱状数据
    :param data_2_admission_bar: 文件2录取柱状数据
    :return: 无
    """
    # 修改字体以支持中文
    plt.rcParams['font.sans-serif'] = 'SimHei'
    plt.rcParams['axes.unicode_minus'] = False
    # 画图
    fig, ax = plt.subplots()
    ax.set_title(title)

    # x标签
    x = np.arange(len(tick_label))
    ax.set_xticks(x)
    ax.set_xticklabels(tick_label)
    # 柱状数据
    rects1 = ax.bar(x - bar_width / 2, data_1_reexamine_bar, bar_width, label=csv_file_1_label, color='#5470c6')
    rects2 = ax.bar(x + bar_width / 2, data_2_reexamine_bar, bar_width, label=csv_file_2_label, color='#91cc75')

    # 标签旋转
    ax.tick_params(labelrotation=90)

    # 未录取数据 = 复试数据 - 录取数据
    data_1_not_admission_bar = [data_1_reexamine_bar[i] - data_1_admission_bar[i] for i in
                                range(len(data_1_reexamine_bar))]
    data_2_not_admission_bar = [data_2_reexamine_bar[i] - data_2_admission_bar[i] for i in
                                range(len(data_2_reexamine_bar))]

    # 画未录取柱状图
    ax.bar(x - bar_width / 2, data_1_not_admission_bar, bar_width, label=not_admission_label, color='red')
    ax.bar(x + bar_width / 2, data_2_not_admission_bar, bar_width, color='red')
    # 展示标签
    ax.legend()
    # 网格线
    plt.grid(True, axis='y')
    # 调整布局
    plt.tight_layout()
    # 保存文件
    plt.savefig(save_file_name)
    # 展示
    plt.show()


if __name__ == '__main__':
    # 分数步长
    step_size = 5
    # 条形宽度
    bar_width = 0.4

    # 获取最低分和最高分
    min_score, max_score = get_min_max_score(csv_file_1_reexamine, csv_file_2_reexamine)

    # 生成x轴标签
    tick_label = create_tick_label(min_score, max_score, step_size)

    # 生成柱状数据
    data_1_reexamine_bar, data_2_reexamine_bar = count_number(csv_file_1_reexamine, csv_file_2_reexamine, min_score,
                                                              max_score, step_size)
    data_1_admission_bar, data_2_admission_bar = count_number(csv_file_1_admission, csv_file_2_admission, min_score,
                                                              max_score, step_size)

    # 画图
    draw_pic(data_1_reexamine_bar, data_2_reexamine_bar, data_1_admission_bar, data_2_admission_bar, save_file_name)
