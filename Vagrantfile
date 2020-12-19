Vagrant.configure(2) do |config|
  config.vm.box = "juniper/ffp-12.1X47-D15.4-packetmode"
  config.vm.boot_timeout = 1000

  config.vm.provider "virtualbox" do |vb|
    vb.memory = 512
    vb.cpus = 2
    vb.gui = false
  end

  # vsrx1
  config.vm.define "vsrx1" do |vsrx|
    vsrx.vm.hostname = "vsrx1"
    vsrx.vm.network :forwarded_port, id: "ssh", guest: 22, host: 2201
    vsrx.vm.network :forwarded_port, id: "netconf", guest: 830, host: 2830
    # ge-0/0/1
    vsrx.vm.network "private_network",
                     virtualbox__intnet: "1-2-1"
    # ge-0/0/2
    vsrx.vm.network "private_network",
                     virtualbox__intnet: "1-2-2"

    config.vm.provider "virtualbox" do |vb|
      vb.customize ["modifyvm", :id, "--nicpromisc2", "deny"]
    end
  end
 
  # vsrx2
  config.vm.define "vsrx2" do |vsrx|
    vsrx.vm.hostname = "vsrx2"
    vsrx.vm.network :forwarded_port, id: "ssh", guest: 22, host: 2202
    vsrx.vm.network :forwarded_port, id: "netconf", guest: 830, host: 2831
    # ge-0/0/1
    vsrx.vm.network "private_network",
                     virtualbox__intnet: "1-2-1"
    # ge-0/0/2
    vsrx.vm.network "private_network",
                     virtualbox__intnet: "1-2-2"
    config.vm.provider "virtualbox" do |vb|
      vb.customize ["modifyvm", :id, "--nicpromisc2", "deny"]
    end
  end

end
