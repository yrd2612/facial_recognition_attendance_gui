import flet as ft
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime,date
from pathlib import Path
import time

def main(page:ft.Page):
    # page.window_max_width =500
    
    page.window_resizable = False
    page.window_height = 600
    page.window_width = 500
    page.title = "FacialRecognition Attendance System"
    img_folder = rf'{os.getcwd()}/imageSet_1'
    if not os.path.exists(img_folder):
        os.makedirs(img_folder)
    time_folder = rf'{os.getcwd()}/time'
    if not os.path.exists(time_folder):
        os.makedirs(time_folder)
    today = date.today()
    today = str(today)
    attendance_file = Path(rf'{os.getcwd()}/time/{today}.txt')
    if attendance_file.is_file():
        pass
    else:
        f = open(rf"{attendance_file}", "x")

    '''
    ///////

    mark attendance

    ///////

    '''
    def recognises(e):
        
        path = img_folder
        images = []
        classNames = []
        myList = os.listdir(f'{path}')
        for cl in myList:
            curImg = cv2.imread(f'{path}/{cl}')
            images.append(curImg)
            classNames.append(os.path.splitext(cl)[0])
        def findEncodings(images):
            encodeList =[]
            for img in images:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)
            return encodeList

        def markAttendance(name):  
            f = open(rf'{time_folder}\{today}.txt','r+')      
            myDataList = f.readlines()
            nameList = []       
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])
            if name not in nameList:
                time_now = datetime.now()
                tString = time_now.strftime('%H:%M:%S')
                dString = time_now.strftime('%d/%m/%Y')
                f.writelines(f'\n{name},{tString},{dString}')

        encodeListKnown = findEncodings(images)
        # print('Encoding Complete')

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
                matchIndex = np.argmin(faceDis)
                if matches[matchIndex]:
                    if faceDis[matchIndex] <0.5:
                        name = classNames[matchIndex].upper()
                        y1, x2, y2, x1 = faceLoc
                        y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 250, 0), cv2.FILLED)
                        cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                        markAttendance(name)
                else:
                    txt = 'Not Recognised'
                    cv2.putText(img, txt, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                
                
            cv2.imshow('webcam', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
    '''
    //////////////

    register new user

    /////////////
    '''
    def take_image(f):
        # page.update()        
        def capture(g):
            close_banner(g)
            cam = cv2.VideoCapture(0)            
            while True:
                result,image = cam.read()
                image = cv2.flip(image,1)
                cv2.imshow("Capture image",image)
                cv2.putText(image," Press q to capture",(0,0),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,0),2)
                os.chdir(img_folder)
                f = file_1.value
                filename = f"{f}.jpg"           
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    # add priview
                    cv2.imwrite(filename,image)
                    break
            cam.release()
            page.snack_bar = ft.SnackBar(ft.Text(f"{f} saved successfully !"))
            page.snack_bar.open = True
            time.sleep(1)
            page.update()

        file_1 = ft.TextField(label="Enter new user")
        def close_banner(c):
            page.banner.open = False
            page.update()
        
        
        page.banner = ft.Banner(
            content=ft.Text(" "),
            actions=[
            file_1,
            ft.TextButton("Submit",on_click=capture),
            ft.TextButton("Close",on_click=close_banner)
            ],
        )

        page.banner.open = True
        page.update()  
    
        
    '''
    //////////
    delete user 
    '''    
    def delete_user(i):
        def deleted(j):
            close_banner(j)
            c_1 = file_2.value
            c = f"{c_1}.jpg"
            if os.remove(rf'{img_folder}\{c}'):
                # page.add(ft.Text(value=f"Deleted user {c_1}"))
                # page.snack_bar = ft.SnackBar(ft.Text(f"{c_1} deleted successfully !"))
                # page.snack_bar.open = True
                page.update()
            else:
                ft.Text(value="Unable to delete")
            
        file_2 = ft.TextField(label="Enter name to delete")
        def close_banner(m):
            page.banner.open = False
            page.snack_bar = ft.SnackBar(ft.Text(f"{file_2.value} deleted successfully !"))
            page.snack_bar.open = True
            time.sleep(1)
            page.update()
        page.banner = ft.Banner(
            content=ft.Text(" "),
            actions=[
                file_2,
                ft.TextButton("Submit",on_click=deleted),
                ft.TextButton("Close",on_click=close_banner),
            ],

        )
        page.banner.open=True

        page.update()
    ''' 
    Mark Attendance

    '''
    def data(n):  
        def check_pass(n):
            default_pass = "attendance" 
            p_1 = file_3.value
            if p_1 == default_pass:
                os.startfile(rf'{time_folder}\{today}.txt')
                # date_attendance()

            else:
                pass
                # canvas.create_text(500,630,text="Incorrect !",fill="black",font=('Helvetica 10 bold')) 
                ft.Text(value="Incorrect")
                page.update()           
        file_3 = ft.TextField(label = "Enter Password ",password=True,can_reveal_password=True)
        def close_banner(x):
            page.banner.open = False
            page.update()
        page.banner = ft.Banner(
            content=ft.Text(" "),
            actions=[
                file_3,
                ft.TextButton("Submit",on_click=check_pass),
                ft.TextButton("Close",on_click=close_banner)

            ]
        )
            
        page.banner.open = True
        page.update()
    '''
    CREATING UI

    '''

    page.add(
        ft.Column(alignment=ft.MainAxisAlignment.END,
            controls= [
                
                ft.Container(
                    ft.ElevatedButton(text=" Take Attendance",expand=True,icon="camera",on_click=recognises,width=400,height=75,)
                ),
                ft.Container(
                    ft.ElevatedButton(text=" Register user",expand=True,icon="save",on_click=take_image,width=400,height=75),
                   
                ),
                ft.Container(
                    ft.ElevatedButton(text=" Delete user",expand=True,icon="delete",on_click=delete_user,width=400,height=75)
                ),
                ft.Container(
                    ft.ElevatedButton(text=" View Attendance",expand=True,icon="check",on_click=data,width=400,height=75)
                )
            ],
        spacing= 30    
        )
    )
    page.padding=50
    page.update()
ft.app(target=main)

