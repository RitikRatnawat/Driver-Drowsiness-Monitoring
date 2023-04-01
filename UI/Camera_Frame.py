from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
from PIL import Image as Img
from LoginFrame import *
from SignupFrame import *
from main import *
from functools import partial
from OptionsFrame import *
import cv2
import os
from keras.models import load_model
import numpy as np
from pygame import mixer
import time
import imutils
# ---------------------------------------------------------------------------------------------

mixer.init()
sound = mixer.Sound('..//ring.wav')

face = cv2.CascadeClassifier('..\\haar cascade files\\haarcascade_frontalface_alt.xml')
leye = cv2.CascadeClassifier('..\\haar cascade files\\haarcascade_lefteye_2splits.xml')
reye = cv2.CascadeClassifier('..\\haar cascade files\\haarcascade_righteye_2splits.xml')



lbl=['Close','Open']

model = load_model('..//model.h5')
path = os.getcwd()

cap = None
camera_image = None
camera_frame = None
view_frame = None
overlay = None
# -----------------------------------------------
def on_camera(root):
	pass		




def add_Camera_UI(root, name, no):
	global camera_image
	global camera_frame
	global view_frame
	global overlay
	title_text = f"Live Camera Feed - "+ str(name) + "  ID : " + str(no)
	root.title(title_text)

	image = ImageTk.PhotoImage(file="rec.png")
	camera_image = Label(root, image=image, border=0, bg="white")
	camera_image.image = image
	camera_image.place(x=0, y=130)
	camera_frame = Frame(root, name= 'camera', bg='white', width = 910, height=485, border =  0, )
	camera_frame.place(x=40, y = 210)


	cam_head = Label(camera_frame, name ="head", bg = "white", fg = "black", text = "Live Camera", border = 0, font=("Microsoft Yahei UI Light", 18, 'bold'))
	cam_head.place(x= 159, y = 5)
	view_frame = Label(camera_frame)
	overlay = Label(camera_frame, name="live", bg = "red", width = 70, height = 30, border = 0)
	overlay.place(x = 10, y = 50)


	naam = "Driver Name : " + str(name)
	driver_name = Label(camera_frame, name = "name", bg= "white", text = naam, border = 0, font=("Microsoft Yahei UI Light", 14, 'bold'))
	driver_name.place(x= 550, y = 180)
	
	id1 = "ID : " + str(no)
	driver_id = Label(camera_frame, name = "id", bg= "white", text =id1, border = 0, font=("Microsoft Yahei UI Light", 14, 'bold'))
	driver_id.place(x= 550, y = 250)

	view_btn = Button(options_frame, width=7, text="View", border=1, font=("Microsoft Yahei UI Light", 10, 'bold'),
                        bg='white', cursor='hand2', fg='teal', activebackground = "white", command= partial(view_cam, root, no))
	view_btn.place(x=590, y=520)


	logout_btn = Button(options_frame, width=7, text="Log Out", border=0,
                        bg='white', cursor='hand2', fg='#EB455F', activebackground = "white", command= partial(logout_action, root))
	logout_btn.place(x=850, y=610)
# -------------------------------------------------------------------------------------------

def view_cam(root, no):
	global view_frame
	global cap 
	global overlay

	overlay.place_forget()
	if no == "001":
		cap = cv2.VideoCapture(0)
	elif no == "002":
		cap = cv2.VideoCapture(1)

	font = cv2.FONT_HERSHEY_COMPLEX_SMALL
	count=0
	score=0
	thicc=2
	rpred=[99]
	lpred=[99]
	while(True):
		ret, frame = cap.read()
		frame = cv2.flip(frame, 1)
		cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		img = Image.fromarray(cv2image)
		imgtk = ImageTk.PhotoImage(image=img)
		view_frame.configure(image = imgtk)
		view_frame.place(x=10,y=50)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	cap.release()
	cv2.destroyAllWindows()

	
# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  #  		faces = face.detectMultiScale(gray,minNeighbors=5,scaleFactor=1.1,minSize=(25,25))
  #   	left_eye = leye.detectMultiScale(gray)
  #   	right_eye =  reye.detectMultiScale(gray)
	 #    cv2.rectangle(frame, (0,height-50) , (200,height) , (0,0,0) , thickness=cv2.FILLED)




def final_options(root):
    remove_options_UI()
    LoginFrame.add_login_UI(root)


def remove_options_UI():
    camera_image.place_forget()
    camera_frame.place_forget()

def logout_action(root):
	open_main = messagebox.askyesno("Log Out", "Are You Sure?")
	if open_main > 0:
		remove_options_UI()
		LoginFrame.add_login_UI(root)
	else:
		if not open_main:
			return



# ---------------------------------------------------------------
	
if __name__ == "__main__":
	root = Tk()
	root.grid_propagate(False)
	UI(root)
	add_Camera_UI(root, "Manish R", "001")
	root.mainloop()
