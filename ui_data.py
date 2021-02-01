import simulation_time as sim_time
import working_data as wd
class ui_data:
    def __init__(self):
        self.token_list = []
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
        self.token_time_label.get(token).config(text=display_t_diff)
        if self.token_repost_time[token]:
            display_rpt_diff = sim_time.get_time_difference(self.token_repost_time.get(token))
            self.token_repost_time_label.get(token).config(text=display_rpt_diff)

    def clear_token(self, token): # move to ui_data.py
        self.token_list.remove(token)
        self.token_start_time.pop(token)
        self.token_time_label.pop(token)
        self.token_repost_time.pop(token)
        self.token_repost_time_label.pop(token)

    def time_diff_start_time(self, token):
        return sim_time.get_time_difference(self.token_start_time.get(token))
    def add_start_time_label(self, token, label_time):
        self.token_time_label[token] = label_time
    def time_diff_repost_time(self, token):
        if self.token_repost_time[token]:
            return sim_time.get_time_difference(self.token_repost_time.get(token))
        else:
            return '--:--'
    def update_repost_time(self, token):
        try:
            self.token_repost_time[token] = int(wd.log_dict.get(token)[-1].get('time'))
        except:
            self.token_repost_time[token] = None

    def add_repost_time_label(self, token, label_repost_time):
        self.token_repost_time_label[token] = label_repost_time