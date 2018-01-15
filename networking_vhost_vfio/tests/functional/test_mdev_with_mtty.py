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
"""Functional tests for the mdev python module.

A suite of functional tests using the sample device driver module supplied
by:

    https://github.com/torvalds/linux/tree/master/samples/vfio-mdev

Allows you to create dummy device, mtty. This test case will only work for a
kernel compiled with the correct samples configured."""

import os

from oslo_config import cfg

from networking_vhost_vfio.mdev import mdev

from networking_vhost_vfio.tests import base

CONF = cfg.CONF
# Define testcase variables for the mtty sample device code
DEV = "/sys/devices/virtual/mtty/mtty"
TYPE_ID = "mtty-1"
DEV_UUID = "83b8f4f2-509f-382f-3c1e-e6bfe0fa1004"


class TestSampleMdev(base.BaseTestCase):
    """Functional testcase for mdev python module."""

    def setUp(self):
        """Setup for testcase."""
        super(TestSampleMdev, self).setUp()
        # Skip tests if sample module not loaded
        if not os.path.exists(DEV):
            self.skipTest("Sample mdev device not loaded.")

        # Give privsep daemon permission for functional tests
        privsep_helper = os.path.join(
            os.getenv('VIRTUAL_ENV'), 'bin', 'privsep-helper')
        self.config(
            helper_command=' '.join(['sudo', '-E', privsep_helper]),
            group='networking_vhost_vfio_mdev')

    def config(self, **kwargs):
        """Override some config values for test setup."""
        group = kwargs.pop('group', None)
        for k, v in kwargs.items():
            CONF.set_override(k, v, group)

    def test_list_device_types(self):
        """Test listing all types of mdev devices."""
        # Generate the list of dev_types and confirm expected value
        type_list = mdev.list_device_types(DEV)
        self.assertEqual(type_list, ['mtty-1', 'mtty-2'])

    def test_dev_type_details(self):
        """Test listing all dev_type operational options."""
        # Generate the list of options and confirm its expected value
        opts_list = mdev.device_type_details(DEV, TYPE_ID)
        self.assertEqual(opts_list, ['device_api', 'create', 'devices',
                         'available_instances', 'name'])

    def test_create_list_remove_device(self):
        """Test creating and removing a new mdev device, confirm via list."""
        # Create a sample mdev device
        mdev.create_device_type(DEV, TYPE_ID, DEV_UUID)

        # Generate the list of devices to confirm device is created
        new_dev = mdev.list_devices(DEV, TYPE_ID)
        self.assertEqual(["83b8f4f2-509f-382f-3c1e-e6bfe0fa1004"], new_dev)

        # Remove the newly created device
        mdev.remove_device(DEV, TYPE_ID, DEV_UUID)

        # Generate the list of devices,confirm device has been destroyed.
        del_dev = mdev.list_devices(DEV, TYPE_ID)
        self.assertEqual([], del_dev)

    def test_list_devices(self):
        """Test generating an empty list of devices."""
        dev_list = mdev.list_devices(DEV, TYPE_ID)
        self.assertEqual(dev_list, [])

    def test_available_devices(self):
        """Test generating the no. of devices that can be created."""
        instances = mdev.available_devices(DEV, TYPE_ID)
        self.assertEqual(instances, 22)

    def test_dev_type_api(self):
        """Test generating the device_api of a device type."""
        api = mdev.device_type_api(DEV, TYPE_ID)
        self.assertEqual(api, 'vfio-pci')

    def test_dev_type_name(self):
        """Test generating the name of the type of a devices."""
        name = mdev.device_type_name(DEV, TYPE_ID)
        self.assertEqual(name, 'Single port serial')

    def test_dev_type_description(self):
        """Test generating the description of the type of device."""
        # This is an optional field which is not enabled by this sample driver
        description = mdev.device_type_description(DEV, TYPE_ID)
        # The filepath will not be found and invalid response will be generated
        self.assertEqual(description, "")

    def test_remove_device_by_uuid(self):
        """Test destroying a device by just it's uuid."""
        # Create a sample mdev device to destroy
        mdev.create_device_type(DEV, TYPE_ID, DEV_UUID)

        # Check device list to confirm it's creation
        new_dev = mdev.list_devices(DEV, TYPE_ID)
        self.assertEqual(new_dev, ["83b8f4f2-509f-382f-3c1e-e6bfe0fa1004"])

        # Remove the device via it's uuid
        mdev.remove_device_by_uuid(DEV_UUID)

        # Check device list to confirm it's deletion
        del_dev = mdev.list_devices(DEV, TYPE_ID)
        self.assertEqual(del_dev, [])
