# get_responsible_staff.py
import initial_load_data as ild
from icecream import ic


def get_staff_type(protocol, step):  # get the staff_type who is responsible for the step in the protocol
    staffer_type = ild.protostep_staff[protocol][step]
    return staffer_type


# when we are getting a staffer with this still give a staffer who is trying to reassign a task
def get_staffer(staff_type):  # get the staffer who is responsible for the step in the protocol
    for s in ild.staffers:  # currently gets the first staffer who matches on staff_type, much more to be done!
        if ild.staffers[s]['~23'] == staff_type:
            return s


def get_device_out(protocol, step):
    staff_type = get_staff_type(protocol, step)  # get the responsible staff_type
    staffer = get_staffer(staff_type)  # get the responsible staffer based on staff_type
    device_out = ild.staff_device[staffer]  # then get the device_out based on the staffer
    return device_out

# for rest of staffers staff_type, current_staffer
def get_other_staffers(staff_type, current_staffer, list):  # get the staffer who is responsible for the step in the protocol
    staff_choices = []
    for s in ild.staffers:  # currently gets the first staffer who matches on staff_type, much more to be done!
        if ild.staffers[s]['~23'] == staff_type and s is not current_staffer:
            if not list:
                return s
            else:
                staff_choices.append(s)
    return staff_choices