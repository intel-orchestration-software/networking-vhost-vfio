===============================================
Building Kernel with Sample Mdev Device(Ubuntu)
===============================================

The following are instructions to compile the kernel with a sample driver
program to demonstrate how to use the mediated device framework, using ubuntu.
This setup is required to run the functional tests provided in this repository.

Find information on this sample driver here:
https://github.com/torvalds/linux/blob/master/Documentation/vfio-mediated-device.txt#L303

Set-up
======

* Install all of the following prerequisites.
  Ubuntu requirements:

    ::

        sudo apt-get update
        sudo apt-get install libncurses5-dev gcc make git exuberant-ctags bc libssl-dev

* Clone the linux kernel repo:

    ::

        git clone https://github.com/torvalds/linux.git
        cd linux

* Make a copy of your old kernel config into your linux repo:

    ::

        cp /boot/config-`uname -r` .config

* Edit this .config file so that you can enable the sample driver. Change the
  line "# CONFIG_SAMPLES is not set" to "CONFIG_SAMPLES=y". To load your
  required sample run:

    ::

        make oldconfig

  You will be asked about all of the available sample modules. When asked about
  CONFIG_SAMPLE_VFIO_MDEV_MTTY enter "m" so that the module will be built.

* Build the linux-image and linux-header .deb files. This process can take a
  number of minutes:

    ::

        make -j deb-pkg LOCALVERSION=-custom

  "custom" is a name you are giving the debian files, this can be changed to
  something more meaningful.

* Install the debian files:

    ::

        dpkg -i linux-image-4.15.0-rc7-custom_4.15.0-rc7-custom-1_amd64.deb
        dpkg -i linux-headers-4.15.0-rc7-custom_4.15.0-rc7-custom-1_amd64.deb

* Update grub so that your machine will boot the new kernel:

    ::

        sudo update-grub2

* Reboot your machine:

    ::

        sudo reboot

* Once your machine has rebooted confirm that it booted with the correct
  kernel:

    ::

        uname –a

* Confirm that your sample mtty.ko module has been built. If built correctly
  it will be located in the "/lib/modules/<KERNEL>/kernel/" samples folder. It
  should also be listed in the "/lib/modules/<KERNEL>/modules.dep" file along
  with its dependencies.

* Load the mtty module, you may have to do this from the directory containing
  the mtty.ko file:

    ::

        modprobe mtty

* Check that the module has been loaded:

    ::

        lsmod | grep mtty

Running the tests
=================

By default the functional tests are skipped, as this sample device is not
installed by default.
To run the functional tests via the tox framework use the following command:

    ::

        tox -e functional

This will run the tests, but if you have not loaded the module correctly these
tests will be skipped even if this commane is run.
