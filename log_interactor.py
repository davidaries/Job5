import tkinter as tk
from tkinter import *
import language_dictionary as ld
from icecream import ic
import initial_load_data as ild
import get_responsible_staff as grs
import communicator


class log_interactor:  # rename to task_reassign
    def __init__(self, language, window, home, device_id):
        self.language = language
        self.window = window
        self.home = home
        self.device_id = device_id
        self.alternate_staff = None
        self.staff_change = False
        self.priority = None

    def create_buttons(self, row, token, priority):
        self.priority = priority
        for _ in range(2):  # space buttons need to figure out a better way to do this
            row += 1
            Label(self.window, text=' ').grid(row=row, column=0)
        btn_pause = Button(self.window, text=ld.get_text_from_dict(self.language, '~6'),
                           command=lambda: self.pause_btn_listener(token),
                           fg="black", bg="gray", height=1, width=10)
        btn_pause.grid(row=row, column=0, sticky='S')
        btn_forward = Button(self.window, text=ld.get_text_from_dict(self.language, '~50'),
                             command=lambda: self.forward_btn_listener(token),
                             fg="black", bg="gray", height=1, width=10)
        btn_forward.grid(row=row, column=1, sticky='S')
        btn_reassign = Button(self.window, text=ld.get_text_from_dict(self.language, '~51'),
                              command=lambda: self.reassign_btn_listener(token),
                              fg="black", bg="gray", height=1, width=10)
        btn_reassign.grid(row=row, column=2, sticky='S')
        row += 1
        btn_return = Button(self.window, text=ld.get_text_from_dict(self.language, '~8'),
                            command=lambda: self.return_btn_listener(token),
                            fg="black", bg="gray", height=1, width=10)
        btn_return.grid(row=row, column=0, sticky='S')
        btn_skip = Button(self.window, text=ld.get_text_from_dict(self.language, '~52'),
                          command=lambda: self.skip_btn_listener(token),
                          fg="black", bg="gray", height=1, width=10)
        btn_skip.grid(row=row, column=1, sticky='S')
        btn_drop = Button(self.window, text=ld.get_text_from_dict(self.language, '~53'),
                          command=lambda: self.drop_btn_listener(token),
                          fg="black", bg="gray", height=1, width=10)
        btn_drop.grid(row=row, column=2, sticky='S')

        ### FUNCTIONALITY to enable/ diable buttons
        # btn_drop.config(state = tk.DISABLED)

    def pause_btn_listener(self, token):
        self.staff_change = False
        log_input = 'N/A'
        self.log_and_reset(self.device_id, '~6', log_input, token)

    def forward_btn_listener(self, token):
        self.staff_change = True
        self.log_textbox('~50', token)
        choices = communicator.get_possible_staff(self.device_id, True)
        self.drop_down(choices)

    def reassign_btn_listener(self, token):
        self.staff_change = True
        self.log_textbox('~51', token)
        self.alternate_staff = communicator.get_possible_staff(self.device_id,False)

    def return_btn_listener(self, token):
        self.staff_change = False
        communicator.add_flow_info(token,'~8')
        self.log_textbox('~8', token)

    def skip_btn_listener(self, token):
        self.staff_change = False
        communicator.add_flow_info(token,'~52')
        self.log_textbox('~52', token)

    def drop_btn_listener(self, token):
        self.staff_change = False
        communicator.add_flow_info(token,'~53')
        self.log_textbox('~53', token)

    def log_textbox(self, status, token):
        self.clear_window()
        log_input = tk.Text(self.window, height=10, width=55)
        log_input.pack(side=TOP)
        Button(self.window, text='Submit',
               command=lambda: self.log_and_reset(self.device_id, status, log_input, token)).pack(side=BOTTOM)

    def log_and_reset(self, device_id, status, log_input, token):
        try: #when log_input comes from the text box
            comments = log_input.get(1.0,"end-1c")
        except: #when log_input comes from a string
            comments = log_input
        communicator.update_log(token, device_id, status, comments, self.priority.get())
        if self.staff_change:
            communicator.change_staffer(token, self.device_id, self.alternate_staff)
        else: #should be removing from UI screen
            if status == '~8':#for returned tasks
                communicator.return_data(token, None)
                self.home.partial_complete(device_id,token)
            elif status =='~52':#for skipped tasks
                communicator.return_data(token, None)
                self.home.partial_complete(device_id,token)
            elif status == '~53':#for dropped tasks
                communicator.return_data(token, None)
                self.home.partial_complete(device_id,token)

        self.home.reset_window(self.device_id, token)

    def drop_down(self, choices):
        Label(self.window, text=ld.get_text_from_dict(self.language, '~56') + ': ').pack(side=LEFT, anchor=N)
        option = StringVar(self.window)
        choices_formatted = []
        for choice in choices:
            choices_formatted.append(communicator.name_from_staff_id(choice))
        communicator.staff_id_from_name(choices_formatted[0])
        drop_down = OptionMenu(self.window, option, *choices_formatted)
        self.alternate_staff = option
        drop_down.pack(side=LEFT, anchor=N)

    def clear_window(self):
        """This function clears the window that it is given allowing it to be a blank canvas before the window
        is repopulated with different widgets
        """
        for widget in self.window.winfo_children():
            widget.destroy()
