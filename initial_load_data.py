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
        ('EmptyEntry', '~19'), ('DropDown', '~17', 'c117'), ('Button', '~20')), None, ({'call': [['p0001', 3, 3]]})],
    3: ['st_1', '~36', 'UI', ('PersonHeader', 'TaskHeader',
        ('Fixed', '~17'), ('DropDown', '~2', 'c102'), ('Button', '~20')), None, ({'call': [['p0001', 4, 3]]})],
    4: ['st_1', '~18', 'UI', ('PersonHeader', 'TaskHeader',
        ('Fixed', '~2'), ('CheckBoxes', '~18', 'c118'), ('Button', '~20')), None, ({})]
    # 1: ['st_1', '~34', 'UI', ('PersonHeader', 'TaskHeader',
    #                           ('ModifyEntry', '~16'), ('Button', '~20')), None, ({'call': [['p0001', 2, 3]]})],
    # 2: ['st_1', '~35', 'UI', ('PersonHeader', 'TaskHeader',
    #                           ('EmptyEntry', '~19'), ('DropDown', '~17', 'c117'), ('Button', '~20')), None,
    #                           ({'call': [['p0001', 3, 3]]})],
    # 3: ['st_1', 'calc BMI', 'murphy', 'murphy005', None, ({'call': [['p0001', 4, 3]]})],
    # 4: ['st_1', '~36', 'UI', ('PersonHeader', 'TaskHeader',
    #                           ('Fixed', '~17'), ('DropDown', '~2', 'c102'), ('Button', '~20')), None,
    #     ({'call': [['p0001', 5, 3]]})],
    # 5: ['st_1', '~18', 'UI', ('PersonHeader', 'TaskHeader',
    #                           ('Fixed', '~2'), ('CheckBoxes', '~18', 'c118'), ('Button', '~20')), None, ({})]
    # 6: ['st_1', 'diabetes screen', 'decision', 'spec', None, ()]
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
    1: '~24', 2: '~25', 3: '~26', 4: '~27'
    }

protostep_staff = {     # putting the staff type assignments for protocol p0001 into the protostep_staff  dictionary
    'p0001': p0001_staff
    }

staffers = {                # a primitive dictionary for staffers that will do for now
    's001': {'~1': 'Joe', '~23': '~24', '~100': '~101'},
    's002': {'~1': 'Jose', '~23': '~25', '~100': '~102'},
    's003': {'~1': 'Maria', '~23': '~26', '~100': '~101'},
    's004': {'~1': 'Mary', '~23': '~27', '~100': '~102'},
    's005': {'~1': 'Ally', '~23': '~24', '~100': '~101'},
    's006': {'~1': 'Mack', '~23': '~25', '~100': '~102'},
    's007': {'~1': 'Natasha', '~23': '~26', '~100': '~101'},
    's008': {'~1': 'Doreen', '~23': '~27', '~100': '~102'}
    }

# these next two rows to be dynamically generated when we have staff login in place.
staff_device = {'s001': 123, 's002': 234, 's003': 345, 's004': 456}
device_staff = {123: 's001', 234: 's002', 345: 's003', 456: 's004'}

staffer_login_info = {'s001': ['pass', False], 's002': ['pass', False],
                      's003': ['pass', False], 's004': ['pass', False],
                      's005': ['pass', False], 's006': ['pass', False],
                      's007': ['pass', False], 's008': ['pass', False]
                      }

# PERSON RELATED DATA ###############################################################
entrants = [['07:02', 'pers101'],  ['07:10', 'pers102'],  ['07:20', 'pers103'],   # what time they enter the clinic
            ['07:30', 'pers104'],  ['07:45', 'pers105'],  ['08:00', 'pers106']]

