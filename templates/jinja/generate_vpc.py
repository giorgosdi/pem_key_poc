from jinja2 import Environment, FileSystemLoader
import yaml
import os
from os.path import isdir,expanduser

class PocTemplate():

    def __init__(self, sceptre_user_data):
        """Init method."""
        # super(PocTemplate, self).__init__()
        self.SCEPTRE_USER_DATA = sceptre_user_data

    home = expanduser('~')
    ENV = Environment(loader=FileSystemLoader('./'))


    with open("./config/dev/poc/vpc.yaml") as config:
        content = yaml.load(config)


    new_dict = content['sceptre_user_data']
    def print_temp(self):
        template = self.ENV.get_template("templates/vpc.yaml")
        return template.render(config=self.new_dict)




def sceptre_handler(sceptre_user_data):
    p = PocTemplate(sceptre_user_data)
    # return PocTemplate(sceptre_user_data).template.to_json()
    return p.print_temp()
