import RunProgram

def builder_copy(target, source, env):
    for t in target:
        rsync = "/usr/bin/rsync --times --force --recursive --update --delete --progress"
        cmdLine = "%s  %s %s" % (rsync, source[0].abspath, t.abspath) 
        #print  cmdLine
        stdout, stderr, returncode = RunProgram.RunProgram(cmdLine)
        
        if stderr and len(stderr):
            print stderr
            return -1
    return 0

class Pipeline(object):
    def __init__(self):
        self.name = "VOID"
        
 