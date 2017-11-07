#!/usr/bin/python
import argparse
from subprocess import Popen, PIPE
import os
import platform




def bash(x):

    proc = Popen(x, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    return (out.strip(), proc.returncode)




def unmounted(): # return list of unmounted disks

    """
    Find Active disks  ( compare mounted and unmounded drives )
    """

    all_disk = bash('fdisk -l | grep  "Disk /dev*" | awk \'{ print $2 }\'| cut -d: -f1')[0].split()
    mounted = bash("cat /proc/mounts | egrep ^/dev. | awk \'{print $1}\' | tr '[0-9]' \' \'" )[0].split()
    target = []

    for disk in all_disk:
        if disk not in mounted:
        target.append(disk)
    return target




def main():
    par = argparse.ArgumentParser(description="Creates VG and logical Volume based on the arguments provided")
    par.add_argument("-V", required=True, dest="Volume_Group Name")
    par.add_argument("-L", required=True, dest="Logical Volume Name")
    par.add_argument("-S", required=True, dest="Logical Volume Size")
    par.add_argument("-m", required=True, dest="Mounting Point")
    par.add_argument("--type", required=False, dest="FS type which will be mounted: (Default ext4)")
    args = par.parse_args()

    fresh = unmounted()  # Take list of unmounted disks

    if bash("pvs")[1] != 0:
        if os.name == "nt"
            print("Os Not Supported")
            break
            sys.exit(1)
        else:
            if platform.dist()[0].lower() == "ubuntu" or "debian":
               install = bash("sudo apt-get install lvm2")[1]
            elif platform.dist()[0].lower() == "fedora" or "centos" or "redhat":
               install = bash("yum install lvm2")[1]

            else:
                print("Distro not supported")
                sys.exit(1)

            if install == 0:
                for disk in fresh:
                    command = "pvcreate " + disk
                    bash(command)




    vgs_disks = bash('')

    #if bash('parted -l | grep -i "unrecognised disk label"')[0].split(":")[1] not None:



if __name__ == "__main__":
    find_unmounted()
