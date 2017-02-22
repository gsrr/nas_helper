import traceback
import sys
import os
from distutils.core import setup

def walkall(rootdir, deployMnt):
    data = []
    for (dirpath, dirnames, filenames) in os.walk(rootdir):
        if len(filenames) != 0:
            data.append(("/" + dirpath.split("/", 1)[1], [dirpath + "/" + f for f in filenames]))
            data.append((deployMnt + "/NAS/misc/SystemFiles/" + dirpath.split("/", 1)[1], [dirpath + "/" + f for f in filenames]))
    return data

def callSetup(deployMnt):
    sys.argv.pop(1)
    setup(
        name="[module_name]",
        version='0.1',
        packages=[],
        license='Creative Commons Attribution-Noncommercial-Share Alike license',
        long_description=open('README').read(),
        data_files=[
            (deployMnt + '/NAS/misc/Cmd/Exec/[cli_position]', ['hapack/[module_name].py']),
            (deployMnt + '/NAS/misc/Cmd/CmdTool/Parser', ['hapack/[module_name]parser.py']),
            (deployMnt + '/NAS/misc/HAAgent/Lib/[lib_position]', ['hapack/[module_name]lib.py']),
            (deployMnt + '/NAS/misc/HAAgent/Lib/[lib_position]', ['hapack/[module_name]restore.py']),
            (deployMnt + '/NAS/misc/HAAgent/Config', ['hapack/[module_name_upper]Config.py']),
            (deployMnt + '/NAS/misc/HAAgent/Config', ['hapack/[module_name_upper]Config.xml']),
        ] + walkall("buildroot", deployMnt),
     )

def removefile(path):
    try:
        os.remove(path)
        print "remove ", path
    except:
        print traceback.format_exc()
        pass
    
# python setup.py install --record files.txt
# cat files.txt | xargs rm -rf
# use pip instead?
def uninstall():
    with open("files.txt", "r") as fr:
        lines = fr.readlines()
        for line in lines:
            line = line.strip()
            removefile(line)

def main():
    try:
        func = getattr(sys.modules[__name__], sys.argv[1])
        func()
    except:
        print "call setup : deploying..."
        #print traceback.format_exc()
        callSetup(sys.argv[1])

if __name__ == "__main__":
    main()
