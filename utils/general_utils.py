from logging import getLogger
import os, glob

import cv2
import numpy as np

logger = getLogger(__name__)


def count_shadow(shadow_arr, is_from_up_to_down=True, is_255_shadow=True):
    assert len(shadow_arr.shape)==2

    if not is_255_shadow:
        shadow_arr = np.where(shadow_arr==255, 0, 255)
    if not is_from_up_to_down:
        shadow_arr = shadow_arr[::-1]
    canvas = np.zeros(shadow_arr.shape)

    for col_idx in range(len(shadow_arr[0])):
        col = shadow_arr[:, col_idx]
        count = 0

        for row_idx_rev, val in enumerate(col):
            if val == 0:
                canvas[row_idx_rev-1, col_idx] = count
                count = 0
                continue
            elif val == 255:
                count += 1
        if count != 0:
            canvas[-1, col_idx] = count

    if not is_from_up_to_down:
        canvas = canvas[::-1]
    return canvas


def concat_tile(im_list_2d):
    # todo ゼロ画像パディングの仕組みとかいれたら？
    return cv2.vconcat([cv2.hconcat([img.astype(np.uint8) for img in im_list_h]) for im_list_h in im_list_2d])


def get_glob_list(dir_name, ext=None, is_random_ok=False):
    if ext is None:
        ext_prefix = ''
    else:
        ext_prefix = f'.{ext}'
    file_list = glob.glob(os.path.join(dir_name, f'*{ext_prefix}'))
    if not is_random_ok:
        file_list.sort()

    return file_list


def is_in(left, right, upper, lower, x_val, y_val):
    is_left_right_in = (left < y_val and right > y_val) or (left > y_val and right < y_val)
    is_upper_lower_in = (upper < x_val and lower > x_val) or (upper > x_val and lower < x_val)
    return is_left_right_in and is_upper_lower_in


if __name__ == '__main__':
    arr_1 = [[255, 255, 255, 0,   0, 0, 255, 0, 0],
             [255, 255, 255, 0,   0, 0, 255, 0, 0],
             [255, 255, 255, 0,   0, 0,   0, 0, 0],
             [255, 255, 255, 0, 255, 0,   0, 0, 0],
             [255, 255, 255, 0, 255, 0,   0, 0, 0],
             [255, 255, 255, 0,   0, 0,   0, 0, 0],
             [  0, 255, 255, 0,   0, 0,   0, 0, 0],
             [  0,   0, 255, 0,   0, 0,   0, 0, 0]]

    print(count_shadow(np.array(arr_1)))
    print('--------')
    print(count_shadow(np.array(arr_1),
                       is_from_up_to_down=False,
                       is_255_shadow=True))
    print('--------')
    print(count_shadow(np.array(arr_1),
                       is_from_up_to_down=False,
                       is_255_shadow=False))
    print('--------')
    print(count_shadow(np.array(arr_1),
                       is_from_up_to_down=True,
                       is_255_shadow=False))


def calc_non_zero_rate(arr):
    is0 = np.where(arr == 0, 1, 0)
    canvas = np.ones(arr.shape)
    return 1 - np.sum(is0) / np.sum(canvas)


def is_almost_square(arr):
    x_size = arr.shape[0]
    y_size = arr.shape[1]
    return (x_size / y_size) > 0.95 and (x_size / y_size) < 1.05


def get_same_base_name(path_name, new_dir_name, prefix='', replace_before=None, replace_after=None):
    assert (replace_before is None and replace_after is None) or (replace_before is not None and replace_after is not None)
    if replace_before is None and replace_after is None:
        return os.path.join(new_dir_name, f'{prefix}{os.path.basename(path_name)}')
    else:
        return os.path.join(new_dir_name, f'{prefix}{os.path.basename(path_name).replace(replace_before, replace_after)}')