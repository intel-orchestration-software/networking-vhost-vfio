#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.

from cliff import _argparse
from cliff import command

from openstackclient.i18n import _
from openstackclient.network.v2 import port


class CreatePort(port.CreatePort):

    def get_parser(self, prog_name):
        old_parser = super(CreatePort, self).get_parser(prog_name)

        parser = _argparse.ArgumentParser(
            description=self.get_description(),
            epilog=self.get_epilog(),
            prog=prog_name,
            formatter_class=command._SmartHelpFormatter,
            conflict_handler='resolve',
            parents=[old_parser],
        )

        parser.add_argument(
            '--vnic-type',
            metavar='<vnic-type>',
            choices=['direct', 'direct-physical', 'macvtap',
                     'normal', 'baremetal', 'virtio-forwarder',
                     'virtio-direct'],
            help=_("VNIC type for this port (direct | direct-physical | "
                   "macvtap | normal | baremetal | virtio-forwarder, | "
                   "virtio-direct, default: normal)")
        )
        return parser


class SetPort(port.SetPort):

    def get_parser(self, prog_name):
        old_parser = super(SetPort, self).get_parser(prog_name)

        parser = _argparse.ArgumentParser(
            description=self.get_description(),
            epilog=self.get_epilog(),
            prog=prog_name,
            formatter_class=command._SmartHelpFormatter,
            conflict_handler='resolve',
            parents=[old_parser],
        )

        parser.add_argument(
            '--vnic-type',
            metavar='<vnic-type>',
            choices=['direct', 'direct-physical', 'macvtap',
                     'normal', 'baremetal', 'virtio-forwarder',
                     'virtio-direct'],
            help=_("VNIC type for this port (direct | direct-physical | "
                   "macvtap | normal | baremetal | virtio-forwarder | "
                   "virtio-direct, default: normal)")
        )
        return parser
