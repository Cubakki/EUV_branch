

class Sbatch_Generator:

    def __init__(self):
        self.plain="#!/bin/bash\n"
        self.allow_set=True

    def add_setting(self, setting_text):
        if self.allow_set:
            self.plain+="#SBATCH {}\n".format(setting_text)
        else:
            raise Exception('Setting is now not allowed')

    def add_settings(self, setting_list):
        if self.allow_set:
            for setting in setting_list:
                self.plain+="#SBATCH {}\n".format(setting)
        else:
            raise Exception('Setting is now not allowed')

    def add_job(self, job_text):
        self.allow_set=False
        self.plain+="{}\n".format(job_text)

    def export(self,path):
        with open(path,'w') as file:
            file.write(self.plain)
            file.close()
        return True