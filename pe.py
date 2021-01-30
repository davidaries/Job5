""" pe.py is the protocol engine, it is heart of keeping things happening within protocols, going step by step,
    and sometimes forking or branching or passing along to other protocols.

"""
import datetime
import random
import initial_load_data as ild
import working_data as wd
import get_responsible_staff as grs
import murphy
import decisioning
import simulation_time as sim_time
from icecream import ic


# START - functions to process the calls for UI (or other external agent)  ######
def process_call_for_pe_queues(call, pdata_appendum, pe_outs, pe_waits):
    """ Process calls to made to UI (and perhaps in future to external agents)

    :param call:
    :type call:
    :param pdata_appendum:
    :type pdata_appendum:
    :param pe_outs:
    :type pe_outs:
    :param pe_waits:
    :type pe_waits:
    :return:
    """
    pe_out, pe_wait = create_pe_queues_additions(pdata_appendum, call)  # call function to get pe_out & pe_wait
    pe_outs[pe_out[0]][pe_out[1]] = pe_out[2]    # this adds the new pe_out to pe_outs
    if pe_wait[1]:    # this if because without it when a protocol ended we'd get a empty pe_wait written anyway
        pe_waits[pe_wait[0]] = pe_wait[1]        # this adds the new pe_wait to pe_waits


def create_pe_queues_additions(pdata_appendum, protostep):
    """ called by process_call_for_pe_queues to create the additions for two pe queues: pe_out and pe_wait

    :param pdata_appendum:
    :type pdata_appendum:
    :param protostep:
    :type protostep:
    :return:
    """
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
# ### END - functions to process the calls for UI (or other external agent)  ######


# START - function to add to adat from pdata with relevant data #####
def datas_expansion(person, entity, parent, datum):
    """

    :param person:
    :type person:
    :param entity:
    :type entity:
    :param parent:
    :type parent:
    :param datum:
    :type datum:
    :return:
    """
    global sim_time
    adatm = random.randint(1001, 9999)  # this to be replaced by get global next datm call
    k = datum['k']
    vt = datum['vt']
    v = datum['v']
    units = datum['units']
    event_dts = sim_time.get_time_stamp()   # someday beyond more complex for microbio etc.
    adat_ = [person, k, [adatm, entity, parent, vt, v, units, event_dts]]
    try:
        wd.adat[adat_[0]][adat_[1]].append(adat_[2])
    except:
        wd.adat[adat_[0]][adat_[1]] = [adat_[2]]
# ### END - function to add to adat from pdata with relevant data #####


# START - PE - the Protocol Engine #############################################################################
# Effectively "PE" is looking at two different pe_ins lists.
# pe_ins_sol are solicted inputs, have an associated pe_wait in pe_waits, and can carry datas for writing to adat
# pe_ins_unsol are unsolicted inputs, with a different format, no associated pe_wait, and carry no datas for adat

def protocol_engine(pe_ins_sol, pe_waits, pe_ins_unsol, pe_outs, pdata):
    """

    :param pe_ins_sol:
    :type pe_ins_sol:
    :param pe_waits:
    :type pe_waits:
    :param pe_ins_unsol:
    :type pe_ins_unsol:
    :param pe_outs:
    :type pe_outs:
    :param pdata:
    :type pdata:
    :return:
    """
    global sim_time
    pdata_appendums = []
    calls_list = []

    if pe_ins_sol:  # solicited inputs
        ic(pe_ins_sol)
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
                    calls_list.append([call, pdata_appendum, pe_outs, pe_waits])    # Jan 22 wondering if we need to / should send pe_outs and pe_waits to the call_list every time
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
                    calls_list.append([call, pdata_appendum, pe_outs, pe_waits])     # Jan 22 wondering if we need to / should send pe_outs and pe_waits to the call_list every time
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
    pdata_appendum, pdata_appendums = [], []

    if calls_list:
        while calls_list:
            call = calls_list.pop(0)  # now we need to get what they are calling
            proto_ = call[0][0]
            step_ = call[0][1]
            call_type = ild.protocols[proto_][step_][2]
            if call_type == 'murphy':
                spec = ild.protocols[proto_][step_][3]
                datas = murphy.murphy(person, spec)
                calls = ild.protocols[proto_][step_][5].get('call')
                # now we need to create the line to write to pdata
                pdatm = random.randint(100001, 999999)
                entity = call[1][2]
                caller = call[1][0]
                protocol = proto_
                step = step_
                thread = call[1][6]
                record_dts = sim_time.get_time_stamp()
                pdata_appendum = [pdatm, person, entity, caller, protocol, step, thread, record_dts, datas]
                pdata.append(pdata_appendum)   # append to pdata
                datas_expansion(person, entity, pdatm, datas['data'][0])  # call expansion of murphy-created to adat
                calls_from_murphy = ild.protocols[proto_][step_][5].get('call')  # now time to think routing
                if calls_from_murphy:   # if the murphy step had calls specified
                    for call_fm in calls_from_murphy:
                        call_type_fm = ild.protocols[call_fm[0]][call_fm[1]][2]    # what is the call_type from murphy?
                        if call_type_fm == 'UI':
                            process_call_for_pe_queues(call_fm, pdata_appendum, pe_outs, pe_waits)  # send to UI process
                        elif call_type_fm in ['murphy', 'decisioning']:
                            calls_list.append([call_fm, pdata_appendum, pe_outs, pe_waits])  # append here for process
            elif call_type == 'UI':                # send to UI process
                process_call_for_pe_queues(call[0], call[1], call[2], call[3])
            elif call_type == 'decisioning':
                existing_calls_for_step = ild.protocols[proto_][step_][5].get('call')  # get any pre-specified steps
                decision_spec = ild.protocols[proto_][step_][3]          # get the decision spec
                decided_ = decisioning.decision(person, decision_spec)   # get a decision: new protocol/step(s) to call
                if decided_:                              # append the new calls of any pre-existing calls
                    decided = decided_.get('call')[0]
                    try:
                        existing_calls_for_step.append(decided)
                    except:
                        existing_calls_for_step = decided
                new_flows = existing_calls_for_step
                for new_flow in new_flows:                # for each call append it here.
                    calls_list.append([new_flow, pdata_appendum, pe_outs, pe_waits])
            else:                                       # at some future point there will be other call_types
                pass
