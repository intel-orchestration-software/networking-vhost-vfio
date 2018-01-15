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

DEV_PATH = os.path.abspath("/sys/bus/mdev/devices")
LOG = logging.getLogger(__name__)


def list_device_types(dev):
    """List of supported mediated device types."""
    dev_types = []
    dev_path = os.path.join(dev, "mdev_supported_types")

    try:
        LOG.info("Listing all supported mdev types.")
        for dev_type in os.listdir(dev_path):
            dev_types.append(dev_type)
    except Exception as exc:
        LOG.info("Failed to list supported mdev types: %s", exc)

    return dev_types


def device_type_details(dev, type_id):
    """List details on device type."""
    type_details = []
    dev_path = os.path.join(dev, "mdev_supported_types", type_id)

    try:
        LOG.info("Listing details on mdev type, %s.", type_id)
        for detail in os.listdir(dev_path):
            type_details.append(detail)
    except Exception as exc:
        LOG.info("Failed to list mdev type details: %s", exc)

    return type_details


@privsep.mdev_context.entrypoint
def create_device_type(dev, type_id, dev_uuid):
    """Create a new mdev device type."""
    create_file = os.path.join(dev, "mdev_supported_types", type_id, "create")

    try:
        LOG.info("Creating a new mdev: %s", dev_uuid)
        with open(create_file, 'a') as create:
            create.write(dev_uuid)
    except Exception as exc:
        LOG.info("Could not create a new mediated device: %s", exc)


def list_devices(dev, type_id):
    """List all mdev devices of this type."""
    devices = []
    dev_path = os.path.join(dev, "mdev_supported_types", type_id, "devices")

    try:
        LOG.info("Listing all existing mdevs.")
        for device in os.listdir(dev_path):
            devices.append(device)
    except Exception as exc:
        LOG.info("Failed to list all existing devices: %s", exc)

    return devices


def available_devices(dev, type_id):
    """List the number of devices that can be created."""
    instances = None
    instances_file = os.path.join(dev, "mdev_supported_types", type_id,
        "available_instances")

    try:
        LOG.info("Reading available instances for mdev, %s", type_id)
        devices = open(instances_file)
        instances = int(devices.readline())
    except Exception as exc:
        LOG.info("Failed to discover all available instances: %s", exc)

    return instances


def device_type_api(dev, type_id):
    """Display API of device type."""
    api = None
    api_file = os.path.join(dev, "mdev_supported_types", type_id, "device_api")

    try:
        LOG.info("Getting API of mdev type, %s", type_id)
        with open(api_file) as f_in:
            dev_api = list(line for line in (l.strip() for l in f_in) if line)
        api = dev_api[0]
    except Exception as exc:
        LOG.info("Failed to return device API: %s", exc)

    return api


def device_type_name(dev, type_id):
    """Display name of mdev device."""
    name = None
    name_file = os.path.join(dev, "mdev_supported_types", type_id, "name")

    try:
        LOG.info("Getting name of mdev type, %s", type_id)
        with open(name_file) as n_line:
            dev = list(line for line in (l.strip() for l in n_line) if line)
        name = dev[0]
    except Exception as exc:
        LOG.info("Failed to return device name: %s", exc)

    return name


def device_type_description(dev, type_id):
    """Display description of device type."""
    description = ""
    description_file = os.path.join(dev, "mdev_supported_types", type_id,
                                    "description")

    try:
        LOG.info("Getting description of mdev type, %s", type_id)
        with open(description_file) as d_file:
            des = list(line for line in (l.strip() for l in d_file) if line)
        description = des[0]
    except Exception as exc:
        LOG.info("Failed to return device description: %s", exc)

    return description


@privsep.mdev_context.entrypoint
def remove_device(dev, type_id, uuid):
    """Destroy the mediated device."""
    remove_file = os.path.join(dev, "mdev_supported_types", type_id, "devices",
                               uuid, "remove")

    try:
        LOG.info("Deleting mdev device: %s", uuid)
        with open(remove_file, 'w') as remove:
            remove.write('1')
    except Exception as exc:
        LOG.info("Could not delete mdev device: %s", exc)


@privsep.mdev_context.entrypoint
def remove_device_by_uuid(uuid):
    """Destroy the mediated device, by uuid."""
    remove_file = os.path.join(DEV_PATH, uuid, "remove")

    try:
        LOG.info("Deleting mdev device with uuid: %s", uuid)
        with open(remove_file, 'w') as remove:
            remove.write('1')
    except Exception as exc:
        LOG.info("Could not delete mdev device: %s", exc)
