#!/usr/bin/env python
#encoding: utf8
import rospy, cv2, math
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class FaceToFace():
    def __init__(self):
        sub = rospy.Subscriber("/cv_camera/image_raw", Image, self.get_image)
        self.pub = rospy.Publisher("face", Image, queue_size=1)
        self.bridge = CvBridge()
        self.image_org = None

    def monitor(self,rect,org):                                 #このメソッドを追加
        if rect is not None:
            cv2.rectangle(org,tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]),(0,255,255),4)
       
        self.pub.publish(self.bridge.cv2_to_imgmsg(org, "bgr8"))
   
    def get_image(self,img):
        try:
            self.image_org = self.bridge.imgmsg_to_cv2(img, "bgr8")
        except CvBridgeError as e:
            rospy.logerr(e)

    def detect_face(self):
        if self.image_org is None:
            return None
    
        org = self.image_org
    
        gimg = cv2.cvtColor(org,cv2.COLOR_BGR2GRAY)
        classifier = "/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml"
        cascade = cv2.CascadeClassifier(classifier)
        face = cascade.detectMultiScale(gimg,1.1,1,cv2.CASCADE_FIND_BIGGEST_OBJECT)
    
        if len(face) == 0:    #len(face)...以下を次のように書き換え
            self.monitor(None,org)
            return None       
                              
        r = face[0]           
        self.monitor(r,org)   
        return r  

    def pic(self):
        r = self.detect_face()
        if r is None:
            return 0.0
	
	x = r[2]
	y = r[3]
	area = abs(x*y)
	
	img = self.image_org
	
	if area <= 30000:
	   cv2.imwrite("/tmp/image.jpg",img)
           rospy.loginfo("Take a picture!!!")
	if area >= 30000:
	   rospy.loginfo("離れて")	


if __name__ == '__main__':
    rospy.init_node('face_to_face')
    fd = FaceToFace()

    rate = rospy.Rate(30)
    while not rospy.is_shutdown():
        rospy.loginfo(fd.detect_face())
        rospy.loginfo(fd.pic())
        rate.sleep()

# Copyright 2016 Ryuichi Ueda
# Released under the MIT License.
# To make line numbers be identical with the book, this statement is written here. Don't move it to the header.
