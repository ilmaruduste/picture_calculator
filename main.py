# https://realpython.com/pysimplegui-python/

import PySimpleGUI as sg
import os.path
import cv2
import numpy as np
import keras
import pandas as pd
import matplotlib.pyplot as plt
import sys

######## DEFINE FUNCTIONS ########
#sorteerib kastid nende x koordinaadi väärtuse põhjal
#st. et eeldame et tehe on kirjutatud ühes reas
def order_boxes(boxes):
    boxes.sort(key=lambda x:x[0])

def get_areas(boxes):
    areas = []
    for box in boxes:
        areas.append(box[2]*box[3])
    return areas

#lõikab bounding boxide põhjal välja pildist huvipakkuvad pildid
def get_crops(image, boxes, draw=False):
    crops = []
    for box in boxes:
        x,y,w,h = box
        crops.append(image[y:y+h,x:x+w])
    if draw:
        for i, crop in enumerate(crops):
            plt.subplot(1,len(crops),i+1)
            #plt.axis('off')
            plt.imshow(crop, cmap="gray")
    return crops

#muudab pildid listis ruudukujuliseks, lisades puhvrit ümber
def make_square(image_list, square_size=None):
    ruudud = []
    for image in image_list:
        h, w = image.shape
        og_square_edge = max(h,w)
        if h > w:
            pool = (h-w)//2
            #vasakule liidetav pilt, laiusega pool, kõrgusega h, värv 255
            vasakule = np.full((h,pool), 255)
            #paremale liidetav pilt, laiusega h-w-pool, kõrgusega h, värv 255
            paremale = np.full((h,h-w-pool), 255)
            ruudud.append(np.concatenate((vasakule,image,paremale), axis=1))
        else:
            pool = (w-h)//2
            #ules liidetav pilt, laiusega w, kõrgusega pool, värv 255
            ules = np.full((pool, w), 255)
            #alla liidetav pilt, laiusega w, kõrgusega w-h-pool, värv 255
            alla = np.full((w-h-pool, w), 255)
            ruudud.append(np.concatenate((ules,image,alla), axis=0))
      
    #vajadusel muudab ruutude suurust
    if square_size != None:
        lopp_ruudud = []
        for image in ruudud:
            lopp_ruudud.append(cv2.resize(np.array(image, dtype='uint8'), (square_size, square_size), interpolation=cv2.INTER_AREA))
        ruudud = lopp_ruudud
    return ruudud

######## LOAD MODEL AND LABELS ########
loaded_model = keras.models.load_model('./math_symbol_classifier_model_v6')
labels_df = pd.read_csv('labels_df_6.csv', sep=';')
# loaded_model = keras.models.load_model('./math_symbol_classifier_model_v4')
# labels_df = pd.read_csv('labels_df_4.csv', sep=';')
labels_df.drop(labels_df.columns[0], axis=1, inplace=True)
true_labels = np.array(labels_df['true_label'])


######## MAIN SCRIPT ########
######## DEFINE GUI LAYOUT ########
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

formula_value_text = "This is your operation: "

# For now, this will only show the name of the file that was chosen
image_viewer_column = [
    [sg.Text("Choose an image from the list on the left:")],
    [sg.Radio("Original", "Radio", size = (10,1), key="-ORIGINAL-")],
    [sg.Radio("OpenCV", "Radio", size = (10,1), key="-OPENCV-")],
    [sg.Text(key = "-TOUT-", size = (150,1))],
    [sg.Text(formula_value_text, key = "-OPERATION-", auto_size_text=True, justification = 'center', size = (150,1))],
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

            elif values["-OPENCV-"]:

                infilename = os.path.normpath(filename)

                img = cv2.imread(filename)

                img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                #blurimine vajalik et eemaldada müra
                blur_img = cv2.GaussianBlur(img_gray,(5,5),0)
                #thresholdimisega teeme hallist taustast valge ja tekstist musta
                ret, thresh = cv2.threshold(blur_img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

                # paksendan jooni kõvasti, et lähedalolevad sümbolid (nt võrdusmärgid) muutuksid üheks
                kernel = np.ones((13,13),np.uint8)
                thresh_dilate = cv2.erode(thresh, kernel, iterations=1)

                contours,hierarchy = cv2.findContours(thresh_dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                # contours,hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                boxed_img = img.copy()
                joined_boxes = []
                for cnt in contours:
                    x,y,w,h = cv2.boundingRect(cnt)
                    # kui kast ei ole terve pildi suurune siis lisame jälgitavasse
                    if w < img_gray.shape[1] and h < img_gray.shape[0]:
                        joined_boxes.append([x,y,w,h])
                    boxed_img = cv2.rectangle(boxed_img,(x,y),(x+w,y+h),(255,0,0),1)

                imgbytes = cv2.imencode(".png", boxed_img)[1].tobytes()

                window["-IMAGE-"].update(data=imgbytes)

                order_boxes(joined_boxes)
                crops = get_crops(thresh, joined_boxes, True)

                crops = make_square(crops)
                tiny_crops = make_square(crops, 45)

                kernel = np.ones((2,2),np.uint8)
                reshaped_crops = np.array([np.reshape(crop,(45,45)) for crop in tiny_crops])
                dilated_crops = np.array([cv2.dilate(crop, kernel, iterations=2) for crop in reshaped_crops])

                predictions = loaded_model.predict(dilated_crops)
                predictions = [np.array(prediction).argmax() for prediction in predictions]

                new_operation_string = "This is your operation: " + " ".join(true_labels[predictions])
                # new_operation_string = " ".join(true_labels[predictions])
                window["-OPERATION-"].update(new_operation_string)

        except:

            print("Unexpected error:", sys.exc_info()[0])
            print("Error!!!!")
            pass
            # pass



window.close()