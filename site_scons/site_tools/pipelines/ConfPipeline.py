import os
import Pipeline
import SCons.Builder
from SCons.Builder import Builder
import SCons.Action
from SCons.Action import Action

pipelineName = "Conf"

class ConfPipeline(Pipeline.Pipeline):
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
        env.KAlias("@build_conf", tgtList)
        return tgtList

       
    def generate(seld, env):
        confBld =Builder(action = Action(Pipeline.builder_copy, cmdstr='[conf] $TARGET'), suffix='.conf') #,  src_suffix='.x'
        env.Append(BUILDERS = {'ConfBuilder' :  confBld})

pipeline = ConfPipeline()
