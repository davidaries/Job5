# d2.py

import query


# BEGIN FUNCTIONS ###################################################

def evaluate_1test(value, crit):
    result = 'T' if eval(str(value[1]) + crit[0] + str(crit[1])) else 'F'
    # print('test = ', (str(value[1]) + crit[0] + str(crit[1])), 'result =', result)
    return result


def evaluate_2tests(value, crit):
    result = 'T' if (eval(str(value[1]) + crit[0] + str(crit[1])) and
                      eval(str(value[1]) + crit[2] + str(crit[3]))) else 'F'
    # print('test = ', (str(value[1]) + crit[0] + str(crit[1])), 'and', (str(value[1]) + crit[2] + str(crit[3])), 'result =', result)
    return result


# def evaluate_string_if(value, crit):
#     result = 'T' if eval(str(value[1]) + crit[0] + str(crit[1])) else 'F'
#     # print('test = ', (str(value[1]) + crit[0] + str(crit[1])), 'result =', result)
#     return result


# BEGIN DECISION_SPECS  ###################################################
spec_dict = {
    'BMI_d1':
    [[
        [[['~47']], 'float', [[' < ', 30], [' >= ', 30]]]
    ],
    [
        [['var11T', 'var12F'], None],
        [['var11F', 'var12T'], {'call': [['p0002', 1, 3]]}],
        ['missing', 'call missing_data_protocol']
    ]]
    }

# END DECISION_SPECS


def decision(person, d_spec):
    decision_spec = spec_dict.get(d_spec)
    var_values = []
    missed = 0
    vars_specs = decision_spec[0]
    for var_spec in vars_specs:
        if len(var_spec[0]) == 1:
            value = query.adat_person_key(person, var_spec[0][0][0])
        else:
            value = query.adat_person_key_options(person, var_spec[0][0], var_spec[0][1], var_spec[0][2], var_spec[0][3])
        if not value:
            value = 'missing'
            missed += 1
        var_values.append([var_spec[0], value])
    if missed > 0:
        return ('missing report', var_values)   # if any variables is missing we stop here and return the report
    # now we can evaluate each
    var_cycles = len(var_values)
    var_cycle = 0
    composite = []
    while var_cycle < var_cycles:
        zz = decision_spec[0][var_cycle]
        crit_cycles = len(decision_spec[0][var_cycle][2])
        crit_cycle = 0
        while crit_cycle < crit_cycles:
            ds = decision_spec[0][var_cycle][2][crit_cycle]
            if len(ds) == 2:
                result = evaluate_1test(var_values[var_cycle][1], ds)
            elif len(ds) == 4:
                result = evaluate_2tests(var_values[var_cycle][1], ds)
            else:
                result = None
                print('\n\nERROR LURKING- length of decision criteria not within range\n\n')
            coded_result = ['var' + str(var_cycle + 1) + str(crit_cycle + 1) + result]
            crit_cycle += 1
            composite = composite + coded_result
        var_cycle += 1
    # print('\n', person, composite)

    table = decision_spec[1]
    for tab in table:
        if tab[0] == composite:
            return tab[1]

# END FUNCTIONS



#
# # BEGIN THE PROGRAM ###################################################
#
# def decide(person, decision_spec):
#
#     flow = decision(person, decision_spec)
#     print(flow)
#
