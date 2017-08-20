
## (UNRELEASED)


### FEATURES:
* builder/AmazonInstance: add support for packer's amazon instance builder
* builder/Azure: add support for packer's azure builder
* builder/CloudStack: add support for packer's cloudstack builder
* builder/DigitalOcean: add support for packer's digitalocean builder
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
