"""
This class is in charge of the main construction of the GUI for Job4
This involves the creation of multiple windows
A root window is created that displays the current time in the simulation.  This root windows also contains a pause
and unpause button (to pause and unpause the program), a button that prints a summary to the console, a button
that generates a login window for a staffer, and a test button that opens all staffer windows and logs them in

"""
from tkinter import *
import language_dictionary as ld
import controller
from home_screen import home_screen
from system_time import system_time

base_language = '~101'

root = Tk()

root.title(ld.get_text_from_dict(base_language, '~11'))  # title for window
root.geometry('430x100+0+0')  # main window geometry
time_lbl = Label(root, text= "test", font = 'Helvetica 18 bold')
time_lbl.grid(row=0,column=1)

# create Log Window
log_window = Toplevel(root)
log_window.title(ld.get_text_from_dict(base_language, '~13'))
log_window.geometry("600x300+0+500")
log_window.withdraw()

timer = system_time(root, time_lbl)
timer.clock()

control = controller
staffers_home = home_screen(root, log_window,control, timer)
staffers_home.add_home(staffers_home)
control.set_global_timer(timer)
control.start(root)

btn_pause = Button(root, text=ld.get_text_from_dict('~101', '~6'), fg="black", bg="gray",
                   command= lambda: timer.stop_clock(True),
                   height=1, width=13)
btn_unpause = Button(root, text=ld.get_text_from_dict('~101', '~7'), fg="black", bg="gray",
                     command= lambda: timer.stop_clock(False), height=1, width=13)
btn_sum = Button(root, text='Current Status', fg="black", bg="gray",
                     command= control.summary, height=1, width=13)
btn_login_page = Button(root, text = 'login', fg="black", bg="gray",
                        command=staffers_home.login_screen, height=1, width=13)
test = Button(root, text = 'test', fg="black", bg="gray",
                        command=staffers_home.login_all, height=1, width=13)
btn_pause.grid(column=0, row=1)
btn_sum.grid(column=1,row=1)
btn_unpause.grid(column=2, row=1)
btn_login_page.grid(column = 0, row =2)
test.grid(column = 2, row =2)
logPadding = 25


root.mainloop()
"""root.mainloop(): begins the visual execution of the program"""
