# -*- coding: utf-8 -*-
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Setup privsep decorator."""

from oslo_privsep import capabilities as c
from oslo_privsep import priv_context

mdev_context = priv_context.PrivContext(
    "networking_vhost_vfio",
    cfg_section="networking_vhost_vfio_mdev",
    pypath=__name__ + ".mdev_context",
    capabilities=[c.CAP_DAC_OVERRIDE,
                  c.CAP_FOWNER],
)
