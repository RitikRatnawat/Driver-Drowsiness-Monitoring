from tkinter import Tk, Label, PhotoImage, Frame, Button
from tkinter import messagebox, filedialog
from PIL import ImageTk, Image
import LoginFrame 
from functools import partial
import OptionsFrame

# -------------------------------------------------------------------------

class UI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sign Language Translator")
        self.root.geometry('1000x710+180+35')
        self.root.resizable(False, False)
        self.root.configure(bg = "white")
        
        icon = PhotoImage(file="icon.png")
        self.root.iconphoto(False, icon)
        
        self.title = ImageTk.PhotoImage(file = "title.png")
        self.title_image = Label(self.root, image = self.title, border = 0)
        self.title_image.image = self.title
        self.title_image.place(x = 0, y = 10)

        add_CaptureImage_UI(root)

 # -----------------------------------------------------------------------
captimg_frame = None
# -----------------------------------------------------------------------



def add_CaptureImage_UI(root):
    root.title("Captured Image Translator")
    global captimg_frame
    
    captimg_frame = Frame(root, name= "captureimage", width= 960, height = 550, bg = 'white')
    captimg_frame.place(x= 20, y=140)

    head1 = Label(captimg_frame, bg= 'white', fg = 'black', text= "Live Camera", font= ('Microsoft Yahei UI Light', 15, 'bold'))
    head1.place(x= 155, y = 5)

    head2 = Label(captimg_frame, bg= 'white', fg = 'black', text= "Captured Image", font= ('Microsoft Yahei UI Light', 15, 'bold'))
    head2.place(x= 650, y = 5)

 	# ------------------------------------------------------------------------

    cameralabel = Label(captimg_frame, bg='black', width= 65, height= 19)
    cameralabel.place(x= 5, y = 50)

    cameralabel2 = Label(captimg_frame, bg='black', width= 65, height= 19)
    cameralabel2.place(x= 495, y = 50)
 	# ----------------------------------------------------------------------------

    capturebtn = Button(captimg_frame, text = "Capture Image", width = 16, font = ('Microsoft Yahei UI Light', 11), bg ="#57a1f8", fg = 'white',cursor ='hand2', border = 0)
    capturebtn.place(x= 148, y= 370)

    head3 = Label(captimg_frame, bg= 'white', fg = 'black', text= "Output:", font= ('Microsoft Yahei UI Light', 15, 'bold'))
    head3.place(x= 495, y = 360)

    output_text = Label(captimg_frame, bg='blue', fg='black', width = 65 , height = 8)
    output_text.place(x = 495 , y = 405)

    backbtn = Button (captimg_frame, width = 18, text = "Back", border = 0, font = ('Micosoft Yahei UI Light', 10), bg = 'white', cursor ='hand2', fg ='#57a1f8', activebackground = "white" , command=partial(final_captimg, root))
    backbtn.place (x = 148, y = 450)

# ------------------------------------------------------------------------------------------

def final_captimg(root):
    open_main = messagebox.askyesno("Log Out", "Are You Sure?")
    if open_main>0:
        remove_captimg_UI()
        OptionsFrame.add_Options_UI(root)
    else:
        if not open_main:
            return
    


def remove_captimg_UI():
    captimg_frame.place_forget()


# ---------------------------------------------------------------------------------
if __name__ == "__main__":
	root = Tk()
	root.grid_propagate(False)
	UI(root)
	root.mainloop()

