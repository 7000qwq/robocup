import os

import cv2
import requests

import face_module as fm


class Robocup():
    def __init__(self):
        self.f_access_token = self.get_token()
        self.face_to_register_list = []
        self.name_of_face_list = []
        self.origin_pics_list = []  # 原图
        self.item_labelled_pics_list = []  # 被yolov7标记物品的图
        self.face_item_labelled_pics_list = []  # olov7标记物品，百度api标记人脸的图
        self.results_face_detect_list = []

    def register_face(self):
        for i in range(len(self.face_to_register_list)):
            fm.face_registration(self.face_to_register_list[i], self.name_of_face_list[i], self.f_access_token)

    def read_pics(self):
        path_face_to_register = os.listdir('./face_to_register/')  # 得到文件夹下的所有文件名称，存在字符串列表中
        path_origin_pics = os.listdir('./origin_pics/')  # 得到文件夹下的所有文件名称，存在字符串列表中
        for path_face in path_face_to_register:
            self.face_to_register_list.append(
                cv2.imread('./face_to_register_list/' + path_face))  # 把每一张待注册的人脸图片读到face_to_register列表中
            self.name_of_face_list.append(path_face.split('.')[0])  # 把每一张待注册的人脸图片的名字读到name_of_face列表中
        for path_origin_pic in path_origin_pics:
            self.origin_pics_list.append(cv2.imread('./origin_pics_list/' + path_origin_pic))  # 把每一张原图读到origin_pics列表中

    def detect_items(self):
        os.system(
            'python ./yolov7-main-master/detect.py')

    def detect_faces(self):
        for i in range(len(self.origin_pics_list)):
            self.results_face_detect_list.append(
                fm.face_detect(self.origin_pics_list[i], self.f_access_token)['result']['face_list'])

    def label_faces(self):
        for i in range(len(self.origin_pics_list)):
            self.face_item_labelled_pics_list.append(
                fm.face_label(self.origin_pics_list[i], self.item_labelled_pics_list[i],
                              self.results_face_detect_list[i]))

    def save_results(self):
        for i in range(len(self.face_item_labelled_pics_list)):
            cv2.imwrite('./results/' + str(i) + '.jpg', self.face_item_labelled_pics_list[i])

    def get_token(self):
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=KuM5BbQrM9RppkwN5eyEKutg&client_secret=oW3KlZSpx5voOFg4p2BWNxjRy0lGNmEB'

        response = requests.get(host)
        if response:
            print(response.json())
            return str(response.json()['access_token'])

if __name__ == "__main__":
    robocup = Robocup()
    robocup.read_pics()
    robocup.register_face()
    robocup.detect_items()
    robocup.detect_faces()
    robocup.label_faces()
    robocup.save_results()
