#!/usr/bin/python
class FilterModule(object):
    '''
    Derives Pretty names for OS platforms from docker images names.
    '''

    def filters(self):
        return{
            'pplatform_family': self.pplatform_family
        }
    
    def pplatform_family(self, image_name):
        # pretty_platform_name = ''
        image_platform_name_map = {
            "jojees/ubuntu:20.04": {
                "NAME": "Ubuntu",
                "VERSION": "20.04.5 LTS (Focal Fossa)",
                "PRETTY_NAME": "Ubuntu 20.04.5 LTS",
                "VERSION_ID": "20.04",
                "CODE_NAME": "focal",
                "SHORT_NAME": "Ubuntu20.04"
            },
            "jojees/ubuntu:22.04": {
                "NAME": "Ubuntu",
                "VERSION": "22.04.2 LTS (Jammy Jellyfish)",
                "PRETTY_NAME": "Ubuntu 22.04.2 LTS",
                "VERSION_ID": "20.04",
                "CODE_NAME": "jammy",
                "SHORT_NAME": "Ubuntu22.04"
            },
            "jojees/ubuntu:18.04": {
                "NAME": "Ubuntu",
                "VERSION": "18.04.6 LTS (Bionic Beaver)",
                "PRETTY_NAME": "Ubuntu 18.04.6 LTS",
                "VERSION_ID": "18.04",
                "CODE_NAME": "bionic",
                "SHORT_NAME": "Ubuntu18.04"
            },
            "oraclelinux:9-slim": {
                "NAME": "Oracle Linux Server",
                "VERSION": "9.1",
                "PRETTY_NAME": "Oracle Linux Server release 9.1",
                "VERSION_ID": "9.1",
                "CODE_NAME": "el9",
                "SHORT_NAME": "Oracle9.1"
            }
        }
        pretty_platform_name = image_platform_name_map[image_name]

        return pretty_platform_name