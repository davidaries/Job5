import tkinter as tk
from tkinter import *
import language_dictionary as ld
from icecream import ic
import working_data as wd
import simulation_time
import initial_load_data as ild
import get_responsible_staff as grs


class log_interactor: # rename to task_reassign
    def __init__(self, language, window, home, device_id):
        self.language = language
        self.window = window
        self.home = home
        self.device_id = device_id
        self.alternate_staff = None
        self.staff_change = False


    def create_buttons(self, row, token):
        for _ in range(3):  # space buttons need to figure out a better way to do this
            row += 1
            Label(self.window, text=' ').grid(row=row, column=0)
        # ld.get_text_from_dict(self.language, value)
        # talk about dictionary
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
        log_input = 'N/A'
        self.log_and_reset(self.device_id, '~6', log_input, token)
        # self.log_interface('~6', token)
        # print('pause')
        # working_data.add_to_log(token, 'test pause')

    def forward_btn_listener(self, token):
        self.staff_change = True
        self.log_interface('~50', token)
        current_staffer = ild.device_staff.get(self.device_id)
        staff_type =ild.staffers.get(current_staffer).get('~23')
        choices = grs.get_other_staffers(staff_type, current_staffer, True)
        self.drop_down(choices)

    def reassign_btn_listener(self, token):
        self.staff_change = True
        self.log_interface('~51', token)
        current_staffer = ild.device_staff.get(self.device_id)
        staff_type =ild.staffers.get(current_staffer).get('~23')
        self.alternate_staff = grs.get_other_staffers(staff_type, current_staffer, False)
        # print('reassign')
        # working_data.add_to_log(token, 'test reassign')

    def return_btn_listener(self, token):
        self.log_interface('~8', token)
        # print('return')
        # working_data.add_to_log(token, 'test return')

    def skip_btn_listener(self, token):
        self.log_interface('~52', token)
        # print('skip')
        # working_data.add_to_log(token, 'test skip')

    def drop_btn_listener(self, token):
        self.log_interface('~53', token)
        # print('drop')
        # working_data.add_to_log(token, 'test drop')
    #
    # def base_log_screen(self):
    #     self.log_interface('BASE')
    #     print('BASE')

    def log_interface(self, status, token):
        self.clear_window()
        log_input = tk.Text(self.window, height = 10, width = 55)
        log_input.pack(side = TOP)
        Button(self.window, text = 'Submit',
               command = lambda :  self.log_and_reset(self.device_id, status, log_input, token)).pack(side = BOTTOM)

    def log_and_reset(self, device_id, status, log_input, token):
        try:
            comments = log_input.get(1.0, "end-1c")  # after some basic reserch on using text boxes in tkinter end-1c is the way
                                          # retrieve all of the text from a textbox
        except:
            comments = log_input
        if self.staff_change:
            self.change_staffer(token)
        time = simulation_time.get_time_stamp()
        user = ild.device_staff.get(device_id)
        priority = None
        # working_data.add_to_log(token,user, time,status,priority,comments)
        log_data = {'user': user, 'time': time, 'status': status, 'priority': priority, 'comments': comments}
        if token in wd.log_dict:
            wd.log_dict.get(token).append(log_data)
        else:
            wd.log_dict[token] = [log_data]
        wd.token_status_dict[token]=status
        self.home.reset_window((self.device_id))

    def drop_down(self, choices):
        Label(self.window, text=ld.get_text_from_dict(self.language, '~56') + ': ').pack(side = LEFT, anchor = N)
        option = StringVar(self.window)
        drop_down = OptionMenu(self.window, option, *choices)
        self.alternate_staff = option
        drop_down.pack(side = LEFT, anchor = N)

    def change_staffer(self, token):
        try:
            new_staff_device = ild.staff_device.get(self.alternate_staff.get())
        except:
            new_staff_device = ild.staff_device.get(self.alternate_staff)
        self.home.change_staff_for_task(token,self.device_id,new_staff_device)
    def clear_window(self):
        """This function clears the window that it is given allowing it to be a blank canvas before the window
        is repopulated with different widgets
        """
        for widget in self.window.winfo_children():
            widget.destroy()