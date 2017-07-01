from jinja2 import Environment, FileSystemLoader
import yaml
import os
from os.path import isdir,expanduser

class CreateInstance():

    def __init__(self, sceptre_user_data):
        self.SCEPTRE_USER_DATA = sceptre_user_data

    home = expanduser('~')

    ENV = Environment(loader=FileSystemLoader('./'))
    with open("./config/dev/poc/poc.yaml") as config:
        content = yaml.load(config)

    new_dict = {}
    new_dict = content['sceptre_user_data']


    def print_temp(self):
        template = self.ENV.get_template("templates/poc.yaml")
        return template.render(config=self.new_dict)


def sceptre_handler(sceptre_user_data):
    p = CreateInstance(sceptre_user_data)
    return p.print_temp()
