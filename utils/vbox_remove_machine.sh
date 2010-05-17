#!/bin/bash

VM_NAME="$1"

if [ -z "$VM_NAME" ]; then
    echo "Usage: $0 <VM_name>"
    exit 1
fi

if [ ! -z "$(VBoxManage --help|grep '\[-name')" ]; then
    options="-"
else
    options="--"
fi

VBoxManage controlvm "$VM_NAME" poweroff
VBoxManage modifyvm "$VM_NAME" ${options}hda none
VBoxManage unregistervm "$VM_NAME"
VBoxManage closemedium disk ~/.VirtualBox/HardDisks/$VM_NAME.vdi 
rm -rf ~/.VirtualBox/Machines/$VM_NAME
rm -rf ~/.VirtualBox/HardDisks/$VM_NAME.vdi
