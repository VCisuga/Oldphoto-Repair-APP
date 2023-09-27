import sys
import requests,base64
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtGui
from qt_material import apply_stylesheet

import warnings
warnings.filterwarnings("ignore")

def GetAccessToeken(APIKEY, SECRETKEY):
    token_host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={ak}&client_secret={sk}'.format(
        ak=APIKEY, sk=SECRETKEY)
    header = {'Content-Type': 'application/json; charset=UTF-8'}
    response = requests.post(url=token_host, headers=header)
    content = response.json()
    access_token = content.get("access_token")
    return access_token

def Reimg(img_path, i):
    APIKEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXX'
    SECRETKEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXX'
    request_url1 = 'https://aip.baidubce.com/rest/2.0/image-process/v1/image_definition_enhance'  # 清晰度
    request_url2 = 'https://aip.baidubce.com/rest/2.0/image-process/v1/colourize'  # 黑白图像上色
    request_url3 = ' https://aip.baidubce.com/rest/2.0/image-process/v1/stretch_restore'  # 拉伸图像恢复
    request_url4 = 'https://aip.baidubce.com/rest/2.0/image-process/v1/denoise'  # 画像去噪
    request_url5 = 'https://aip.baidubce.com/rest/2.0/image-process/v1/color_enhance'  # 色彩增强
    request_url = {1: request_url1, 2: request_url2, 3: request_url3, 4: request_url4, 5: request_url5}
    access_token = GetAccessToeken(APIKEY, SECRETKEY)
    if type(img_path) == type('a'):
        picture1 = open(img_path, 'rb')
        img_base1 = base64.b64encode(picture1.read()).decode()
    else:
        img_base1 = base64.b64encode(img_path).decode()
    datamsg = {"image": img_base1}
    request_url[i] = request_url[i] + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url[i], data=datamsg, headers=headers)

    if response:
        ans = response.json()
        imgData = base64.b64decode(ans['image'])  # 将二进制数据转换为图像
            #     leniyimg = open('./Repair.jpg', 'wb')
            #     leniyimg.write(imgData)
            #     leniyimg.close()
        return imgData
 
