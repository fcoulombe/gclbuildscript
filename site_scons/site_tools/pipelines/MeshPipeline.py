import os
import Pipeline
import SCons.Builder
from SCons.Builder import Builder
import SCons.Action
from SCons.Action import Action
import RunProgram

pipelineName = "Mesh"
def builder_mesh(target, source, env):
    MeshConverterExe = env.File("build/"+env['BUILD_VARIANT']+"/program/tools/meshconverter/meshconverter").abspath
    
    cmdLine = "%s  %s %s" % (MeshConverterExe, source[0].abspath, target[0].abspath) 
    #print  cmdLine
    stdout, stderr, returncode = RunProgram.RunProgram(cmdLine)
        
    print stdout
    if stderr and len(stderr):
        print stderr
        return -1
    if returncode != 0:
        return 1
    
    return 0

class MeshPipeline(Pipeline.Pipeline):
    def __init__(self):
        self.name = pipelineName + "Pipeline"
        print self.name
        
    def ProcessData(self, env, target):
        target = env.Dir(str(target)+"/"+pipelineName)

        t = target.srcnode().abspath
        
        tgtList = []
        if not os.path.exists(t):
            return tgtList
            
        dirList = os.listdir(str(t))  
        for d in dirList:
            tgtList.extend(env.MeshBuilder(env.File("%s/%s" % (str(target),d))))
        env.Depends(tgtList, env.Alias("@meshconverter"))
        env.AlwaysBuild(tgtList);
        env.KAlias("@build_meshes", tgtList)
        return tgtList

       
    def generate(seld, env):
        bld =Builder(action = Action(builder_mesh, cmdstr='[mesh] $TARGET'), suffix='.mesh', src_suffix='.fbx')
        env.Append(BUILDERS = {'MeshBuilder' :  bld})
      
pipeline = MeshPipeline()