# controller.py
import initial_load_data as ild
import pe
import working_data as wd
import simulation_time
import sim_create_ui

from icecream import ic


# START - setting things up ##########################################################
# Things here previously are now set up in working data
def check_entrant():
    """This function checks to see if any people are arriving and the current current time.  If there are any, they
    are added to pe_ins_unsol to be processed by the PE"""
    time_str = simulation_time.get_formatted_time().strftime("%H:%M")
    for ent in ild.entrants:
        if time_str == ent[0]:
            wd.pe_ins_unsol.append(['ip01', simulation_time.get_time_stamp(),
                                              {'person': ent[1], 'entity': None, 'actor': '~self',
                                               'call': [['p0001', 1, 3]]}])


# START - simulation ##########################################################
def simulate():
    if not simulation_time.pause():
        # Now let's run the protocol engine
        pe.protocol_engine(wd.pe_ins_sol, wd.pe_ins_unsol, wd.pe_outs, wd.pe_waits, wd.pdata)
        check_entrant()
    simulation_time.root.after(1000, simulate)

######This code calls to set up the UI the sim time then begins the simulation
sim_create_ui.setup_ui()
simulation_time.clock()
simulate()
simulation_time.root.mainloop()# this must be included here (the 'mainloop' of the tk root) for the UI to function
                               # not sure if there is a better way to handle this


# ### END - simulation ##########################################################
def poll_tasks(device_id):
    """This returns a list of tasks to be displayed in a staffer's window
    :param device_id: unique id of a staffers device
    :type device_id: str
    :return: the tasks to be completed by the staffer
    :rtype: list"""
    return wd.pe_outs.get(str(device_id))


def return_completion(token, data_return):
    """This function allows the staffers to return data to the controller to be processed by the controller once
    they have been added to pe_ins_sol list
    :param token: the token of the task in question
    :type token: int
    :param data_return: the data returned from the UI
    :type data_return: list"""
    if token:
        wd.pe_ins_sol.append([token, simulation_time.get_time_stamp(), {
            'data': data_return}])  ########################################## ? data as ild?
