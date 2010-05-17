#!/bin/bash

VM_NAME="$1"

if [ -z "$VM_NAME" ]; then
    echo "Usage: $0 <VM_name>"
    exit
fi

VBoxManage controlvm "$VM_NAME" poweroff
VBoxManage modifyvm "$VM_NAME" --hda none
VBoxManage unregistervm "$VM_NAME"
VBoxManage closemedium disk ~/.VirtualBox/HardDisks/$VM_NAME.vdi 
rm -rf ~/.VirtualBox/Machines/$VM_NAME
rm -rf ~/.VirtualBox/HardDisks/$VM_NAME.vdi
