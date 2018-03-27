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

from neutron_lib.api.definitions import portbindings

from neutron.agent import securitygroups_rpc
from neutron.plugins.ml2.drivers.openvswitch.mech_driver \
    import mech_openvswitch as ml2d
from neutron.services.logapi.drivers.openvswitch import driver as log_driver
from neutron.services.qos.drivers.openvswitch import driver as ovs_qos_driver

AGENT_TYPE = "virtio-direct"


class OVSVirtioDirectMechanismDriver(ml2d.OpenvswitchMechanismDriver):

    def __init__(self):
        sg_enabled = securitygroups_rpc.is_firewall_enabled()
        vif_details = {portbindings.CAP_PORT_FILTER: sg_enabled,
                       portbindings.OVS_HYBRID_PLUG: False}
        super(ml2d.OpenvswitchMechanismDriver, self).__init__(
            AGENT_TYPE,
            portbindings.VIF_TYPE_OVS,
            vif_details,
            supported_vnic_types=[portbindings.VNIC_NORMAL,
                                  portbindings.VNIC_DIRECT,
                                  portbindings.VNIC_VIRTIO_DIRECT])
        ovs_qos_driver.register()
        log_driver.register()

    def bind_port(self, context):
        #NOTE this intentionally does not call it's immediate parent.
        super(ml2d.OpenvswitchMechanismDriver, self).bind_port(context)
