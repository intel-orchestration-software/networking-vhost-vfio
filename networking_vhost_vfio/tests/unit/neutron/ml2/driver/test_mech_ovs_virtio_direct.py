# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_config import cfg

from neutron.plugins.ml2.drivers.openvswitch.agent.common import \
    constants as a_const

from neutron.tests.unit.plugins.ml2.drivers.openvswitch.mech_driver.test_mech_openvswitch import OpenvswitchMechanismBaseTestCase  # noqa

from networking_vhost_vfio.neutron.ml2.driver \
    import mech_ovs_virtio_direct


class OpenvswitchMechanismVHOSTVFIOTestCase(OpenvswitchMechanismBaseTestCase):

    GOOD_MAPPINGS = {'fake_physical_network': 'fake_bridge'}

    GOOD_TUNNEL_TYPES = ['gre', 'vxlan']

    NETDEV_CONFIGS = {'bridge_mappings': GOOD_MAPPINGS,
                    'tunnel_types': GOOD_TUNNEL_TYPES,
                    'datapath_type': a_const.OVS_DATAPATH_NETDEV,
                    'ovs_capabilities': {'iface_types': []}}

    SYSTEM_CONFIGS = {'bridge_mappings': GOOD_MAPPINGS,
                      'tunnel_types': GOOD_TUNNEL_TYPES,
                      'datapath_type': a_const.OVS_DATAPATH_SYSTEM,
                      'ovs_capabilities': {'iface_types': []}}

    AGENT_NETDEV = {'alive': True,
                    'configurations': NETDEV_CONFIGS,
                    'host': 'host'}

    AGENT_SYSTEM = {'alive': True,
                    'configurations': SYSTEM_CONFIGS,
                    'host': 'host'}

    def setUp(self):
        super(OpenvswitchMechanismBaseTestCase, self).setUp()
        cfg.CONF.set_override('firewall_driver', 'openvswitch',
                              'SECURITYGROUP')
        self.driver = mech_ovs_virtio_direct.OVSVirtioDirectMechanismDriver()
        self.driver.initialize()
