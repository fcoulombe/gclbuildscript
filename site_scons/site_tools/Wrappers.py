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