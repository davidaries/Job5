# controller.py
import initial_load_data as ild
import pe

# START - setting things up ##########################################################
# Some empty data fields to be used
pdata = []
pe_ins_sol = []  # protocol engine inputs
pe_ins_unsol = []
pe_outs = {}  # protocol engine outputs
pe_waits = {}  # protocol engine waits
pe_outs['123'] = {}  # when a staff member signs in with a device the device needs an empty dictionary
pe_outs['234'] = {}  # these four pe_outs rows will go away when we have a staff sign in process
pe_outs['345'] = {}
pe_outs['456'] = {}

time_label = None
global timer


def set_global_timer(timer_ref):
    """This function creates a reference to the simulation time module used for reporting current simulation time
    :param timer_ref: a reference to the system_time module
    :type timer_ref: module"""
    global timer
    timer = timer_ref
    pe.set_sim_time(timer_ref)


def check_entrant():
    """This function checks to see if any people are arriving and the current current time.  If there are any, they
    are added to pe_ins_unsol to be processed by the PE"""
    global timer
    time_str= timer.get_formatted_time().strftime("%H:%M")
    for ent in ild.entrants:
        if time_str == ent[0]:
            pe_ins_unsol.append(['ip01', timer.get_time_stamp(),
                                 {'person': ent[1], 'entity': None, 'actor': '~self', 'call': [['p0001', 1, 3]]}])


def start(root):
    # START - simulation ##########################################################
    def simulate():
        if not timer.pause():
            # Now let's run the protocol engine
            pe.protocol_engine(pe_ins_sol, pe_waits, pe_ins_unsol, pe_outs, pdata, ild.adat)
            check_entrant()
        root.after(1000, simulate)
    simulate()

# ### END - simulation ##########################################################
def poll_tasks(device_id):
    """This returns a list of tasks to be displayed in a staffer's window
    :param device_id: unique id of a staffers device
    :type device_id: str
    :return: the tasks to be completed by the staffer
    :rtype: list"""
    return pe_outs.get(str(device_id))


def return_completion(token, data_return):
    """This function allows the staffers to return data to the controller to be processed by the controller once
    they have been added to pe_ins_sol list
    :param token: the token of the task in question
    :type token: int
    :param data_return: the data returned from the UI
    :type data_return: list"""
    global timer
    if token:
        pe_ins_sol.append([token, timer.get_time_stamp(), {'data': data_return}])     ########################################## ? data as ild?


# START - PRINTING CURRENT DATA STATUS - ONLY FOR REVIEW/TROUBLESHOOTING ##########
def summary():
    print('\n========= Summary data at this point =========================================================')
    print('\npdata =', pdata)
    for h in pdata:
        print(h)

    print('\npe_outs =', pe_outs)
    dev_outs = pe_outs.keys()
    for i in pe_outs:
        print('device_out = ', i)
        for ii in pe_outs[i]:
            print('  ', ii, pe_outs[i][ii])

    print('\npe_waits =', pe_waits)
    for j in pe_waits:
        print(j, pe_waits[j])

# ### END - PRINTING CURRENT DATA STATUS - ONLY FOR REVIEW/TROUBLESHOOTING ##########
