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

import os

from neutron_lib.api.definitions import portbindings

from neutron.agent import securitygroups_rpc
from neutron.plugins.ml2.drivers.openvswitch.agent.common \
    import constants as a_const
from neutron.plugins.ml2.drivers.openvswitch.mech_driver \
    import mech_openvswitch as ml2d

AGENT_TYPE = "ovs-vhost-vfio"


class OVSvHostVFIOMechanismDriver(ml2d.OpenvswitchMechanismDriver):

    def __init__(self):
        super(OVSvHostVFIOMechanismDriver, self).__init__()
        sg_enabled = securitygroups_rpc.is_firewall_enabled()
        hybrid_plug_required = False
        self.vif_details = {
            portbindings.CAP_PORT_FILTER: sg_enabled,
            portbindings.OVS_HYBRID_PLUG: hybrid_plug_required}

    def get_vif_type(self, context, agent, segment):
        a_config = agent['configurations']
        datapath = a_config.get(
            'datapath_type', a_const.OVS_DATAPATH_SYSTEM)
        return (portbindings.VIF_TYPE_VHOST_VFIO if
                datapath == a_const.OVS_DATAPATH_SYSTEM
                else portbindings.VIF_TYPE_OVS)

    def _pre_get_vif_details(self, agent, context):
        a_config = agent['configurations']
        vif_type = self.get_vif_type(context, agent, segment=None)
        if vif_type != portbindings.VIF_TYPE_VHOST_VFIO:
            details = dict(self.vif_details)
            hybrid = portbindings.OVS_HYBRID_PLUG
            if hybrid in a_config:
                # we only override the vif_details for hybrid plugging set
                # in the constructor if the agent specifically requests it
                details[hybrid] = a_config[hybrid]
        else:
            mdev_path = self.mdev_path(agent, context.current['id'])
            profile = context.current.get(portbindings.PROFILE)
            type = profile.get(portbindings.VHOST_VFIO_TYPE)
            parent = profile.get(portbindings.VHOST_VFIO_MDEV_PARENT)
            details = {portbindings.CAP_PORT_FILTER: False,
                       portbindings.OVS_HYBRID_PLUG: False,
                       portbindings.VHOST_VFIO_MDEV_PATH: mdev_path,
                       portbindings.VHOST_VFIO_MDEV_PARENT: parent,
                       portbindings.VHOST_VFIO_TYPE: type}
        details[portbindings.OVS_DATAPATH_TYPE] = a_config.get(
            'datapath_type', a_const.OVS_DATAPATH_SYSTEM)
        return details

    @staticmethod
    def mdev_path(agent, port_id):
        """Return the mdev path for a given port"""
        basedir = "/sys/bus/mdev/devices/"
        return os.path.join(basedir, port_id)
