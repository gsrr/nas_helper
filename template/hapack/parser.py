import argparse

class [module_name_upper]Parser:
    def __init__(self):
        self.cmds = ['[module_name]_test']
        self.parser_[module_name] = argparse.ArgumentParser(prog="[module_name]", add_help=False)
        self.parser_[module_name]_test = argparse.ArgumentParser(prog="[module_name]_test", add_help=False)
        self.parser_[module_name]_test.add_argument("-z", nargs="?", required=True)

    def find(self, args):
        cnt = 0
        cmd = "[module_name]"
        while cnt < len(args):
            cmd += ("_" + args[cnt])
            if cmd in self.cmds:
                break
            cnt += 1
        args = args[cnt+1:]
        namespace = getattr(self, "parser" + "_" + cmd).parse_args(args).__dict__
        return cmd, namespace
