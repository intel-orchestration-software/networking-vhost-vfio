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


class ExceptionBase(Exception):
    """Base Exception

    To correctly use this class, inherit from it and define
    a 'msg_fmt' property. That msg_fmt will get printf'd
    with the keyword arguments provided to the constructor.

    """
    msg_fmt = ("An unknown exception occurred.")

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs

        if not message:
            try:
                message = self.msg_fmt % kwargs
            except Exception:
                # at least get the core message out if something happened
                message = self.msg_fmt

        self.message = message
        super(ExceptionBase, self).__init__(message)

    def format_message(self):
        # NOTE(mrodden): use the first argument to the python Exception object
        # which should be our full NovaException message, (see __init__)
        return self.args[0]


class LibraryNotInitialized(ExceptionBase):
    msg_fmt = ("Before using the os_vif library, you need to call "
               "os_vif.initialize()")


class NoMatchingPlugin(ExceptionBase):
    msg_fmt = ("No VIF plugin was found with the name %(plugin_name)s")


class NoMatchingPortProfileClass(ExceptionBase):
    msg_fmt = ("No PortProfile class was found with the name %(name)s")


class NoSupportedPortProfileVersion(ExceptionBase):
    msg_fmt = ("PortProfile class %(name)s "
               "versions %(got_versions)s do not satisfy "
               "min=%(min_version)s max=%(max_version)s")


class NoMatchingVIFClass(ExceptionBase):
    msg_fmt = ("No VIF class was found with the name %(name)s")


class NoSupportedVIFVersion(ExceptionBase):
    msg_fmt = ("VIF class %(name)s versions %(got_versions)s "
               "do not satisfy min=%(min_version)s max=%(max_version)s")


class PlugException(ExceptionBase):
    msg_fmt = ("Failed to plug VIF %(vif)s. Got error: %(err)s")


class UnplugException(ExceptionBase):
    msg_fmt = ("Failed to unplug VIF %(vif)s. Got error: %(err)s")


class NetworkMissingPhysicalNetwork(ExceptionBase):
    msg_fmt = ("Physical network is missing for network %(network_uuid)s")


class NetworkInterfaceNotFound(ExceptionBase):
    msg_fmt = ("Network interface %(interface)s not found")


class NetworkInterfaceTypeNotDefined(ExceptionBase):
    msg_fmt = ("Network interface type %(type)s not defined")


class ExternalImport(ExceptionBase):
    msg_fmt = ("Use of this module outside of os_vif is not allowed. It must "
               "not be imported in os-vif plugins that are out of tree as it "
               "is not a public interface of os-vif.")
