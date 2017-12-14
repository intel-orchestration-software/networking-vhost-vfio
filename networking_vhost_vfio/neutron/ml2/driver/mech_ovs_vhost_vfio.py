
from neutron_lib.api.definitions import portbindings

from neutron.agent import securitygroups_rpc
from neutron.plugins.ml2.drivers.openvswitch.mech_driver \
    import mech_openvswitch as ml2d

AGENT_TYPE = "ovs-vhost-vfio"


class OVSvHostVFIOMechanismDriver(ml2d.OpenvswitchMechanismDriver):

    def __init__(self):
        sg_enabled = securitygroups_rpc.is_firewall_enabled()
        hybrid_plug_required = False
        vif_details = {portbindings.CAP_PORT_FILTER: sg_enabled,
                       portbindings.OVS_HYBRID_PLUG: hybrid_plug_required}

        super(OVSvHostVFIOMechanismDriver, self).__init__(
            AGENT_TYPE,
            portbindings.VIF_TYPE_OVS,
            vif_details, supported_vnic_types=[portbindings.VNIC_NORMAL,
                                               portbindings.VNIC_VHOST_VFIO])


    def bind_port(self, context):
        vnic_type = context.current.get(portbindings.VNIC_TYPE,
                                        portbindings.VNIC_VHOST_VFIO)
        profile = context.current.get(portbindings.PROFILE)
        capabilities = []
        if profile:
            capabilities = profile.get('capabilities', [])
        super(OVSvHostVFIOMechanismDriver, self).bind_port(context)

    def get_vif_type(self, context, agent, segment):
        # TODO(sean-k-mooney): add some check for vhost-vfio support
        # and set vif type port binding failed if not met.
        return portbindings.VIF_TYPE_VHOST_VFIO

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
