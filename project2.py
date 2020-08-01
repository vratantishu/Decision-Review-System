import tkinter
import cv2
import PIL.Image, PIL.ImageTk
from functools import partial
import threading
import imutils
import time


stream = cv2.VideoCapture("clip.mp4")
flag= True

def play(speed):
    global flag
    print(f"you clicked on play, speed is {speed}")
    # play the vedio in reverse mode
    frame1= stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)

    grabbed, frame = stream.read()
    if not grabbed:
        exit()

    frame= imutils.resize(frame, width= SET_WIDTH, height=SET_HEIGHT)
    frame=PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor= tkinter.NW)
    if flag:
        canvas.create_text(134,26, fill="black", font="Times 26 bold,", text="Decision Pending")
    flag= not flag


def pending(decision):
    # 1. display decision pending image
    frame = cv2.cvtColor(cv2.imread("pending.jpg"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image= frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)

    # 2. wait for 1 sec
    time.sleep(1)

    # 3. display sponsor image
    frame = cv2.cvtColor(cv2.imread("sponsor.jpg"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)

    # 4. wait for 1.5 sec
    time.sleep(1.5)
    # 5. display out/not out image
    if decision == 'out':
        decisionImg= 'out.jpg'
        frame = cv2.cvtColor(cv2.imread(decisionImg), cv2.COLOR_BGR2RGB)
        frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
        frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        canvas.image = frame
        canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
    else:
        decisionImg= "not_out.jpg"
        frame= cv2.cvtColor(cv2.imread(decisionImg), cv2.COLOR_BGR2RGB)
        frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
        frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        canvas.image = frame
        canvas.create_image(0,0, image=frame, anchor=tkinter.NW)



def out():
      thread= threading.Thread(target=pending, args= ('out',))
      thread.daemon= 1
      thread.start()
      print("player is out")

def not_out():
    thread = threading.Thread(target=pending, args=('not out',))
    thread.daemon = 1
    thread.start()
    print("player is not_out")



# width and height of our main screen

SET_WIDTH= 650
SET_HEIGHT= 380
#tkinter GUI starts here

window=tkinter.Tk()
window.title("Vratant Third Umpire Decision Review System")
cv_img= cv2.cvtColor(cv2.imread("welcome.jpg"),cv2.COLOR_BGR2RGB)
canvas= tkinter.Canvas(window, width= SET_WIDTH, height= SET_HEIGHT)
photo= PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
Image_on_canavs= canvas.create_image(0,0, ancho=tkinter.NW, image=photo)
canvas.pack()

#buttons to control playback

btn= tkinter.Button(window, text="<< Previous (fast)", width=50, command= partial(play,-10))
btn.pack()

btn= tkinter.Button(window, text="<< Previous (slow)", width=50, command= partial(play, -2))
btn.pack()

btn= tkinter.Button(window, text="Forward (fast) >>", width=50, command= partial(play, 10))
btn.pack()

btn= tkinter.Button(window, text="Forward (slow) >>", width=50, command= partial(play, 2))
btn.pack()

btn= tkinter.Button(window, text="OUT", width=50, command= out)
btn.pack()

btn= tkinter.Button(window, text="NOT_OUT", width=50, command= not_out)
btn.pack()


window.mainloop()