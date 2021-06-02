#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import keras?\
import cv2
import numpy as np
from math import sqrt, ceil, floor

IMAGE_PATH = '../data/images'
MODEL_PATH = '../models'


class ImageProcessing():

    def __init__(self):

        self.image = None

        return None

    def read_image(self, file_path):
        '''画像を読み込む
        '''
        self.image = cv2.imread(file_path)
        return None

    def set_image(self, image):
        '''画像をセットする
        '''
        self.image = image
        return None

    def thresholding(self, auto=None, threshold=100):
        '''画像を2値化する
        '''

        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        if auto:
            ret, image = cv2.threshold(image, 0, 255, cv2.THRESH_OTSU)
        else:
            ret, image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)

        return image

    def laplacian(self, ddepth=0):
        ''' エッジ検出のLaplacianフィルタ処理
        ddepth: 出力画像のビット震度
        '''
        # image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        image = cv2.Laplacian(self.image, ddepth)
        return image

    def sobel(self, ddepth=0, dx=0, dy=1):
        ''' エッジ検出のSobelフィルタ処理
        ddepth = 0 #  出力画像のビット震度
        dx = 0 # x方向の微分次数
        dy = 1 # y方向の微分次数
        '''
        image = cv2.Sobel(self.image, ddepth, dx, dy)
        return image

    def canny(self, threshold1 = 40., threshold2 = 200.):
        '''エッジ検出のCannyフィルタ処理
        '''
        image = cv2.Canny(self.image, threshold1, threshold2)
        return image

    def detect_face(self):
        '''入力画像の顔を検知して、ボックスで囲う。
        return image
        '''
        cascade_file = MODEL_PATH + '/haarcascade_frontalface_alt2.xml'
        if cascade_file is None:
            print('Reading model error. Please check model file path.'  )
        cascade_face = cv2.CascadeClassifier(cascade_file)

        # 顔を探して配列で返す
        face_list = cascade_face.detectMultiScale(image, minSize=(20, 20))
        for (x, y, w, h) in face_list:
            border_color = (0, 0, 255)
            border_size = 2
            cv2.rectangle(image, (x, y), (x+w, y+h), border_color, thickness=border_size)
        
        return image

    def show_image(self, winname, image):
        '''imageオブジェクトを表示する
        '''
        cv2.imshow(winname, image)
        print('Press any key')
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return None

    def resize(self, image, scale_percent=100):
        '''画像をリサイズする
        スケールは%形式
        '''
        width = int(img.shape[1] * scale / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        # resize image
        resize_image = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        return resize_image

    def resize_abs(self, imgae, windows_width, window_height):
        width_scale_percent = windows_width / imgae.shape[1] * 100
        height_scale_percent =  window_height / image.shape[0] * 100

        if width_scale_percent > height_scale_percent:
            return self.resize(image, width_scale_percent)
        else:
            return self.resize(image, height_scale_percent)

    def save_image(self, file, image):
        '''imageを保存する
        ディレクトリは事前に指定している
        '''
        cv2.imwrite(IMAGE_PATH + '/' + file + '.jpg', image)
        return None
    
    def save_multi_images(self, images_dict):
        for key in images_dict.keys():
            self.save_image(key, images_dict[key])

if __name__ == "__main__":
    cp = ImageProcessing()
    cp.read_image('../data/images/pen.bmp')

    # multi_savingの練習
    # lap_image = cp.laplacian()
    # sobel_image = cp.sobel()
    # cannny_image = cp.canny()
    # images_dict = {'lap_image': lap_image, 'sobel_image': sobel_image, 'canny_image': cannny_image}
    # cp.save_multi_images(images_dict)

    threshol_image = cp.thresholding(threshold=50)
    cp.show_image('a', threshol_image)