# adat is a dictionary where the key is the person, and then each person is a dictionary
# where the key is k, and value is a list with lists (inner lists) within.
# each of the inner lists has the following seven fields.
# adatm[0], entity[1], parent[2], vt[3], v[4], units[5], event_dts[6]
adat = {
    'pers101': {
        '~1': [[101, None, None, 's', 'Tina', None, 1603824276.5]],
        '~14': [[102, None, None, '~', '~22', None, 1603824276.5]],
        '~15': [[103, None, None, 'f', 40, '~40', 1603824276.5]],
        '~16': [[104, None, None, 's', '202-888-5431', None, 1603824276.5]],
        '~17': [[105, None, None, '~', '~28', None, 1603824276.5]],
        '~2': [[116, None, None, '~', '~5', None, 1603824276.5]],
        '~45': [[116, None, None, 'f', 1.7, '~46', 1603800000.5]],
        '~19': [[113, None, None, 'f', 70, '~41', 1603800000.5],
                [114, None, None, 'f', 71, '~41', 1603812000.5],
                [115, None, None, 'f', 72, '~41', 1603824276.5]]
    },
    'pers102': {
        '~1': [[107, None, None, 's', 'Tony', None, 1603824276.5]],
        '~14': [[108, None, None, '~', '~21', None, 1603824276.5]],
        '~15': [[109, None, None, 'f', 35, '~40', 1603824276.5]],
        '~16': [[110, None, None, 's', '703-999-3341', None, 1603824276.5]],
        '~17': [[111, None, None, '~', '~29', None, 1603824276.5]],
        '~2': [[112, None, None, '~', '~30', None, 1603824276.5]],
        '~45': [[116, None, None, 'f', 1.9, '~46', 1603800000.5]],
        '~19': [[116, None, None, 'f', 75, '~41', 1603800000.5],
                [117, None, None, 'f', 74, '~41', 1603812000.5],
                [118, None, None, 'f', 75, '~41', 1603824276.5]]
    },
    'pers103': {
        '~1': [[121, None, None, 's', 'Bill', None, 1603824276.5]],
        '~14': [[122, None, None, '~', '~21', None, 1603824276.5]],
        '~15': [[123, None, None, 'f', 21, '~40', 1603824276.5]],
        '~16': [[124, None, None, 's', '703-999-8888', None, 1603824276.5]],
        '~17': [[125, None, None, '~', '~29', None, 1603824276.5]],
        '~2': [[126, None, None, '~', '~30', None, 1603824276.5]],
        '~45': [[116, None, None, 'f', 2.0, '~46', 1603800000.5]],
        '~19': [[127, None, None, 'f', 88, '~41', 1603800000.5],
                [128, None, None, 'f', 92, '~41', 1603812000.5],
                [129, None, None, 'f', 94, '~41', 1603824276.5]]
    },
    'pers104': {
        '~1': [[131, None, None, 's', 'Mary', None, 1603824276.5]],
        '~14': [[132, None, None, '~', '~22', None, 1603824276.5]],
        '~15': [[133, None, None, 'f', 66, '~40', 1603824276.5]],
        '~16': [[134, None, None, 's', '703-999-1111', None, 1603824276.5]],
        '~17': [[135, None, None, '~', '~29', None, 1603824276.5]],
        '~2': [[136, None, None, '~', '~30', None, 1603824276.5]],
        '~45': [[116, None, None, 'f', 1.8, '~46', 1603800000.5]],
        '~19': [[137, None, None, 'f', 44, '~41', 1603800000.5],
                [138, None, None, 'f', 43, '~41', 1603812000.5],
                [139, None, None, 'f', 42, '~41', 1603824276.5]]
    },
    'pers105': {
        '~1': [[141, None, None, 's', 'Lisa', None, 1603824276.5]],
        '~14': [[142, None, None, '~', '~22', None, 1603824276.5]],
        '~15': [[143, None, None, 'f', 35, '~40', 1603824276.5]],
        '~16': [[144, None, None, 's', '703-999-3341', None, 1603824276.5]],
        '~17': [[145, None, None, '~', '~29', None, 1603824276.5]],
        '~2': [[146, None, None, '~', '~30', None, 1603824276.5]],
        '~45': [[116, None, None, 'f', 1.6, '~46', 1603800000.5]],
        '~19': [[147, None, None, 'f', 54, '~41', 1603800000.5],
                [148, None, None, 'f', 56, '~41', 1603812000.5],
                [149, None, None, 'f', 53, '~41', 1603824276.5]]
    },
    'pers106': {
        '~1': [[141, None, None, 's', 'Neal', None, 1603824276.5]],
        '~14': [[142, None, None, '~', '~21', None, 1603824276.5]],
        '~15': [[143, None, None, 'f', 18, '~40', 1603824276.5]],
        '~16': [[144, None, None, 's', '612-926-0000', None, 1603824276.5]],
        '~17': [[145, None, None, '~', '~29', None, 1603824276.5]],
        '~2': [[146, None, None, '~', '~30', None, 1603824276.5]],
        '~45': [[116, None, None, 'f', 1.8, '~46', 1603800000.5]],
        '~19': [[147, None, None, 'f', 54, '~41', 1603800000.5],
                [148, None, None, 'f', 56, '~41', 1603812000.5],
                [149, None, None, 'f', 59, '~41', 1603824276.5]]
    }
}
