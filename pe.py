# pe.py

import datetime
import random
import initial_load_data as ild
import get_responsible_staff as grs
import murphy
import simulation_time as sim_time

# global sim_time
#
#
# def set_sim_time(s_time):
#     """This function creates a reference to the simulation time module used for reporting current simulatio time
#     :param s_time: a reference to the system_time module
#     :type s_time: module"""
#     global sim_time
#     sim_time = s_time

# START - function to process the calls for UI (or other external agent)  ######
def process_call_for_pe_queues(call, pdata_appendum, pe_outs, pe_waits):
    pe_out, pe_wait = create_pe_queues_additions(pdata_appendum, call)  # call function to get pe_out & pe_wait
    pe_outs[pe_out[0]][pe_out[1]] = pe_out[2]    # this adds the new pe_out to pe_outs
    if pe_wait[1]:    # this if because without it when a protocol ended we'd get a empty pe_wait written anyway
        pe_waits[pe_wait[0]] = pe_wait[1]        # this adds the new pe_wait to pe_waits

# ### END - function to process the calls for UI (or other external agent)  ######

# START - function to create a pe_out and a pe_wait - called by process_call_for_pe_queues and is part of PE #####
def create_pe_queues_additions(pdata_appendum, protostep):
    # global sim_time
    # for reference pdata_appendum = [pdatm[0], person[1], entity[2], caller[3],
    #                                 protocol[4], step[5], thread[6], record_dts[7], datas[8]]
    protocol, step, priority = protostep[0], protostep[1], protostep[2]
    token = random.randint(1000000000000001, 9999999999999999)   # the token is used later to match a pe_in (from the UI) with its corresponding pe_wait
    # the next fields are read directly from pdata_addendum
    caller = pdata_appendum[0]
    person = pdata_appendum[1]
    entity = pdata_appendum[2]
    thread = pdata_appendum[6]
    if step == 1:   # if this is the first step in a protocol it needs a new thread number
        thread = random.randint(100001, 999999)
    # the next four are from the protocol specification for that step
    task = ild.protocols[protocol][step][1]
    task_type = ild.protocols[protocol][step][2]
    spec = ild.protocols[protocol][step][3]
    flow = ild.protocols[protocol][step][5]
    # then a few more loose fields
    time_posted = sim_time.get_time_stamp()
    time_reposted = None    # placeholder until this functionality is developed
    status = '~4522'        # placeholder until this functionality is developed
    log = None              # placeholder until this functionality is developed
    # here we run the grs function to get what device to write to
    device_out = str(grs.get_device_out(protocol, step))
    # and now we compile the two items to be returned
    pe_out = [device_out, token, [person, entity, priority, task, task_type, spec, time_posted, time_reposted, status, log]]
    pe_wait = [token, [device_out, log, time_posted, person, entity, caller, protocol, step, thread, flow]]
    return pe_out, pe_wait
# ### END - function to create a pe_out and a pe_wait - called by process_call_for_pe_queues and is part of PE ####


# START - function to add to adat from pdata with relevant data #####
def datas_expansion(person, entity, parent, datum):
    global sim_time
    adatm = random.randint(1001, 9999)  # this to be replaced by get global next datm call
    k = datum['k']
    vt = datum['vt']
    v = datum['v']
    units = datum['units']
    event_dts = sim_time.get_time_stamp()   # someday beyond more complex for microbio etc.
    adat_ = [person, k, [adatm, entity, parent, vt, v, units, event_dts]]
    try:
        ild.adat[adat_[0]][adat_[1]].append(adat_[2])
    except:
        ild.adat[adat_[0]][adat_[1]] = [adat_[2]]
# ### END - function to add to adat from pdata with relevant data #####


# START - PE - the Protocol Engine #############################################################################
# Effectively "PE" is looking at two different pe_ins lists.
# pe_ins_sol are solicted inputs, have an associated pe_wait in pe_waits, and can carry datas for writing to adat
# pe_ins_unsol are unsolicted inputs, with a different format, no associated pe_wait, and carry no datas for adat

