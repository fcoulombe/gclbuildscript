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
from Component import DefaultCFlagsSetter
from Component import DefaultLFlagsSetter
from Component import Component
        
componentList = dict()
    
def AddComponent(self, name, cflags, incpath, lib, dependencies, cflagsSetter=DefaultCFlagsSetter, lflagsSetter=DefaultLFlagsSetter):
    global componentList
    comp = Component()
    comp.name = name
    comp.cflags = cflags
    comp.incpath = incpath
    comp.lib = lib
    comp.dependencies = dependencies
    comp.CFlagsSetter = cflagsSetter
    comp.LFlagsSetter = lflagsSetter
    
    if not componentList.has_key(comp.name):
        componentList[comp.name] = comp
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
        if componentList[dep].CFlagsSetter == DefaultCFlagsSetter:
            if self.GetOption("print-component-dependencies"): 
                for c in componentList[dep].incpath:
                    print "adding cpppath: %s" % (str(c))
            
            
            incpath = componentList[dep].incpath
            if incpath:
                self.Append(CPPPATH=incpath)
                self.Append(CXXPATH=incpath)
                self.Append(CPATH=incpath)
                
            cflags = componentList[dep].cflags
            if cflags:
                self.Append(CPPFLAGS=cflags)
                self.Append(CXXFLAGS=cflags)
                self.Append(CFLAGS=cflags)
        else:
            componentList[dep].CFlagsSetter(self)   
    
def AppendDependenciesLFlags(self, dependencies):
    global componentList
    for dep in dependencies:
        if componentList[dep].LFlagsSetter == DefaultLFlagsSetter:
            self.Append(LIBS=componentList[dep].lib)
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
