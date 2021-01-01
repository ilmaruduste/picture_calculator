# https://realpython.com/pysimplegui-python/

import PySimpleGUI as sg
import os.path
import cv2


# First the window layout in 2 columns
file_list_column = [
    [
        sg.Text("Image Folder"),
        sg.In(size=(25,2), enable_events=True, key = "-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(values=[], enable_events=True, size = (80, 40), key = "-FILE LIST-")
    ],
]

# For now will only show the name of the file that was chosen
image_viewer_column = [
    [sg.Text("Choose an image from the list on the left:")],
    [sg.Radio("Original", "Radio", size = (10,1), key="-ORIGINAL-")],
    [sg.Radio("OpenCV", "Radio", size = (10,1), key="-OPENCV-")],
    [sg.Text(size=(40,1), key = "-TOUT-")],
    [sg.Image(key="-IMAGE-")],
]

# --- Full Layout ---


layout = [
    [
        sg.Column(file_list_column),
        sg.VSeparator(),
        sg.Column(image_viewer_column),
    ]
]

window = sg.Window("Image Viewer", layout)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    # Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []
            # file_list = ["asdasd.jpg"]
        
        fnames = [
            f for f in file_list if os.path.isfile(os.path.join(folder,f))
            and f.lower().endswith((".png", ".gif"))
        ]
        window["-FILE LIST-"].update(fnames)
    
    elif event == "-FILE LIST-": # A file was chosen from the listbox
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-TOUT-"].update(filename)

            if values["-ORIGINAL-"]:
                window["-IMAGE-"].update(filename=filename)

                # Debug statement
                print("In original")

            elif values["-OPENCV-"]:
                

                # https://stackoverflow.com/questions/24385714/detect-text-region-in-image-using-opencv



                img = cv2.imread(filename)
                img2gray = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)[:,:,0]
                ret, mask = cv2.threshold(img2gray, 180, 255, cv2.THRESH_BINARY)
                image_final = cv2.bitwise_and(img2gray, img2gray, mask=mask)
                ret, new_img = cv2.threshold(image_final, 180, 255, cv2.THRESH_BINARY) # for black text , cv.THRESH_BINARY_INV

                print("Before kernel")
                kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,
                                                         3))  # to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more
                
                print("After kernel")
                dilated = cv2.dilate(new_img, kernel, iterations=9)  # dilate , more the iteration more the dilation
                print("After dilated")

                # image, contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
                contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
                print("After contours")


                for contour in contours:
                    # get rectangle bounding contour
                    [x, y, w, h] = cv2.boundingRect(contour)

                    # Don't plot small false positives that aren't text
                    if w < 35 and h < 35:
                        continue

                    # draw rectangle around contour on original image
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)

                frame = img
                print("After frame")

                imgbytes = cv2.imencode(".png", frame)[1].tobytes()
                print("After imgbytes")

                # Debug statement
                print("In OpenCV1")

                window["-IMAGE-"].update(data=imgbytes)
                                
                # Debug statement
                print("In OpenCV2")
        except:
            pass



window.close()