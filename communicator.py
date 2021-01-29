import initial_load_data as ild
import simulation_time
import working_data as wd

from icecream import ic


def update_log(token, device_id, status, comments, priority):
    time = simulation_time.get_time_stamp()
    user = ild.device_staff.get(device_id)
    wd.pe_outs.get(str(device_id))[token][2]=priority# only changes for token, not sure how to update pe with this info
    log_data = {'user': user, 'time': time, 'status': status, 'priority': priority, 'comments': comments}
    if token in wd.log_dict:
        wd.log_dict.get(token).append(log_data)
    else:
        wd.log_dict[token] = [log_data]
    wd.token_status_dict[token] = status


def change_staffer(token, current_staffer, alternate_staffer):
    try:
        new_staff_device = ild.staff_device.get(alternate_staffer.get())
    except:
        new_staff_device = ild.staff_device.get(alternate_staffer)
    # ic(new_staff_device)
    wd.pe_waits.get(token)[0] = str(new_staff_device)
    pe_out = wd.pe_outs[str(current_staffer)].pop(token)
    wd.pe_outs.get(str(new_staff_device))[token] = pe_out


def return_data(token, data_return):
    """This function sends the appropriate data for the token in question to be processed by the controller
    :param token: unique token id used for tasks
    :type token: int
    :param data_return: list of the corresponding data for the token
    :type data_return: list"""
    flow_info = None
    if token in wd.flow_data:
        flow_info = wd.flow_data.get(token)
    wd.pe_ins_sol.append([token, simulation_time.get_time_stamp(),
                          {'data': data_return, 'log': wd.log_dict.get(token), 'flow': flow_info}])
    # ic(wd.pe_ins_sol)
    # keep expanding on this dictionary to include final log and flow


def get_tasks(device_id):
    """This function returns the current list of tasks for a staffer based on their device_id
    :param device_id: a unique id for the staffers device
    :type device_id: str"""
    # ic(device_id)
    # ic(working_data.pe_outs.get(device_id))
    return wd.pe_outs.get(str(device_id))


def get_status(token):
    if token in wd.token_status_dict:
        return wd.token_status_dict.get(token)  # if there is a marked status return it
    else:
        return '~55'  # default to assingn dictionary value

def add_flow_info(token, flow):
    if token in wd.flow_data:
        wd.flow_data.get(token).append(flow)
    else:
        wd.flow_data[token] = [flow]
    #simplified
    #wd.flow_data[token] = flow