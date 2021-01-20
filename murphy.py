# murphy.py

"""
main idea is that something can call a murphy, to get a calculation or some logic
and the murphy gets the data it needs using query.py
then return value(s) to whatever called it

at some point review decisioning.xlsx - and maybe shrink it, revise rename it, ...
and is there anything still of value in murphy.docx?

Okay, a murphy can come in with options of last, earliest, latest. And that would be by each variable I guess

do we still have an issue of order of calling variables?
since murphy is handling them as a, b, c based on order received
we need to be sure that they come from the caller in that order
-- the UI that guides the user in building the call to murphy must do that.

think about how to call data that is relative to other data? Something that must follow something else.
today we're thinking that is done by querying for plenty of data, and then handling it inside the murphy

Many murphys simply take what it was specified maps_keys_values and do their thing
Other (future) murphys (e.g., diffdx) might just be called by the Murphy number and would have within them
(in a data table of some sort) the specs on data what data to call.

On units:
- Some murphys may need conversion to different units before use (e.g., BMI)
- for those, when the values are pulled in, there needs to be a specification of the units the murphy expects
- and a check for what came in to see if it matches - and if not a routine to
- convert the number to the units the murphy uses
- do the murphy (as usual)
- and if the murphy created something with units, potentially reconvert the units back to what the sender expects
- and the sender would have to had also specified what those units should be
- Hmm, a lot to specify. It may be easier just to create different murphys to handle such cases if there aren't many.
"""

import query


def murphy_mkv(person, murphy_num, maps_keys_values):
    values = []
    for mkv in maps_keys_values:
        key = mkv[1]
        valuespec = mkv[2]
        if not valuespec:
            v = query.adat_person_key(person, key)
            values.append(v[1])
        if valuespec:
            last = valuespec[0]
            earliest = valuespec[1]
            latest = valuespec[2]
            vs = query.adat_person_key_options(person, key, last, earliest, latest)
            for v in vs:
                values.append(v[1])
    result = eval(murphy_num + '(' + str(values) + ')')
    return result


def murphy(person, murphy_num):
    # result = eval(murphy_num + '(' + str(person) + ')')                        # despite this line of looking just the one five lines above
    # result = eval("m005('pers105')")                                           # (though there values where numbers and here person is a string)
    # result = eval('m005(' + "'pers105'" + ')')                                 # spent hours, leaving it like this because there has to be cleaner way
    # result = eval(murphy_num + '(' + "'pers105'" + ')')                        # for now, only way I can figure to generate: "'pers105'"
    result = eval(
        murphy_num + '(' + '"' + "'" + str(person) + "'" + '"' + ')')  # is with: '"' + "'" + str(person) + "'" + '"'
    return result  # but then it needs trimming after reception in the murphy


def murmkv001(values):  # divide a by ten
    a = values[0]
    result = a / 10
    return result


def murmkv002(values):  # divide a by b
    a, b = values[0], values[1]
    result = a / b
    return result


def murmkv003(values):  # calculate average of a
    a = values
    if a:
        result = sum(a) / len(a)
        return result
    else:
        return []


def murmkv004(values):  # receive weight and height and calculate BMI
    a, b = values[0], values[1]
    result = round(a / b ** 2, 1)
    return result


def murphy005(person):  # receive person and calculate BMI
    person = person[1:-1]  # the convoluted mess coming in needs this
    a, b = query.adat_person_key(person, '~19')[1], query.adat_person_key(person, '~45')[1]
    result = round(a / b ** 2, 1)
    return result


"""Other possible murphy ideas
trend - this could innumerably complex, depending on how many values, recency, 
  range of measurement error, short term or long term, etc.
  so, trend will be a pretty interesting function

outlier - to score as high or low might also be a function that could be invoked. 
  It would mean hitting a reference table that would have to be local

"""