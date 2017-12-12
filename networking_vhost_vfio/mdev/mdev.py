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
"""Python module for vfio_mdev framework."""

import os

from networking_vhost_vfio.mdev import privsep

from oslo_log import log as logging

LOG = logging.getLogger(__name__)
SYS_PATH = os.path.abspath("/sys/devices/virtual/")
DEV_PATH = os.path.abspath("/sys/bus/mdev/devices/")


def list_device_types(phys_dev):
    """List of supported mediated device types."""
    dev_types = []
    dev_path = os.path.join(SYS_PATH, phys_dev, "mdev_supported_types")

    try:
        LOG.info("Listing all supported mdev types.")
        for dev_type in os.listdir(dev_path):
            dev_types.append(dev_type)
    except Exception as exc:
        LOG.info("Failed to list supported mdev types: %s", exc)

    return dev_types


def device_type_details(phys_dev, type_id):
    """List details on device type."""
    type_details = []
    dev_path = os.path.join(
        SYS_PATH, phys_dev, "mdev_supported_types", type_id)

    try:
        LOG.info("Listing details on mdev type, %s.", type_id)
        for detail in os.listdir(dev_path):
            type_details.append(detail)
    except Exception as exc:
        LOG.info("Failed to list mdev type details: %s", exc)

    return type_details


@privsep.mdev_context.entrypoint
def create_device_type(phys_dev, type_id, uuid):
    """Create a new mdev device type."""
    create_file = os.path.join(
        SYS_PATH, phys_dev, "mdev_supported_types", type_id, "create")

    try:
        LOG.info("Creating a new mdev: %s", uuid)
        with open(create_file, 'a') as create:
            create.write(uuid + '\n')
    except Exception as exc:
        LOG.info("Could not create a new mediated device: %s", exc)


def list_devices(phys_dev, type_id):
    """List all mdev devices of this type."""
    devices = []
    dev_path = os.path.join(
        SYS_PATH,
        phys_dev, "mdev_supported_types", type_id, "devices")

    try:
        LOG.info("Listing all existing mdevs.")
        for device in os.listdir(dev_path):
            devices.append(device)
    except Exception as exc:
        LOG.info("Failed to list all existing devices: %s", exc)

    return devices


def available_devices(phys_dev, type_id):
    """List the number of devices that can be created."""
    instances = None
    instances_file = os.path.join(
        SYS_PATH, phys_dev, "mdev_supported_types", type_id,
        "available_instances")

    try:
        LOG.info("Reading available instances for mdev, %s", type_id)
        with open(instances_file, 'r') as file:
            instances = file.read()
    except Exception as exc:
        LOG.info("Failed to discover all available instances: %s", exc)

    return instances


def device_type_api(phys_dev, type_id):
    """Display VFIO device API of device type."""
    api = None
    api_file = os.path.join(
        SYS_PATH, phys_dev, "mdev_supported_types", type_id, "device_api")

    try:
        LOG.info("Getting API of mdev type, %s", type_id)
        with open(api_file, 'r') as file:
            api = file.read()
    except Exception as exc:
        LOG.info("Failed to return device API: %s", exc)

    return api


def device_type_name(phys_dev, type_id):
    """Display name of mdev device."""
    name = None
    name_file = os.path.join(
        SYS_PATH, phys_dev, "mdev_supported_types", type_id, "name")

    try:
        LOG.info("Getting name of mdev type, %s", type_id)
        with open(name_file, 'r') as file:
            name = file.read()
    except Exception as exc:
        LOG.info("Failed to return device name: %s", exc)

    return name


def device_type_description(phys_dev, type_id):
    """Display description of device type."""
    description = ""
    description_file = os.path.join(
        SYS_PATH, phys_dev, "mdev_supported_types", type_id, "description")

    try:
        LOG.info("Getting description of mdev type, %s", type_id)
        with open(description_file, 'r') as file:
            description = file.read()
    except Exception as exc:
        LOG.info("Failed to return device description: %s", exc)

    return description


def device_attributes(phys_dev, type_id, uuid):
    """List attributes of mediated device."""
    attributes = []
    attribute_path = os.path.join(
        SYS_PATH, phys_dev, "mdev_supported_types", type_id, "devices", uuid)

    try:
        LOG.info("Listing devices attributes.")
        for attribute in os.listdir(attribute_path):
            attributes.append(attribute)
    except Exception as exc:
        LOG.info("Failed to list device attributes: %s", exc)

    return attributes


def device_attributes_by_uuid(uuid):
    """List attributes of mediated device with uuid."""
    attributes = []
    attribute_path = os.path.join(DEV_PATH, uuid)

    try:
        LOG.info("Listing devices attributes.")
        for attribute in os.listdir(attribute_path):
            attributes.append(attribute)
    except Exception as exc:
        LOG.info("Failed to list device attributes: %s", exc)

    return attributes


def device_type(phys_dev, type_id, uuid):
    """Display type supported by mediated device."""
    mdev_type = None
    type_file = os.path.join(
        SYS_PATH, phys_dev, "mdev_supported_types", type_id, "devices",
        uuid, "mdev_type")

    try:
        LOG.info("Getting mdev device type, %s", uuid)
        with open(type_file, 'r') as file:
            mdev_type = file.read()
    except Exception as exc:
        LOG.info("Failed to return device type: %s", exc)

    return mdev_type


def device_type_by_uuid(uuid):
    """Display type supported by mediated device, by uuid."""
    mdev_type = None
    type_file = os.path.join(DEV_PATH, uuid, "mdev_type")

    try:
        LOG.info("Getting mdev device type with uuid, %s", uuid)
        with open(type_file, 'r') as file:
            mdev_type = file.read()
    except Exception as exc:
        LOG.info("Failed to return device type: %s", exc)

    return mdev_type


@privsep.mdev_context.entrypoint
def remove_device(phys_dev, type_id, uuid):
    """Destroy the mediated device."""
    remove_file = os.path.join(
        SYS_PATH, phys_dev, "mdev_supported_types", type_id, "devices",
        uuid, "remove")

    try:
        LOG.info("Deleting mdev device: %s", uuid)
        with open(remove_file, 'w+') as remove:
            remove.write('1')
    except Exception as exc:
        LOG.info("Could not delete mdev device: %s", exc)


@privsep.mdev_context.entrypoint
def remove_device_by_uuid(uuid):
    """Destroy the mediated device, by uuid."""
    remove_file = os.path.join(DEV_PATH, uuid, "remove")

    try:
        LOG.info("Deleting mdev device with uuid: %s", uuid)
        with open(remove_file, 'w+') as remove:
            remove.write('1')
    except Exception as exc:
        LOG.info("Could not delete mdev device: %s", exc)
