# !/bin/bash

PCI_ADDRS=`ls --ignore={bind,module,unbind,new_id,remove_id,uevent} /sys/bus/pci/drivers/virtio-pci/`
ADDRS=${PCI_ADDRS[0]}

for addr in ${ADDRS:12}
do
    sudo echo "vfio_pci" > /sys/bus/pci/drivers/virtio-pci/"$addr"/driver_override
done
