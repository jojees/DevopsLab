#!/usr/bin/python
class FilterModule(object):
    """
    Derives environment types based on network name.
    """

    def filters(self):
        return {"penvironment_placement": self.penvironment_placement}

    def penvironment_placement(self, network_name):

        environment_mapping = {
            "EXTERNAL": ["prod", "europe", "govcloud", "syd", "mumbai", "sng"],
            "INTERNAL": ["test", "stage", "preprod", "uat", "dev"],
        }
        penvironment_placement = "INTERNAL"
        for environment in environment_mapping.keys():
            if network_name in environment_mapping[environment]:
                penvironment_placement = environment
        return penvironment_placement
