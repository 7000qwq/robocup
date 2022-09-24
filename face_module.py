# encoding:utf-8

import base64
import math

import cv2
import requests


# client_id 为官网获取的AK， client_secret 为官网获取的SK
def get_token():
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + f_client_id + '&client_secret=' + f_client_secret
    response = requests.get(host)
    if response:
        return str(response.json()['access_token'])


def cv2_base64(image):
    base64_str = cv2.imencode('.jpg', image)[1].tobytes()
    base64_str = base64.b64encode(base64_str)
    return base64_str


def face_search(cut, f_access_token):
    # 人脸搜索
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/search"
    cut_base64 = cv2_base64(cut)
    newparams = {"image": cut_base64, "image_type": "BASE64", "group_id_list": "robocup"}
    request_url = request_url + "?access_token=" + f_access_token
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=newparams, headers=headers)
    if response:
        return response.json()


def face_find(cut, f_access_token):
    # 人脸查找，若有结果返回1
    face_result = face_search(cut, f_access_token)
    try:
        for face in face_result['result']['user_list']:
            if face['score'] > 70:
                return face['user_id']
    except:
        pass
    return 0


def face_registration(cut, new_name, f_access_token):
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


def face_detect(pic, f_access_token):
    #   人脸检测与属性分析
    pic = cv2_base64(pic)
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"

    newparams = {"image": pic, "image_type": "BASE64", "max_face_num": 10, "face_field": "gender,quality"}

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

    w = int(frame.shape[0])  # 截取长
    h = int(frame.shape[1])  # 图片的高
    top = max(0, top)
    height = min(height, top + h)
    left = max(0, left)
    width = min(width, left + w)

    cut = frame[top:top + height, left:left + width]
    return cut


def piant_individual(individual, frame):
    # 在frame上绘制矩形
    top = math.floor(individual['location']['top'])
    height = math.floor(individual['location']['height'])
    width = math.floor(individual['location']['width'])
    left = math.floor(individual['location']['left'])

    w = int(frame.shape[0])  # 截取长
    h = int(frame.shape[1])  # 图片的高
    top = max(0, top)
    height = min(height, top + h)
    left = max(0, left)
    width = min(width, left + w)

    frame = cv2.rectangle(frame, (left, top), (left + width, top + height), (0, 255, 255), 2)
    return frame


def face_label(origin_pic, item_labelled_pic, result):
    if result['quality']['completeness'] == 1:  # 检测到的人脸质量正常
        cut = cut_individual(result, origin_pic)
        user_id = face_find(cut)
        if user_id != 0:  # 人脸库中有这张脸 需要框起来然后标注
            frame = piant_individual(result, item_labelled_pic)
            cv2.putText(frame, str(user_id) + str(' ') + str(result['gender']['type']),
                        (int(result['location']['left']), int(result['location']['top'])),
                        cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
    return frame


if __name__ == '__main__':  # 这句话是为了在别的py程序import的时候不执行

    relist = getPhoto_one()
    for picpa in relist:
        path = r"C:\\Users\\7000qwq\\Desktop\\testimage\\re\\" + picpa
        img = cv2.imread(path)
        new_name = picpa[:-4]
        face_registration(img, new_name)

    telist = getPhoto_two()
    for picpa in telist:
        try:
            path = r"C:\\Users\\7000qwq\\Desktop\\testimage\\de\\" + picpa
            img = cv2.imread(path)
            frame = img  # frame是画了框的图 原图是img
            detect_res = face_detect(img)
            print("人脸检测：")
            print(detect_res)
            if detect_res['error_code'] != 0:
                print(detect_res['error_msg'])

            else:
                for face in detect_res['result']['face_list']:
                    if face['quality']['completeness'] == 1:  # 检测到的人脸质量正常   and face_module['quality']['blur'] <= 1

                        cut = cut_individual(face, img)
                        user_id = face_find(cut)
                        if user_id != 0:  # 人脸库中有这张脸 需要框起来然后标注

                            frame = piant_individual(face, frame)
                            #  frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            cv2.putText(frame, str(user_id) + str(' ') + str(face['gender']['type']),
                                        (int(face['location']['left']), int(face['location']['top'])),
                                        cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
                            cv2.namedWindow('myPicture', 0)
                            cv2.imshow('myPicture', frame)
                            cv2.waitKey()
                            cv2.destroyWindow('myPicture')

            cv2.imwrite(picpa + "_face.jpg", frame)  # 保存图片
        except:
            continue