class picture(QWidget):
    def __init__(self):
        super(picture, self).__init__()

        self.setWindowIcon(QtGui.QIcon('logo.png'))

        self.setWindowTitle("旧照片重塑")
        self.resize(970, 900)

        self.key = 0
        self.imgData = ''

        self.pix = QtGui.QPixmap('./logo2.png')
        self.label1 = QLabel(self)
        self.label1.setFixedSize(160, 160)  # 设置标签大小
        self.label1.move(355, 15)  # 设置位置
        self.label1.setPixmap(self.pix)
        self.label1.setScaledContents(True)  # 自适应QLabel大小

        self.label = QLabel(self)
        self.label.setFixedSize(600, 500)  # 设置标签大小
        self.label.move(40, 180)  # 设置位置
        pixmap = QtGui.QPixmap('老照片.jpg')  # 加载图像
        ratio = min(self.label.width() / pixmap.width(), self.label.height() / pixmap.height())
        self.scaled_pixmap = pixmap.scaled(pixmap.width() * ratio, pixmap.height() * ratio)  # 缩放图像
        self.label.setPixmap(self.scaled_pixmap)  # 设置背景

        self.label2 = QLabel(self)
        self.label2.setFixedSize(600, 500)  # 设置标签大小
        self.label2.move(500, 180)  # 设置位置
        pixmap2 = QtGui.QPixmap('Repair1.jpg')  # 加载图像
        ratio2 = min(self.label2.width() / pixmap2.width(), self.label2.height() / pixmap2.height())
        self.scaled_pixmap2 = pixmap2.scaled(pixmap2.width() * ratio2, pixmap2.height() * ratio2)  # 缩放图像
        self.label2.setPixmap(self.scaled_pixmap2)  # 设置背景

        self.label3 = QLabel(self)
        self.label3.setFixedSize(500, 30)  # 设置标签大小
        self.label3.move(560, 730)  # 设置位置

        self.label4 = QLabel(self)
        self.label4.setFixedSize(300, 20)  # 设置标签大小
        self.label4.setText('示例图片来源于网络 仅用于效果展示 侵权立删')
        self.label4.move(40, 860)  # 设置位置
 
        btn = QPushButton(self)
        btn.setText("上传图片")
        btn.move(40, 800)
        btn.clicked.connect(self.openimage)

        btn1 = QPushButton(self)
        btn1.setText("恢复清晰度")
        btn1.move(170, 800)
        btn1.clicked.connect(self.repair_qx)

        # btn2 = QPushButton(self)
        # btn2.setText("图像修复")
        # btn2.move(460, 800)
        # btn2.clicked.connect(self.repair_xf)

        btn2 = QPushButton(self)
        btn2.setText("图像着色")
        btn2.move(300, 800)
        btn2.clicked.connect(self.repair_zs)

        btn3 = QPushButton(self)
        btn3.setText("修复图像比例")
        btn3.move(430, 800)
        btn3.clicked.connect(self.repair_ls)

        btn4 = QPushButton(self)
        btn4.setText("图像去噪")
        btn4.move(580, 800)
        btn4.clicked.connect(self.repair_qz)

        btn5 = QPushButton(self)
        btn5.setText("图像色彩增强")
        btn5.move(710, 800)
        btn5.clicked.connect(self.repair_zq)

        btn6 = QPushButton(self)
        btn6.setText("智能优化")
        btn6.move(865, 800)
        btn6.clicked.connect(self.repair_AI)

        btn_one = QPushButton(self)
        btn_one.setText("老照片1")
        btn_one.move(40, 730)
        btn_one.clicked.connect(self.open_one)

        btn_two = QPushButton(self)
        btn_two.setText("老照片2")
        btn_two.move(170, 730)
        btn_two.clicked.connect(self.open_two)

        btn_th = QPushButton(self)
        btn_th.setText("老照片3")
        btn_th.move(300, 730)
        btn_th.clicked.connect(self.open_th)

        btn_save = QPushButton(self)
        btn_save.setText("保存图片")
        btn_save.move(430, 730)
        btn_save.clicked.connect(self.save_img)

    def resizeEvent(self, event):
        # 当窗口大小变化时，重新计算并缩放图像
        ratio = min(self.label.width() / self.scaled_pixmap.width(), self.label.height() / self.scaled_pixmap.height())
        scaled_pixmap = self.scaled_pixmap.scaled(self.scaled_pixmap.width() * ratio,
                                                  self.scaled_pixmap.height() * ratio)
        self.label.setPixmap(scaled_pixmap)  # 设置缩放后的图像

    def openimage(self):
        try:
            self.key = 3
            global imgName
            imgName, imgType = QFileDialog.getOpenFileName(self, "上传图片", "", "*.jpg;;*.png;;All Files(*)")
            pixmap = QtGui.QPixmap(imgName)  # 加载图像
            ratio = min(self.label.width() / pixmap.width(), self.label.height() / pixmap.height())
            self.scaled_pixmap = pixmap.scaled(pixmap.width() * ratio, pixmap.height() * ratio)  # 缩放图像
            self.label.setPixmap(self.scaled_pixmap)  # 设置背景

            if self.scaled_pixmap.width() < self.scaled_pixmap.height():
                self.resize(970, 900)
                self.label1.move(360, 15)  # 设置位置
                self.label2.move(500, 180)  # 设置位置
            else:
                self.resize(1360, 900)
                self.label1.move(585, 15)  # 设置位置
                self.label2.move(700, 180)  # 设置位置
            self.label2.setText('等待处理..............')
            self.label3.setText('成功接收到图像 请继续操作')
        except:
            pass

    def repair(self, i):
        try:
            if self.key == 0:
                self.imgData = Reimg('./Repair1.jpg', i)
            elif self.key == 1:
                self.imgData = Reimg('./Repair2.jpg', i)
            elif self.key == 2:
                self.imgData = Reimg('./Repair3.jpg', i)
            elif self.key == 3:
                self.imgData = Reimg(imgName, i)
            else:
                self.imgData = Reimg(self.imgData, i)
            self.key = 4
            print(self.key)
            pixmap2 = QtGui.QPixmap()
            pixmap2.loadFromData(self.imgData)
            ratio2 = min(self.label2.width() / pixmap2.width(), self.label2.height() / pixmap2.height())
            self.scaled_pixmap2 = pixmap2.scaled(pixmap2.width() * ratio2, pixmap2.height() * ratio2)  # 缩放图像
            self.label2.setPixmap(self.scaled_pixmap2)  # 设置背景
        except:
            pass

    def repair_qx(self):
        self.repair(1)
        self.label3.setText('图像清晰度修复完成')

    def repair_zs(self):
        self.repair(2)
        self.label3.setText('图像着色完成')

    def repair_ls(self):
        self.repair(3)
        self.label3.setText('图像恢复原比例完成')

    def repair_qz(self):
        self.repair(4)
        self.label3.setText('图像去噪完成')

    def repair_zq(self):
        self.repair(5)
        self.label3.setText('图像色彩增强完成')

    def repair_AI(self):
        for k in range(1,5):
            self.repair(k)
        self.label3.setText('智能优化完成')

    def open_one(self):
        self.key = 0
        pixmap = QtGui.QPixmap('./老照片.jpg')  # 加载图像
        ratio = min(self.label.width() / pixmap.width(), self.label.height() / pixmap.height())
        self.scaled_pixmap = pixmap.scaled(pixmap.width() * ratio, pixmap.height() * ratio)  # 缩放图像
        self.label.setPixmap(self.scaled_pixmap)  # 设置背景

        pixmap2 = QtGui.QPixmap('./Repair1.jpg')  # 加载图像
        ratio2 = min(self.label2.width() / pixmap2.width(), self.label2.height() / pixmap2.height())
        self.scaled_pixmap2 = pixmap2.scaled(pixmap2.width() * ratio2, pixmap2.height() * ratio2)  # 缩放图像
        self.label2.setPixmap(self.scaled_pixmap2)  # 设置背景

        if self.scaled_pixmap.width() < self.scaled_pixmap.height():
            self.resize(970, 900)
            self.label1.move(360, 15)  # 设置位置
            self.label2.move(500, 180)  # 设置位置

        self.label3.setText('示例图片切换为老照片1 图像着色效果演示')

    def open_two(self):
        self.key = 1
        pixmap = QtGui.QPixmap('./老照片2.jpg')  # 加载图像
        ratio = min(self.label.width() / pixmap.width(), self.label.height() / pixmap.height())
        self.scaled_pixmap = pixmap.scaled(pixmap.width() * ratio, pixmap.height() * ratio)  # 缩放图像
        self.label.setPixmap(self.scaled_pixmap)  # 设置背景

        pixmap2 = QtGui.QPixmap('./Repair2.jpg')  # 加载图像
        ratio2 = min(self.label2.width() / pixmap2.width(), self.label2.height() / pixmap2.height())
        self.scaled_pixmap2 = pixmap2.scaled(pixmap2.width() * ratio2, pixmap2.height() * ratio2)  # 缩放图像
        self.label2.setPixmap(self.scaled_pixmap2)  # 设置背景

        if self.scaled_pixmap.width() < self.scaled_pixmap.height():
            self.resize(970, 900)
            self.label1.move(360, 15)  # 设置位置
            self.label2.move(500, 180)  # 设置位置

        self.label3.setText('示例图片切换为老照片2 图像着色效果演示')

    def open_th(self):
        self.key = 2
        pixmap = QtGui.QPixmap('./老照片3.png')  # 加载图像
        ratio = min(self.label.width() / pixmap.width(), self.label.height() / pixmap.height())
        self.scaled_pixmap = pixmap.scaled(pixmap.width() * ratio, pixmap.height() * ratio)  # 缩放图像
        self.label.setPixmap(self.scaled_pixmap)  # 设置背景

        pixmap2 = QtGui.QPixmap('./Repair3.jpg')  # 加载图像
        ratio2 = min(self.label2.width() / pixmap2.width(), self.label2.height() / pixmap2.height())
        self.scaled_pixmap2 = pixmap2.scaled(pixmap2.width() * ratio2, pixmap2.height() * ratio2)  # 缩放图像
        self.label2.setPixmap(self.scaled_pixmap2)  # 设置背景

        if self.scaled_pixmap.width() >= self.scaled_pixmap.height():
            self.resize(1360, 900)
            self.label1.move(585, 15)  # 设置位置
            self.label2.move(700, 180)  # 设置位置

        self.label3.setText('示例图片切换为老照片3 图像着色效果演示')

    def save_img(self):
        if len(self.imgData) != 0:
            leniyimg = open('Repair.jpg', 'wb')
            leniyimg.write(self.imgData)
            leniyimg.close()
            self.label3.setText("保存成名为'Repair'的jpg图像")
        else:
            self.label3.setText("保存失败，请重新操作")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_blue.xml', invert_secondary=True)
    my = picture()
    my.show()
    sys.exit(app.exec_())
