
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
    
    
def ExpandDependencies(dependencies, expandedDependencyList):
    global componentList
    for dep in dependencies:
        ExpandDependencies(componentList[dep].dependencies, expandedDependencyList)
        expandedDependencyList.append(dep)
    
    
def AppendDependenciesCFlags(self, dependencies):
    expandedDependencyList = []
    ExpandDependencies(dependencies, expandedDependencyList)    
    for dep in expandedDependencyList:
        if componentList[dep].incpath:
            self.Append(CPPPATH=componentList[dep].incpath)
        else:
            componentList[dep].CFlagsSetter(self)   
    
def AppendDependenciesLFlags(self, dependencies):
    expandedDependencyList = []
    ExpandDependencies(dependencies, expandedDependencyList)    
    for dep in expandedDependencyList:
        if componentList[dep].lib:
            self.Append(LINKFLAGS=componentList[dep].lib)
        else:
            componentList[dep].LFlagsSetter(self)      
    

def generate(env, *args, **kw):
    env.AddMethod(AddComponent)
    env.AddMethod(AppendDependenciesCFlags)
    env.AddMethod(AppendDependenciesLFlags)


def exists():
    print "we exists"
