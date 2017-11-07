#!/usr/bin/python
import os
import sys
from subprocess import Popen, PIPE



def bash(command):
    """
    Bash wrapper to move arround
    """
    proc = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)

    out, err = proc.communicate()
    return out.strip(), err.strip(), proc.returncode


def verify_mounts(name_look):
    """
    This function verifies if nfs mount is the one we want to mount
    """
    hold = []
    for disk in str(bash('df -h')[0].strip()[0]).split("\n"):
        if disk not in hold or disk is not name_look:
            hold.append(disk)
            print "Mount from source not found on server, procceeding with mount"
        else:
            print "Found {} mounted .. proceeding with unmount".format(disk)
            cmd = "umount " + disk
            umnt = bash(cmd)[2]
            if umnt != 0:
                print "Could not unmount {}".format(disk)
                sys.exit(1)



def create_dir(name):
    """
    Create OS directories where the mountpoint and new location will
    be available
    """
    if os.path.exists(name):
        print "Found dir {} ... atempting to delete".format(name)
        try:
            os.removedirs(name)
        except OSError:
            print "Unable to delete {} Please remove it manualy".format(name)
            sys.exit(1)
    try:
        os.makedirs(name)
        #os.chown(name, root, )
    except OSError:
        print "Could not create directory: {}".format(name)
        sys.exit(1)



def rsync(source, target):
    """
    Make Rsync copy
    """
    com = "rsync -avh " + source + " " + target
    cop = bash(com)[2]
    if cop != 0:
        print "Rsync not working..."
        sys.exit(1)


def main(sourceip):
    ip = sourceip
    command = "showmount -e " + ip + " | grep -i reserved"
    source = bash(command)[0].split() # Take source dir

    if bash(command)[2] == 0:
        print "Found NFS share"
        dirs = ["/tmp/newdest", "/tmp/mount"]
        for direc in dirs:
            create_dir(direc)
        mounter_cmd = "sudo mount -t nfs -o rw,nfsvers=3 " + ip +":" + source[0] + \
                                                                                             " {}".format(dirs[1])
        mounter = bash(mounter_cmd)[2]
     #   print mounter
        if mounter == 0:
            print "Share found, starting rsync"
            #src = dirs[0] # Source to rsync only the content of that directory  
            src = str(dirs[1]) + "/*"
            print src
            rsync(dirs[1], src)
        elif mounter == 32:
            print "{} could not be mounted. Source server has denied access".format(source[0])
            sys.exit(1)
    else:
        print "Not found"

#if __name__ == " __main__":
main('192.168.1.2')
