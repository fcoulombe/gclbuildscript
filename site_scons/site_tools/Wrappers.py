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

def builder_unit_test(target, source, env):
    app = str(source[0].abspath)
    if os.spawnl(os.P_WAIT, app, app)==0:
        open(str(target[0]),'w').write("PASSED\n")
    else:
        return 1


def BuildFiles(self, src_files, dependencies):
    self.AppendDependenciesCFlags(dependencies)
    objs = self.Object(src_files)
    return objs
    
def UnitTest(self, name, src_files, dependencies):
    prog = self.KProgram(name, src_files, dependencies)
    self.Test(name+".passed", prog)
    self.Alias(name+"_run", name+".passed")
    self.Alias("@run_all", self.Alias(name+"_run"))
    
def KProgram(self, name, src_files, dependencies):
    objs = self.BuildFiles(src_files, dependencies)
    self.AppendDependenciesLFlags(dependencies)
    prog = self.Program(name, objs)
    for dep in dependencies:
        self.Depends(prog, self.Alias("@"+dep))
    self.Alias("@"+name, prog)
    return prog
    
def KStaticLibrary(self, name,  src_files, dependencies):
    objs = self.BuildFiles(src_files, dependencies)
    self.AppendDependenciesLFlags(dependencies) 
    lib = self.StaticLibrary(name, objs)
    for dep in dependencies:
        self.Depends(lib, self.Alias("@"+dep))
    self.Alias("@"+name, lib)
    return lib
    
def generate(env, *args, **kw):
    env.AddMethod(KProgram)
    env.AddMethod(KStaticLibrary)
    env.AddMethod(UnitTest)
    env.AddMethod(BuildFiles)
    
    # Create a builder for tests
    bld = env.Builder(action = builder_unit_test)
    env.Append(BUILDERS = {'Test' :  bld})



def exists():
    print "we exists"