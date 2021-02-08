import initial_load_data as ild
import simulation_time
import working_data as wd
import get_responsible_staff as grs
from icecream import ic


def update_log(token, device_id, status, comments, priority):
    time = simulation_time.get_time_stamp()
    user = ild.device_staff.get(device_id)
    wd.pe_outs.get(str(device_id))[token][2] = priority
    log_data = {'user': user, 'time': time, 'status': status, 'priority': priority, 'comments': comments}
    if token in wd.log_dict:
        wd.log_dict.get(token).append(log_data)
    else:
        wd.log_dict[token] = [log_data]
    wd.token_status_dict[token] = status


def change_staffer(token, current_staffer, alternate_staffer, status):
    new_staff_device = None
    try:
        if alternate_staffer[0] == 's':
            new_staff_device = ild.staff_device.get(alternate_staffer)
    except:
        name = alternate_staffer.get()
        new_staff_device = ild.staff_device.get(staff_id_from_name(name))

    wd.pe_waits.get(token)[0] = str(new_staff_device)  # may change with dict implementation
    pe_out = wd.pe_outs[str(current_staffer)].pop(token)
    pe_out[8] = status #update status with forward or reassign
    wd.pe_outs.get(str(new_staff_device))[token] = pe_out


def return_data(token, data_return):
    """This function sends the appropriate data for the token in question to be processed by the controller
    :param token: unique token id used for tasks
    :type token: int
    :param data_return: list of the corresponding data for the token
    :type data_return: list"""
    # ic(token, data_return)
    ic('returning',token)
    flow_info = None
    if token in wd.flow_data:
        flow_info = wd.flow_data.get(token)
    wd.pe_ins_sol.append([token, simulation_time.get_time_stamp(),
                          {'data': data_return, 'log': wd.log_dict.get(token), 'flow': flow_info}])


def get_tasks(device_id):
    """This function returns the current list of tasks for a staffer based on their device_id
    :param device_id: a unique id for the staffers device
    :type device_id: str"""
    return wd.pe_outs.get(str(device_id))


def add_flow_info(token, flow):
    wd.flow_data[token] = flow


def get_possible_staff(id_current_staff, is_list):
    current_staffer = ild.device_staff.get(id_current_staff)
    staff_type = ild.staffers.get(str(current_staffer)).get('~23')
    return grs.get_other_staffers(staff_type, current_staffer, is_list)


def staff_id_from_name(name):
    for staff in ild.staffers:
        if ild.staffers.get(staff).get('~1') == name:
            return staff


def name_from_staff_id(staff_id):
    return ild.staffers.get(staff_id).get('~1')


def pause_tasks(staff_id, token, status):
    wd.pe_outs.get(str(staff_id)).get(token)[8] = status
