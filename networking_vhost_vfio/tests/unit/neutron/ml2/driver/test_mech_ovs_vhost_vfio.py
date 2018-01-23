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

import mock

from oslo_config import cfg

from neutron_lib.api.definitions import portbindings

from neutron.plugins.ml2.drivers.openvswitch.agent.common import \
    constants as a_const

from neutron.tests.unit.plugins.ml2.drivers.openvswitch.mech_driver.test_mech_openvswitch import OpenvswitchMechanismBaseTestCase  # noqa

from networking_vhost_vfio.neutron.ml2.driver \
    import mech_ovs_vhost_vfio


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
        self.driver = mech_ovs_vhost_vfio.OVSvHostVFIOMechanismDriver()
        self.driver.initialize()

    def test_get_vif_type(self):
        result = self.driver.get_vif_type(None, self.AGENT_SYSTEM, None)
        self.assertEqual(portbindings.VIF_TYPE_VHOST_VFIO, result)

        result = self.driver.get_vif_type(None, self.AGENT_NETDEV, None)
        self.assertEqual(portbindings.VIF_TYPE_OVS, result)

    def _test_pre_get_vif_details(self, pb_vif_type):
        mock_type = "mock_mdev_type"
        mock_parent = "mock_parent_device"
        mock_id = "292daba0-1e2f-43a2-b8da-82826fb9c22f"

        self.driver.get_vif_type = mock.Mock(return_value=pb_vif_type)
        mock_context = mock.Mock()
        mock_profile = {portbindings.VHOST_VFIO_MDEV_TYPE: mock_type,
                        portbindings.VHOST_VFIO_PARENT_DEVICE: mock_parent}
        mock_context.current = {}
        mock_context.current['id'] = mock_id
        mock_context.current[portbindings.PROFILE] = mock_profile

        details = self.driver._pre_get_vif_details(self.AGENT_NETDEV,
                                                   mock_context)
        self.assertIn(portbindings.OVS_DATAPATH_TYPE, details.keys())
        self.assertIn(portbindings.CAP_PORT_FILTER, details.keys())
        self.assertIn(portbindings.OVS_HYBRID_PLUG, details.keys())
        return details

    def test_pre_get_vif_details_vif_type_ovs(self):
        pb_vif_type = "blah"
        details = self._test_pre_get_vif_details(pb_vif_type)

        self.assertNotIn(portbindings.VHOST_VFIO_MDEV_PATH, details.keys())
        self.assertNotIn(portbindings.VHOST_VFIO_PARENT_DEVICE, details.keys())
        self.assertNotIn(portbindings.VHOST_VFIO_MDEV_TYPE, details.keys())

    def test_pre_get_vif_details_vif_type_vfio(self):
        mock_type = "mock_mdev_type"
        mock_parent = "mock_parent_device"
        mock_id = "292daba0-1e2f-43a2-b8da-82826fb9c22f"
        pb_vif_type = portbindings.VIF_TYPE_VHOST_VFIO
        details = self._test_pre_get_vif_details(pb_vif_type)

        self.assertIn(portbindings.VHOST_VFIO_MDEV_PATH, details.keys())
        self.assertIn(portbindings.VHOST_VFIO_PARENT_DEVICE, details.keys())
        self.assertIn(portbindings.VHOST_VFIO_MDEV_TYPE, details.keys())
        self.assertEqual(details[portbindings.VHOST_VFIO_MDEV_TYPE],
                         mock_type)
        self.assertEqual(details[portbindings.VHOST_VFIO_PARENT_DEVICE],
                         mock_parent)
        self.assertEqual(details[portbindings.VHOST_VFIO_MDEV_PATH],
                         "/sys/bus/mdev/devices/" + mock_id)
