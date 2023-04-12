import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

step_size = 5
bar_width = 0.4

academic_degree_df = pd.read_csv('csv_data/2023/2023_083500_reexamine.csv')
professional_degree_df = pd.read_csv('csv_data/2023/2023_085405_reexamine.csv')

academic_total_score = academic_degree_df['Total Points']
professional_total_score = professional_degree_df['Total Points']

# Sort Asc
academic_total_score = academic_total_score.sort_values().reset_index(drop=True)
professional_total_score = professional_total_score.sort_values().reset_index(drop=True)

curr_pointer_a = 0
curr_pointer_p = 0

min_score = min(academic_total_score.min(), professional_total_score.min())
max_score = max(academic_total_score.max(), professional_total_score.max())

down = min_score - 1
up = down + step_size

tick_label = []
a_bar = []
p_bar = []

while down <= max_score:
    range_label = '({}, {}]'.format(down, up)
    count_p = count_a = 0
    while curr_pointer_p < len(professional_total_score) and professional_total_score[curr_pointer_p] <= up:
        count_p += 1
        curr_pointer_p += 1
    while curr_pointer_a < len(academic_total_score) and academic_total_score[curr_pointer_a] <= up:
        count_a += 1
        curr_pointer_a += 1
    a_bar.append(count_a)
    p_bar.append(count_p)
    tick_label.append(range_label)

    down += step_size
    up += step_size

fig, ax = plt.subplots()
ax.set_title('HDU 2023')

x = np.arange(len(tick_label))
ax.set_xticks(x)
ax.set_xticklabels(tick_label)
rects1 = ax.bar(x - bar_width / 2, a_bar, bar_width, label='083500', color='#5470c6')
rects2 = ax.bar(x + bar_width / 2, p_bar, bar_width, label='085405', color='#91cc75')


ax.tick_params(labelrotation=90)

academic_admission_df = pd.read_csv('csv_data/2023/2023_083500_admission.csv')
professional_admission_df = pd.read_csv('csv_data/2023/2023_085405_admission.csv')

academic_admission = academic_admission_df['Total Points']
academic_admission = academic_admission.sort_values().reset_index(drop=True)

professional_admission = professional_admission_df['Total Points']
professional_admission = professional_admission.sort_values().reset_index(drop=True)

down = min_score - 1
up = down + step_size

curr_pointer_a_a = 0
curr_pointer_p_a = 0

a_a_bar = []
p_a_bar = []

while down <= max_score:
    range_label = '({}, {}]'.format(down, up)
    count_p = count_a = 0
    while curr_pointer_p_a < len(professional_admission) and professional_admission[curr_pointer_p_a] <= up:
        count_p += 1
        curr_pointer_p_a += 1
    while curr_pointer_a_a < len(academic_admission) and academic_admission[curr_pointer_a_a] <= up:
        count_a += 1
        curr_pointer_a_a += 1
    p_a_bar.append(count_p)
    a_a_bar.append(count_a)
    tick_label.append(range_label)

    down += step_size
    up += step_size

a_f_bar = [a_bar[i] - a_a_bar[i] for i in range(len(a_bar))]
p_f_bar = [p_bar[i] - p_a_bar[i] for i in range(len(p_bar))]

ax.bar(x - bar_width / 2, a_f_bar, bar_width, label='NOT ADMISSION', color='red')
ax.legend()

ax.bar(x + bar_width / 2, p_f_bar, bar_width, label='NOT ADMISSION', color='red')

plt.tight_layout()
plt.show()
