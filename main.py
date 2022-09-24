# encoding:utf-8

import requests
import base64
import datetime
import operator
import os
import cv2
import math

# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=KuM5BbQrM9RppkwN5eyEKutg&client_secret=oW3KlZSpx5voOFg4p2BWNxjRy0lGNmEB'
response = requests.get(host)
if response:
    print(response.json())
    f_access_token = str(response.json()['access_token'])



def cv2_base64(image):
    base64_str = cv2.imencode('.jpg',image)[1].tobytes()
    base64_str = base64.b64encode(base64_str)
    return base64_str

def face_search(cut):
    # 人脸搜索
    # access_token1 = "24.5d7a52306b69800634cd64cc64f6f7c5.2592000.1646729435.282335-25559586"
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/search"
    cut_base64 = cv2_base64(cut)
    newparams = {"image": cut_base64, "image_type": "BASE64", "group_id_list": "robocup"}
    request_url = request_url + "?access_token=" + f_access_token
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=newparams, headers=headers)
    if response:
        return response.json()

def face_find(cut):
    # 人脸查找，若有结果返回1
    face_result = face_search(cut)
    print("人脸查找：")
    print(face_result)
    try:
        for face in face_result['result']['user_list']:
            if face['score'] > 70:
                print("人脸查找找到了：")
                print(face['user_id'])
                return face['user_id']
    except:
        pass
    return 0

def face_registration(cut, new_name):
    #  人脸注册
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add"
    cut_base64 = cv2_base64(cut)

    newparams = {"image": cut_base64, "image_type": "BASE64", "group_id": "robocup", "user_id": new_name}
    request_url = request_url + "?access_token=" + f_access_token
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=newparams, headers=headers)
    if response:
        print(response.json())
        return response.json()

def face_detect(pic):
    #   人脸检测与属性分析
    pic = cv2_base64(pic)
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"

    newparams = {"image": pic, "image_type":"BASE64", "max_face_num": 10, "face_field": "gender,quality"}

    request_url = request_url + "?access_token=" + f_access_token
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=newparams, headers=headers)
    if response:
        return (response.json())

def cut_individual(individual, frame):
    # 将origin按照多主体识别的结果切成一个个cut, 返回cut
    top = math.floor(individual['location']['top'])
    height = math.floor(individual['location']['height'])
    width = math.floor(individual['location']['width'])
    left = math.floor(individual['location']['left'])
    cut = frame[top:top+height, left:left+width]
    return cut

def piant_individual(individual, frame):
    # 在frame上绘制矩形
    top = math.floor(individual['location']['top'])
    height = math.floor(individual['location']['height'])
    width = math.floor(individual['location']['width'])
    left = math.floor(individual['location']['left'])
    frame = cv2.rectangle(frame, (left, top), (left + width, top + height), (0, 255, 255), 2)
    return frame



def getPhoto_one():
    path_photo = 'C:/Users/7000qwq/Desktop/testimage/re' # 所有photo所在的文件夹目录
    #
    files_list = os.listdir(path_photo) # 得到文件夹下的所有文件名称，存在字符串列表中
    #
    print(files_list) # 打印path_photo文件夹下的所有文件
    #

    return files_list


def getPhoto_two():
    path_photo = 'C:/Users/7000qwq/Desktop/testimage/de' # 所有photo所在的文件夹目录
    #
    files_list = os.listdir(path_photo) # 得到文件夹下的所有文件名称，存在字符串列表中
    #
    print(files_list) # 打印path_photo文件夹下的所有文件
    return files_list



#  if __name__ == '__main__':       #这句话是为了在别的py程序import的时候不执行


relist = getPhoto_one()
for picpa in relist:
    path = r"C:\\Users\\7000qwq\\Desktop\\testimage\\re\\" + picpa
    img = cv2.imread(path)
    new_name = picpa[:-4]
    face_registration(img, new_name)


telist = getPhoto_two()
for picpa in telist:
    path = r"C:\\Users\\7000qwq\\Desktop\\testimage\\de\\" + picpa
    img = cv2.imread(path)
    frame = img  # frame是画了框的图 原图是img
    detect_res = face_detect(img)
    print("人脸检测：")
    print( detect_res )
    if detect_res['error_code'] != 0:
        print(detect_res['error_msg'])

    else:
        for face in detect_res['result']['face_list']:
            if face['quality']['completeness'] == 1:     # 检测到的人脸质量正常   and face['quality']['blur'] <= 1

                cut = cut_individual(face, img)
                user_id = face_find(cut)
                if user_id != 0:  #  人脸库中有这张脸 需要框起来然后标注

                    frame = piant_individual(face, frame)
                    #  frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    cv2.putText(frame, str(user_id) + str(' ') + str(face['gender']['type']), (int(face['location']['left']), int(face['location']['top'])), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
                    cv2.namedWindow('myPicture', 0)
                    cv2.imshow('myPicture', frame)
                    cv2.waitKey()
                    cv2.destroyWindow('myPicture')

    cv2.imwrite(picpa + "_face.jpg", frame)  # 保存图片


