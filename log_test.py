from icecream import ic

log_dict={}

def add_to_log(token, txt):
    ic(token)
    ic(txt)
    if token in log_dict:
        log_dict.get(token).append(txt)
    else:
        log_dict[token] = [txt]

def get_log(token):
    return log_dict.get(token)