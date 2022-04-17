import tkinter as tk
from tkinter import ttk
from turtle import bgcolor, color
import DeLoRa
import YL800N


window = tk.Tk()
window.title("DeLoRa")
window.geometry("600x500")
window.resizable(True, True)

tabControl = ttk.Notebook(window)
messagesTab = ttk.Frame(tabControl)
settingsTab = ttk.Frame(tabControl)



tabControl.add(messagesTab, text="Message")
tabControl.add(settingsTab, text="Settings")

tabControl.pack(expand=True, fill=tk.BOTH)




ttk.Label(settingsTab, text="Username").grid(sticky="W", row=0, column=0)
username_entry = ttk.Entry(settingsTab)
username_entry.grid(sticky="W", row=0, column=1)

ttk.Label(settingsTab, text="COM Port").grid(sticky="W", row=1, column=0)
com_combobox = ttk.Combobox(settingsTab, values=YL800N.YL800N.get_com_port_list(), state="readonly")
com_combobox.grid(sticky="W", row=1, column=1)

apply_settings_button = ttk.Button(settingsTab, text="Apply")
apply_settings_button.grid(sticky="W", row=2, column=1)



tabControl.select(settingsTab)

# frame = tk.Frame(window)
# frame.pack(expand=True, fill=tk.BOTH)



# Displays messages
message_text = tk.Text(messagesTab)
message_text.configure(state='disabled')
message_text.pack(expand=True, fill=tk.BOTH)

# Query entry box
query_entry = tk.Entry(messagesTab)
query_entry.pack(side=tk.BOTTOM, fill=tk.X)

DLR = None

def apply_settings(e):
    global DLR
    selected_com_port = None

    if DLR is not None:
        DLR.quit()

    for com_port in YL800N.YL800N.get_com_port_list():
        print(com_port)
        
        if str(com_port) == com_combobox.get():
            selected_com_port = com_port

    DLR = DeLoRa.DeLoRa(selected_com_port.device, username_entry.get())




apply_settings_button.bind("<Button-1>", apply_settings)



enter_mem = False


def keyPress(e):
    global enter_mem
    
    if e.keycode == 13 and not enter_mem:
        enter_mem = True
        message_text.configure(state='normal')

        query = query_entry.get()


        query_result = DLR.send_query(query)


        message_text.insert(tk.END, query_result)
        message_text.configure(state='disabled')

        query_entry.delete(0, tk.END)
    

def keyRelease(e):
    global enter_mem
    if e.keycode == 13:
        enter_mem = False


query_entry.bind("<KeyPress>", keyPress)
query_entry.bind("<KeyRelease>", keyRelease)

window.mainloop()



