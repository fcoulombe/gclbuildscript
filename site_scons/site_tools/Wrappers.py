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

def BuildFiles(self, src_files, dependencies):
    self.AppendDependenciesCFlags(dependencies)
    objs = self.Object(src_files)
    return objs
    
def KProgram(self, name, src_files, dependencies):
    expandedDependencyList = []
    self.ExpandDependencies( dependencies, expandedDependencyList)   
    if self.GetOption("print-component-dependencies"): 
        print "prog: %s \t\tdep: %s" % (name,expandedDependencyList)
        for f in src_files:
            print "src: %s" % str(f)
    
    objs = self.BuildFiles(src_files, expandedDependencyList)
    self.AppendDependenciesLFlags(expandedDependencyList)
    prog = self.Program(name, objs)
    self.CopyDllDepencency(prog, expandedDependencyList)
    progAlias =self.KAlias("@"+name, prog)
    for dep in expandedDependencyList:
        self.Depends(progAlias, self.KAlias("@"+dep))
    
    self.KAlias("@build_all", prog)
    return prog
    
def KStaticLibrary(self, name,  src_files, dependencies):
    expandedDependencyList = []
    self.ExpandDependencies( dependencies, expandedDependencyList)    
    if self.GetOption("print-component-dependencies"): 
        print "lib: %s \t\tdep: %s" % (name,expandedDependencyList)
        for f in src_files:
            print "src: %s" % str(f)
    objs = self.BuildFiles(src_files, expandedDependencyList)
    self.AppendDependenciesLFlags(expandedDependencyList) 
    lib = self.StaticLibrary(name, objs)
    staticLibAlias = self.KAlias("@"+name, lib)
    for dep in expandedDependencyList:
        self.Depends(staticLibAlias, self.KAlias("@"+dep))
    
    self.KAlias("@build_all", lib)
    return lib


aliasSet = []
def displayAliases(self):
    print "ALIASES"
    for a in sorted(list(set(aliasSet))):
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
    env.AddMethod(BuildFiles)
    

def exists():
    print "we exists"