def protocol_engine(pe_ins_sol, pe_waits, pe_ins_unsol, pe_outs, pdata, adat):
    global sim_time
    pdata_appendums = []
    calls_list = []
    pe_int_calls = []
    pe_ext_calls = []

    if pe_ins_sol:  # solicited inputs
        while pe_ins_sol:
            pe_in_sol = pe_ins_sol.pop(0)
            token_in = pe_in_sol[0]
            pe_wait = pe_waits[token_in]
            # Here we gather the data to append a new row to pdata
            pdatm = random.randint(100001, 999999)  # this to be replaced by get global next datm call
            person = pe_wait[3]
            entity = pe_wait[4]
            caller = pe_wait[5]
            protocol = pe_wait[6]
            step = pe_wait[7]
            thread = pe_wait[8]
            datas = pe_in_sol[2]
            record_dts = sim_time.get_time_stamp()
            actor = pe_in_sol[2].get('actor')      # why isn't this going somewhere????????????????????????????
            pdata_appendum = [pdatm, person, entity, caller, protocol, step, thread, record_dts, datas]
            pdata_appendums.append(pdata_appendum)
            calls = pe_wait[9].get('call')
            if calls:  # there can be more than one call
                for call in calls:
                    calls_list.append([call, pdata_appendum, pe_outs, pe_waits])
            # And finally need to remove the lines processed from pe_outs and pe_waits
            del pe_outs[pe_waits[token_in][0]][token_in]
            del pe_waits[token_in]


    if pe_ins_unsol:  # unsolicited inputs
        while pe_ins_unsol:
            pe_in_unsol = pe_ins_unsol.pop(0)
            token_in = pe_in_unsol[0]
            # Here we compile the data to append a new row to pdata
            pdatm = random.randint(100001, 999999)  # this to be replaced by get global next datm call
            person = pe_in_unsol[2].get('person')
            entity = pe_in_unsol[2].get('entity')
            caller = None  # since there is no caller row
            protocol = pe_in_unsol[0]   # for unsolicited inputs pe_in[0] will be the name of the unsolicited protocol
            step = 1  # hmm - will it always be 1?
            thread = random.randint(100001, 999999)  # this to be replaced by get global next thread call
            datas = None  # Do not expect unsolicited pe_ins to carry data to be written to adat (could be dangerous)
            record_dts = sim_time.get_time_stamp()
            # and then create the row to append and append
            pdata_appendum = [pdatm, person, entity, caller, protocol, step, thread, record_dts, datas]
            pdata_appendums.append(pdata_appendum)
            calls = pe_in_unsol[2].get('call')
            if calls:
                for call in calls:
                    calls_list.append([call, pdata_appendum, pe_outs, pe_waits])
            # And finally need to remove the lines processed from pe_outs and pe_waits
            if token_in != 'ip01':
                del pe_outs[pe_waits[token_in][0]][token_in]
                del pe_waits[token_in]

    if pdata_appendums:
        for pdat in pdata_appendums:
            pdata.append(pdat)
            if pdat[8]:
                datums = pdat[8].get('data')  # if KVP data for expansion it is added to adat
                if datums:  # we gather the additional data needed to append to adat
                    for datum in datums:
                        datas_expansion(pdat[1], pdat[2], pdat[0], datum)


    if calls_list:
        for call in calls_list:  #  now we need to get what they are calling
            call_type = ild.protocols[call[0][0]][1][2]
            if call_type == 'murphy':
                spec = ild.protocols[call[0]][call[1]][3]
                result = murphy.murphy(person, spec)
                # now we need to write to pdata and adat, then go on to the next line
            elif call_type == 'UI':
                process_call_for_pe_queues(call[0], call[1], call[2], call[3])
            elif call_type == 'decisioning':
                pass
            else:
                pass
