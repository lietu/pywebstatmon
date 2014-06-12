# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

    # Every Vagrant virtual environment requires a box to build off of.
    config.vm.box = "hashicorp/precise64"
    config.vm.boot_timeout = 30

    # The url from where the 'config.vm.box' box will be fetched if it
    # doesn't already exist on the user's system.
    config.vm.box_url = "hashicorp/precise64"

    # Make the source code available on the guest
    config.vm.synced_folder ".", "/src"

    # Forward a HTTP port for checking out the WebUI
    config.vm.network "forwarded_port", guest: 8000, host: 8000

    # For masterless Salt Stack
    config.vm.synced_folder "salt/roots/", "/srv/"

    config.vm.provision :salt do |salt|
        salt.minion_config = "salt/minion"
        salt.run_highstate = true
        salt.verbose = true
    end
end
