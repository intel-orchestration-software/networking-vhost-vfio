from setuptools import setup
from os import system

_name = 'networking_vhost_vfio'
_description = 'OpenStack plugins for vhost_vfio support'
_url = 'https://github.com/intel-orchestration-software/networking-vhost-vfio'
_requirements = [
    "pytest"
]

setup(name="networking_vhost_vfio",
      description = _description,
      url = _url,
      packages = [_name],
      install_requires = _requirements,
      include_package_data=True,
      )
