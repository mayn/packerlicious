
## (UNRELEASED)


## 0.8.1 (unreleased)

### BUG FIX:
# builder/GoogleCompute: source_image_family / source_image exactly one should be required [GH-111]

## 0.8.0 (May 30, 2018)

packer v1.2.4 feature sync [GH-107]

### BUG FIX:
* builder/AliCloud: correct image_disk_mappings definition, disk_delete_with_instance datatype

### MISC:
* (builder, post-processor, provisioner): additional properties




## 0.7.0 (April 22, 2018)

packer v1.2.2 feature sync [GH-105]

### NOTEWORTHY
* builder/Alicloud: rename to builder/AliCloud
* post-processor/AlicloudImport: rename to post-processor/AliCloudImport

### FEATURES:
* builder/NaverCloud: add support for packer's ncloud builder
* builder/OracleClassic: add support for packer's oracle-classic builder
* builder/Scaleway: add support for packer's scaleway builder

### MISC:
* (builder, post-processor, provisioner): additional properties



## 0.6.1 (April 20, 2018)

### BUG FIX:
* builder/VmwareIso: add missing format property [GH-103]



## 0.6.0 (March 18, 2018)

### NOTEWORTHY
* Drop support for EOL python versions (2.6, 3.3) [GH-98]
* builder/HyperV: rename to builder/HypervIso [GH-100]

### FEATURES:
* builder/HypervVmcx: add support for packer's Hyper-V (from a vmcx) builder [GH-97]
* builder/ParallelsIso: add support for packer's parallels ISO builder [GH-99]
* builder/ParallelsPvm: add support for packer's parallels PVM builder [GH-99]
* provisioner: add support for packer pause_before [GH-90]

### IMPROVEMENTS:
* fix list of list(aka jagged array) attributes causing exception during rendering [GH-101]
* builder/Amazon: add attribute temporary_security_group_source_cidr [GH-79]
* builder/Docker: add attribute fix_upload_owner [GH-73]
* builder/HypervIso: add attribute vhd_temp_path [GH-78]
* builder/VirtualboxOvf: add attribute keep_registered [GH-76]
* builder/VMwareIso: add attribute disable_vnc [GH-75]
* provisioner/puppet: add attribute guest_os_type [GH-74]

### MISC:

* ci: install packer binary for ci testing [GH-77]



## 0.5.0 (October 13, 2017)
Thanks to all the hacktoberfest participants that made this release possible.


### FEATURES:
* builder/AmazonChroot: add support for packer's amazon chroot builder [GH-19]
* builder/AmazonEbsSurrogate: add support for packer's amazon ebs surrogate builder [GH-19]
* builder/AmazonEbsVolume: add support for packer's amazon ebs volume builder [GH-19]
* builder/LXC: add support for packer's lxc builder [GH-37]
* builder/LXD: add support for packer's lxd builder [GH-33]
* builder/OracleOCI: add support for packer's oracle oci builder [GH-50]
* post_processor/VSphereTemplate: add support for packer's vsphere template builder [GH-60]

### IMPROVEMENTS:
* add python3 compatibility [GH-35]

### MISC:
* remove duplicated keys from HyperV and VirtualboxIso builders [GH-61]
* add licence and classifiers to setup.py [GH-59]
* add github pull request template [GH-47]
* appveyor support for testing on windows [GH-36]
* appveyor add python3 testing[GH-39]
* appveyor tox testenv, default PYTHON to empty string[ GH-51]
* appveyor fix python 2.6 build environment [GH-53]
* remove leading ellipsis from README.rst [GH-29]
* add amazon builders to supported list [GH-32]
* add lxc builder to supported list [GH-41]
* improve test coverage for list of builders [GH-34]



## 0.4.0 (Augutst 20, 2017)

### FEATURES:
* builder/Alicloud: add support for packer's alicloud ecs builder
* builder/AmazonInstance: add support for packer's amazon instance builder
* builder/Azure: add support for packer's azure builder
* builder/CloudStack: add support for packer's cloudstack builder
* builder/DigitalOcean: add support for packer's digital ocean builder
* builder/GoogleCompute: add support for packer's google compute builder
* builder/HyperV: add support for packer's hyperv iso builder
* builder/Null: add support for packer's null builder
* builder/OneAndOne: add support for packer's oneandone builder
* builder/OpenStack: add support for packer's openstack builder
* builder/ProfitBricks: add support for packer's ProfitBricks builder
* builder/Qemu: add support for packer's qemu builder
* builder/Triton: add support for packer's triton builder
* builder/VirtualboxIso: add support for packer's virtualbox iso builder
* builder/VirtualboxOvf: add support for packer's virtualbox ovf builder
* builder/VMwareIso: add support for packer's vmware iso builder
* builder/VMwareVmx: add support for packer's vmware vmx builder



## 0.3.0 (August 16, 2017)

### FEATURES:
* provisioner/ChefClient: add support for packer's chef client provisioner
* provisioner/ChefSolo: add support for packer's chef solo provisioner
* provisioner/Converge: add support for packer's converge provisioner
* provisioner/PowerShell: add support for packer's powershell provisioner
* provisioner/PuppetMasterless: add support for packer's puppet masterless provisioner
* provisioner/PuppetServer: add support for packer's puppet server provisioner
* provisioner/WindowsShell: add support for packer's windows shell provisioner
* provisioner/WindowsRestart: add support for packer's windows restart provisioner



## 0.2.2 (August 13, 2017)

### BUG FIXES:
* fix variable reference logic

### OTHER:
* update test coverage



## 0.2.1 (August 12, 2017)

### BUG FIXES:
* fix failing builds. Switch travis-ci to use tox, disable python3 builds for now

### OTHER:
* update descriptions in setup.py
* add copyright header to py files



## 0.2.0 (August 11, 2017)

### FEATURES:
* builder/AmazonEbs: add support for packer's amazon ebs builder
* builder/docker: add support for packer's docker builder
* builder/file: add support for packer's file builder
* post_processor/Alicloud import: add support for packer's Alicloud import post-processor
* post_processor/AmazonImport: add support for packer's amazon import post-processor
* post_processor/Artifice: add support for packer's artifice post-processor
* post_processor/Atlas: add support for packer's atlas post-processor
* post_processor/Checksum: add support for packer's checksum post-processor
* post_processor/Compress: add support for packer's compress post-processor
* post_processor/DockerImport: add support for packer's docker import post-processor
* post_processor/DockerPush: add support for packer's docker push post-processor
* post_processor/DockerSave: add support for packer's docker save post-processor
* post_processor/DockerTag: add support for packer's docker tag post-processor
* post_processor/GoogleComputeExport: add support for packer's google compute image exporter post-processor
* post_processor/Manifest: add support for packer's manifest post-processor
* post_processor/ShellLocal: add support for packer's shell local post-processor
* post_processor/Vagrant: add support for packer's vagrant post-processor
* post_processor/VagrantCloud: add support for packer's vagrant cloud post-processor
* post_processor/VSphere: add support for packer's vsphere post-processor
* provisioner/Ansible: add support for packer's ansible provisioner
* provisioner/AnsibleLocal: add support for packer's ansible local provisioner
* provisioner/File: add support for packer's file provisioner
* provisioner/SaltMasterless: add support for packer's salt masterless provisioner
* provisioner/Shell: add support for packer's shell provisioner
* provisioner/ShellLocal: add support for packer's shell local provisioner
