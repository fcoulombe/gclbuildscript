import os
import Pipeline
import SCons.Builder
from SCons.Builder import Builder
import SCons.Action
from SCons.Action import Action

pipelineName = "Material"

class MaterialPipeline(Pipeline.Pipeline):
    def __init__(self):
        self.name = pipelineName + "Pipeline"
        print self.name
        
    def ProcessData(self, env, target):
        target = env.Dir(str(target)+"/"+pipelineName)
        #textureTgtList = self.Texture(env.Dir(str(target)+"/Texture"))
        t = target.srcnode().abspath
        
        tgtList = []
        if not os.path.exists(t):
            return tgtList
            
        dirList = os.listdir(str(t))
        for d in dirList:
            tgtList.extend(env.MaterialBuilder(env.File("%s/%s" % (str(target),d))))

        env.AlwaysBuild(tgtList);
        env.KAlias("@build_materials", tgtList)
        return tgtList

       
    def generate(seld, env):
        materialBld =Builder(action = Action(Pipeline.builder_copy, cmdstr='[material] $TARGET'), suffix='.mat')
        env.Append(BUILDERS = {pipelineName + 'Builder' :  materialBld})

pipeline = MaterialPipeline()