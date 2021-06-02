#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
import bcapclient
import cv2
from cv_bridge import CvBridge
from datetime import datetime
import numpy as np
import time
import rospy
from sensor_msgs.msg import Image

from canon_camera.srv import CanonImage, CanonImageRequest, CanonImageResponse

DATA_PATH = '../data'


class ControlCanonCamera():

    client = None
    robot_handler = None
    camera_handler = None
    variable_handler = None

    def __init__(self, hz=1.0, save_image=False):
        # b-CAP Client
        self.client = bcapclient.BCAPClient(host='133.11.216.228',
                                            port=5007,
                                            timeout=1000)

        # b-CAP client start
        self.client.service_start()
        
        # Get Robot Handler
        self.robot_handler = self.client.controller_connect(
            '',
            'CaoProv.DENSO.VRC',
            'localhost', '')
        rospy.loginfo('Robot handler is {}'.format(self.robot_handler))

        # Get Camera Handler
        self.camera_handler = self.client.controller_connect(
            'N10-W02',
            'CaoProv.Canon.N10-W02',
            '',
            'Conn=eth:133.11.216.229, Timeout=3000')
        rospy.loginfo('Camera handler is {}'.format(self.camera_handler))
        self.hz = hz
        self.save_image = save_image
        rospy.loginfo('Setting hz {}'.format(self.hz))
        self.image_pub = rospy.Publisher('~rgb', Image, queue_size=10)
        if self.variable_handler is None:
            self.variable_handler = self.client.controller_getvariable(
                self.camera_handler,
                'IMAGE')
        print('IMAGE handler is {}.'.format(self.variable_handler))

    def run(self):
        r = rospy.Rate(self.hz)  # 10hz
        while not rospy.is_shutdown():
            image = self.get_image()
            self.image_pub.publish(image)
            r.sleep()

    def get_image(self):
        '''撮影し、イメージを獲得する
        '''
        # OneShot
        self.client.controller_execute(
            self.camera_handler, 'OneShotFocus', '')   # 0.06
        # Add variable(101)
        image_buff = self.client.variable_getvalue(
            self.variable_handler)   # around 1.2s
        # convert image(btyes) to numpy and save it
        nparr = np.frombuffer(image_buff, dtype=np.uint8)
        cv_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if self.save_image:
            cv2.imwrite(DATA_PATH + '/' + str(datetime.now()) + '.jpg', cv_image)
        # to send image to other node, convert 'cv2.image' to 'sensor.msgs.Image' which is ROS image format
        bridge = CvBridge()
        image_message = bridge.cv2_to_imgmsg(cv_image, encoding="passthrough")

        return image_message

    def release_all_controller(self):
        '''ロボットとカメラのコントローラをリリースする
        '''

        self.client.controller_disconnect(self.robot_handler)
        self.client.controller_disconnect(self.camera_handler)
        
        return None

# def get_image_func():
#     '''撮影し、イメージを獲得する関数
#     クラスを作成する前に作ったやつでね…
#     '''
        
#     # b-CAP Client 
#     client = bcapclient.BCAPClient(host='192.168.0.1', port=5007, timeout=1000)

#     # b-CAP client start
#     client.service_start()
    
#     # Get Robot Handler
#     robot_handler = client.controller_connect('', 'CaoProv.DENSO.VRC', 'localhost', '')
#     print 'Robot handler is {}.'.format(robot_handler)

#     # Get Camera Handler
#     camera_handler = client.controller_connect('N10-W02', 'CaoProv.Canon.N10-W02', '', 'Conn=eth:192.168.0.90, Timeout=3000')
#     print 'Camera handler is {}.'.format(camera_handler)
#     # OneShot
#     client.controller_execute(camera_handler, 'OneShotFocus', '')

#     # Get Variable ID
#     variable_handler = client.controller_getvariable(camera_handler, 'IMAGE')
#     print('IMAGE handler is {}.'.format(variable_handler))

#     # Add variable(101)
#     image_buff = client.variable_getvalue(variable_handler)

#     # convert image(btyes) to numpy and show it
#     nparr = np.frombuffer(image_buff , dtype=np.uint8)
#     cv_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#     cv2.imwrite(DATA_PATH + '/' + str(datetime.now()) + '.jpg', cv_image)

#     # convert cv2 image to sensor.msgs.Image which is ROS image format
#     bridge = CvBridge()
#     print 'bridge success'
#     image_message = bridge.cv2_to_imgmsg(cv_image, encoding="passthrough")
#     print 'convert success'

#     # cv_image = cv2.resize(cv_image, (0,0), fx=0.5, fy=0.5) 
#     # cv2.imshow('image',  cv_image)
#     # cv2.waitKey(0)

#     return image_message

def main():

    rospy.init_node('camera_server') # 任意のノード名を作成

    camera_node = ControlCanonCamera()
    camera_node.run()
    


if __name__ == "__main__":
    main()
