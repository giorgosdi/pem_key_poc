from jinja2 import Environment, FileSystemLoader
import yaml

class PocTemplate(CloudformationAbstractBaseClass):

    def __init__(self, sceptre_user_data):
        """Init method."""
        super(PocTemplate, self).__init__()
        self.SCEPTRE_USER_DATA = sceptre_user_data

    ENV = Environment(loader=FileSystemLoader('./'))

    with open("config/vpc.yaml") as config:
        print config
        content = yaml.load(config)


    print content

    template = ENV.get_template("templates/vpc.yaml")
    print template.render(config=content)




def sceptre_handler(sceptre_user_data):
    return PocTemplate(sceptre_user_data).template.to_json()
