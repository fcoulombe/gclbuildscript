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


valgrindExe = ['/usr/local/bin/valgrind --leak-check=full --dsymutil=yes --quiet  --show-reachable=yes ']
extraValgrindOptions = ""

     

def builder_unit_test_with_valgrind(target, source, env):
    suppressionFiles = [env.File('#tools/GCL_test.supp') , 
                        env.File('#tools/helloworld.supp') ,
                        env.File('#tools/SDL.supp') ,
                         ]

    app = str(source[0].abspath)
    cwd = os.getcwd()
    print "[Valgrind TEST]: %s" % app
    cmdLine = [valgrindExe + suppressionString + app]
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
    app = str(source[0].abspath)
    cwd = os.getcwd()
    print "[TEST]: %s" % app
    cmdLine = [app]
    
    p = subprocess.Popen(cmdLine, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.path.dirname(app))
    stdout, stderr  = p.communicate()
    #print stdout
    #print stderr
    if  stderr and len(stderr) != 0:
        print stderr
        return 1
    if p.returncode != 0:
        print stderr
        return 1
    open(str(target[0]),'w').write("PASSED\n")
    return 0
    

def builder_rsync(target, source, env):
    for t in target:
        rsync = "/usr/bin/rsync --times --force --recursive --update --delete --progress"
        print "%s  %s %s" % (rsync, t.srcnode().abspath, os.path.dirname(t.abspath))
        os.system("%s  %s %s" % (rsync, t.srcnode().abspath, os.path.dirname(t.abspath)))
    return 0

def BuildFiles(self, src_files, dependencies):
    self.AppendDependenciesCFlags(dependencies)
    objs = self.Object(src_files)
    return objs
    
def UnitTest(self, name, src_files, dependencies, data):
    prog = self.KProgram(name, src_files, dependencies)
    rsyncedData = self.RSync(data, None)
    self.AlwaysBuild(rsyncedData)
    self.Depends(prog, rsyncedData)
    self.Test(name+".passed", prog)
    self.KAlias(name+"_run", name+".passed")
    self.KAlias("@run_all", self.KAlias(name+"_run"))
    
def KProgram(self, name, src_files, dependencies):
    objs = self.BuildFiles(src_files, dependencies)
    self.AppendDependenciesLFlags(dependencies)
    prog = self.Program(name, objs)
    for dep in dependencies:
        self.Depends(prog, self.KAlias("@"+dep))
    self.KAlias("@"+name, prog)
    return prog
    
def KStaticLibrary(self, name,  src_files, dependencies):
    objs = self.BuildFiles(src_files, dependencies)
    self.AppendDependenciesLFlags(dependencies) 
    lib = self.StaticLibrary(name, objs)
    for dep in dependencies:
        self.Depends(lib, self.KAlias("@"+dep))
    self.KAlias("@"+name, lib)
    return lib


aliasSet = []
def displayAliases(self):
    print "ALIASES"
    for a in list(set(aliasSet)):
        print a
    
def KAlias(self, alias, targets=None):
    aliasSet.append(alias)
    if targets:
        return self.Alias(alias, targets)
    else:
        return self.Alias(alias)
    
def generate(env, *args, **kw):
    env.AddMethod(KProgram)
    env.AddMethod(KStaticLibrary)
    env.AddMethod(KAlias)
    env.AddMethod(displayAliases)
    env.AddMethod(UnitTest)
    env.AddMethod(BuildFiles)
    
    # Create a builder for tests
    bld = None
    if env.GetOption('useValgrind'):
        for s in suppressionFiles:
            extraValgrindOptions += " --suppressions=" + "".join(s.abspath)
        bld = env.Builder(action = builder_unit_test_with_valgrind)
    else:
        bld = env.Builder(action = builder_unit_test)
    env.Append(BUILDERS = {'Test' :  bld})

    # Create a builder for RSync
    rsyncBld = env.Builder(action = builder_rsync)
    env.Append(BUILDERS = {'RSync' :  rsyncBld})

def exists():
    print "we exists"