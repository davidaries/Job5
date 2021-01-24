from tkinter import *
from language_dictionary import language_dictionary as ld
from icecream import ic
import log_test
import working_data


class log_interactor: # rename to task_reassign
    def __init__(self, language, window, home, device_id):
        self.language = language
        self.window = window
        self.home = home
        self.device_id = device_id

    def create_buttons(self, row, token):
        for _ in range(3):  # space buttons need to figure out a better way to do this
            row += 1
            Label(self.window, text=' ').grid(row=row, column=0)
        # ld.get_text_from_dict(self.language, value)
        # talk about dictionary
        btn_pause = Button(self.window, text='Pause',
                           command=lambda: self.pause_btn_listener(token),
                           fg="black", bg="gray", height=1, width=10)
        btn_pause.grid(row=row, column=0, sticky='S')
        btn_forward = Button(self.window, text='Forward',
                             command=lambda: self.forward_btn_listener(token),
                             fg="black", bg="gray", height=1, width=10)
        btn_forward.grid(row=row, column=1, sticky='S')
        btn_reassign = Button(self.window, text='Reassign',
                              command=lambda: self.reassign_btn_listener(token),
                              fg="black", bg="gray", height=1, width=10)
        btn_reassign.grid(row=row, column=2, sticky='S')
        row += 1
        btn_return = Button(self.window, text='Return',
                            command=lambda: self.return_btn_listener(token),
                            fg="black", bg="gray", height=1, width=10)
        btn_return.grid(row=row, column=0, sticky='S')
        btn_skip = Button(self.window, text='Skip',
                          command=lambda: self.skip_btn_listener(token),
                          fg="black", bg="gray", height=1, width=10)
        btn_skip.grid(row=row, column=1, sticky='S')
        btn_drop = Button(self.window, text='Drop',
                          command=lambda: self.drop_btn_listener(token),
                          fg="black", bg="gray", height=1, width=10)
        btn_drop.grid(row=row, column=2, sticky='S')

    def pause_btn_listener(self, token):
        self.log_interface('pause')
        print('pause')
        working_data.add_to_log(token, 'test pause')

    def forward_btn_listener(self, token):
        self.log_interface('forward')
        print('forward')
        working_data.add_to_log(token, 'test forward')

    def reassign_btn_listener(self, token):
        self.log_interface('reassign')
        print('reassign')
        working_data.add_to_log(token, 'test reassign')

    def return_btn_listener(self, token):
        self.log_interface('return')
        print('return')
        working_data.add_to_log(token, 'test return')

    def skip_btn_listener(self, token):
        self.log_interface('skip')
        print('skip')
        working_data.add_to_log(token, 'test skip')

    def drop_btn_listener(self, token):
        self.log_interface('drop')
        print('drop')
        working_data.add_to_log(token, 'test drop')

    def base_log_screen(self):
        self.log_interface('BASE')
        print('BASE')

    def log_interface(self, action):
        self.clear_window()
        log_input = Text(self.window, height = 9, width = 30)
        log_input.pack()
        Button(self.window, text = 'Submit', command = lambda :  self.home.reset_staffer_home(self.device_id)).pack()

    def clear_window(self):
        """This function clears the window that it is given allowing it to be a blank canvas before the window
        is repopulated with different widgets
        """
        for widget in self.window.winfo_children():
            widget.destroy()