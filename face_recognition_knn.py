import testMySQLshow
import testMySQLcreatenewaccount
import testMySQLaddvalue
import math
from sklearn import neighbors
import os
import os.path
import pickle
from PIL import Image, ImageDraw
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import cv2
import time

cap=cv2.VideoCapture(0)  #抓取攝影機
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'PNG', 'JPG', 'JPEG'}
def train(train_dir, model_save_path=None, n_neighbors=None, knn_algo='ball_tree', verbose=False):  #訓練
    X = []
    y = []
    # Loop through each person in the training set
    for class_dir in os.listdir(train_dir):
        if not os.path.isdir(os.path.join(train_dir, class_dir)):
            continue
        # Loop through each training image for the current person
        for img_path in image_files_in_folder(os.path.join(train_dir, class_dir)):
            image = face_recognition.load_image_file(img_path)
            face_bounding_boxes = face_recognition.face_locations(image)
            if len(face_bounding_boxes) != 1:
                # If there are no people (or too many people) in a training image, skip the image.
                if verbose:
                    print("Image {} not suitable for training: {}".format(img_path, "Didn't find a face" if len(face_bounding_boxes) < 1 else "Found more than one face"))
            else:
                # Add face encoding for current image to the training set
                X.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0])
                y.append(class_dir)

    # Determine how many neighbors to use for weighting in the KNN classifier
    if n_neighbors is None:
        n_neighbors = int(round(math.sqrt(len(X))))
        if verbose:
            print("Chose n_neighbors automatically:", n_neighbors)

    # Create and train the KNN classifier
    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
    knn_clf.fit(X, y)

    # Save the trained KNN classifier
    if model_save_path is not None:
        with open(model_save_path, 'wb') as f:
            pickle.dump(knn_clf, f)

    return knn_clf


def predict(X_img_path, knn_clf=None, model_path=None, distance_threshold=0.35):  #偵測

    if not os.path.isfile(X_img_path) or os.path.splitext(X_img_path)[1][1:] not in ALLOWED_EXTENSIONS:
        raise Exception("Invalid image path: {}".format(X_img_path))

    if knn_clf is None and model_path is None:
        raise Exception("Must supply knn classifier either thourgh knn_clf or model_path")

    # Load a trained KNN model (if one was passed in)
    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)

    # Load image file and find face locations
    X_img = face_recognition.load_image_file(X_img_path)
    X_face_locations = face_recognition.face_locations(X_img)

    # If no faces are found in the image, return an empty result.
    if len(X_face_locations) == 0:
        return []

    # Find encodings for faces in the test iamge
    faces_encodings = face_recognition.face_encodings(X_img, known_face_locations=X_face_locations)

    # Use the KNN model to find the best matches for the test face
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]

    # Predict classes and remove classifications that aren't within the threshold
    return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]

"""
def show_prediction_labels_on_image(img_path, predictions):

    pil_image = Image.open(img_path).convert("RGB")
    draw = ImageDraw.Draw(pil_image)

    for name, (top, right, bottom, left) in predictions:
        # Draw a box around the face using the Pillow module
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

        # There's a bug in Pillow where it blows up with non-UTF-8 text
        # when using the default bitmap font
        name = name.encode("UTF-8")

        # Draw a label with a name below the face
        text_width, text_height = draw.textsize(name)
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
        draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))

    # Remove the drawing library from memory as per the Pillow docs
    del draw

    # Display the resulting image
    pil_image.save("/face/save/{}".format(image_file))
"""
if __name__ == "__main__":
    os.system("sudo rm -r /face/train/*")
    while True:
        k=0
        g=0
        w=0
        for image_file in os.listdir("/face/test"):  #偵測目前會員有幾位(k)
            k+=1
        ret, frame=cap.read()  #從攝影機擷取一張影像
        cv2.imshow('Webcam',frame)   #顯示影像
        d=cv2.waitKey(10)  #等待按鍵事件
        if d==97:  #按下鍵盤a，進行拍攝
            os.system('sudo mkdir /face/train/{}'.format(k+1)) #建立暫存顧客的照片資料夾
            for i in range(1,6): #連續拍5張照片
                cv2.imwrite('/face/train/{}/{}.jpg'.format(k+1, i), frame)
                ret, frame=cap.read()
                cv2.imshow('Webcam',frame)
            print("Training KNN classifier...")
            classifier = train("/face/train", model_save_path="trained_knn_model.clf", n_neighbors=2)
            print("Training complete!")
            for image_file in os.listdir("/face/test"):
                full_file_path = os.path.join("/face/test", image_file))
                predictions = predict(full_file_path, model_path="trained_knn_model.clf")
                for name, (top, right, bottom, left) in predictions: #
                    if name=="unknown":  #是否辨識到會員
                        g+=1
                    else:
                        name=("{}".format(image_file)) #抓取照片名稱
                        name=name.replace('.jpg','')  #副檔名去掉
                        testMySQLshow.name(name)  #顯示會員資料
                        testMySQLaddvalue.name(name)  #新增購買商品
                        os.system("sudo rm -r /face/train/{}".format(k+1))  #刪除暫存照片
                        w=1
                        break
                    if g==k:   #如果表示true，就表示此顧客並非是會員
                        print("Have not account!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                        ans=raw_input("Do you want add new account?(y/n)")
                        if ans=='y': #輸入y，建立會員，並將顧客照片丟到會員照片區，之後刪除暫存照片
                            testMySQLcreatenewaccount.name(k+1)
                            os.system("sudo cp /face/train/{}/1.jpg /face/test/{}.jpg".format(k+1,k+1))
                            os.system("sudo rm -r /face/train/{}".format(k+1))
                            w=1
                        elif ans=='n':  #輸入n，刪除暫存照片
                            os.system("sudo rm -r /face/train/{}".format(k+1))
                            w=1
                if w==1:  #當w是1時，表示結束，跳出
                    break
            print("finish!!!!!!!!!!!!!!!!!!!!!!")
        elif d==113: #按下q，結束程式
            break
cap.release()  #釋放攝影機
cv2.destroyAllWindows()  #關閉所有OpenCV視窗
