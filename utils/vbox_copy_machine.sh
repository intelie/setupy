#!/bin/bash
# Created by Álvaro Justen

VBOX_PATH="$HOME/.VirtualBox"
LOG="vbox.log"

ORIGINAL_VM_NAME="$1"
NEW_VM_NAME="$2"
ROOT_VDI="$VBOX_PATH/HardDisks/$ORIGINAL_VM_NAME.vdi"
VM_MEMORY=1024

if [ -z "$ORIGINAL_VM_NAME" ] || [ -z "$NEW_VM_NAME" ]; then
    echo "Usage: $0 <original VM> <new VM>"
    echo "This script will create a copy of <original VM> called <new VM>, attach HD, configure network as bridge and them start the VM."
    echo "Please use a VM with only one HD attached and .vdi file with the same name of the VM."
    exit 1
fi


execute_and_log() {
    show_ok=0
    if [ ! "$1" = '-n' ]; then
        echo -n "[$(date +'%Y-%m-%d %H:%M:%S')] $1 ... "
        show_ok=1
    fi
    shift
    output=$($@ 2>&1)
    echo "$output" >> "$LOG"
    if [ $? -eq 0 ]; then
        if [ $show_ok -eq 1 ]; then
            echo 'OK'
        fi
    else
        echo "ERROR! Check $LOG log file for outputs"
    fi
}

#use Linux26_64 for 64-bit machine
execute_and_log "Creating virtual machine Linux2.6 32-bit based on $ROOT_VDI" VBoxManage createvm -name "$NEW_VM_NAME" -ostype Linux26 -register
execute_and_log "Setting memory to $VM_MEMORY" VBoxManage modifyvm "$NEW_VM_NAME" --memory $VM_MEMORY
execute_and_log 'Configuring network card' VBoxManage modifyvm "$NEW_VM_NAME" --nic1 hostif
execute_and_log -n VBoxManage modifyvm "$NEW_VM_NAME" --nictype1 82543GC
execute_and_log -n VBoxManage modifyvm "$NEW_VM_NAME" --cableconnected1 on
#execute_and_log -n VBoxManage modifyvm "$NEW_VM_NAME" --hostifdev1 eth0
execute_and_log 'Cloning the HD' VBoxManage clonehd $ROOT_VDI $VBOX_PATH/HardDisks/$NEW_VM_NAME.vdi
execute_and_log 'Enabling SATA' VBoxManage modifyvm "$NEW_VM_NAME" --sata on
execute_and_log -n VBoxManage openmedium disk $VBOX_PATH/HardDisks/$NEW_VM_NAME.vdi
execute_and_log 'Attaching the HD to the new machine' VBoxManage modifyvm $NEW_VM_NAME --hda $VBOX_PATH/HardDisks/$NEW_VM_NAME.vdi
execute_and_log 'Starting the virtual machine' VBoxManage startvm "$NEW_VM_NAME"
