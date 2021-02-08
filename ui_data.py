import simulation_time as sim_time
import working_data as wd
from icecream import ic


class ui_data:
    def __init__(self):
        self.token_list = []
        self.name_row = {}
        self.token_start_time = {}
        self.token_time_label = {}
        self.token_repost_time = {}
        self.token_repost_time_label = {}
        self.tokens_completed = []

    def should_display(self, task, tasks):
        if task not in self.token_list and task not in self.tokens_completed:
            self.token_start_time[task] = tasks.get(task)[6]
            self.token_list.append(task)
            return True
        return False

    def should_update_time(self, task, at_home):
        if task in self.token_time_label and task not in self.tokens_completed and at_home:
            self.update_wait_time(task)

    def update_wait_time(self, token):
        """This function updates the wait time for a person that has arrived in the staffers home screen
        :param token: the randomly generated value associated with the task for that person
        :type token: int"""
        display_t_diff = sim_time.get_time_difference(self.token_start_time.get(token))
        if self.token_repost_time[token]:
            display_t_diff += '/' + sim_time.get_time_difference(self.token_repost_time.get(token))
        self.token_time_label.get(token).config(text=display_t_diff)
        # if self.token_repost_time[token]:
        #     display_rpt_diff = "%s%s"%(sim_time.get_time_difference(self.token_repost_time.get(token)),
        #                                )
        #     self.token_repost_time_label.get(token).config(text=display_rpt_diff)

    def clear_token(self, token):  # move to ui_data.py
        self.token_list.remove(token)
        self.token_start_time.pop(token)
        self.token_time_label.pop(token)
        self.token_repost_time.pop(token)
        self.name_row.clear()

    def time_diff_start_time(self, token):
        try:
            return sim_time.get_time_difference(self.token_start_time.get(token))
        except:
            return None

    def add_start_time_label(self, token, label_time):
        self.token_time_label[token] = label_time

    def update_repost_time(self, token):
        try:
            self.token_repost_time[token] = int(wd.log_dict.get(token)[-1].get('time'))
        except:
            self.token_repost_time[token] = None

    def add_token_row_name(self, row, name):
        self.name_row[name] = row+1

    def check_in_display(self, name):
        if name in self.name_row:
            return True
        return False

    def return_insert_row(self, name):
        return int(self.name_row[name])

    def organize_tasks(self, tasks):
        priority_tasks = {}
        ordered_tokens=[]
        try:
            for t in tasks:
                if t not in self.tokens_completed:
                    priority_tasks[t]=tasks.get(t)[2]
            tuple_tasks = sorted(priority_tasks.items(), key =lambda item: item[1])

            for tup in tuple_tasks:
                ordered_tokens.append(tup[0])
            return ordered_tokens
        except:
            print('no tasks')
