# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "generic/alpine38"
  config.vm.network "public_network"
  config.vm.provision :shell, inline: "sudo apk --update add --no-cache python py-pip"

end
