#!/usr/bin/env python
"""
# Generic set of useful constants and expressions for building
# cloudformation templates with Troposphere
#
# Some messages terse/abbreviated to save characters and try to
# stay within CFN upload limits. Also the default messages may not
# be terribly useful without additional context so are largely
# here for completeness
#
"""

# USER ONES
DEFAULT_VPC_CIDR = "10.7.0.0/20"

QUAD_ZERO_CIDR = "0.0.0.0/0"

AWS_ACCOUNT = {
    "AWS_DEV":      "111111111111",
    "AWS_PROD":     "222222222222",
}

# for internal construction, since most AWS resources have this form

EIGHT_DIGIT_HEX = "[a-f0-9]{8}"


PROJECT = "Test"

DOMAIN = {
    "prod": {
        "name": "prod.test.aws.",
        "r53_public": "Z3KV543KTKLBUI",
        "r53_private": "Z3KV543KTKLBUz",
    },
    "stg": {
        "name": "stg.test.aws.",
        "r53_public": "Z99MEM9B3JNV",
        "r53_private": "Z99MEM9B3JNz",
    },
    "dev": {
        "name": "dev.test.aws.",
        "r53_public": "Z1STG144DJHC7O",
        "r53_private": "Z1STG144DJHC7z",
    }
}

# Organisation Specifics
COMPANY_NAME_PREFIX = "HRM"


# Disabled in the base class
ENVIRONMENT = ["dev", "qa", "prod", "stg", "sand"]

# for simple strings

OR_NULL_REGEX             = "|^$"
NUMBER_STRING             = "\d+"
OPTIONAL_NUMBER_STRING    = "\d*"
ALPHANUMERIC_LC_STRING    = "[a-z0-9\-]*"
ALPHANUMERIC_STRING       = "[a-zA-Z0-9]*"
VALID_STRING_REGEX        = "[a-zA-Z]" + ALPHANUMERIC_STRING
OPTIONAL_CSV_STRING       = "[a-zA-Z0-9\-,]+|^$"
INVALID_STRING_MSG        = "Must be alphanumeric string"
OPTIONAL_TIME_WINDOW      = "\d\d:\d\d-\d\d:\d\d|^$"

# eg 12.34.56.78

IP_MSG                    = "Enter an IP"
EIP_MAX_LENGTH            = 15
VALID_IP_REGEX            = "\\d{1,3}+\\.\\d{1,3}+\\.\\d{1,3}+\\.\\d{1,3}"
INVALID_IP_MSG            = "Must be valid IP xx.xx.xx.xx"

VALID_DOMAIN_REGEX        = "^[\S]+?\.[^\.\s]+$"
INVALID_DOMAIN_MSG        = "Must be a valid domain eg. corporate.local"

# eg ami-a1b2c3d4

AMI_MSG                   = "Enter existing AMI"
VALID_AMI_REGEX           = "ami-" + EIGHT_DIGIT_HEX
INVALID_AMI_MSG           = "Must be valid AMI = ami-xxxxxxxx"

# eg my-aws-key

VALID_ACCOUNT_ID_REGEX    = "^[\d]{12}$"
INVALID_ACCOUNT_ID_MSG    = "Must be a 12 digit account number eg 123456789012"

KEYNAME_MSG               = "Enter name of existing key"
VALID_KEYNAME_REGEX       = "[\w-\.]*"
INVALID_KEYNAME_MSG       = "Must be valid key name"

# eg 12.34.56.78/32

CIDR_IP_MSG               = "Enter a CIDR form IP"
CIDR_MAX_LENGTH           = 18
VALID_CIDR_IP_REGEX       = VALID_IP_REGEX + "/\\d{1,2}"
INVALID_CIDR_IP_MSG       = "Must be valid CIDR form xx.xx.xx.xx/xx"

# eg eipalloc-a1b2c3d4

EIPALLOC_MSG              = "Enter elastic IP allocation"
VALID_EIPALLOC_REGEX      = "eipalloc-" + EIGHT_DIGIT_HEX
INVALID_EIPALLOC_MSG      = "Must be valid EIP alloc = eipalloc-xxxxxxxx"


