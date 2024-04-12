import pandas as pd
import matplotlib.pyplot as plt

import matplotlib
del matplotlib.font_manager.weight_dict['roman']
matplotlib.font_manager._rebuild()
plt.rcParams['font.family'] = 'Times New Roman' #全体のフォントを設定
plt.rcParams['mathtext.fontset'] = 'stix' # math fontの設定
plt.rcParams['font.size'] = 14 # 全体のフォントサイズが変更されます。


def main(csv_file):
    # Read file
    df = pd.read_csv(csv_file)

    # Set values
    x = df['epoch'].values
    y0 = df['loss'].values
    y1 = df['val_loss'].values

    # Set background color to white
    # fig, ax = plt.subplots(figsize=(5 * 1.618, 5))
    fig, ax = plt.subplots(figsize=(5 * 1, 5))

    ax.tick_params(labelsize=14)
    font = {'family': 'serif',
            # 'color': 'darkred',
            'weight': 'normal',
            'size': 16,
            }
    # Plot lines
    plt.xlabel('Epoch', fontdict=font)
    plt.ylabel('Loss', fontdict=font)
    ax.plot(x, y0, label='train_loss')
    ax.plot(x, y1, label='val_loss')
    ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    ax.yaxis.offsetText.set_fontsize(14)

    # plt.plot(x, y0, label='train_loss')
    # plt.plot(x, y1, label='val_loss')

    plt.xlim(0, 150)
    plt.ylim(0, 0.0001)
    # plt.tick_params(labelsize=14)
    # plt.ticklabel_format('y', 'sci')
    # Visualize
    plt.legend()
    plt.legend(fontsize=14)
    axis = ['top', 'bottom', 'left', 'right']
    line_width = [0, 2, 2, 0]

    for a, w in zip(axis, line_width):  # change axis width
        ax.spines[a].set_linewidth(w)

    plt.tight_layout()
    plt.savefig(f"./temp_loss_curve.png", bbox_inches="tight", pad_inches=0.0)


if __name__ == '__main__':

    # path = '/mnt/data_2/dataset/02_sumitomo_cad/30_trained_models/20200616_material_perturb_1_512_rgbhsv_15000/20200623_1_multi_gaus_512/log.csv'
    # path = '/mnt/data_2/dataset/02_sumitomo_cad/30_trained_models/20200622_3_multi_roughness_rgbhsv_15000/20200711_fullscale_512/log.csv'
    path = '/mnt/data_2/dataset/02_sumitomo_cad/30_trained_models/20200622_3_multi_roughness_rgbhsv_15000/20200711_nochange_fullscale_512_2/log.csv'
    path = ''
    main(path)
