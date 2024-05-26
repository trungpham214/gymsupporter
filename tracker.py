from abc import abstractmethod
import cv2
import mediapipe as mp
import numpy as np

#angle calculation
def get_coordinates(landmarks, joint_coords):
    coordinate = []
    for i in joint_coords:
        coordinate.append([landmarks[i].x,landmarks[i].y])
    return coordinate

def get_angle(coordinates):
    a = np.array(coordinates[0])
    b = np.array(coordinates[1])
    c = np.array(coordinates[2])

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle > 180.0:
        angle = 360-angle

    return angle

def get_joint(joint):
    return {
        'bicep':[11, 13, 15],
        'shoulder': [23, 11, 13]
    }[joint]

class Tracker:
    def __init__(self, exercise) -> None:
        self.exercise = exercise
        self.angle = 0
        self.counter = 0
        self.run = False
        self.stage = ""

    @abstractmethod
    def set_counter(self):
        pass

    def main(self) -> None:
        if self.run:
            mp_drawing = mp.solutions.drawing_utils
            mp_pose = mp.solutions.pose

            vid = cv2.VideoCapture(0)
            width  = vid.get(cv2.CAP_PROP_FRAME_WIDTH)   # float `width`
            height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height`

            with mp_pose.Pose() as pose:
                while vid.isOpened():
                    ret, frame = vid.read()

                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image.flags.writeable = False

                    results = pose.process(image)

                    image.flags.writeable = True
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                    try:
                        landmarks = results.pose_landmarks.landmark

                        coordinate = get_coordinates(landmarks, get_joint(self.exercise))
                        self.angle = get_angle(coordinate).astype(int)

                        # cv2.putText(image, str(self.angle), tuple(np.multiply(coordinate[1], [width, height]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)
                            
                        # Curl counter logic
                        if self.angle > 160:
                            self.stage = "down"
                        if self.angle < 30 and self.stage =='down':
                            self.stage="up"
                            self.counter +=1
                            print(self.counter)        

                    except:
                        pass


                    #drawing landmarks
                    # mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)           


                    # cv2.imshow('Tracker', image)

                    # if cv2.waitKey(10) & 0xFF == ord('q'):
                    #     break

                    if not self.run:
                        # print("finished")
                        break

            vid.release()
            cv2.destroyAllWindows()

    def switch_state(self):
        if self.run:
            self.counter = 0
        self.run = not self.run

