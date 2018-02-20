local xtrace=$(set +o | grep xtrace)
local error_on_clone=${ERROR_ON_CLONE}
if [ "$VERBOSE" == 'True' ]; then
    # enabling verbosity on whole plugin - default behavior
    set -o xtrace
fi
# disabling ERROR_NO_CLONE to allow this plugin work with devstack-gate
ERROR_ON_CLONE=False

    # Initial source of lib script
    source $NETWORKING_VHOST_VFIO_DIR/devstack/libs/vhost-vfio

    case $1 in
        "stack")
            case $2 in
                "pre-install")
                    # cloning source code
                    echo_summary "Cloning of src files for vhost-vfio not required"
                ;;
                "install")
                    # Perform installation of vhost-vfio
                    sudo -EH yum install -y crudini || sudo -EH apt-get install -y crudini
                    sudo pip install -e "${NETWORKING_VHOST_VFIO_DIR}"

                    if [ $NETWORKING_OVS_INSTALL == 'True' ]; then
                        echo_summary "Configuring, installing and starting OVS for networking_vhost_vfio"
                        install_networking_vhost_vfio
                        allocate_VFs
                        #start_networking_ovs
                    else
                        echo_summary "OVS fornetworking_vhost_vfio will not be installed"
                    fi
                ;;
                "post-config")
                    vhost_vfio_config_update
                ;;
                "extra")
                    :
                ;;
            esac
        ;;
        "unstack")
            sudo pip uninstall "${NETWORKING_VHOST_VFIO_DIR}"
        ;;
        "clean")
            # Remove state and transient data
            # Remember clean.sh first calls unstack.sh
            # this is a noop
            :
        ;;
esac

ERROR_ON_CLONE=$error_on_clone
$xtrace
