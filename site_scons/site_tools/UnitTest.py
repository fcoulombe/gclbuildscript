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

import RunProgram
import os.path
import SCons.Builder
import subprocess
from SCons.Builder import Builder
from SCons.Action import Action

valgrindExe = ['/usr/local/bin/valgrind --leak-check=full --dsymutil=yes --quiet  --show-reachable=yes ']
extraValgrindOptions = ""
     

def builder_unit_test_with_valgrind(target, source, env):
    global extraValgrindOptions
    print "[valgrind test] %s " % str(target)


    app = str(source[0].abspath)
    cwd = os.getcwd()
    cmdLine = [valgrindExe + extraValgrindOptions + app]
    print cmdLine
    p = subprocess.Popen(cmdLine, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.path.dirname(app))
    stdout, stderr  = p.communicate()
    if  stderr and len(stderr) != 0:
        print stderr
        return 1
    if p.returncode != 0:
        print stderr
        return 1
    open(str(target[0]),'w').write("PASSED\n")
    return 0
    

def builder_unit_test(target, source, env):
    #print "[test] %s " % str(source[0])
    app = str(source[0].abspath)
    cwd = os.getcwd()
    cmdLine = [app]
    
    p = subprocess.Popen(cmdLine, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.path.dirname(app))
    stdout, stderr  = p.communicate()
    #print stdout
    #print stderr
    if  stdout and len(stdout) != 0:
        print stdout.strip()
    if  stderr and len(stdout) != 0:
        print stderr
        return 1
    if p.returncode != 0:
        print stderr
        return 1
    open(str(target[0]),'w').write("PASSED\n")
    return 0
    
def string_it(target, source, env):
    return "test %s" % str(source[0])
   
def UnitTest(self, name, src_files, dependencies, data):
    prog = self.KProgram(name, src_files, dependencies)
    processedData = self.Data(data)
    #self.AlwaysBuild(processedData)
    #self.Depends(prog, processedData)
    
    passed = self.File(name+".passed")
    tested = self.Test(passed, prog)
    self.Depends(tested, processedData)
    
    self.AlwaysBuild(tested)
    
    self.KAlias("@build_all", prog)
    runAlias = self.KAlias(name+"_run", tested)
    self.KAlias("@run_all", runAlias)
    return prog
    
def generate(env, *args, **kw):
    global extraValgrindOptions
    env.AddMethod(UnitTest)
    
    # Create a builder for tests
    bld = None
    if env.GetOption('useValgrind'):
        suppressionFiles = [env.File('#tools/GCL_test.supp') , 
                        #env.File('#tools/helloworld.supp') ,
                        #env.File('#tools/SDL.supp') ,
                         ]
        for s in suppressionFiles:
            extraValgrindOptions += " --suppressions=" + "".join(s.abspath)
        bld = env.Builder(action = env.Action(builder_unit_test_with_valgrind, cmdstr='$SOURCE'))
    else:
        bld = Builder(action = Action(builder_unit_test, cmdstr='[test] $SOURCE'))
    env.Append(BUILDERS = {'Test' :  bld})


def exists():
    print "we exists"
