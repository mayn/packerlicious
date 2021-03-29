==============
packerlicious
==============

.. image:: https://ci.appveyor.com/api/projects/status/734n8y5s0wtqspj7/branch/master?svg=true
    :target: https://ci.appveyor.com/project/dkasyanov/packerlicious


About
=====

packerlicious - a python library to create `packer`_ templates.


This project leverages the logic engine of `troposphere`_.


Installation
============
packerlicious can be installed via pip:

.. code:: sh

    $ pip install packerlicious


Examples
========

Below is the packerlicious equivalent of `packer's example template`_

.. code:: python

    >>> from packerlicious import builder, provisioner, Template
    >>> template = Template()
    >>> template.add_builder(
            builder.AmazonEbs(
                access_key="...",
                secret_key="...",
                region = "us-east-1",
                source_ami="ami-fce3c696",
                instance_type="t2.micro",
                ssh_username="ubuntu",
                ami_name="packer {{timestamp}}"
            )
        )
    <packerlicious.builder.AmazonEbs object at 0x104e87ad0>
    >>> template.add_provisioner(
            provisioner.Shell(
                script="setup_things.sh"
            )
        )
    <packerlicious.provisioner.Shell object at 0x1048c08d0>
    >>> print(template.to_json())
    {
      "builders": [
        {
          "access_key": "...",
          "ami_name": "packer {{timestamp}}",
          "instance_type": "t2.micro",
          "region": "us-east-1",
          "secret_key": "...",
          "source_ami": "ami-fce3c696",
          "ssh_username": "ubuntu",
          "type": "amazon-ebs"
        }
      ],
      "provisioners": [
        {
          "script": "setup_things.sh",
          "type": "shell"
        }
      ]
    }


Currently supported Packer resources
======================================

Builders:

- alicloud-ecs
- amazon-chroot
- amazon-ebs
- amazon-ebssurrogate
- amazon-ebsvolume
- amazon-instance
- azure-arm
- cloudstack
- digitalocean
- docker
- file
- googlecompute
- hcloud
- hetznercloud
- hyperone
- hyperv-iso
- hyperv-vmcx
- linode
- lxc
- lxd
- ncloud
- null
- oneandone
- openstack
- oracle-classic
- parallels-iso
- parallels-pvm
- profitbricks
- proxmox
- qemu
- scaleway
- tencentcloud-cvm
- triton
- vagrant
- virtualbox-iso
- virtualbox-ovf
- vmware-iso
- vmware-vmx
- yandex

Post Processors:

- alicloud-import
- amazon-import
- artifice
- atlas
- checksum
- compress
- digitalocean-import
- docker-import
- docker-push
- docker-save
- docker-tag
- googlecompute-import
- googlecompute-export
- manifest
- shell-local
- vagrant
- vagrant-cloud
- vsphere
- vsphere-template

Provisioners:

- ansible-local
- ansible
- breakpoint
- chef-client
- chef-solo
- converge
- file
- inspec
- powershell
- puppet-masterless
- puppet-server
- salt-masterless
- shell
- shell-local
- windows-shell
- windows-restart


Community Plugins:

Builders:

- jetbrains-infra/packer-builder-vsphere (vsphere-iso, vsphere-clone)
- solo-io/packer-builder-arm-image

Provisioners:

- jrbeilke/packer-provisioner-inspec

Licensing
=========

packerlicious is licensed under the `Apache license 2.0`_.
See `LICENSE`_ for the full license text.


packerlicious contains source code from `troposphere`_ which is licensed under the `BSD 2-Clause license`_



.. _`packer`: https://www.packer.io/
.. _`troposphere`: https://github.com/cloudtools/troposphere
.. _`LICENSE`: https://github.com/dkasyanov/packerlicious/blob/master/LICENSE
.. _`Apache license 2.0`: https://opensource.org/licenses/Apache-2.0
.. _`BSD 2-Clause license`: http://opensource.org/licenses/BSD-2-Clause
.. _`semantic versioning`: http://semver.org/
.. _`packer's example template`: https://www.packer.io/docs/templates/index.html#example-template
