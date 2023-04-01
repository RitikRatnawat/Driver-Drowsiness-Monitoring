from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
from PIL import Image as Img
from functools import partial
import numpy as np
from tensorflow import keras
import cv2
import OptionsFrame
import imutils


background = None
accumulated_weight = 0.5

ROI_top = 100
ROI_bottom = 350
ROI_left = 150
ROI_right = 400

word_dict = {0:'One', 1:'Two',2:'Three',3:'Four',4:'Five',5:'Six',6:'Seven',7:'Eight',8:'Nine'}

model = keras.models.load_model("Sign_Language_Translator_ADAM.h5") 
# -------------------------------------------------------------------------

livet_frame = None
cap = None
camera_Label = None
cam_on = False
overlay = None
num_of_frames = 0
output_text = None

# -----------------------------------------------------------------------------------------

def calculate_accumulated_avg(frame, accumulated_weight):
    global background
    
    if background is None:
        background = frame.copy().astype("float")
        return None
    
    cv2.accumulateWeighted(frame, background, accumulated_weight)
    
    
def segment_hand(frame, threshold=25):
    global background
    
    diff = cv2.absdiff(background.astype("uint8"), frame)
    
    _, thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)

    return thresholded


def predict():
    global cam_on, num_of_frames

    if cam_on:
        global cap
        global camera_Label
        global output_text
        
        ret, frame = cap.read()

        if ret:
            frame = cv2.flip(frame, 1)
            
            roi = frame[ROI_top:ROI_bottom, ROI_left:ROI_right]
            gray_frame = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            gray_frame = cv2.GaussianBlur(gray_frame, (9, 9), 0)
            
            if num_of_frames < 70:
                calculate_accumulated_avg(gray_frame, accumulated_weight)

                cv2.putText(frame, "FETCHING BACKGROUND...PLEASE WAIT", 
                            (120, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
            else:
                hand = segment_hand(gray_frame)

                if hand is not None:
                    thresholded = hand
                
                    thresholded = cv2.resize(thresholded, (64, 64))
                    thresholded = cv2.cvtColor(thresholded, cv2.COLOR_GRAY2RGB)
                    thresholded = np.reshape(thresholded, (1, thresholded.shape[0], thresholded.shape[1], 3))
                    
                    pred = model.predict(thresholded)
                    output_text.configure(text = "Sign Translation : "+word_dict[np.argmax(pred)])
                else:
                    cv2.putText(frame, 'No hand detected...', (200, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
            
            cv2.rectangle(frame, (ROI_left, ROI_top), (ROI_right,ROI_bottom), (255,128,0), 3)
            num_of_frames += 1
            
            frame = imutils.resize(frame, width=490)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            camera_Label.place(x=180, y=60)
            camera_Label.imgtk = imgtk
            camera_Label.configure(image=imgtk)
        
        camera_Label.after(20, predict)


def start_camera():
    global cam_on, cap, overlay
    stop_camera()
    cam_on = True
    cap = cv2.VideoCapture(0)
    overlay.place_forget()
    predict()


def stop_camera():
    global cam_on, camera_Label
    global num_of_frames, output_text
    cam_on = False
    num_of_frames = 0
    output_text.configure(text = "")
    
    if camera_Label:
        camera_Label.place_forget()
        overlay.place(x=180, y=60)

    if cap:
        cap.release()


# --------------------------------------------------------------------
def add_LiveTranslator_UI(root):
    root.title("Live Translator")

    global livet_frame, camera_Label, overlay
    livet_frame = Frame(root, name="livetranslator",
                        width=960, height=550, bg='white')
    livet_frame.place(x=20, y=140)

    head1 = Label(livet_frame, bg='white', fg='black', text="Live Camera", font=(
        'Microsoft Yahei UI Light', 22, 'bold'))
    head1.place(x=350, y=5)

    camera_Label = Label(livet_frame)
    overlay = Label(livet_frame, bg='black', width=70, height=25)
    overlay.place(x=180, y=60)


# --------------------------------------------------------
    startCam = Button(livet_frame, text="Start Camera", width=16, font=('Microsoft Yahei UI Light', 11), bg="#57a1f8", fg='white', cursor='hand2', border=0,
                      command=start_camera)
    startCam.place(x=750, y=180)

    stopCam = Button(livet_frame, text="Stop Camera", width=16, font=('Microsoft Yahei UI Light', 11), bg="#57a1f8", fg='white', cursor='hand2', border=0,
                     command=stop_camera)
    stopCam.place(x=750, y=250)

    backBtn = Button(livet_frame, width=18, text="Back", border=0, font=('Microsoft Yahei UI Light', 10),
                     bg='white', cursor='hand2', fg='#57a1f8', activebackground="white", command=partial(final_livet, root))
    backBtn.place(x=750, y=350)

    global output_text
    output_text = Label(livet_frame, fg='black', bg="white", width=41, height=2, relief="ridge", 
                        borderwidth=3, font=("Cambria", 16))
    output_text.place(x=177, y=455)

# ----------------------------------------------------------------------------------------------------------------------------------------


def final_livet(root):
    open_main = messagebox.askyesno("Log Out", "Are You Sure?")
    if open_main > 0:
        remove_livet_UI()
        OptionsFrame.add_Options_UI(root)
    else:
        if not open_main:
            return


def remove_livet_UI():
    livet_frame.place_forget()
# ----------------------------------------------------------------------