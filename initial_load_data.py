"""initial_load_data.py is data to be used in this program
   In the future such data will be loaded from tables, not come from this module.

"""

# PROTOCOL TABLE DATA ###############################################################
# We will be loading from a protocol table, which has these fields
# protocol, step, step_type, description, task, task_type, spec, write, flow
# And and were creating protocol dictionary, which has these fields:
# step_type[0], task[1], task_type[2], spec[3], write[4], flow[5]

p0001 = {      # this is what protocol p0001 with its four steps will look like when loaded from the table
    1: ['st_1', '~34', 'UI', ('PersonHeader', 'TaskHeader',
        ('ModifyEntry', '~16'), ('Button', '~20')), None, ({'call': [['p0001', 2, 3]]})],
    2: ['st_1', '~35', 'UI', ('PersonHeader', 'TaskHeader',
        ('EmptyEntry', '~19', {'vt': 'f', 'range': [0.1, 250], 'units': '~41'}), ('DropDown', '~17', 'c117'), ('Button', '~20')), None, ({'call': [['p0001', 3, 3]]})],
    3: ['st_1', 'calc BMI', 'murphy', 'murphy005', None, ({'call': [['p0001', 4, 3]]})],
    4: ['st_1', 'diabetes screen', 'decisioning', 'BMI_d1', None, ({'call': [['p0001', 5, 3]]})],
    5: ['st_1', '~36', 'UI', ('PersonHeader', 'TaskHeader',
        ('Fixed', '~17'), ('DropDown', '~2', 'c102'), ('Button', '~20')), None, ({'call': [['p0001', 6, 3]]})],
    6: ['st_1', '~18', 'UI', ('PersonHeader', 'TaskHeader',
                              ('Fixed', '~2'), ('CheckBoxes', '~18', 'c118'), ('Button', '~20')), None, ({})]
    }

p0002 = {      # this is what protocol p0001 with its four steps will look like when loaded from the table
    1: ['st_1', '~18', 'UI', ('PersonHeader', 'TaskHeader',
        ('Fixed', '~2'), ('CheckBoxes', '~18', 'c119'), ('Button', '~20')), None, ({})]
    }

ip01 = {       # this is what the intake protocol ip-1 with its one step will look like when loaded from the table
    1: ['st_1', '~ip01_task', '~ip01_task_type', None, None, ({'call': [['p0001', 1, 3]]})]
    }

protocols = {      # here we create the protocols dictionary and load the two protocols into it.
    'p0001': p0001,
    'p0002': p0002,
    'ip01': ip01
    }

choices = {    # What to display in UI as choices. True appears in short list, False only in the complete list.
    'c117': [['~28', True], ['~29', True]],
    'c102': [['~5', True], ['~30', True], ['~37', False], ['~38', False], ['~39', False]],
    'c118': [['~31', True], ['~32', True]],
    'c119': [['~44', True]]
    }

# STAFFING RELATED TABLE DATA ###############################################################
p0001_staff = {     # assigning a staff type to each step in protocol p0001
    1: '~24', 2: '~25', 5: '~26', 6: '~27'
    }

p0002_staff = {     # assigning a staff type to each step in protocol p0001
    1: '~27'
    }

protostep_staff = {     # putting the staff type assignments for protocol p0001 into the protostep_staff  dictionary
    'p0001': p0001_staff,
    'p0002': p0002_staff
    }

staffers = {                # a primitive dictionary for staffers that will do for now
    's001': {'~1': 'Joe', '~23': '~24', '~100': '~101'},
    's002': {'~1': 'Jose', '~23': '~25', '~100': '~102'},
    's003': {'~1': 'Maria', '~23': '~26', '~100': '~101'},
    's004': {'~1': 'Mary', '~23': '~27', '~100': '~102'},
    's005': {'~1': 'Ally', '~23': '~24', '~100': '~102'},
    's006': {'~1': 'Mack', '~23': '~25', '~100': '~101'},
    's007': {'~1': 'Natasha', '~23': '~26', '~100': '~102'},
    's008': {'~1': 'Doreen', '~23': '~27', '~100': '~101'},
    's009': {'~1': 'Thomas', '~23': '~24', '~100': '~101'},
    's010': {'~1': 'Lauren', '~23': '~25', '~100': '~102'},
    's011': {'~1': 'Dennis', '~23': '~26', '~100': '~101'},
    's012': {'~1': 'Rachel', '~23': '~27', '~100': '~102'}
    }

# these next two rows to be dynamically generated when we have staff login in place.
staff_device = {'s001': 123, 's002': 234, 's003': 345, 's004': 456,
                's005': 567, 's006': 678, 's007': 789, 's008': 987,
                's009': 876, 's010': 765, 's011': 654, 's012': 543}
device_staff = {123: 's001', 234: 's002', 345: 's003', 456: 's004',
                567: 's005', 678: 's006', 789: 's007', 987: 's008',
                876: 's009', 765: 's010', 654: 's011', 543: 's0012'}

staffer_login_info = {'s001': ['pass', False], 's002': ['pass', False],
                      's003': ['pass', False], 's004': ['pass', False],
                      's005': ['pass', False], 's006': ['pass', False],
                      's007': ['pass', False], 's008': ['pass', False],
                      's009': ['pass', False], 's010': ['pass', False],
                      's011': ['pass', False], 's012': ['pass', False]
                      }

# PERSON RELATED DATA ###############################################################
entrants = [['07:02', 'pers101'],  ['07:40', 'pers102'],  ['07:45', 'pers103'],   # what time they enter the clinic
            ['08:00', 'pers104'],  ['08:15', 'pers105'],  ['08:30', 'pers106']]


# adat is a dictionary where the key is the person, and then each person is a dictionary
# where the key is k, and value is a list with lists (inner lists) within.
# each of the inner lists has the following seven fields.
# adatm[0], entity[1], parent[2], vt[3], v[4], units[5], event_dts[6]

