
import mock

from oslo_config import cfg

from neutron_lib.api.definitions import portbindings

from neutron.plugins.ml2.drivers.openvswitch.agent.common import (
constants as a_const)
from neutron.tests.unit.plugins.ml2 import _test_mech_agent as base
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


