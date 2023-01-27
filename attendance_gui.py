from tkinter import *
root= Tk()
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime



root.geometry("800x800")

root.title("Facial Recognition Attendance System")



def recognises():
    import cv2
    import numpy as np
    import face_recognition
    import os
    from datetime import datetime

    path = 'imageSet'
    images = []
    classNames = []
    myList = os.listdir(path)
    print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)

    def findEncodings(images):
        encodeList =[]
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    def markAttendance(name):
        # f = open('Attendance.txt', 'r+')
        # with open('Attendance.txt', 'r+') as f:
        # with f:
        f = open(r'Attendance.txt','r+')
        myDataList = f.readlines()
        nameList = []
        # for line in myDataList:
        #     entry = line.split(',')
        #     nameList.append(entry[0])
        # if name not in nameList:
        #     time_now = datetime.now()
        #     tString = time_now.strftime('%H:%M:%S')
        #     dString = time_now.strftime('%d/%m/%Y')
        #     f.writelines(f'\n{name},{tString},{dString}')
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            time_now = datetime.now()
            tString = time_now.strftime('%H:%M:%S')
            dString = time_now.strftime('%d/%m/%Y')
            f.writelines(f'\n{name},{tString},{dString}')
        print('mark attendance is working')




    encodeListKnown = findEncodings(images)
    print('Encoding Complete')

    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            print(faceDis)
            matchIndex = np.argmin(faceDis)
            print('match index is ',matchIndex)
            if matches[matchIndex]:
                print(faceDis[matchIndex],' matchindex lowest')
                if faceDis[matchIndex] <0.5:
                    name = classNames[matchIndex].upper()
                    print(name)
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 250, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    markAttendance(name)
            else:
                txt = 'Not Recognised'
                cv2.putText(img, txt, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            # markAttendance(name)
            
            
        cv2.imshow('webcam', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


# def capture(new_name):
#     cam = cv2.VideoCapture(0)
#     while True:
#         result,image = cam.read()
#         image = cv2.flip(image,1)
#         cv2.imshow("Capture image",image)
#         directory =r'D:\code\projects\attendance\imageSet'
#         os.chdir(directory)
#         # filename_1 = ()
#         filename = 'f{new_new}.jpg'            
#         cv2.putText(image,"Press q to capture",(10,100),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),3)
#         # if cv2.waitKey(1) and 0xFF == ord('s'):
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             # name = "{}.png".format(new_name)
#             cv2.imwrite(filename,image)
#             cv2.putText(image,"Image Captured \nPress q to quit",(10,10),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,0),3)
#             break
#     cam.release()

def take_image():
    def capture():
        cam = cv2.VideoCapture(0)
        while True:
            result,image = cam.read()
            image = cv2.flip(image,1)
            cv2.imshow("Capture image",image)
            directory =r'D:\code\projects\attendance\imageSet'
            os.chdir(directory)
            file_1 = new_name.get()
            filename = f"{file_1}.jpg"           
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.imwrite(filename,image)
                break
        cam.release()
    new_name = StringVar()
    b=Entry(root,textvariable=new_name)
    b.place(x=50,y=300)
    canvas.create_text(100,275,text="Enter Name", fill="black", font=('Helvetica 12 bold'))
    Button(text="  ok   ",font="comicsans 8 bold",bg="yellow",padx=30,command=capture).place(x=200,y=300)
    
def delete_user():
    def deleted():
        c_1 = deleted_user.get()
        c = f"{c_1}.jpg"
        os.remove(r'D:\code\projects\attendance\imageSet\{}'.format(c))
    deleted_user = StringVar()
    d=Entry(root,textvariable=deleted_user)
    d.place(x=50,y=450)
    canvas.create_text(150,430,text="Enter user name to delete",fill="black",font=('Helvetica 12 bold'))
    Button(text="  ok   ",font="comicsans 8 bold",bg="yellow",padx=30,command=deleted).place(x=200,y=450)

def data():
    def check_pass():
        default_pass = "attendance" 
        p_1 = password.get()
        if p_1 == default_pass:
            os.startfile("Attendance.txt")
        else:
            canvas.create_text(100,680,text="Incorrect !",fill="black",font=('Helvetica 12 bold'))


        pass
    
    canvas.create_text(110,585,text="Enter password",fill="black",font=('Helvetica 12 bold'))
    password = StringVar()
    Entry(root,textvariable=password).place(x=50,y=600)
    Button(text="  ok   ",font="comicsans 8 bold",bg="yellow",padx=30,command=check_pass).place(x=200,y=600)


    
    

# Button(text=" ").grid(row=0,column=0)
canvas= Canvas(root, width= 800, height= 800)
canvas.place(x=0,y=0)
Button(text=" Mark Your Attendance",font="comicsans 12 bold",bg="yellow",padx=20,pady=10,command=recognises).place(x=50,y=50)
Button(text="   Register new face   ",font="comicsans 12 bold",bg="yellow",padx=30,pady=10,command=take_image).place(x=50,y=200)
Button(text="   Derigister user     ",font="comicsans 12 bold",bg="yellow",padx=37,pady=10,command=delete_user).place(x=50,y=350)
Button(text="View Attendance data",font="comicsans 12 bold",bg="yellow",padx=30,pady=10,command=data).place(x=50,y=500)

root.mainloop()