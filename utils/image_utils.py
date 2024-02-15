from logging import getLogger
import os

import cv2
import numpy as np
from tqdm import tqdm

logger = getLogger(__name__)



def nor_to_img(nor_arr):
    return ((nor_arr + 1) / 2 * 255).astype(np.uint8)


def calc_log2_ratio(arr_a, arr_b):
    a_bit = 10e-6
    return np.log2((arr_b + a_bit) / (arr_a + a_bit))


def get_blob(img_src, is_gray=False):
    '''
    blobを返す
    :return:
    '''
    if not is_gray:
        img_src = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)
    img_src = np.where(img_src == 255, 255, 0).astype(np.uint8)
    n, label = cv2.connectedComponents(img_src)
    return n, label


def find_contour(blobs):
    ret, thresh = cv2.threshold(blobs, 127, 255, 0)
    return cv2.findContours(thresh, 1, cv2.CHAIN_APPROX_NONE)


def get_biggest_blob(blobs):
    '''
    一番大きなBlobの領域とその重心座標を返す
    '''
    contours, hierarchy = find_contour(blobs)

    area_list = []
    for i in range(len(contours)):
        cnt = contours[i]
        area = cv2.contourArea(cnt)
        area_list.append(area)

    cnt_max = contours[int(np.argmax(area_list))]
    try:
        M = cv2.moments(cnt_max)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
    except:
    # 一番大きなBlobの面積が極小ピクセルだった場合
        cx = int(cnt_max[0][0][0])
        cy = int(cnt_max[0][0][1])

    cleansed_src = np.zeros(blobs.shape).astype(np.uint8)
    cv2.fillConvexPoly(cleansed_src, cnt_max, 255)
    return cleansed_src.astype(np.uint8), (cx, cy)

def count_contour(blobs, is_small_delete=False, size=0):
    contours, hierarchy = find_contour(blobs)
    count = 0
    for contour in contours:
        if is_small_delete:
            if len(contour) > size:
                count += 1
        else:
            count += 1
    return count


def blob_mean(vals, n, label):
    '''
    blobごとに平均をとる
    :param vals:
    :param blobs:
    :return:
    '''
    height_src = np.zeros(vals.shape)
    for i in tqdm(range(n)):
        one_roof = np.where(label == i, 1, 0)
        one_val = vals * one_roof
        one_mean = np.sum(one_val) / np.sum(one_roof)
        height_src += one_roof * one_mean
    return height_src


def blob_zero(vals, n, label, m=0):
    '''
    値mのblobをフィルタする
    :param vals:
    :param blobs:
    :return:
    '''
    filtered_src = np.zeros(vals.shape)
    for i in range(n):
        one_roof = np.where(label == i, 1, 0)
        one_val = vals * one_roof
        one_mean = np.sum(one_val) / np.sum(one_roof)
        if one_mean == m:
            filtered_src += one_roof
    return filtered_src


def blob_mean_threshold(vals, n, label, threshold):
    '''
    blobごとに平均をとり閾値より高ければTrueを返す
    :param vals:
    :param blobs:
    :return:
    '''
    bool_src = np.zeros(vals.shape)
    for i in range(n):
        one_roof = np.where(label == i, 1, 0)
        one_val = vals * one_roof
        one_mean = np.sum(one_val) / np.sum(one_roof)
        if one_mean > threshold:
            bool_src += one_roof
    return bool_src


def blob_small_delete_threshold(vals, n, label, threshold, is_gray=True):
    '''
    blobごとに面積を算出し、閾値以下を消す
    :param vals:
    :param blobs:
    :return:
    '''
    if not is_gray:
        vals = cv2.cvtColor(vals, cv2.COLOR_BGR2GRAY)

    rt_src = np.zeros(vals.shape)

    for i in range(n):
        one_roof = np.where(label == i, 1, 0)
        one_val = vals * one_roof
        one_area = np.sum(one_roof)
        if one_area > threshold:
            rt_src += one_val
    return rt_src


