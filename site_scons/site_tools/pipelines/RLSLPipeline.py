import os
import Pipeline
import SCons.Builder
from SCons.Builder import Builder
import SCons.Action
from SCons.Action import Action

pipelineName = "RLSL"

class RLSLPipeline(Pipeline.Pipeline):
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
        tgtList = env.RSync(target, None)
        
        env.AlwaysBuild(tgtList);
        env.KAlias("@build_rlsl", tgtList)
        return tgtList

       
    def generate(seld, env):
        rlslBld =Builder(action = Action(Pipeline.builder_copy, cmdstr='[rlsl] $TARGET'), suffix='.rlsl') #,  src_suffix='.x'
        env.Append(BUILDERS = {'RLSLBuilder' :  rlslBld})

pipeline = RLSLPipeline()
