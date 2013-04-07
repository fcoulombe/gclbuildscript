import os
import platform
import Pipeline
import SCons.Builder
from SCons.Builder import Builder
import SCons.Action
from SCons.Action import Action
import RunProgram

pipelineName = "Script"
if platform.architecture()[0] == "64bit":
    LuaCompilerExePath = "#3rdparty/lua/bin/luac64.exe"
else:
    LuaCompilerExePath = "#3rdparty/lua/bin/luac.exe"

global LuaCompilerExe

def builder_script(target, source, env):
    global LuaCompilerExe
    cmdLine = "%s -o %s %s" % (LuaCompilerExe, target[0].abspath, source[0].abspath) 
    #print  cmdLine
    stdout, stderr, returncode = RunProgram.RunProgram(cmdLine)
        
    print stdout
    if stderr and len(stderr):
        print stderr
        return -1
    if returncode != 0:
        return 1
    
    return 0
class ScriptPipeline(Pipeline.Pipeline):
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
            print "Script: " + d
            tgtList.extend(env.ScriptBuilder(env.File("%s/%s" % (str(target),d))))

        env.AlwaysBuild(tgtList);
        env.KAlias("@build_scripts", tgtList)
        return tgtList

       
    def generate(seld, env):
        global LuaCompilerExe
        LuaCompilerExe = env.File(LuaCompilerExePath).abspath
    
        scriptBld =Builder(action = Action(builder_script, cmdstr='[script] $TARGET'), suffix='.luascript')
        env.Append(BUILDERS = {pipelineName + 'Builder' :  scriptBld})

pipeline = ScriptPipeline()