def polylines_blob(img, blobs, color_tuple, line_width=1, is_small_delete=False, size=0):
    contours, hierarchy = find_contour(blobs)
    if is_small_delete:
        for contour in contours:
            if len(contour) > size:
                img = cv2.drawContours(img, [contour], -1, color_tuple, line_width)
    else:
        img = cv2.drawContours(img, contours, -1, color_tuple, line_width)
    return img


def rotate_image(image, angle, center=None):
    if center is None:
        center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(center, angle, 1.0)
    # rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result


if __name__ == '__main__':
    src_path = '/mnt/data/dataset/satellite/osaka/80_plan_b/31_shp_tile/14_osaka_v2_a/000000_000001.png'
    src = cv2.imread(src_path)
    n, label = get_blob(src, is_gray=False)
    src_deleted = blob_small_delete_threshold(src, n, label, 1000, is_gray=False)
    cv2.imwrite('./temp.png', src_deleted)


def img_to_8bit(arr, verbose=False):
    if verbose:
        print(arr.max())
        print(arr.min())

    arr = np.clip(arr, 0, 1) * 255
    arr_r = arr[:, :, 0:1]
    arr_g = arr[:, :, 1:2]
    arr_b = arr[:, :, 2:]
    arr = np.concatenate([arr_b, arr_g, arr_r], axis=2)
    return arr.astype(np.uint8)


def z_to_8bit(arr, threshold=8, verbose=False):
    if verbose:
        print(arr.max())
        print(arr.min())

    arr_noinf = np.where(arr == np.inf, threshold, arr)
    arr = (arr_noinf - arr_noinf.min()) / (arr_noinf.max() - arr_noinf.min()) * 255
    arr_r = arr[:, :, 0:1]
    arr_g = arr[:, :, 1:2]
    arr_b = arr[:, :, 2:]
    arr = np.concatenate([arr_b, arr_g, arr_r], axis=2)
    return arr.astype(np.uint8)


def add_margin(img, w_size, h_size):
    num_channel = img.shape[2]
    h, w = img.shape[:2]  # 画像の大きさ
    tmp = img[:, :]
    size_h = h + w + (256 - (h+w) % h_size)
    size_w = h + w + (256 - (h+w) % w_size)

    start_h = int((size_h - h) / 2)
    end_h = int((size_h + h) / 2)
    start_w = int((size_w - w) / 2)
    end_w = int((size_w + w) / 2)

    new_img = cv2.resize(np.zeros((1, 1, num_channel)), (size_h, size_w))
    new_img[start_h: end_h, start_w: end_w] = tmp
    return new_img, h, w, size_h, size_w


def add_margin_canvas(img, w_size, h_size):
    h, w = img.shape[:2]  # 画像の大きさ
    tmp = img[:, :]

    size_h = h + h_size*2
    size_w = w + w_size*2
    start_h = int((size_h - h) / 2)
    end_h = int((size_h + h) / 2)
    start_w = int((size_w - w) / 2)
    end_w = int((size_w + w) / 2)

    new_img = cv2.resize(np.zeros((1, 1)), (size_h, size_w))
    new_img[start_h: end_h, start_w: end_w] = tmp
    return new_img


def add_margin_binary(img, w_size, h_size):
    if len(img.shape) == 3:
        num_channel = img.shape[2]
    else:
        num_channel = 1
    h, w = img.shape[:2]  # 画像の大きさ
    size_h = h + w + (256 - (h+w) % h_size)
    size_w = h + w + (256 - (h+w) % w_size)

    start_h = int((size_h - h) / 2)
    end_h = int((size_h + h) / 2)
    start_w = int((size_w - w) / 2)
    end_w = int((size_w + w) / 2)

    new_img = cv2.resize(np.zeros((1, 1, num_channel), dtype=np.uint8), (size_h, size_w))
    new_img[start_h: end_h, start_w: end_w] = img
    return new_img, h, w, size_h, size_w


