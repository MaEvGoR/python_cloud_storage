# -*- mode: ruby -*-
# vi: set ft=ruby :
BOX_PATH = 'hadoop_image.box'

Vagrant.configure("2") do |config|

 config.vm.define "namenode" do |subconfig|
   subconfig.vm.box_check_update = false
   subconfig.vm.box = "ubuntu/trusty64"
   subconfig.vm.hostname = "namenode"
   subconfig.vm.network :private_network, ip: "10.0.0.11"
   subconfig.vm.network "forwarded_port", guest: 8088, host: 8088
   subconfig.vm.provider "virtualbox" do |v|
    v.memory = 512
   end
 end

 config.vm.define "datanode1" do |subconfig|
   subconfig.vm.box_check_update = false
   subconfig.vm.box = "ubuntu/trusty64"
   subconfig.vm.box_url = BOX_PATH
   subconfig.vm.hostname = "datanode1"
   subconfig.vm.network :private_network, ip: "10.0.0.12"
   subconfig.vm.provider "virtualbox" do |v|
    v.memory = 512
   end
 end

 config.vm.define "datanode2" do |subconfig|
   subconfig.vm.box_check_update = false
   subconfig.vm.box = "ubuntu/trusty64"
   subconfig.vm.box_url = BOX_PATH
   subconfig.vm.hostname = "datanode2"
   subconfig.vm.network :private_network, ip: "10.0.0.13"
   subconfig.vm.provider "virtualbox" do |v|
    v.memory = 512
   end
 end

 config.vm.define "client1" do |subconfig|
   subconfig.vm.box_check_update = false
   subconfig.vm.box = "ubuntu/trusty64"
   subconfig.vm.box_url = BOX_PATH
   subconfig.vm.hostname = "client1"
   subconfig.vm.network :private_network, ip: "10.0.0.100"
   subconfig.vm.provider "virtualbox" do |v|
    v.memory = 512
   end
 end

 config.vm.define "client2" do |subconfig|
   subconfig.vm.box_check_update = false
   subconfig.vm.box = "ubuntu/trusty64"
   subconfig.vm.box_url = BOX_PATH
   subconfig.vm.hostname = "client2"
   subconfig.vm.network :private_network, ip: "10.0.0.101"
   subconfig.vm.provider "virtualbox" do |v|
    v.memory = 512
   end
 end

end