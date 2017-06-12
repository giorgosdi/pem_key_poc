from troposphere import FindInMap, GetAZs, Ref, Select, Template, Parameter, \
    Join, Output, Base64, Tags, If, AWS_NO_VALUE, Equals, Sub
import constants
import troposphere.ec2 as ec2
import troposphere.elasticloadbalancing as elb
import abc

class CloudformationAbstractBaseClass:

    """ Abstract base class with some common CFN functionality """

    __metaclass__ = abc.ABCMeta

    def __init__(self,template=None):
        # Add local vars

        if template:
            self.tempalte = template
        else:
            self.template = Template()

        self.DEFAULT_TAGS = []

        self.add_mappings()
        self.add_mandatory_tags()
        self.subnets_to_return = {}
        self.sgs_to_return = {}

        self.options_dict = {
            "keyname": {
                "Namespace": "aws:autoscaling:launchconfiguration",
                "OptionName": "EC2KeyName",
                "Type": "AWS::EC2::KeyPair::KeyName"
            },
            "instance_profile": {
                "Namespace": "aws:autoscaling:launchconfiguration",
                "OptionName": "IamInstanceProfile",
                "Type": "String"
            },
            "instance_type": {
                "Namespace": "aws:autoscaling:launchconfiguration",
                "OptionName": "InstanceType",
                "Type": "String"
            },
            "ec2_subnets": {
                "Namespace": "aws:ec2:vpc",
                "OptionName": "Subnets",
                "Type": "String"
            },
            "elb_subnets": {
                "Namespace": "aws:ec2:vpc",
                "OptionName": "ELBSubnets",
                "Type": "String"
            },
            "ec2_sgs": {
                "Namespace": "aws:autoscaling:launchconfiguration",
                "OptionName": "SecurityGroups",
                "Type": "String"
            },
            "elb_sgs": {
                "Namespace": "aws:elb:loadbalancer",
                "OptionName": "SecurityGroups",
                "Type": "String"
            }

        }

    def add_mappings(self):
        self.region_to_az = self.template.add_mapping('RegionToAz', constants.REGION_TO_AZ)
        self.environment_map = self.template.add_mapping('ENVIRONMENTSHORT', constants.ENVIRONMENTSHORT)

    def add_mandatory_tags(self):

        """ Add parameters for mandatory tags and naming policies """

        self.resource_prefix = self.template.add_parameter(Parameter(
            "ResourcePrefix",
            Description="Resource name prefix (eg project code..)",
            Type="String",
            MaxLength="16",
            Default=constants.COMPANY_NAME_PREFIX,
            AllowedPattern=constants.VALID_STRING_REGEX,
            ConstraintDescription=constants.INVALID_STRING_MSG
        ))
        self.template.add_condition(
            "ResourcePrefixIsNull",
            Equals(Ref(self.resource_prefix), ""))
        self.resource_prefix_is_null = "ResourcePrefixIsNull"

        self.environment_parameter = self.add_tag("Environment", Parameter(
            "Environment",
            Description="Value for Environment tag",
            Type="String",
            MinLength="1"
        ))
        self.owner_parameter = self.add_tag("Owner", Parameter(
            "Owner",
            Description="Value for Owner",
            Type="String",
        ))
        

    def add_tag(self, tag_key, tag_parameter, map_name=None, map_field=None):
        # Check that the input is a parameter type
        if not isinstance(tag_parameter, Parameter):
            raise ValueError('tag_parameter must be a troposphere.Parameter type')
        if tag_parameter not in self.template.parameters.values():
            self.template.add_parameter(tag_parameter)
        if map_name is None:
            # Tag value provided directly through parameter value
            self.DEFAULT_TAGS.append(
                ec2.Tag(key=tag_key, value=Ref(tag_parameter))
            )
        else:
            # Tag value must be looked up in the tag mapping
            self.DEFAULT_TAGS.append(
                ec2.Tag(
                    key=tag_key,
                    value=FindInMap(map_name, Ref(tag_parameter), map_field)
                )
            )
        return tag_parameter

    def get_tags_as_list(self, *name_joins):
        tag_list = [ec2.Tag("Name", Join("-", [nj for nj in name_joins]))]
        tag_list.extend(self.DEFAULT_TAGS)
        return tag_list

    def _record_template(self, Resource):
        """Adds the resource to the output, and adds the resource ID to the
        outputs."""
        self.template.add_resource(Resource)
        self.template.add_output(Output(
            "{0}Id".format(Resource.name),
            Description="{0} ID".format(Resource.resource["Type"]),
            Value=Ref(Resource)
        ))
        return Resource

    def get_resource_name(self, *name_joins):
        if 'custom_name' in self.sceptre_user_data:
            name_parts = [self.sceptre_user_data['custom_name']]
        else:
            name_parts = [
                FindInMap("RegionToAz", Ref("AWS::Region"), "SHORTREGION"),
                FindInMap("ENVIRONMENTSHORT", Ref(self.environment_parameter), "SHORTNAME"),
                If(
                    self.resource_prefix_is_null,
                    AWS_NO_VALUE,
                    Ref(self.resource_prefix))
            ]
        name_parts.extend(name_joins)
        return Join("-", name_parts)

    def get_subnet_param(self, subnet, single=False):

        if subnet[:7] == 'subnet-':
            return subnet

        elif subnet.startswith('!stack_output'):
             return subnet
        elif subnet[:7] != 'subnet-':
            if subnet not in self.template.parameters.keys():
                if single:
                    self.template.add_parameter(
                        Parameter(
                            subnet,
                            Type='String',
                            Description='Subnet ID for {}'.format(subnet)
                        )
                    )
                else:

                    self.template.add_parameter(
                        Parameter(
                            subnet,
                            Type='List<String>',
                            Description='Subnet ID for {}'.format(subnet)
                        )
                    )

            return Ref(subnet)

    def get_sg_param(self, sg):
        if sg[:3] != 'sg-':
            if sg not in self.template.parameters.keys():

                self.template.add_parameter(
                    Parameter(
                        sg,
                        Type='List<AWS::EC2::SecurityGroup::Id>',
                        Description='Security group ID for {}'.format(sg)
                    )
                )

            return Ref(sg)

        else:
            return sg

    def add_from_external(self, item):
        self.template.parameters = self.merge_dicts(self.template.parameters, item.template.parameters)
        self.template.resources = self.merge_dicts(self.template.resources, item.template.resources)
        self.template.outputs = self.merge_dicts(self.template.outputs, item.template.outputs)

    def merge_dicts(self, master, additional):
        new = master.copy()
        new.update(additional)
        return new

    def from_file(self, filepath, delimiter='', blanklines=False, scriptvariables={}):
        """
        Imports userdata from a file.
        :type filepath: string
        :param filepath
        The absolute path to the file.
        :type delimiter: string
        :param: delimiter
        Delimiter to use with the troposphere.Join().
        :type blanklines: boolean
        :param blanklines
        If blank lines shoud be ignored
        rtype: troposphere.Base64
        :return The base64 representation of the file.
        """

        data = []

        try:
            with open(filepath, 'r') as f:
                for line in f:
                    if blanklines and line.strip('\n\r ') == '':
                        continue

                    if scriptvariables:
                        data.append(Sub(line.format(**scriptvariables)))
                    else:
                        data.append(Sub(line))

        except IOError:
            raise IOError('Error opening or reading file: {}'.format(filepath))

        return Base64(Join(delimiter, data))