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

from neutron_lib.agent import l2_extension


class VhostVfioL2Ext(l2_extension.L2AgentExtension):

    def initialize(self, connection, driver_type):
        pass

    def consume_api(self, agent_api):
        pass

    def handle_port(self, context, port):
        pass

    def delete_port(self, context, port):
        pass
