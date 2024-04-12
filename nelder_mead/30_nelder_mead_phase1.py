import json
import glob
import os

import matplotlib.pyplot as plt
from matplotlib import gridspec

from config.const\
    import get_real_img_5070_rotation_bending_est_dir_name
from utils.general_utils import get_glob_list, get_same_base_name


import matplotlib
del matplotlib.font_manager.weight_dict['roman']
matplotlib.font_manager._rebuild()
plt.rcParams['font.family'] = 'Times New Roman' #全体のフォントを設定
plt.rcParams['mathtext.fontset'] = 'stix' # math fontの設定
plt.rcParams['font.size'] = 14 # 全体のフォントサイズが変更されます。



if __name__ == '__main__':
    VERSION_PREFIX = '20200622_3_multi_roughness_rgbhsv_15000'
    EXPERIMENT_PREFIX = '20200711_nochange_fullscale_512_2'
    EPOCH_IDX = 140 #best
    VALIDATION_VERSION_PREFIX = 'multi_scale_offset_min_rotation_rgbhsv_512_2'
    ITEM_PREFIX = '0035_error_RSP01_UGGT0B9KS38_20190205-140125_754'


    # Read file
    est_dir = get_real_img_5070_rotation_bending_est_dir_name(
        version_prefix=VERSION_PREFIX,
        validation_version_prefix=VALIDATION_VERSION_PREFIX,
        experiment_prefix=EXPERIMENT_PREFIX,
        epoch_idx=EPOCH_IDX,
        item_prefix=ITEM_PREFIX
    )

    est_paths_1 = glob.glob(os.path.join(est_dir, '01*.json'))
    est_paths_1.sort()

    est_paths_2 = glob.glob(os.path.join(est_dir, '02*.json'))
    est_paths_2.sort()


    # Set values
    y0 = []
    y1 = []
    y2 = []
    y3 = []
    y4 = []
    y5 = []
    y6 = []
    for est_path_1 in est_paths_1:
        with open(est_path_1, 'r') as f:
            info_dict = json.load(f)
        offset_x, offset_y, offset_z = info_dict['offset']
        rotation_deg_x, rotation_deg_y, rotation_deg_z = info_dict['rotation_deg']
        loss = info_dict['res']

        loss = loss ** 0.5 / (512 + 256)

        y0.append(offset_x * 100)
        y1.append(offset_y * 100)
        y2.append(offset_z * 100)
        y3.append(rotation_deg_x)
        y4.append(rotation_deg_y)
        y5.append(rotation_deg_z)
        y6.append(loss)
    x = list(range(len(y0)))

    # for est_path_2 in est_paths_2:
    #     with open(est_path_2, 'r') as f:
    #         info_dict = json.load(f)
    #     pin_0_deg = info_dict['pin_moving_deg'][0]
    #     pin_1_deg = info_dict['pin_moving_deg'][1]
    #     pin_2_deg = info_dict['pin_moving_deg'][2]
    #     pin_3_deg = info_dict['pin_moving_deg'][3]
    #
    # Set background color to white
    fig = plt.figure(figsize=(7, 5 + 2))

    spec = gridspec.GridSpec(ncols=1, nrows=2,
                             height_ratios=[5, 2])

    # fig, ax1 = plt.subplots(figsize=(5 * 1.618, 5))
    ax1 = fig.add_subplot(spec[0])
    ax3 = fig.add_subplot(spec[1])
    # fig, ax1 = plt.subplots(figsize=(5 * 1, 5))
    ax2 = ax1.twinx()
    ax1.tick_params(labelsize=14)
    ax2.tick_params(labelsize=14)
    ax3.tick_params(labelsize=14)

    colorlist = [
                 'royalblue',
                 'deepskyblue',
                 'skyblue',
                 'deeppink',
                 'hotpink',
                 'pink',
                 'black',
                 ]

    font = {
        # 'family': 'serif',
            # 'color': 'darkred',
            'weight': 'normal',
            'size': 16,
            }
    ax1.set_xlabel('Step', fontdict=font)
    ax1.set_ylabel('Offset (mm)', fontdict=font)
    ax2.set_ylabel('Rotation (deg)', fontdict=font)
    ax3.set_xlabel('Step', fontdict=font)
    ax3.set_ylabel('Loss', fontdict=font)

    ax1.plot(x, y0, label='offset X', color=colorlist[0])
    ax1.plot(x, y1, label='offset Y', color=colorlist[1])
    ax1.plot(x, y2, label='offset Z', color=colorlist[2])
    ax2.plot(x, y3, label='rotation θ', color=colorlist[3])
    ax2.plot(x, y4, label='rotation φ', color=colorlist[4])
    ax2.plot(x, y5, label='rotation λ', color=colorlist[5])
    ax3.plot(x, y6, label='rotation λ', color=colorlist[6])


    # 凡例
    # グラフの本体設定時に、ラベルを手動で設定する必要があるのは、barplotのみ。plotは自動で設定される＞
    handler1, label1 = ax1.get_legend_handles_labels()
    handler2, label2 = ax2.get_legend_handles_labels()

    ax1.legend(handler1, label1, bbox_to_anchor=(0.72, 0.04), loc='lower right', borderaxespad=1.)
    ax2.legend(handler2, label2, bbox_to_anchor=(1, 0.04), loc='lower right', borderaxespad=1.)
    # 凡例をまとめて出力する
    # ax2.legend(handler1 + handler2, label1 + label2, loc=1, borderaxespad=1., )

    ax1.set_xlim([0, 2000])
    ax1.set_ylim([-4, 4])
    ax2.set_ylim([-3, 3])
    ax3.set_xlim([0, 2000])
    ax3.set_ylim([0, 0.05])
    ax3.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    ax3.yaxis.offsetText.set_fontsize(14)

    fig.suptitle('Phase 1: Position/Rotation and Loss by each step')
    # ax1.set_title('Position / Rotation')
    # ax2.set_title('Loss')

    # plt.tight_layout()

    axis = ['top', 'bottom', 'left', 'right']
    line_width_1 = [0, 2, 2, 2]
    line_width_3 = [0, 2, 2, 0]

    for a, w in zip(axis, line_width_1):  # change axis width
        ax1.spines[a].set_linewidth(w)
        ax2.spines[a].set_linewidth(w)

    for a, w in zip(axis, line_width_3):  # change axis width
        ax3.spines[a].set_linewidth(w)
    plt.savefig(f"./temp_phase1.png", bbox_inches="tight", pad_inches=0.0)

