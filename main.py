import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
import cv2
import math as m
import mediapipe as mp
from playsound import playsound

def findDistance(x1, y1, x2, y2):
    dist = m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist

def findAngle(x1, y1, x2, y2):
    ang = m.degrees(m.atan2(y1-y2, x1-x2) - m.atan2(y1-y2, x2-x2))
    return abs(ang)

font = cv2.FONT_HERSHEY_SIMPLEX

dark_red = (127, 25, 25)
dark_green = (50, 121, 63)
dark_brown = (91, 77, 42)
brown = (182, 154, 84)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

global sv
sv = 0
global ex
ex = 0
global axer
axer = 0
global bxer
bxer = 0
global cxer
cxer = 0

class Dialog(QWidget):
    def __init__(self):
        super(Dialog, self).__init__()
        self.resize(600, 100)
        self.setWindowTitle('Choose an exercise:')
        p = QPalette()
        gradient = QLinearGradient(0, 0, 400, 400)
        gradient.setColorAt(0.2, QColor(16, 62, 56))
        gradient.setColorAt(0.8, QColor(15, 27, 33))
        p.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(p)

        self.gridLayout = QGridLayout()
        self.horizontalLayout = QHBoxLayout()

        self.aBTN = QPushButton()
        self.aBTN.setIcon(QIcon('axer.jpg'))
        self.aBTN.setIconSize(QSize(100, 100))
        self.aBTN.setStyleSheet('background-color:rgb(255, 255, 255); color:rgb(182, 154, 84); border-style:outset; border-width:3px; border-color:rgb(182, 154, 84)')
        self.aBTN.clicked.connect(self.Axercise)

        self.bBTN = QPushButton()
        self.bBTN.setIcon(QIcon('bxer.jpg'))
        self.bBTN.setIconSize(QSize(100, 100))
        self.bBTN.setStyleSheet('background-color:rgb(255, 255, 255); color:rgb(182, 154, 84); border-style:outset; border-width:3px; border-color:rgb(182, 154, 84)')
        self.bBTN.clicked.connect(self.Bxercise)

        self.cBTN = QPushButton()
        self.cBTN.setIcon(QIcon('cxer.jpg'))
        self.cBTN.setIconSize(QSize(100, 100))
        self.cBTN.setStyleSheet('background-color:rgb(255, 255, 255); color:rgb(182, 154, 84); border-style:outset; border-width:3px; border-color:rgb(182, 154, 84)')
        self.cBTN.clicked.connect(self.Cxercise)

        self.horizontalLayout.addWidget(self.aBTN)
        self.horizontalLayout.addWidget(self.bBTN)
        self.horizontalLayout.addWidget(self.cBTN)

        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.setLayout(self.gridLayout)
    
    def Axercise(self):
        global axer
        axer = 1
        global bxer
        bxer = 0
        global cxer
        cxer = 0
        self.close()

    def Bxercise(self):
        global axer
        axer = 0
        global bxer
        bxer = 1
        global cxer
        cxer = 0
        self.close()

    def Cxercise(self):
        global axer
        axer = 0
        global bxer
        bxer = 0
        global cxer
        cxer = 1
        self.close()

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(1280, 720)
        self.setWindowTitle('Posture')
        p = QPalette()
        gradient = QLinearGradient(0, 0, 400, 400)
        gradient.setColorAt(0.2, QColor(16, 62, 56))
        gradient.setColorAt(0.8, QColor(15, 27, 33))
        p.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(p)

        self.gridLayout = QGridLayout()
        self.verticalLayout = QVBoxLayout()
        self.horizontalLayout = QHBoxLayout()
        self.verticalLayout_2 = QVBoxLayout()

        self.StreamLBL = QLabel('Connecting to the webcam...')
        self.StreamLBL.setMaximumWidth(640)
        self.StreamLBL.setMaximumHeight(480)
        self.StreamLBL.setFont(QFont('Century Gothic', 18))
        self.StreamLBL.setStyleSheet('color:rgb(182, 154, 84); border-style:outset; border-width:3px; border-color:rgb(182, 154, 84)')
        self.StreamLBL.setAlignment(Qt.AlignCenter)

        self.SuperviseBTN = QPushButton('Posture Supervising')
        self.SuperviseBTN.setFont(QFont('Century Gothic', 18))
        self.SuperviseBTN.setStyleSheet('color:rgb(182, 154, 84); border-style:outset; border-width:3px; border-color:rgb(182, 154, 84)')
        self.SuperviseBTN.clicked.connect(self.Supervising)

        self.ExerciseBTN = QPushButton('Exercising')
        self.ExerciseBTN.setFont(QFont('Century Gothic', 18))
        self.ExerciseBTN.setStyleSheet('color:rgb(182, 154, 84); border-style:outset; border-width:3px; border-color:rgb(182, 154, 84)')
        self.ExerciseBTN.clicked.connect(self.Exercising)

        self.StopBTN = QPushButton('Stop')
        self.StopBTN.setFont(QFont('Century Gothic', 18))
        self.StopBTN.setStyleSheet('color:rgb(182, 154, 84); border-style:outset; border-width:3px; border-color:rgb(182, 154, 84)')
        self.StopBTN.clicked.connect(self.Stop)

        self.verticalLayout_2.addWidget(self.SuperviseBTN)
        self.verticalLayout_2.addWidget(self.ExerciseBTN)
        self.verticalLayout_2.addWidget(self.StopBTN)

        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout.addWidget(self.StreamLBL)
        
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.Thread = Thread()
        self.Thread.ImageUpdate.connect(self.ImageUpdateSlot)

        self.setLayout(self.gridLayout)
        self.Thread.start()

    def ImageUpdateSlot(self, Image):
        self.StreamLBL.setPixmap(QPixmap.fromImage(Image))

    def Supervising(self):
        global sv
        sv = 1
        global ex
        ex = 0

    def Exercising(self):
        global sv
        sv = 0
        global ex
        ex = 1
        global reps
        reps = 0
        self.Dialog = Dialog()
        self.Dialog.show()

    def Stop(self):
        global sv
        sv = 0
        global ex
        ex = 0
        global axer
        axer = 0
        global bxer
        bxer = 0
        global cxer
        cxer = 0

