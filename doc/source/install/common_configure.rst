2. Edit the ``/etc/networking_vhost_vfio/networking_vhost_vfio.conf`` file and complete the following
   actions:

   * In the ``[database]`` section, configure database access:

     .. code-block:: ini

        [database]
        ...
        connection = mysql+pymysql://networking_vhost_vfio:NETWORKING_VHOST_VFIO_DBPASS@controller/networking_vhost_vfio