AWS_LINUX_AMI = {
    "eu-west-1":      {"AMI": "ami-f9e77f8a"},
    "us-east-1":      {"AMI": "ami-2f726546"},
    "us-west-2":      {"AMI": "ami-b8f69f88"},  # oregon
    "us-west-1":      {"AMI": "ami-84f1cfc1"},
    "ap-southeast-1": {"AMI": "ami-787c2c2a"},  # singapore
    "ap-southeast-2": {"AMI": "ami-0bc85031"},  # sydney
    "ap-northeast-1": {"AMI": "ami-a1bec3a0"},  # tokyo
    "sa-east-1":      {"AMI": "ami-89de7c94"}
}

UBUNTU_14_AMI = {
    'ap-northeast-1': {"AMI": 'ami-936d9d93'},   # Asia Pacific (Tokyo)
    # Asia Pacific (Singapore)
    'ap-southeast-1': {"AMI": 'ami-96f1c1c4'},
    'ap-southeast-2': {"AMI": 'ami-69631053'},   # Asia Pacific (Sydney)
    'eu-central-1':   {"AMI": 'ami-accff2b1'},   # EU (Frankfurt)
    'eu-west-1':      {"AMI": 'ami-47a23a30'},   # EU (Ireland)
    # South America (Sao Paulo)
    'sa-east-1':      {"AMI": 'ami-4d883350'},
    'us-east-1':      {"AMI": 'ami-d05e75b8'},   # US East (N. Virginia)
    'us-west-1':      {"AMI": 'ami-df6a8b9b'},   # US West (N. California)
    'us-west-2':      {"AMI": 'ami-5189a661'}   # US West (Oregon)
}

AZN_20150301_AMI = {
    'ap-northeast-1': {"AMI": 'ami-db7b39e1'},   # Asia Pacific (Tokyo)
    'ap-southeast-1': {"AMI": 'ami-d44b4286'},   # Asia Pacific (Singapore)
    'ap-southeast-2': {"AMI": 'ami-b3337e89'},   # Asia Pacific (Sydney)
    'eu-central-1':   {"AMI": 'ami-a6b0b7bb'},   # EU (Frankfurt)
    'eu-west-1':      {"AMI": 'ami-e4d18e93'},   # EU (Ireland)
    'sa-east-1':      {"AMI": 'ami-55098148'},   # South America (Sao Paulo)
    'us-east-1':      {"AMI": 'ami-0d4cfd66'},   # US East (N. Virginia)
    'us-west-1':      {"AMI": 'ami-d5c5d1e5'},   # US West (N. California)
    'us-west-2':      {"AMI": 'ami-d5c5d1e5'}    # US West (Oregon)
}

DEFAULT_ACL_RULES = {
    "egress": {
        "100": {
            "Protocol": "-1",
            "RuleAction": "Allow",
            "Cidr": "0.0.0.0/0"
        }
    },
    "ingress": {
        "100": {
            "Protocol": "-1",
            "RuleAction": "Allow",
            "Cidr": "0.0.0.0/0"
        }
    }
}

AZ_NAMES = ["a", "b", "c", "d", "e"]

REGION_TO_AZ = {
    "eu-central-1": {
        "AZ": ["eu-central-1a", "eu-central-1b"],
        "SHORTREGION": "euc1"
    },
    "eu-west-2": {
        "AZ": ["eu-west-2a", "eu-west-2b"],
        "SHORTREGION": "euw2"
    },
    "eu-west-1": {
        "AZ": ["eu-west-1a", "eu-west-1b", "eu-west-1c"],
        "SHORTREGION": "euw1"
    }
}

SOLUTION_STACK_NAMES = {
    "java": "64bit Amazon Linux 2016.09 v2.4.4 running Java 8",
    "nodejs": "64bit Amazon Linux 2014.03 v1.0.9 running Node.js"
}

ENVIRONMENTSHORT = {
    "datagateway-sand": {
        "SHORTNAME": "dg-sand"
    },
    "sharedservices": {
        "SHORTNAME": "ss"
    }
}

def constant(f):
    def fset(self, value):
        raise TypeError("Cannot set constant property {0}".format(f))

    def fget(self):
        return f()
    return property(fget, fset)

if __name__ == "__main__":
    pass