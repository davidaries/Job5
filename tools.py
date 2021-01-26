import working_data
import initial_load_data as ild
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

    print('\nadats =', ild.adat)
    for i in ild.adat:
        print('person = ', i)
        for ii in ild.adat[i]:
            print('  ', ii, ild.adat[i][ii])