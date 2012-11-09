import os
import Pipeline
import SCons.Builder
from SCons.Builder import Builder
import SCons.Action
from SCons.Action import Action

pipelineName = "Font"

class FontPipeline(Pipeline.Pipeline):
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
        env.KAlias("@build_fonts", tgtList)
        return tgtList

       
    def generate(seld, env):
        fontBld =Builder(action = Action(Pipeline.builder_copy, cmdstr='[font] $TARGET'), suffix='.ttf', src_suffix='.font')
        env.Append(BUILDERS = {'FontBuilder' :  fontBld})
       
pipeline = FontPipeline()