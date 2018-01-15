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

# Input variables for tests
DEV = "device"
TYPE_ID = "dev_type_id"
DEV_UUID = "dev_uuid"


class MdevTestCase(base.BaseTestCase):
    """Test case for the mdev module and its functionalities."""

    def setUp(self):
        """TestCase setup"""
        super(MdevTestCase, self).setUp()
        privsep.mdev_context.set_client_mode(False)

    @mock.patch.object(mdev, "LOG")
    @mock.patch.object(os, "listdir")
    @mock.patch.object(os, "path")
    def test_list_dev_types_invalid(self, path, listdir, LOG):
        """Test empty list of mdev types"""
        listdir.return_value = None
        types = mdev.list_device_types(DEV)

        # Check the file path being created
        path.join.assert_called_with("device", "mdev_supported_types")
        LOG.info.assert_called_with("Failed to list supported mdev types: %s",
                                    mock.ANY)
        self.assertEqual([], types)

    @mock.patch.object(mdev, "LOG")
    @mock.patch.object(os, "listdir")
    @mock.patch.object(os, "path")
    def test_list_dev_types_valid(self, path, listdir, LOG):
        """Test listing supported mdev types."""
        listdir.return_value = ['type_1', 'type_2', 'type_3']
        types = mdev.list_device_types(DEV)

        # Check the file path being created
        path.join.assert_called_with("device", "mdev_supported_types")
        LOG.info.assert_called_once_with("Listing all supported mdev types.")
        self.assertEqual(['type_1', 'type_2', 'type_3'], types)

    @mock.patch.object(mdev, "LOG")
    @mock.patch.object(os, "listdir")
    @mock.patch.object(os, "path")
    def test_dev_type_details_invalid(self, path, listdir, LOG):
        """Test failure to get any dev_type details."""
        listdir.return_value = None
        type_details = mdev.device_type_details(DEV, TYPE_ID)

        # Check the file path and the return value of the function
        path.join.assert_called_with("device", "mdev_supported_types",
                                     "dev_type_id")
        LOG.info.assert_called_with("Failed to list mdev type details: %s",
                                    mock.ANY)
        self.assertEqual([], type_details)

    @mock.patch.object(mdev, "LOG")
    @mock.patch.object(os, "listdir")
    @mock.patch.object(os, "path")
    def test_dev_type_details_valid(self, path, listdir, LOG):
        """Test getting mdev type details."""
        listdir.return_value = ['detail_1', 'detail_2', 'detail_3']
        type_details = mdev.device_type_details(DEV, TYPE_ID)

        # Check the file path and the return value of the function
        path.join.assert_called_with("device", "mdev_supported_types",
                                     "dev_type_id")
        LOG.info.assert_called_once_with("Listing details on mdev type, %s.",
                                         "dev_type_id")
        self.assertEqual(['detail_1', 'detail_2', 'detail_3'], type_details)

    @mock.patch.object(mdev, "LOG")
    @mock.patch.object(os, "write")
    @mock.patch.object(os, "path")
    def test_create_dev_type_invalid(self, path, write, LOG):
        """Test failure to create a new mdev type."""
        mdev.create_device_type(DEV, TYPE_ID, DEV_UUID)

        # Check the file path and the return value of the function
        path.join.assert_called_with("device", "mdev_supported_types",
                                     "dev_type_id", "create")
        LOG.info.assert_called_with(
            "Could not create a new mediated device: %s", mock.ANY)
        write.assert_not_called()

    def test_create_dev_type_valid(self):
        """Test creating a new mdev type."""
        # TODO(helenam100): Include a valid create mdev test

    @mock.patch.object(mdev, "LOG")
    @mock.patch.object(os, "listdir")
    @mock.patch.object(os, "path")
    def test_list_dev_invalid(self, path, listdir, LOG):
        """Test failure to generate a list of mdev devices."""
        listdir.return_value = None
        devices = mdev.list_devices(DEV, TYPE_ID)

        # Check the file path and the return value of the function
        path.join.assert_called_with("device", "mdev_supported_types",
                                     "dev_type_id", "devices")
        LOG.info.assert_called_with("Failed to list all existing devices: %s",
                                    mock.ANY)
        self.assertEqual([], devices)

    @mock.patch.object(mdev, "LOG")
    @mock.patch.object(os, "listdir")
    @mock.patch.object(os, "path")
    def test_list_dev_valid(self, path, listdir, LOG):
        """Test listing mdev devices."""
        listdir.return_value = ['device_1', 'device_2', 'device_3']
        devices = mdev.list_devices(DEV, TYPE_ID)

        # Check the file path and the return value of the function
        path.join.assert_called_with("device", "mdev_supported_types",
                                     "dev_type_id", "devices")
        LOG.info.assert_called_once_with("Listing all existing mdevs.")
        self.assertEqual(['device_1', 'device_2', 'device_3'], devices)

    @mock.patch.object(mdev, "LOG")
    @mock.patch.object(os, "read")
    def test_available_dev_invalid(self, read, LOG):
        """Test failure to return no. of available mdev devices."""
        instances = mdev.available_devices(DEV, TYPE_ID)

        # Check the return value of the function
        LOG.info.assert_called_with(
            "Failed to discover all available instances: %s", mock.ANY)
        self.assertIsNone(instances)
        read.assert_not_called()

    def test_available_dev_valid(self):
        """Test returning no. of available mdev devices."""
        # TODO(helenam100): Include a valid test for available instances

    @mock.patch.object(mdev, "LOG")
    @mock.patch.object(os, "read")
    def test_dev_type_api_invalid(self, read, LOG):
        """Test failure to get api of mdev device type."""
        api = mdev.device_type_api(DEV, TYPE_ID)

        # Check the return value of the function
        LOG.info.assert_called_with("Failed to return device API: %s",
                                    mock.ANY)
        self.assertIsNone(api)
        read.assert_not_called()

    def test_dev_type_api_valid(self):
        """Test getting api of mdev device type."""
        # TODO(helenam100): Include a valid test for device type api

    @mock.patch.object(mdev, "LOG")
    @mock.patch.object(os, "read")
    def test_dev_type_name_invalid(self, read, LOG):
        """Test failure to get the name of mdev device."""
        type_name = mdev.device_type_name(DEV, TYPE_ID)

        # Check the return value of the function
        LOG.info.assert_called_with("Failed to return device name: %s",
                                    mock.ANY)
        self.assertIsNone(type_name)
        read.assert_not_called()

    def test_dev_type_name_valid(self):
        """Test getting name of mdev device."""
        # TODO(helenam100): Include a valid test for device type name

    @mock.patch.object(mdev, "LOG")
    @mock.patch.object(os, "read")
    def test_dev_type_description_invalid(self, read, LOG):
        """Test failure to get a description of device type."""
        description = mdev.device_type_description(DEV, TYPE_ID)

        # Check the return value of the function
        LOG.info.assert_called_with("Failed to return device description: %s",
                                    mock.ANY)
        self.assertEqual("", description)
        read.assert_not_called()

    @mock.patch.object(mdev, "LOG")
    @mock.patch.object(os, "read")
    @mock.patch.object(os, "open")
    @mock.patch.object(os, "path")
    def test_dev_type_description_valid(self, path, os_open, read, LOG):
        """Test getting description of device type."""
        # TODO(helenam100): Include a valid test for device type description

    @mock.patch.object(mdev, "LOG")
    @mock.patch.object(os, "listdir")
    @mock.patch.object(os, "path")
    def test_dev_attributes_invalid(self, path, listdir, LOG):
        """Test failure to list the mdev device attributes."""
        listdir.return_value = None
        attributes = mdev.device_attributes(DEV, TYPE_ID, DEV_UUID)

        # Check the file path and the return value of the function
        path.join.assert_called_with("device", "mdev_supported_types",
                                     "dev_type_id", "devices", "dev_uuid")
        LOG.info.assert_called_with("Failed to list device attributes: %s",
                                    mock.ANY)
        self.assertEqual([], attributes)

    @mock.patch.object(mdev, "LOG")
    @mock.patch.object(os, "listdir")
    @mock.patch.object(os, "path")
    def test_dev_attributes_valid(self, path, listdir, LOG):
        """Test listing the mdev device attributes."""
        listdir.return_value = ['attrib_1', 'attrib_2', 'attrib_3']
        attributes = mdev.device_attributes(DEV, TYPE_ID, DEV_UUID)

        # Check the file path and the return value of the function
        path.join.assert_called_with("device", "mdev_supported_types",
                                     "dev_type_id", "devices", "dev_uuid")
        LOG.info.assert_called_once_with("Listing devices attributes.")
        self.assertEqual(['attrib_1', 'attrib_2', 'attrib_3'], attributes)

    @mock.patch.object(mdev, "LOG")
    @mock.patch.object(os, "listdir")
    @mock.patch.object(os, "path")
    def test_dev_attributes_by_uuid_invalid(self, path, listdir, LOG):
        """Test failure to list the mdev device attributes with uuid."""
        listdir.return_value = None
        attributes = mdev.device_attributes_by_uuid(DEV_UUID)

        # Check the file path and the return value of the function
        path.join.assert_called_with("/sys/bus/mdev/devices", "dev_uuid")
        LOG.info.assert_called_with("Failed to list device attributes: %s",
                                    mock.ANY)
        self.assertEqual([], attributes)

    @mock.patch.object(mdev, "LOG")
    @mock.patch.object(os, "listdir")
    @mock.patch.object(os, "path")
    def test_dev_attributes_by_uuid_valid(self, path, listdir, LOG):
        """Test listing mdev device attributes with uuid."""
        listdir.return_value = ['attrib_1', 'attrib_2', 'attrib_3']
        attributes = mdev.device_attributes_by_uuid(DEV_UUID)

        # Check the file path and the return value of the function
        path.join.assert_called_with("/sys/bus/mdev/devices", "dev_uuid")
        LOG.info.assert_called_once_with("Listing devices attributes.")
        self.assertEqual(['attrib_1', 'attrib_2', 'attrib_3'], attributes)

    @mock.patch.object(mdev, "LOG")
    @mock.patch.object(os, "write")
    def test_remove_dev_invalid(self, write, LOG):
        """Test failure to destroy an mdev device."""
        mdev.remove_device(DEV, TYPE_ID, DEV_UUID)

        # Check log and write file call
        LOG.info.assert_called_with("Could not delete mdev device: %s",
                                    mock.ANY)
        write.assert_not_called()

    def test_remove_dev_valid(self):
        """Test destroying an mdev device."""
        # TODO(helenam100): Include a valid remove device test

    @mock.patch.object(mdev, "LOG")
    @mock.patch.object(os, "write")
    def test_remove_dev_by_uuid_invalid(self, write, LOG):
        """Test failure to destroy an mdev device with uuid."""
        mdev.remove_device_by_uuid(DEV_UUID)

        # Check log and write file call
        LOG.info.assert_called_with("Could not delete mdev device: %s",
                                    mock.ANY)
        write.assert_not_called()

    def test_remove_dev_by_uuid_valid(self):
        """Test destroying an mdev device with uuid."""
        # TODO(helenam100): Include a valid remove device by uuid test
