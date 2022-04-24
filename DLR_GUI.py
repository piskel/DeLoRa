
import tkinter as tk
from tkinter import ttk

import DeLoRa
import YL800N


class DLR_GUI:

    def __init__(self):

        self.__dlr = DeLoRa.DeLoRa()
        self.__window = tk.Tk()
        
        # GUI Windows configuration
        self.__window.title("DeLoRa")
        self.__window.geometry("600x500")
        self.__window.resizable(True, True)

        # Tab control configuration
        self.__tabControl = ttk.Notebook(self.__window)
        self.__messagesTab = ttk.Frame(self.__tabControl)
        self.__settingsTab = ttk.Frame(self.__tabControl)
        self.__tabControl.add(self.__messagesTab, text="Messages")
        self.__tabControl.add(self.__settingsTab, text="Settings")
        self.__tabControl.select(self.__settingsTab)
        self.__tabControl.pack(expand=True, fill=tk.BOTH)



        # Messages tab configuration
        self.__message_text = tk.Text(self.__messagesTab)
        self.__message_text.configure(state='disabled')
        self.__message_text.pack(expand=True, fill=tk.BOTH)

        self.__query_entry = tk.Entry(self.__messagesTab)
        self.__query_entry.pack(side=tk.BOTTOM, fill=tk.X)

        self.__enter_key_mem = False
        self.__query_entry.bind("<KeyPress>", self.__query_keypress)
        self.__query_entry.bind("<KeyRelease>", self.__query_release)


        # Settings tab configuration
        self.__username = None
        self.__usernameLabel = tk.Label(self.__settingsTab, text="Username")
        self.__usernameLabel.grid(sticky="W", row=0, column=0)

        self.__usernameEntry = tk.Entry(self.__settingsTab)
        self.__usernameEntry.grid(sticky="W", row=0, column=1)

        self.__com_port = None
        self.__COMPortLabel = tk.Label(self.__settingsTab,text="COM Port")
        self.__COMPortLabel.grid(sticky="W", row=1, column=0)

        self.__COMPortCombobox = ttk.Combobox(self.__settingsTab, values=YL800N.YL800N.get_com_port_list(), state="readonly")
        self.__COMPortCombobox.grid(sticky="W", row=1, column=1)

        self.__applySettingsButton = tk.Button(self.__settingsTab, text="Apply")
        self.__applySettingsButton.grid(sticky="W", row=2, column=1)
        self.__applySettingsButton.bind("<Button-1>", self.__apply_settings)

        


    def start(self):
        self.__window.mainloop()

    
    def stop(self):
        self.__window.destroy()
    

    def __query_keypress(self, e):
        
        if e.keycode == 13 and not self.__enter_key_mem:
            self.__enter_key_mem = True

            query = self.__query_entry.get()
            print(query)        
            self.__query_entry.delete(0, tk.END)
                
    def __query_release(self, e):
        if e.keycode == 13:
            self.__enter_key_mem = False
    
    def __apply_settings(self, e):
        self.__username = self.__usernameEntry.get()

        for com_port in YL800N.YL800N.get_com_port_list():
            if str(com_port) == self.__COMPortCombobox.get():
                selected_com_port = com_port
                self.__com_port = com_port
        
        self.__dlr.set_com_port(self.__com_port)
        

    def __check_gui_config(self):
        pass
    

