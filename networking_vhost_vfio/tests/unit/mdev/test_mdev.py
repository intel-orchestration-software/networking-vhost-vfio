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
"""Unit tests for mdev_vfio abi."""

import os

import mock

from networking_vhost_vfio.mdev import mdev

from networking_vhost_vfio.mdev import privsep

from networking_vhost_vfio.tests import base

# Define input variables for tests
DEV = "device"
TYPE_ID = "dev_type_id"
DEV_UUID = "dev_uuid"


class mdevTestCase(base.BaseTestCase):
    """Test case base class for all unit tests."""

    def setUp(self):
        """Setup for testcase."""
        super(mdevTestCase, self).setUp()
        privsep.mdev_context.set_client_mode(False)

    @mock.patch.object(os, "listdir")
    @mock.patch.object(os, "path")
    def test_list_dev_types(self, path, listdir):
        """Test listing supported mdev types."""
        types = mdev.list_device_types(DEV)

        # Check the file path being created
        path.join.assert_called_with("/sys", "device",
                                     "mdev_supported_types")
        listdir.assert_called_with(path.join.return_value)
        self.assertEqual([], types)

    @mock.patch.object(os, "listdir")
    @mock.patch.object(os, "path")
    def test_dev_type_details(self, path, listdir):
        """Test getting mdev type details."""
        type_details = mdev.device_type_details(DEV, TYPE_ID)

        # Check the file path and the return value of the function
        path.join.assert_called_with("/sys", "device",
                                     "mdev_supported_types", "dev_type_id")
        listdir.assert_called_with(path.join.return_value)
        self.assertEqual([], type_details)

    @mock.patch.object(os, "path")
    def test_create_dev_type(self, path):
        """Test creating a new mdev type."""
        mdev.create_device_type(DEV, TYPE_ID, DEV_UUID)

        # Check the file path and the return value of the function
        path.join.assert_called_with("/sys", "device", "mdev_supported_types",
                                     "dev_type_id", "create")

    @mock.patch.object(os, "listdir")
    @mock.patch.object(os, "path")
    def test_list_dev(self, path, listdir):
        """Test listing mdev devices."""
        devices = mdev.list_devices(DEV, TYPE_ID)

        # Check the file path and the return value of the function
        path.join.assert_called_with("/sys", "device",
                                     "mdev_supported_types", "dev_type_id",
                                     "devices")
        listdir.assert_called_with(path.join.return_value)
        self.assertEqual([], devices)

    @mock.patch.object(os, "path")
    def test_available_dev(self, path):
        """Test returning no. of available mdev devices."""
        instances = mdev.available_devices(DEV, TYPE_ID)

        # Check the file path and the return value of the function
        path.join.assert_called_with("/sys", "device",
                                     "mdev_supported_types", "dev_type_id",
                                     "available_instances")
        self.assertIsNone(instances)

    @mock.patch.object(os, "path")
    def test_dev_type_api(self, path):
        """Test getting api of mdev device type."""
        api = mdev.device_type_api(DEV, TYPE_ID)

        # Check the file path and the return value of the function
        path.join.assert_called_with("/sys", "device",
                                     "mdev_supported_types", "dev_type_id",
                                     "device_api")
        self.assertIsNone(api)

    @mock.patch.object(os, "path")
    def test_dev_type_name(self, path):
        """Test getting name of mdev device."""
        type_name = mdev.device_type_name(DEV, TYPE_ID)

        # Check the file path and the return value of the function
        path.join.assert_called_with("/sys", "device",
                                     "mdev_supported_types", "dev_type_id",
                                     "name")
        self.assertIsNone(type_name)

    @mock.patch.object(os, "path")
    def test_dev_type_description(self, path):
        """Test getting description of device type."""
        description = mdev.device_type_description(DEV, TYPE_ID)

        # Check the file path and the return value of the function
        path.join.assert_called_with("/sys", "device",
                                     "mdev_supported_types", "dev_type_id",
                                     "description")
        self.assertEqual("", description)

    @mock.patch.object(os, "listdir")
    @mock.patch.object(os, "path")
    def test_dev_attributes(self, path, listdir):
        """Test listing the mdev device attributes."""
        attributes = mdev.device_attributes(DEV, TYPE_ID, DEV_UUID)

        # Check the file path and the return value of the function
        path.join.assert_called_with("/sys", "device",
                                     "mdev_supported_types", "dev_type_id",
                                     "devices", "dev_uuid")
        listdir.assert_called_with(path.join.return_value)
        self.assertEqual([], attributes)

    @mock.patch.object(os, "listdir")
    @mock.patch.object(os, "path")
    def test_dev_attributes_by_uuid(self, path, listdir):
        """Test listing mdev device attributes with uuid."""
        attributes = mdev.device_attributes_by_uuid(DEV_UUID)

        # Check the file path and the return value of the function
        path.join.assert_called_with("/sys/bus/mdev/devices", "dev_uuid")
        listdir.assert_called_with(path.join.return_value)
        self.assertEqual([], attributes)

    @mock.patch.object(os, "path")
    def test_dev_type(self, path):
        """Test getting mdev device type with uuid."""
        mdev_type = mdev.device_type(DEV, TYPE_ID, DEV_UUID)

        # Check the file path and the return value of the function
        path.join.assert_called_with("/sys", "device",
                                     "mdev_supported_types", "dev_type_id",
                                     "devices", "dev_uuid", "mdev_type")
        self.assertIsNone(mdev_type)

    @mock.patch.object(os, "path")
    def test_dev_type_by_uuid(self, path):
        """Test getting mdev device type with uuid."""
        mdev_type = mdev.device_type_by_uuid(DEV_UUID)

        # Check the file path and the return value of the function
        path.join.assert_called_with("/sys/bus/mdev/devices", "dev_uuid",
                                     "mdev_type")
        self.assertIsNone(mdev_type)

    @mock.patch.object(os, "path")
    def test_remove_dev(self, path):
        """Test destroying an mdev device."""
        mdev.remove_device(DEV, TYPE_ID, DEV_UUID)

        # Check the file path and the return value of the function
        path.join.assert_called_with("/sys", "device",
                                     "mdev_supported_types", "dev_type_id",
                                     "devices", "dev_uuid", "remove")

    @mock.patch.object(os, "path")
    def test_remove_dev_by_uuid(self, path):
        """Test destroying an mdev device with uuid."""
        mdev.remove_device_by_uuid(DEV_UUID)

        # Check the file path and the return value of the function
        path.join.assert_called_with("/sys/bus/mdev/devices", "dev_uuid",
                                     "remove")
