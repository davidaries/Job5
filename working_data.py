import simulation_time
from icecream import ic
pdata = []
pe_ins_sol = []  # protocol engine inputs
pe_ins_unsol = []
pe_outs = {}  # protocol engine outputs
pe_waits = {}  # protocol engine waits
pe_outs['123'] = {}  # when a staff member signs in with a device the device needs an empty dictionary
pe_outs['234'] = {}  # these four pe_outs rows will go away when we have a staff sign in process
pe_outs['345'] = {}
pe_outs['456'] = {}
log_dict = {}

def get_pe_outs(device_id):
    return pe_outs.get(str(device_id))

def return_completion(token, data_return):
    """This function allows the staffers to return data to the controller to be processed by the controller once
    they have been added to pe_ins_sol list
    :param token: the token of the task in question
    :type token: int
    :param data_return: the data returned from the UI
    :type data_return: list"""
    if token:
        pe_ins_sol.append([token, simulation_time.get_time_stamp(),
                           {'data': data_return}])


def add_to_log(token, txt):
    # basic log addition
    # ic(token)
    # ic(txt)
    if token in log_dict:
        log_dict.get(token).append(txt)
    else:
        log_dict[token] = [txt]

def get_log(token):
    return log_dict.get(token)