class Thread(QThread):
    ImageUpdate = pyqtSignal(QImage)
    def run(self):
        self.ThreadActive = True
        cap = cv2.VideoCapture(0)
        good_frames = 0
        bad_frames = 0
        best_time = 0
        reps = 0
        repeat = 0
        while self.ThreadActive:
            success, Image = cap.read()
            if success:
                Image = cv2.flip(Image, 1)
                Image = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)
                
                if sv == 1 or ex == 1:
                    fps = cap.get(cv2.CAP_PROP_FPS)
                    h, w = Image.shape[:2]

                    keypoints = pose.process(Image)

                    lm = keypoints.pose_landmarks
                    lmPose = mp_pose.PoseLandmark

                    if lm != None:
                        l_shldr_x = int(lm.landmark[lmPose.LEFT_SHOULDER].x * w)
                        l_shldr_y = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h)
                        r_shldr_x = int(lm.landmark[lmPose.RIGHT_SHOULDER].x * w)
                        r_shldr_y = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)

                        l_ear_x = int(lm.landmark[lmPose.LEFT_EAR].x * w)
                        l_ear_y = int(lm.landmark[lmPose.LEFT_EAR].y * h)
                        r_ear_x = int(lm.landmark[lmPose.RIGHT_EAR].x * w)
                        r_ear_y = int(lm.landmark[lmPose.RIGHT_EAR].y * h)

                        c_shldr_x = int((l_shldr_x + r_shldr_x) / 2)
                        c_shldr_y = int((l_shldr_y + r_shldr_y) / 2)
                        c_ear_x = int((l_ear_x + r_ear_x) / 2)
                        c_ear_y = int((l_ear_y + r_ear_y) / 2)

                        cv2.line(Image, (l_shldr_x, l_shldr_y), (r_shldr_x, r_shldr_y), brown, 4)
                        cv2.line(Image, (l_ear_x, l_ear_y), (r_ear_x, r_ear_y), brown, 4)
                        cv2.line(Image, (c_shldr_x, c_shldr_y), (c_ear_x, c_ear_y), brown, 4)

                        cv2.circle(Image, (l_shldr_x, l_shldr_y), 7, dark_brown, -1)
                        cv2.circle(Image, (r_shldr_x, r_shldr_y), 7, dark_brown, -1)

                        cv2.circle(Image, (l_ear_x, l_ear_y), 7, dark_brown, -1)
                        cv2.circle(Image, (r_ear_x, r_ear_y), 7, dark_brown, -1)


                if sv == 1:
                    if lm != None:
                        rotation = findDistance(l_shldr_x, l_shldr_y, r_shldr_x, r_shldr_y)

                        if rotation > 150:
                            cv2.putText(Image, 'Turn Sideways!', (10, 30), font, 1, dark_red, 2)

                        neck_angle = findAngle(c_shldr_x, c_shldr_y, c_ear_x, c_ear_y)

                        if neck_angle <= 15 and rotation <= 150:
                            bad_frames = 0
                            good_frames += 1
                            angle_text_string = 'Neck Angle: ' + str(int(neck_angle)) 
                            cv2.putText(Image, angle_text_string, (10, 30), font, 1, dark_green, 2)

                        elif neck_angle > 15 and rotation <= 150:
                            bad_frames += 1
                            good_frames = 0
                            angle_text_string = 'Neck Angle: ' + str(int(neck_angle)) 
                            cv2.putText(Image, angle_text_string, (10, 30), font, 1, dark_red, 2)

                    good_time = (1 / fps) * good_frames
                    bad_time =  (1 / fps) * bad_frames
                    
                    if good_time > best_time:
                        best_time = good_time

                    time_string_best = 'Best Time: ' + str(round(best_time, 1)) + 's'
                    cv2.putText(Image, time_string_best, (w - 280, h - 10), font, 1, dark_green, 2)

                    if good_time > 0:
                        time_string_good = 'Good Posture: ' + str(round(good_time, 1)) + 's'
                        cv2.putText(Image, time_string_good, (10, h - 10), font, 1, dark_green, 2)
                    else:
                        time_string_bad = 'Bad Posture: ' + str(round(bad_time, 1)) + 's'
                        cv2.putText(Image, time_string_bad, (10, h - 10), font, 1, dark_red, 2)

                    if bad_time > 2:
                        playsound('C:/posture/fail.mp3')

                if ex == 1:
                    if lm != None:
                        l_hip_x = int(lm.landmark[lmPose.LEFT_HIP].x * w)
                        l_hip_y = int(lm.landmark[lmPose.LEFT_HIP].y * h)
                        r_hip_x = int(lm.landmark[lmPose.RIGHT_HIP].x * w)
                        r_hip_y = int(lm.landmark[lmPose.RIGHT_HIP].y * h)

                        l_knee_x = int(lm.landmark[lmPose.LEFT_KNEE].x * w)
                        l_knee_y = int(lm.landmark[lmPose.LEFT_KNEE].y * h)
                        r_knee_x = int(lm.landmark[lmPose.RIGHT_KNEE].x * w)
                        r_knee_y = int(lm.landmark[lmPose.RIGHT_KNEE].y * h)

                        l_ankle_x = int(lm.landmark[lmPose.LEFT_ANKLE].x * w)
                        l_ankle_y = int(lm.landmark[lmPose.LEFT_ANKLE].y * h)
                        r_ankle_x = int(lm.landmark[lmPose.RIGHT_ANKLE].x * w)
                        r_ankle_y = int(lm.landmark[lmPose.RIGHT_ANKLE].y * h)
                        
                        l_elbow_x = int(lm.landmark[lmPose.LEFT_ELBOW].x * w)
                        l_elbow_y = int(lm.landmark[lmPose.LEFT_ELBOW].y * h)
                        r_elbow_x = int(lm.landmark[lmPose.RIGHT_ELBOW].x * w)
                        r_elbow_y = int(lm.landmark[lmPose.RIGHT_ELBOW].y * h)

                        l_wrist_x = int(lm.landmark[lmPose.LEFT_WRIST].x * w)
                        l_wrist_y = int(lm.landmark[lmPose.LEFT_WRIST].y * h)
                        r_wrist_x = int(lm.landmark[lmPose.RIGHT_WRIST].x * w)
                        r_wrist_y = int(lm.landmark[lmPose.RIGHT_WRIST].y * h)

                        cv2.line(Image, (l_shldr_x, l_shldr_y), (l_hip_x, l_hip_y), brown, 4)
                        cv2.line(Image, (r_shldr_x, r_shldr_y), (r_hip_x, r_hip_y), brown, 4)
                        cv2.line(Image, (l_hip_x, l_hip_y), (r_hip_x, r_hip_y), brown, 4)
                        cv2.line(Image, (l_hip_x, l_hip_y), (l_knee_x, l_knee_y), brown, 4)
                        cv2.line(Image, (r_hip_x, r_hip_y), (r_knee_x, r_knee_y), brown, 4)
                        cv2.line(Image, (l_knee_x, l_knee_y), (l_ankle_x, l_ankle_y), brown, 4)
                        cv2.line(Image, (r_knee_x, r_knee_y), (r_ankle_x, r_ankle_y), brown, 4)
                        cv2.line(Image, (l_shldr_x, l_shldr_y), (l_elbow_x, l_elbow_y), brown, 4)
                        cv2.line(Image, (r_shldr_x, r_shldr_y), (r_elbow_x, r_elbow_y), brown, 4)
                        cv2.line(Image, (l_elbow_x, l_elbow_y), (l_wrist_x, l_wrist_y), brown, 4)
                        cv2.line(Image, (r_elbow_x, r_elbow_y), (r_wrist_x, r_wrist_y), brown, 4)

                        cv2.circle(Image, (l_shldr_x, l_shldr_y), 7, dark_brown, -1)
                        cv2.circle(Image, (r_shldr_x, r_shldr_y), 7, dark_brown, -1)

                        cv2.circle(Image, (l_ear_x, l_ear_y), 7, dark_brown, -1)
                        cv2.circle(Image, (r_ear_x, r_ear_y), 7, dark_brown, -1)

                        cv2.circle(Image, (l_hip_x, l_hip_y), 7, dark_brown, -1)
                        cv2.circle(Image, (r_hip_x, r_hip_y), 7, dark_brown, -1)

                        cv2.circle(Image, (l_knee_x, l_knee_y), 7, dark_brown, -1)
                        cv2.circle(Image, (r_knee_x, r_knee_y), 7, dark_brown, -1)

                        cv2.circle(Image, (l_elbow_x, l_elbow_y), 7, dark_brown, -1)
                        cv2.circle(Image, (r_elbow_x, r_elbow_y), 7, dark_brown, -1)

                        cv2.circle(Image, (l_wrist_x, l_wrist_y), 7, dark_brown, -1)
                        cv2.circle(Image, (r_wrist_x, r_wrist_y), 7, dark_brown, -1)

                        if axer == 1:
                            if ((l_knee_y - l_hip_y) <= 30 ) and ((r_knee_y - r_hip_y) <= 30 ) and (repeat == 0):
                                repeat = 1

                            if ((l_knee_y - l_hip_y) >= 100 ) and ((r_knee_y - r_hip_y) >= 100 ) and (repeat == 1):
                                reps += 1
                                repeat = 0

                        if bxer == 1:
                            if (l_ear_y > l_wrist_y) and (l_ear_y > l_elbow_y) and (l_ear_x < l_wrist_x) and (repeat == 0):
                                reps += 1
                                repeat = 1

                            if (r_ear_y > r_wrist_y) and (r_ear_y > r_elbow_y) and (r_ear_x < r_wrist_x) and (repeat == 1):
                                reps += 1
                                repeat = 0

                        if cxer == 1:
                            if (l_ear_x < r_hip_x) and (repeat == 0):
                                reps += 1
                                repeat = 1

                            if (r_ear_x > r_hip_x) and (repeat == 1):
                                reps += 1
                                repeat = 0

                    if reps < 10:
                        exercise_string = 'Reps done: ' + str(reps) + ' / 10'
                        cv2.putText(Image, exercise_string, (10, 30), font, 1, dark_green, 2)
                    else:
                        cv2.putText(Image, 'Good job!', (10, 30), font, 1, dark_green, 2)
                        if axer + bxer + cxer == 0:
                            reps = 0
                
                #Image = cv2.cvtColor(Image, cv2.COLOR_RGB2BGR)

                ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)

        cap.release()
        cv2.destroyAllWindows()

    def stop(self):
        self.ThreadActive = False
        self.quit()

if __name__ == "__main__":
    App = QApplication(sys.argv)
    Root = MainWindow()
    Root.show()
    sys.exit(App.exec())