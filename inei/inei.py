from logging import getLogger

logger = getLogger(__name__)

if __name__ == '__main__':
    import cv2
    input_filename = '/path/to/Screenshot.png'
    # pngじゃないとだめ
    output_filename = ''
    bgr = cv2.imread(input_filename)
    b = bgr[:,:,0:1]
    g = bgr[:,:,1:2]
    r = bgr[:,:,2:]
    import numpy as np
    mask_b = np.where(b > 127, 0, 255).astype(np.uint8)
    mask_g = np.where(g > 127, 0, 255).astype(np.uint8)
    mask_r = np.where(r > 127, 0, 255).astype(np.uint8)
    b = np.zeros(b.shape).astype(np.uint8)
    g = np.zeros(g.shape).astype(np.uint8)
    bgra = cv2.merge([b,g,r+(200-r).astype(np.uint8),mask_g])
    # bgra = cv2.merge([b,g,(mask_g*0.7).astype(np.uint8),mask_g])
    cv2.imwrite(output_filename, bgra)

    # 結果確認用
    import matplotlib.pyplot as plt
    # th1 = cv2.adaptiveThreshold(b, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
    #                             cv2.THRESH_BINARY, 11, 2)
    # th2 = cv2.adaptiveThreshold(g, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
    #                             cv2.THRESH_BINARY, 11, 2)
    # # th3 = cv2.adaptiveThreshold(r, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
    # #                             cv2.THRESH_BINARY, 11, 2)
    # blur = cv2.GaussianBlur(r, (3, 3), 0)
    # ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    titles = ['Original Image', 'Global Thresholding (v = 127)',
              'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
    images = [bgr,mask_b[:,:,0],mask_g[:,:,0],mask_r[:,:,0]]

    for i in range(4):
        plt.subplot(2, 2, i + 1), plt.imshow(images[i], 'gray')
        plt.title(titles[i])
        plt.xticks([]), plt.yticks([])
    plt.show()
    pass
