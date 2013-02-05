import os
import Pipeline
import SCons.Builder
from SCons.Builder import Builder
import SCons.Action
from SCons.Action import Action
import RunProgram

pipelineName = "Music"
def builder_music(target, source, env):
    if env['PLATFORM'] == 'win32':
        lameExe = env.File("#3rdParty/lame/lame.exe").abspath
        oggEncExe = env.File("#3rdParty/ogg/bin/oggenc.exe").abspath
        cmdLine = "%s --decode %s - | %s -o %s -" % (lameExe, source[0].abspath, oggEncExe, target[0].abspath) 
    else:
        cmdLine = "mpg321 %s -w - | oggenc -o %s -" % (source[0].abspath, target[0].abspath) 
    if env.GetOption('verbose'):
        print  cmdLine
    stdout, stderr, returncode = RunProgram.RunProgram(cmdLine)
        
    #print stdout
    if stderr and len(stderr):
        print stderr
        return -1
    if returncode != 0:
        print stdout
        return 1
    
    return 0

class MusicPipeline(Pipeline.Pipeline):
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
            tgtList.extend(env.MusicBuilder(env.File("%s/%s" % (str(target),d))))
  
        env.AlwaysBuild(tgtList);
        env.KAlias("@build_musics", tgtList)
        return tgtList

       
    def generate(seld, env):
        musicBld =Builder(action = Action(builder_music, cmdstr='[music] $TARGET'), suffix='.ogg', src_suffix='.mp3')
        env.Append(BUILDERS = {'MusicBuilder' :  musicBld})
      
pipeline = MusicPipeline()