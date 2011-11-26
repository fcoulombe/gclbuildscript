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

def DefaultCFlagsSetter(env):
    return
    
def DefaultLFlagsSetter(env):
    return

class Component(object):
    def __init__(self, name, incpath, lib, dependencies, cflagsSetter=DefaultCFlagsSetter, lflagsSetter=DefaultLFlagsSetter):
        self.name = name
        self.incpath = incpath
        self.lib = lib
        self.dependencies = dependencies
        self.CFlagsSetter = cflagsSetter
        self.LFlagsSetter = lflagsSetter
        #self.libpath = libpath
        
componentList = dict()
    
def AddComponent(self, name, incpath, lib, dependencies, cflagsSetter=DefaultCFlagsSetter, lflagsSetter=DefaultLFlagsSetter):
    global componentList
    if not componentList.has_key(name):
        newComponent = Component(name, incpath, lib, dependencies, cflagsSetter, lflagsSetter)
        componentList[name] = newComponent
    else:
        print "we're adding a component twice?"
    
    
def ExpandDependencies(self, dependencies, expandedDependencyList):
    global componentList
    for dep in dependencies:
        self.ExpandDependencies(componentList[dep].dependencies, expandedDependencyList)
        expandedDependencyList.insert(0,dep)
    
    
def AppendDependenciesCFlags(self, dependencies):
    global componentList
    for dep in dependencies:
        if componentList[dep].incpath:
            if self.GetOption("print-component-dependencies"): 
                for c in componentList[dep].incpath:
                    print "adding cpppath: %s" % (str(c))
            self.Append(CPPPATH=componentList[dep].incpath)
            self.Append(CXXPATH=componentList[dep].incpath)
            self.Append(CPATH=componentList[dep].incpath)
        else:
            componentList[dep].CFlagsSetter(self)   
    
def AppendDependenciesLFlags(self, dependencies):
    global componentList
    for dep in dependencies:
        if componentList[dep].lib:
            
            self.Append(LIBS=componentList[dep].lib)
            #self.Append(LINKFLAGS=componentList[dep].lib)
            if self.GetOption("print-component-dependencies"): 
                for c in componentList[dep].lib:
                    print "adding linkflag: %s" % (str(c))
        else:
            componentList[dep].LFlagsSetter(self)      
    

def generate(env, *args, **kw):
    env.AddMethod(AddComponent)
    env.AddMethod(AppendDependenciesCFlags)
    env.AddMethod(AppendDependenciesLFlags)
    env.AddMethod(ExpandDependencies)


def exists():
    print "we exists"
