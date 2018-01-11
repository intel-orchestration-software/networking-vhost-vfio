# 2017 - 2018 Intel Corporation. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import abc
import six

from networking_vhost_vfio.neutron.service import api_def

from neutron_lib.api import extensions as api_extensions
from neutron_lib.services import base as service_base


class VhostVfio(api_extensions.APIExtensionDescriptor):

    api_definition = api_def

    @classmethod
    def get_plugin_interface(cls):
        return VhostVfioServicePluginBase

    def get_extended_resources(self, version):
        if version == "2.0":
            return dict(list(api_def.RESOURCE_ATTRIBUTE_MAP.items()))
        else:
            return {}


@six.add_metaclass(abc.ABCMeta)
class VhostVfioServicePluginBase(service_base.ServicePluginBase):

    prefix_path = api_def.API_PREFIX

    def get_plugin_description(self):
        return "Plugin to update the Placement API with vhost-vfio states"

    @classmethod
    def get_plugin_type(cls):
        return "vhost-vfio"
