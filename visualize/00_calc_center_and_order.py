from logging import getLogger
import os
import json
from collections import OrderedDict

import numpy as np
import matplotlib.pyplot as plt


from config.const\
    import NUM_PIN, get_real_img_5081_estimate_dict_dir_name,\
    REAL_IMG_5082_dir_name
from utils.general_utils import get_glob_list

logger = getLogger(__name__)


import matplotlib
del matplotlib.font_manager.weight_dict['roman']
matplotlib.font_manager._rebuild()
plt.rcParams['font.family'] = 'Times New Roman' #全体のフォントを設定
plt.rcParams['mathtext.fontset'] = 'stix' # math fontの設定
plt.rcParams['font.size'] = 14 # 全体のフォントサイズが変更されます。


def get_pin_rotation_deg_list_from_json(json_path, offset_deg=0.0):
    with open(json_path, 'r')as f:
        info_json = json.load(f)
    rt_list = []
    for pin_idx in range(NUM_PIN):
        pin_rotation_deg = info_json[f'pin_{pin_idx}_deg'] - offset_deg
        rt_list.append(pin_rotation_deg)
    return rt_list


if __name__ == '__main__':

    ##編集可能↓
    KEY_VERSION_PREFIX = '20200622_3_multi_roughness_rgbhsv_15000'
    # KEY_EXPERIMENT_NAME = '20200711_fullscale_512'
    # KEY_EPOCH_IDX = 13  # Best
    # KEY_EPOCH_IDX = 81
    # KEY_EPOCH_IDX = 113
    # KEY_EPOCH_IDX = 116  # Best

    KEY_EXPERIMENT_NAME = '20200711_nochange_fullscale_512_2'
    KEY_EPOCH_IDX = 140

    # KEY_VALIDATION_VERSION_PREFIX = 'rgb_512'
    # KEY_VALIDATION_VERSION_PREFIX = 'rgbhsv_512' #best
    # KEY_VALIDATION_VERSION_PREFIX = 'rgbhsv_512_simple'
    # KEY_VALIDATION_VERSION_PREFIX = 'multi_scale_offset_rotation_rgbhsv_512'
    # KEY_VALIDATION_VERSION_PREFIX = 'multi_scale_offset_min_rotation_rgbhsv_512'
    KEY_VALIDATION_VERSION_PREFIX = 'multi_scale_offset_min_rotation_rgbhsv_512_2'
    # KEY_VALIDATION_VERSION_PREFIX = 'multi_scale_offset_min_rotation_rgbhsv_512_3'

    ## 学習時のDataset名と実験名を指定
    VERSION_PREFIX = '20200622_3_multi_roughness_rgbhsv_15000'
    # EXPERIMENT_PREFIX = '20200703_simplednn_4'
    # EPOCH_IDX = 999
    EXPERIMENT_PREFIX = '20200704_simplednn_16pointss_1'
    EPOCH_IDX = 1499

    normal_range_start = 3
    normal_range_end = 14

    move_range_start = 53
    move_range_end = 71

    ##編集可能↑

    # load result
    from_dir = get_real_img_5081_estimate_dict_dir_name(VERSION_PREFIX, EXPERIMENT_PREFIX, EPOCH_IDX,
                                                              KEY_VERSION_PREFIX, KEY_VALIDATION_VERSION_PREFIX, KEY_EXPERIMENT_NAME, KEY_EPOCH_IDX)
    title_prefix = f'SimpleNN_{VERSION_PREFIX}_exp={EXPERIMENT_PREFIX}_epoch{EPOCH_IDX:04d}' \
                   f'_Keypoint_{KEY_VERSION_PREFIX}_val={KEY_VALIDATION_VERSION_PREFIX}_exp={KEY_EXPERIMENT_NAME}_epoch{KEY_EPOCH_IDX:04d}'
    from_list = get_glob_list(from_dir, 'json')
    to_dir = REAL_IMG_5082_dir_name

    normal_pin_rotation_list = []
    for idx in range(normal_range_start, normal_range_end):
        from_item = from_list[idx]
        normal_pin_rotation_list.extend(get_pin_rotation_deg_list_from_json(from_item))

    # todo: ない方がベスト
    # for idx in range(move_range_start, move_range_end):
    #     from_item = from_list[idx]
    #     normal_pin_rotation_list.extend(get_pin_rotation_deg_list_from_json(from_item))

    print(normal_pin_rotation_list)

    est_dict = OrderedDict()
    mean_est_normal = float(np.mean(normal_pin_rotation_list))
    for from_item in from_list:
        img_prefix = os.path.basename(from_item).replace('.json', '')

        est_deg_list = get_pin_rotation_deg_list_from_json(from_item, mean_est_normal)
        max_est_deg = float(np.max(np.abs(est_deg_list)))
        print(img_prefix, est_deg_list)
        est_dict[img_prefix] = max_est_deg

    od_sorted_value = OrderedDict(
        sorted(est_dict.items(), key=lambda x: x[1], reverse=True)
    )
    # print(od_sorted_value)
    x = []
    y = []
    for key in od_sorted_value.keys():
        # print(key, od_sorted_value[key])
        x.append(key)
        y.append(od_sorted_value[key])

    x = np.array(x)
    y = np.array(y)

    # 散布図を描画
    # plt.scatter(y, x)
    # plt.xticks(rotation=90)
    # plt.yticks(rotation=90)
    # plt.tight_layout()
    # plt.show()

    colors = ["royalblue", "deepskyblue", "red"]

    # fig = plt.figure(figsize=(10, 25), dpi=100)
    fig = plt.figure(figsize=(10, 4), dpi=500)
    ax = fig.add_subplot(111)


    idx_error = None
    idx_move = None
    idx_normal = None

    for i in range(len(x)):
        if x[i][5:] == 'normal' or x[i][5:] == 'move' or x[i][5:] == 'error':
            continue
        print(x[i], y[i])
        if 'error' in x[i]:
            color = colors[2]
            label = 'error'
            if idx_error is None:
                idx_error = i
        elif 'move' in x[i]:
            color = colors[1]
            label = 'move'
            if idx_move is None:
                idx_move = i
        else:
            color = colors[0]
            label = 'normal'
            if idx_normal is None:
                idx_normal = i

        # ax.scatter(y[i], x[i][5:], color=color)

        # ax.scatter(x[i][-19:], y[i], color=color, label=label)
        ax.scatter(x[i], y[i], color=color, label=label)
        # ax.scatter(x[i][5:], y[i], color=color)
    # plt.xlabel('(deg)')
    font = {
        # 'family': 'serif',
            # 'color': 'darkred',
            'weight': 'normal',
            'size': 7,
            }
    plt.ylabel('Max Bending Angle (deg)')
    plt.xticks(rotation=90, fontsize=6)
    # plt.legend(fontsize=14)
    handler1, label1 = ax.get_legend_handles_labels()
    ax.legend([handler1[idx_error],
              handler1[47],
              handler1[idx_move]],
              ['error', 'normal', 'move'], loc=1, borderaxespad=1.)

    # plt.tick_params(labelsize=10)
    ax.grid(axis='y')
    ax.set_ylim([0, 15])

    plt.title('Max Bending Angle of each sample: descending order')
    plt.tight_layout()

    axis = ['top', 'bottom', 'left', 'right']
    line_width = [0, 2, 2, 0]

    for a, w in zip(axis, line_width):  # change axis width
        ax.spines[a].set_linewidth(w)

    save_path = os.path.join(to_dir, f'{title_prefix}.png')
    # save_path = os.path.join(to_dir, f'{title_prefix}_best.png')
    plt.savefig(save_path)
    # plt.show()

    pass
