# controller.py
import initial_load_data as ild
import pe
import working_data
import simulation_time
# import sim_main_window
from tkinter import *
import language_dictionary as ld
# import controller
from sim_staff_window_manager import home_screen
from icecream import ic
# START - setting things up ##########################################################
# Some empty data fields to be used
# pdata = []
# pe_ins_sol = []  # protocol engine inputs
# pe_ins_unsol = []
# pe_outs = {}  # protocol engine outputs
# pe_waits = {}  # protocol engine waits
# pe_outs['123'] = {}  # when a staff member signs in with a device the device needs an empty dictionary
# pe_outs['234'] = {}  # these four pe_outs rows will go away when we have a staff sign in process
# pe_outs['345'] = {}
# pe_outs['456'] = {}
#
# time_label = None
# global timer
#
#
# def set_global_timer(timer_ref):
#     """This function creates a reference to the simulation time module used for reporting current simulation time
#     :param timer_ref: a reference to the system_time module
#     :type timer_ref: module"""
#     global timer
#     timer = timer_ref
#     pe.set_sim_time(timer_ref)

root = Tk()

def check_entrant():
    """This function checks to see if any people are arriving and the current current time.  If there are any, they
    are added to pe_ins_unsol to be processed by the PE"""
    time_str= simulation_time.get_formatted_time().strftime("%H:%M")
    for ent in ild.entrants:
        if time_str == ent[0]:
            working_data.pe_ins_unsol.append(['ip01', simulation_time.get_time_stamp(),
                                 {'person': ent[1], 'entity': None, 'actor': '~self', 'call': [['p0001', 1, 3]]}])


# def start(root):
# START - simulation ##########################################################
def simulate():
    if not simulation_time.pause():
        # Now let's run the protocol engine
        pe.protocol_engine(working_data.pe_ins_sol, working_data.pe_waits, working_data.pe_ins_unsol,
                           working_data.pe_outs, working_data.pdata, ild.adat)
        check_entrant()
    # ic(working_data.pe_outs)
    root.after(1000, simulate)
simulate()

# ### END - simulation ##########################################################
def poll_tasks(device_id):
    """This returns a list of tasks to be displayed in a staffer's window
    :param device_id: unique id of a staffers device
    :type device_id: str
    :return: the tasks to be completed by the staffer
    :rtype: list"""
    return working_data.pe_outs.get(str(device_id))


def return_completion(token, data_return):
    """This function allows the staffers to return data to the controller to be processed by the controller once
    they have been added to pe_ins_sol list
    :param token: the token of the task in question
    :type token: int
    :param data_return: the data returned from the UI
    :type data_return: list"""
    if token:
        working_data.pe_ins_sol.append([token, simulation_time.get_time_stamp(), {'data': data_return}])     ########################################## ? data as ild?


# START - PRINTING CURRENT DATA STATUS - ONLY FOR REVIEW/TROUBLESHOOTING ##########
def summary():
    print('\n========= Summary data at this point =========================================================')
    print('\npdata =', working_data.pdata)
    for h in working_data.pdata:
        print(h)

    print('\npe_outs =', working_data.pe_outs)
    dev_outs = working_data.pe_outs.keys()
    for i in working_data.pe_outs:
        print('device_out = ', i)
        for ii in working_data.pe_outs[i]:
            print('  ', ii, working_data.pe_outs[i][ii])

    print('\npe_waits =', working_data.pe_waits)
    for j in working_data.pe_waits:
        print(j, working_data.pe_waits[j])

# ### END - PRINTING CURRENT DATA STATUS - ONLY FOR REVIEW/TROUBLESHOOTING ##########
def setup_ui():
    base_language = '~101'

    # root = Tk()

    root.title(ld.get_text_from_dict(base_language, '~11'))  # title for window
    root.geometry('430x100+0+0')  # main window geometry
    time_lbl = Label(root, text="test", font='Helvetica 18 bold')
    time_lbl.grid(row=0, column=1)

    # create Log Window
    log_window = Toplevel(root)
    log_window.title(ld.get_text_from_dict(base_language, '~13'))
    log_window.geometry("600x300+0+500")
    log_window.withdraw()
    staffers_home = home_screen(root, log_window)
    staffers_home.add_home(staffers_home)

    simulation_time.clock(root, time_lbl)

    btn_pause = Button(root, text=ld.get_text_from_dict('~101', '~6'), fg="black", bg="gray",
                       command=lambda: simulation_time.stop_clock(True),
                       height=1, width=13)
    btn_unpause = Button(root, text=ld.get_text_from_dict('~101', '~7'), fg="black", bg="gray",
                         command=lambda: simulation_time.stop_clock(False), height=1, width=13)
    btn_sum = Button(root, text='Current Status', fg="black", bg="gray",
                     command=summary, height=1, width=13)
    btn_login_page = Button(root, text='login', fg="black", bg="gray",
                            command=staffers_home.login_screen, height=1, width=13)
    test = Button(root, text='test', fg="black", bg="gray",
                  command=staffers_home.login_all, height=1, width=13)
    btn_pause.grid(column=0, row=1)
    btn_sum.grid(column=1, row=1)
    btn_unpause.grid(column=2, row=1)
    btn_login_page.grid(column=0, row=2)
    test.grid(column=2, row=2)
    logPadding = 25

    root.mainloop()

setup_ui()
simulate()