from logging import getLogger
import os

import cv2
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import gridspec

import matplotlib
del matplotlib.font_manager.weight_dict['roman']
matplotlib.font_manager._rebuild()
plt.rcParams['font.family'] = 'Times New Roman' #全体のフォントを設定
plt.rcParams['mathtext.fontset'] = 'stix' # math fontの設定
plt.rcParams['font.size'] = 16 # 全体のフォントサイズが変更されます。

from config.const\
    import get_real_img_5020_masked_dir_name, get_real_img_5041_csv_path_name,\
    get_real_img_5040_dataset_dir_name, get_real_img_5030_normalized_dir_name,\
    get_rendered_0000_img_dir_name
logger = getLogger(__name__)

def save_hist(target_r, target_g, target_b, save_path):
    fig = plt.figure(figsize=(10, 5))

    spec = gridspec.GridSpec(ncols=1, nrows=1,
                             height_ratios=[1])

    ax = fig.add_subplot(spec[0])
    hist_r, bins_target_r = np.histogram(target_r, 256, [0, 1])
    hist_g, bins_target_g = np.histogram(target_g, 256, [0, 1])
    hist_b, bins_target_b = np.histogram(target_b, 256, [0, 1])

    x = (np.array(list(range(256))) / 256).tolist()
    ax.plot(x, hist_r, color='red', label='R channel')
    ax.plot(x, hist_g, color='green', label='G channel')
    ax.plot(x, hist_b, color='blue', label='B channel')
    ax.set_title('Luminance Histogram of R/G/B channel')
    ax.set_xlabel('Luminance')
    ax.set_ylabel('Num Pixels')

    axis = ['top', 'bottom', 'left', 'right']
    line_width = [0, 2, 2, 0]

    for a, w in zip(axis, line_width):  # change axis width
        ax.spines[a].set_linewidth(w)
        ax.spines[a].set_linewidth(w)

    plt.legend()
    plt.legend(fontsize=14)
    # save_path = os.path.join(to_dir, f'{title_prefix}_best.png')
    plt.savefig(save_path)


def flatten_luminance(target, is_bgr=True):
    if is_bgr:
        target_r = target[:, :, 2].flatten().astype(np.float32)
        target_g = target[:, :, 1].flatten().astype(np.float32)
        target_b = target[:, :, 0].flatten().astype(np.float32)
    else:
        target_r = target[:, :, 0].flatten().astype(np.float32)
        target_g = target[:, :, 1].flatten().astype(np.float32)
        target_b = target[:, :, 2].flatten().astype(np.float32)
    new_target_r = []
    for r_ in target_r:
        if r_ > 0.01:
            new_target_r.append(r_)

    new_target_g = []
    for g_ in target_g:
        if g_ > 0.01:
            new_target_g.append(g_)

    new_target_b = []
    for b_ in target_b:
        if b_ > 0.01:
            new_target_b.append(b_)

    target_r = np.array(new_target_r)
    target_g = np.array(new_target_g)
    target_b = np.array(new_target_b)
    return target_r, target_g, target_b


if __name__ == '__main__':
    data_ver = '20200526_template'
    target_path = os.path.join(get_rendered_0000_img_dir_name(data_ver), '0000000000.npy')

    from_img_path = '/mnt/data_2/dataset/02_sumitomo_cad/50_real_img/21_masked_png/0001_error.png'
    to_img_path = '/mnt/data_2/dataset/02_sumitomo_cad/50_real_img/50_estimate/20200622_3_multi_roughness_rgbhsv_15000_val=rgbhsv_512_exp=20200711_nochange_fullscale_512_2_epoch0140/0001_error_00_img.png'

    target = np.load(target_path)
    from_img = cv2.imread(from_img_path).astype(np.float32) / 255
    to_img = cv2.imread(to_img_path).astype(np.float32) / 255

    target_r, target_g, target_b = flatten_luminance(target)
    from_r, from_g, from_b = flatten_luminance(from_img, is_bgr=True)
    # todo: どうやらヒストグラム合わせ以降でRGBとBGRを間違っているっぽい
    to_r, to_g, to_b = flatten_luminance(to_img, is_bgr=False)

    save_path_target = os.path.join('./temp_hist_target.png')
    save_path_from = os.path.join('./temp_hist_from.png')
    save_path_to = os.path.join('./temp_hist_to.png')

    save_hist(target_r, target_g, target_b, save_path_target)
    save_hist(from_r, from_g, from_b, save_path_from)
    save_hist(to_r, to_g, to_b, save_path_to)


    pass
