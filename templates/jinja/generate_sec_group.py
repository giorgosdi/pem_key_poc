from jinja2 import Environment, FileSystemLoader
import yaml
import os
from os.path import isdir,expanduser

class SecGroupTemplate():

    def __init__(self, sceptre_user_data):
        """Init method."""
        # super(PocTemplate, self).__init__()
        self.SCEPTRE_USER_DATA = sceptre_user_data

    home = expanduser('~')

    ENV = Environment(loader=FileSystemLoader('./'))
    with open("./config/dev/poc/secgroups.yaml") as config:
        content = yaml.load(config)

    rules = content['sceptre_user_data']['sec_group']['ingress']
    new_dict = {}
    new_dict['sceptre_user_data'] = ''
    new_dict['rules'] = {}
    new_dict['tags'] = content['sceptre_user_data']['tags']

    for rule in range(len(rules)):
        # content['sceptre_user_data']['sec_group']['ingress']["rule{}".format(rule)] = content['sceptre_user_data']['sec_group']['ingress'][rule]
        new_dict['rules']["rule{}".format(rule)] = {
            'protocol' : content['sceptre_user_data']['sec_group']['ingress'][rule].split(' ')[0],
            'ip' : content['sceptre_user_data']['sec_group']['ingress'][rule].split(' ')[1],
            'from' : int(content['sceptre_user_data']['sec_group']['ingress'][rule].split(' ')[2]),
            'to' : int(content['sceptre_user_data']['sec_group']['ingress'][rule].split(' ')[-1])
         }


    # print new_dict

    def print_temp(self):
        template = self.ENV.get_template("templates/secgroups.yaml")
        return template.render(config=self.new_dict)




def sceptre_handler(sceptre_user_data):
    p = SecGroupTemplate(sceptre_user_data)
    # return PocTemplate(sceptre_user_data).template.to_json()
    return p.print_temp()
