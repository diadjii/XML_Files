import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory
from lxml import etree
from helpers import delete_invalid_contracts, find_invalid_entity_code
from tkinter import END, messagebox
import os

window = tk.Tk()
window.title("Traitement Fichier XML")
window.geometry("800x400")
window.maxsize(900,800)

frame1 = tk.Frame(master=window, width=800, height=450, bg="white")
frame1.pack(fill=tk.BOTH,side=tk.LEFT, expand=True)

fr_buttons = tk.Frame(window,bg="white")

title = tk.Label(master=frame1, text="Traitement de Fichier XML",bg="white", fg="orange")
title.place(x=90, y=12)
title.config(font=("Courier", 44))

label1 = tk.Label(master=frame1, text="Veuillez choisir le fichier XML a corrigé",bg="white", fg="black")
label1.place(x=90, y=130)

label2 = tk.Label(master=frame1, text="Veuillez choisir le fichier retourné par la banque",bg="white", fg="black")
label2.place(x=90, y=190)

label4 = tk.Label(master=frame1, text="Veuillez indiquer où sauvegarder le fichier traité",bg="white", fg="black")
label4.place(x=90, y=260)

input1 = tk.Entry(window,bg="white", fg="black",width=50)
input1.place(x=90, y=150)

input2 = tk.Entry(window,bg="white", fg="black",width=50)
input2.place(x=90, y=210)

input4 = tk.Entry(window,bg="white", fg="black",width=50)
input4.place(x=90, y=280)

def open_xml_file():
    input1.delete(0,END)
    filepath = askopenfilename(
        filetypes=[("XML Files", "*.xml")]
    )
    if not filepath:
        return
    
    input1.insert(10,filepath)
    
def open_xml_data_file():
    input2.delete(0,END)
    filepath = askopenfilename(
        filetypes=[("XML Files", "*.xml")]
    )
    
    if not filepath:
        return
    
    input2.insert(10,filepath)
    

# function to specify the saving directory
def get_folder_path():
    input4.delete(0,END)
    filepath = askdirectory(mustexist=True)
    
    if not filepath:
        return
    
    input4.insert(20,filepath)
    

def start_process():
    xml_data = input1.get()
    feedback_file = input2.get()
    try:
        raw = etree.parse(xml_data)
    
        feedback = etree.parse(feedback_file)
        #get the feedback filename
        xml_filename = xml_data.split('/')[-1]

        contracts_codes = find_invalid_entity_code(feedback.getroot())

        delete_invalid_contracts(raw.getroot(),contracts_codes)

        saving_dir = input4.get()
        filepath = saving_dir+'/'+xml_filename

        raw.write(filepath)
        messagebox.showinfo(title="Génération du fichier", message="Traitement terminé. Fichier bien sauvegardé dans :" + saving_dir)
    
    except RuntimeError as err:
        messagebox.showerror(title="Génération du fichier", message="Echec du traitement. " + err)
    

    

btn_open1 = tk.Button(master=frame1, text="Choisir le Fichier",command=open_xml_file, bg="light blue",bd=0,borderwidth=0)
btn_open1.pack()
btn_open1.place(x=600,y=150)

btn_open2 = tk.Button(master=frame1, text="Elements à Supprimer",command=open_xml_data_file)
btn_open2.place(x=600,y=210)

btn_open3 = tk.Button(master=frame1, text="Lancer le Traitement",command=start_process)
btn_open3.place(x=250,y=350)

btn_open4 = tk.Button(master=frame1, text="Sauvegarder dans",command=get_folder_path)
btn_open4.place(x=600,y=280)

window.mainloop()