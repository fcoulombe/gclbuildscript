#Copyright (C) 2011 by Francois Coulombe

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# 

import os.path
import SCons.Builder
from SCons.Builder import Builder

import SCons.Action
from SCons.Action import Action

import RunProgram

def builder_robocopy(target, source, env):
    rsyncExe = ""
    rsyncExe = "robocopy"
    #print "target %s" % target[0]
    #print "source %s" % source[0]
    #if the user has specified a source. usually when rsyncing to install dir
    if source:
        if not os.path.exists(target[0].abspath):
            RunProgram.RunProgram("mkdir %s" % target[0].abspath)
        rsync = rsyncExe
        cmdLine = "%s  %s %s /mir" % (rsync, source[0].abspath, target[0].abspath) 
        print  cmdLine
        stdout, stderr, returncode = RunProgram.RunProgram(cmdLine) 
        if stderr and len(stderr):
            print stderr
            return -1
    else:
        for t in target:
            #create folder if it doesn't exists
            if not os.path.exists(t.abspath):
                RunProgram.RunProgram("mkdir %s" % t.abspath)
            rsync = rsyncExe 
            cmdLine = "%s  %s %s /mir" % (rsync, t.srcnode().abspath, t.abspath) 
            #print  cmdLine
            stdout, stderr, returncode = RunProgram.RunProgram(cmdLine)
            if stderr and len(stderr):
                print stderr
                return -1
    return 0

def builder_rsync(target, source, env):
    rsyncExe = ""
    if env["PLATFORM"] == "win32":
        rsyncExe = "robocopy"
    else:
        rsyncExe = "rsync  --times --force --recursive --update --delete --progress "
    #print "target %s" % target[0]
    #print "source %s" % source[0]
    #if the user has specified a source. usually when rsyncing to install dir
    if source:
        if not os.path.exists(target[0].abspath):
            RunProgram.RunProgram("mkdir -p %s" % target[0].abspath)
        rsync = rsyncExe
        cmdLine = "%s  %s %s" % (rsync, source[0].abspath, os.path.dirname(target[0].abspath)) 
        #print  cmdLine
        stdout, stderr, returncode = RunProgram.RunProgram(cmdLine)
        if returncode != 0:
            print "there was a problem with rsync"
            print stdout
            return -1    
        if stderr and len(stderr):
            print stderr
            return -1
    else:
        for t in target:
            #create folder if it doesn't exists
            if not os.path.exists(t.abspath):
                RunProgram.RunProgram("mkdir -p %s" % t.abspath)
            rsync = rsyncExe 
            cmdLine = "%s  %s %s" % (rsync, t.srcnode().abspath, os.path.dirname(t.abspath)) 
            #print  cmdLine
            stdout, stderr, returncode = RunProgram.RunProgram(cmdLine)
            if returncode != 0:
                print "there was a problem with rsync"
                print stdout
                return -1
            if stderr and len(stderr):
                print stderr
                return -1
    return 0

    
def generate(env, *args, **kw):
    # Create a builder for RSync
    if env["PLATFORM"] == "win32":
        rsyncBld =Builder(action = Action(builder_robocopy, cmdstr='[rsync] $TARGET'))
    else:
        rsyncBld =Builder(action = Action(builder_rsync, cmdstr='[rsync] $TARGET'))
    
    env.Append(BUILDERS = {'RSync' :  rsyncBld})

def exists():
    print "we exists"