def rotate_img(img, az):
    # 高さを定義
    height = img.shape[0]
    # 幅を定義
    width = img.shape[1]
    # 回転の中心を指定
    center = (int(width / 2), int(height / 2))
    # 回転角を指定
    angle = az
    # スケールを指定
    scale = 1.0
    # getRotationMatrix2D関数を使用
    trans = cv2.getRotationMatrix2D(center, angle, scale)
    # アフィン変換
    return cv2.warpAffine(img, trans, (width, height))


def split_img(img, vsize, hsize, w_offset=0, h_offset=0):
    h, w = img.shape[:2]  # 画像の大きさ
    w = w - w_offset
    h = h - h_offset
    img = img[h_offset:, w_offset:]
    num_vsplits, num_hsplits = np.floor_divide([h, w], [vsize, hsize])  # 分割数
    crop_img = img[:num_vsplits * vsize, :num_hsplits * hsize]

    print('{} -> {}'.format(img.shape, crop_img.shape))
    # 分割する。
    out_imgs = []
    for h_idx, h_img in enumerate(np.vsplit(crop_img, num_vsplits)):  # 垂直方向に分割する。
        out_imgs_v = []
        for v_idx, v_img in enumerate(np.hsplit(h_img, num_hsplits)):  # 水平方向に分割する。
            out_imgs_v.append(v_img)
        out_imgs.append(out_imgs_v)

    out_imgs = np.array(out_imgs)
    print(out_imgs.shape)
    return out_imgs



def normalize_all_npy(arr_path_list, b_mean_shift, g_mean_shift, r_mean_shift,
                      b_std_shift, g_std_shift, r_std_shift,
                      is_mask_applied=False, arr_mask_path_list=None,
                      is_save=False, bgr_nor_save_dir=None, hsv_nor_save_dir=None,
                      verbose=False, val_factor=1, min_val=-1, max_val=1):
    if is_mask_applied:
        assert arr_mask_path_list is not None

    b_means = []
    g_means = []
    r_means = []

    b_stds = []
    g_stds = []
    r_stds = []

    for idx, from_item in enumerate(tqdm(arr_path_list)):

        bgr = np.load(from_item)
        if is_mask_applied:
            mask_path = arr_mask_path_list[idx]
            mask_bgr = np.load(mask_path)

        bgr = bgr.astype(np.float32) / val_factor
        bgr_normalized = normalize_bgr(bgr,
                                       b_mean_shift, g_mean_shift, r_mean_shift,
                                       b_std_shift, g_std_shift, r_std_shift, min_val, max_val)

        b = bgr_normalized[:, :, 0]
        g = bgr_normalized[:, :, 1]
        r = bgr_normalized[:, :, 2]

        b_means.append(np.mean(b))
        g_means.append(np.mean(g))
        r_means.append(np.mean(r))
        b_stds.append(np.std(b))
        g_stds.append(np.std(g))
        r_stds.append(np.std(r))

        hsv_final = remap_bgr_to_hsv(bgr_normalized)

        # 保存
        if is_save:
            assert bgr_nor_save_dir is not None
            assert hsv_nor_save_dir is not None
            save_path_nor = os.path.join(bgr_nor_save_dir, os.path.basename(from_item).replace('.png', '.npy'))
            save_path_hsv = os.path.join(hsv_nor_save_dir, os.path.basename(from_item).replace('.png', '.npy'))
            np.save(save_path_nor, bgr_normalized)
            np.save(save_path_hsv, hsv_final)

    return calc_mean_std(b_means, g_means, r_means,
                         b_stds, g_stds, r_stds,
                         verbose=verbose)

