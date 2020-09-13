from deepface import DeepFace
import cv2
import webbrowser
from youtubesearchpython import SearchVideos
import json
from random import randint

cam = cv2.VideoCapture(0)
cv2.namedWindow("frame")

img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("frame", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        #ESC was pressed
        print("Closing...")
        break
    elif k%256 == 32:
        #SPACE was pressed
        #images get saved to database, change if needed
        img_name = "../Database/img{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written". format(img_name))
        demography = DeepFace.analyze(img_name, actions = ['emotion'])
        emotion = demography["dominant_emotion"]
        print("Emotion: ", emotion)
        search = None

        #based on emotion detected random youtube video will be played
        #sad, fear emotion detected
        if emotion in ["sad", "fear"]:
            search = SearchVideos("sad music playlist", offset = 1, mode = "json", max_results = 20)
        #happy, surprise, neutral emotion detected
        elif emotion in ["happy", "surprise", "neutral"]:
            search = SearchVideos("happy music playlist", offset = 1, mode = "json", max_results = 20)
        #angry, disgust emotion detected
        elif emotion in ["angry", "disgust"]:
            search = SearchVideos("calm music playlist", offset = 1, mode = "json", max_results = 20)
        chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
        results = search.result()
        Y = json.loads(results)
        index = randint(0, 19)
        url = Y["search_result"][index]["link"]
        webbrowser.get(chrome_path).open(url)
        img_counter += 1
cam.release()
cv2.destroyAllWindows()
