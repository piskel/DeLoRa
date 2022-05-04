import time
import threading
import tkinter as tk
from tkinter import ttk

from DeLoRa import DeLoRa
from YL800N_HEX import YL800N


class DLR_GUI:
    """Class to handle the GUI."""

    def __init__(self):

        self.__dlr: DeLoRa = None
        self.__window = tk.Tk()

        # GUI Windows configuration
        self.__window.title("DeLoRa")
        self.__window.geometry("600x500")
        self.__window.resizable(True, True)

        # Tab control configuration
        self.__tab_control = ttk.Notebook(self.__window)
        self.__messages_tab = ttk.Frame(self.__tab_control)
        self.__settings_tab = ttk.Frame(self.__tab_control)
        self.__tab_control.add(self.__messages_tab, text="Messages")
        self.__tab_control.add(self.__settings_tab, text="Settings")
        self.__tab_control.select(self.__settings_tab)
        self.__tab_control.pack(expand=True, fill=tk.BOTH)

        # Messages tab configuration
        self.__message_text = tk.Text(self.__messages_tab)
        self.__message_text.configure(state='disabled')
        self.__message_text.pack(expand=True, fill=tk.BOTH)

        self.__query_entry = tk.Entry(self.__messages_tab)
        self.__query_entry.pack(side=tk.BOTTOM, fill=tk.X)

        self.__enter_key_mem = False
        self.__query_entry.bind("<KeyPress>", self.__query_keypress)
        self.__query_entry.bind("<KeyRelease>", self.__query_release)

        # Settings tab configuration
        self.__username = None
        self.__username_label = tk.Label(self.__settings_tab, text="Username")
        self.__username_label.grid(sticky="W", row=0, column=0)

        self.__username_entry = tk.Entry(self.__settings_tab)
        self.__username_entry.grid(sticky="W", row=0, column=1)

        self.__com_port = None
        self.__com_port_label = tk.Label(self.__settings_tab,text="COM Port")
        self.__com_port_label.grid(sticky="W", row=1, column=0)

        self.__com_port_combobox = ttk.Combobox(
            self.__settings_tab,
            values=YL800N.get_com_port_list(),
            state="readonly")
        self.__com_port_combobox.grid(sticky="W", row=1, column=1)

        self.__apply_settings_button = tk.Button(self.__settings_tab, text="Apply")
        self.__apply_settings_button.grid(sticky="W", row=2, column=1)
        self.__apply_settings_button.bind("<Button-1>", self.__apply_settings)
        self.__apply_settings_button.bind("<Key-space>", self.__apply_settings)
        self.__apply_settings_button.bind("<Key-Return>", self.__apply_settings)

        self.__reception_thread = threading.Thread(target=self.__message_reception)
        self.__reception_thread.daemon = False

        # self.__window.protocol("WM_DELETE_WINDOW", self.stop)


    def __message_reception(self):
        """Handles receiving messages from the DeLoRa module."""
        while True:
            if self.__dlr is not None:
                if not self.__dlr.is_input_buffer_empty():
                    received_message = self.__dlr.read_com()
                    if received_message is not None:
                        self.__insert_in_message_text_box(str(received_message.decode("utf-8")))
            time.sleep(0.1)


    def start(self):
        """Starts the GUI."""
        self.__reception_thread.start()
        print("Thread starting ...")
        self.__window.mainloop()

    def stop(self):
        """Stops the GUI."""
        # FIXME : Separate thread not stopping properly
        self.__window.destroy()

    def __insert_in_message_text_box(self, message:str):
        """Inserts a message in the message text box.

        Args:
            message (str): The message to insert.
        """        
        self.__message_text.configure(state='normal')
        self.__message_text.insert(tk.END, message + "\n")
        self.__message_text.see(tk.END)
        self.__message_text.configure(state='disabled')

    def __query_keypress(self, event):
        """Handles the key press event of the query entry."""
        if event.keycode == 13 and not self.__enter_key_mem:
            self.__enter_key_mem = True

            query = self.__query_entry.get()
            self.__query_entry.delete(0, tk.END)
            str_message = self.__dlr.send_message(query)
            self.__insert_in_message_text_box(str_message)


    def __query_release(self, event):
        """Handles the key release event of the query entry."""
        if event.keycode == 13:
            self.__enter_key_mem = False

    def __apply_settings(self, _event):
        """Handles the apply settings button click event."""
        self.__username = self.__username_entry.get()

        for com_port in YL800N.get_com_port_list():
            if str(com_port) == self.__com_port_combobox.get():
                self.__com_port = com_port

        if self.__dlr is not None:
            self.__dlr.stop()

        self.__dlr = DeLoRa(self.__username, self.__com_port)
