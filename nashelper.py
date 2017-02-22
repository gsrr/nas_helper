import sys
import os
import shutil
import copy
import traceback


def read_conf():
    conf = {}
    with open("conf", "r") as fr:
        lines = fr.readlines()
        for line in lines:
            line = line.strip()
            key,value = line.split("=", 1)
            conf[key] = value
    return conf

def create_module_dir(module_name):
    if os.path.exists(module_name):
        ret = raw_input("Delete %s directory?(Y/N)"%module_name)
        if "y" == ret.lower():
            shutil.rmtree(module_name)
    shutil.copytree("template", module_name)

def initfile(sfile, conf):
    conf['module_name_upper'] = conf["module_name"].upper()
    s2d = {
        'cli.py' : conf['module_name'] + ".py",
        'lib.py' : conf['module_name'] + "lib.py",
        'restore.py' : conf['module_name'] + "restore.py",
        'config.py' : conf['module_name_upper'] + "Config.py",
        'config.xml' : conf['module_name_upper'] + "Config.xml",
        'info.py' : conf['module_name_upper'] + "Info.py",
        'parser.py' : conf['module_name'] + "parser.py",
    }
    
    lines = None
    with open(sfile, "r") as fr:
        lines = fr.readlines()    

    keywords = ["[module_name]", "[module_name_upper]", "[cli_position]", "[lib_position]"]
    try:
        dfile = os.path.dirname(sfile) + "/" + s2d[os.path.basename(sfile)] 
        os.remove(sfile)
    except:
        dfile = sfile

    print "create file:%s"%dfile
    with open(dfile, "w") as fw:
        for line in lines:
            for key in keywords:
                if key in line :
                    line = line.replace(key, conf[key.lstrip("[").rstrip("]")])

            fw.write(line)
def init():
    try:
        conf = read_conf()
        module_name = raw_input("Please enter the module_name(default=%s):"%conf['module_name'])
        cli_position = raw_input("Please enter the cli position(default=%s):"%conf['cli_position'])
        lib_position = raw_input("Please enter the lib position(default=%s):"%conf['lib_position'])
        if module_name != "":
            conf['module_name'] = module_name 
        if cli_position != "":
            conf['cli_position'] = cli_position
        if lib_position != "":
            conf['lib_position'] = lib_position
        create_module_dir(conf['module_name'])

        files = os.walk(conf['module_name'])
        print files
        for (dirpath, dirname, filename) in files:
            for f in filename:
                f = dirpath + "/" + f
                f = f.replace("template", conf['module_name'])
                initfile(f , conf)
    except:
        print traceback.format_exc()

    os.chdir(module_name)
    os.system("python setup.py /usr/local install --install-purelib=./")
    os.system("python /usr/local/NAS/misc/HAAgent/HAAgentRun.py kill")
    os.system("python /usr/local/NAS/misc/HAAgent/HAAgentRun.py")

def main():
    func = getattr(sys.modules[__name__], sys.argv[1])
    func()

if __name__ == "__main__":
    main()