def normalize_bgr(bgr,
                  b_mean_shift, g_mean_shift, r_mean_shift,
                  b_std_shift, g_std_shift, r_std_shift, min_val=-1, max_val=1):
    b = bgr[:, :, 0:1]
    g = bgr[:, :, 1:2]
    r = bgr[:, :, 2:]

    b = normalize_one_channel(b, b_mean_shift, b_std_shift)
    g = normalize_one_channel(g, g_mean_shift, g_std_shift)
    r = normalize_one_channel(r, r_mean_shift, r_std_shift)

    bgr_after = np.concatenate([b, g, r], axis=2)
    return np.clip(bgr_after, min_val, max_val)


def normalize_one_channel(arr, mean_shift, std_shift):
    arr = np.array(arr).astype(np.float32)
    arr = arr * std_shift
    arr = arr + mean_shift
    return arr


def remap_bgr_to_hsv(bgr_normalized):
    hsv = cv2.cvtColor(((bgr_normalized + 1) * 128).astype(np.uint8), cv2.COLOR_BGR2HSV)
    h = hsv[:, :, 0:1]
    s = hsv[:, :, 1:2]
    v = hsv[:, :, 2:]

    h = remap(h)
    s = remap(s)
    v = remap(v)

    return np.concatenate([h, s, v], axis=2)


def remap(arr):
    arr = arr - arr.min()
    arr = arr / arr.max()
    arr = (arr * 2) - 1
    return arr


def calc_mean_std(b_means, g_means, r_means,
                  b_stds, g_stds, r_stds, verbose=False):
    if verbose:
        print('\t b_mean=', np.mean(b_means))
        print('\t g_mean=', np.mean(g_means))
        print('\t r_mean=', np.mean(r_means))

        print('\t b_std=', np.mean(b_stds))
        print('\t g_std=', np.mean(g_stds))
        print('\t r_std=', np.mean(r_stds))

    return np.mean(b_means), np.mean(g_means), np.mean(r_means), np.mean(b_stds), np.mean(g_stds), np.mean(r_stds)


def concat_tile(im_list_2d):
    # todo ゼロ画像パディングの仕組みとかいれたら？
    return cv2.vconcat([cv2.hconcat([img.astype(np.uint8) for img in im_list_h]) for im_list_h in im_list_2d])


def get_mean_std_shift_val(out_imgs, mean_after_val=0, std_after_val=40 / 256):
    std_b = np.std(out_imgs[:, :, :, 0:1])
    std_g = np.std(out_imgs[:, :, :, 1:2])
    std_r = np.std(out_imgs[:, :, :, 2:])

    std_shift_b = std_after_val / std_b
    std_shift_g = std_after_val / std_g
    std_shift_r = std_after_val / std_r

    out_imgs_b = out_imgs[:, :, :, 0:1] * std_shift_b
    out_imgs_g = out_imgs[:, :, :, 1:2] * std_shift_g
    out_imgs_r = out_imgs[:, :, :, 2:] * std_shift_r

    mean_b = np.mean(out_imgs_b)
    mean_g = np.mean(out_imgs_g)
    mean_r = np.mean(out_imgs_r)

    mean_shift_b = mean_after_val - mean_b
    mean_shift_g = mean_after_val - mean_g
    mean_shift_r = mean_after_val - mean_r

    return mean_shift_b, mean_shift_g, mean_shift_r, std_shift_b, std_shift_g, std_shift_r


def normalize_imgs(out_imgs,
                   mean_shift_b, mean_shift_g, mean_shift_r,
                   std_shift_b, std_shift_g, std_shift_r):
    b = out_imgs[:, :, :, 0:1]
    g = out_imgs[:, :, :, 1:2]
    r = out_imgs[:, :, :, 2:3]

    b = std_shift_b * b
    g = std_shift_g * g
    r = std_shift_r * r

    b = mean_shift_b + b
    g = mean_shift_g + g
    r = mean_shift_r + r

    return np.concatenate([b, g, r], axis=3)
