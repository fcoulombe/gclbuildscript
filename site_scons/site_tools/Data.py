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

import os.path
import SCons.Builder
from SCons.Builder import Builder

import SCons.Action
from SCons.Action import Action

import RunProgram

def builder_copy(target, source, env):
    for t in target:
        rsync = "/usr/bin/rsync --times --force --recursive --update --delete --progress"
        cmdLine = "%s  %s %s" % (rsync, source[0].abspath, t.abspath) 
        #print  cmdLine
        stdout, stderr, returncode = RunProgram.RunProgram(cmdLine)
        
        if stderr and len(stderr):
            print stderr
            return -1
    return 0


def builder_texture(target, source, env):
    for t in target:
        rsync = "/usr/bin/rsync --times --force --recursive --update --delete --progress"
        cmdLine = "%s  %s %s" % (rsync, source[0].abspath, t.abspath) 
        #print  cmdLine
        stdout, stderr, returncode = RunProgram.RunProgram(cmdLine)
        
        if stderr and len(stderr):
            print stderr
            return -1
    return 0

def Texture(self, target):
    t = target.srcnode().abspath
    
    tgtList = []
    if not os.path.exists(t):
        return tgtList
        
    dirList = os.listdir(str(t))
    tgtList = self.RSync(target, None)
    #for d in dirList:
    #    tgtList.extend(self.bTexture(self.File("%s/%s" % (str(target),d))))
    return tgtList

def Sound(self, target):
    t = target.srcnode().abspath
    
    tgtList = []
    if not os.path.exists(t):
        return tgtList
        
    dirList = os.listdir(str(t))
    tgtList = self.RSync(target, None)
    #for d in dirList:
    #    tgtList.extend(self.bTexture(self.File("%s/%s" % (str(target),d))))
    return tgtList

def builder_material(target, source, env):
    for t in target:
        rsync = "/usr/bin/rsync --times --force --recursive --update --delete --progress"
        cmdLine = "%s  %s %s" % (rsync, source[0].abspath, t.abspath+source[0].abspath[-9:]) 
        #print  cmdLine
        stdout, stderr, returncode = RunProgram.RunProgram(cmdLine)
        
        if stderr and len(stderr):
            print stderr
            return -1
    return 0

def Material(self, target):
    t = target.srcnode().abspath
    
    tgtList = []
    if not os.path.exists(t):
        return tgtList
        
    dirList = os.listdir(str(t))
    
    for d in dirList:
        tgtList.extend(self.bMaterial(self.File("%s/%s" % (str(target),d))))
    return tgtList
    
    
def builder_mesh(target, source, env):
    MeshConverterExe = env.File("build/"+env['BUILD_VARIANT']+"/program/tools/meshconverter/meshconverter").abspath
    
    cmdLine = "%s  %s %s" % (MeshConverterExe, source[0].abspath, target[0].abspath) 
    print  cmdLine
    stdout, stderr, returncode = RunProgram.RunProgram(cmdLine)
        
    print stdout
    if stderr and len(stderr):
        print stderr
        return -1
    if returncode != 0:
        return 1
    
    return 0

def Mesh(self, target):
    
    t = target.srcnode().abspath
    
    tgtList = []
    if not os.path.exists(t):
        return tgtList
        
    dirList = os.listdir(str(t))
    
    for d in dirList:
        tgtList.extend(self.bMesh(self.File("%s/%s" % (str(target),d))))
    self.Depends(tgtList, self.Alias("@meshconverter"))
    return tgtList

def builder_music(target, source, env):
    if env['PLATFORM'] == 'win32':
        lameExe = env.File("#3rdParty/lame/lame.exe").abspath
        oggEncExe = env.File("#3rdParty/ogg/oggenc2.exe").abspath
        cmdLine = "%s --decode %s - | %s -o %s -" % (lameExe, source[0].abspath, oggEncExe, target[0].abspath) 
    else:
        cmdLine = "mpg321 %s -w - | oggenc -o %s -" % (source[0].abspath, target[0].abspath) 
    print  cmdLine
    stdout, stderr, returncode = RunProgram.RunProgram(cmdLine)
        
    print stdout
    if stderr and len(stderr):
        print stderr
        return -1
    if returncode != 0:
        return 1
    
    return 0

def Music(self, target):
    
    t = target.srcnode().abspath
    
    tgtList = []
    if not os.path.exists(t):
        return tgtList
        
    dirList = os.listdir(str(t))
    
    for d in dirList:
        tgtList.extend(self.bMusic(self.File("%s/%s" % (str(target),d))))
    return tgtList
    

def builder_sprite_old(target, source, env):
    for t in target:
        rsync = "/usr/bin/rsync --times --force --recursive --update --delete --progress"
        cmdLine = "%s  %s %s" % (rsync, t.srcnode().abspath, os.path.dirname(t.abspath)) 
        #print  cmdLine
        stdout, stderr, returncode = RunProgram.RunProgram(cmdLine)
        
        if stderr and len(stderr):
            print stderr
            return -1
    return 0

from xml.etree import ElementTree
import struct
def builder_sprite(target, source, env):
    for t in target:
        #XML parsing
        root = ElementTree.parse(source[0].srcnode().abspath).getroot()
        rootChildren = root.getchildren()
        header = rootChildren[0]
        width = header.get("width")
        height = header.get("height")
        frameCount = header.get("frame_count")
        
        textures = rootChildren[1]
        textureCount = len(textures.getchildren())
        textureList = []
        #here we should probably check that all textures are the same size
        for tex in textures.getchildren():
            textureFilename = tex.get("filename")
            textureList.append(textureFilename)
            
            
        #binary writing
        f = open(t.abspath, "wb+")
        #print "width: %d" % int(width)
        #print "height: %d" % int(height)
        #print "frameCount: %d" % int(frameCount)
        #print "textureCount: %d" % int(textureCount)
        pad = 0 #pad to 64bits
        binaryData = struct.pack("HHIII", int(width), int(height), int(frameCount), int(textureCount), int(pad))
        f.write(binaryData)
        for tex in textureList:
            f.write(struct.pack("I", len(tex)))
            f.write(tex)
            f.write("\0")
        f.close()
    return 0

def Sprite(self, target):
    t = target.srcnode().abspath
    
    tgtList = []
    if not os.path.exists(t):
        return tgtList
        
    dirList = os.listdir(str(t))
    
    for d in dirList:
        tgtList.extend(self.bSprite(self.File("%s/%s" % (str(target),d))))
    return tgtList
    
def Data(self, target):
    tgtList = []
    for t in target:
        dataPath = t.srcnode().abspath
        if not os.path.exists(dataPath):
            continue
        textureTgtList = self.Texture(self.Dir(str(t)+"/Texture"))
        self.AlwaysBuild(textureTgtList);
        self.KAlias("@build_texture", textureTgtList)
        
        soundTgtList = self.Sound(self.Dir(str(t)+"/Sound"))
        self.AlwaysBuild(soundTgtList);
        self.KAlias("@build_sound", soundTgtList)
        
        materialTgtList = self.Material(self.Dir(str(t)+"/Material"))
        self.KAlias("@build_material", materialTgtList)
        meshTgtList = self.Mesh(self.Dir(str(t)+"/Mesh"))
        self.KAlias("@build_mesh", meshTgtList)
        spriteTgtList = self.Sprite(self.Dir(str(t)+"/Sprite"))
        self.KAlias("@build_sprite", spriteTgtList)
        musicTgtList = self.Music(self.Dir(str(t)+"/Music"))
        self.KAlias("@build_music", musicTgtList)
        tgtList = textureTgtList
        tgtList.extend( soundTgtList)
        tgtList.extend( materialTgtList)
        tgtList.extend( meshTgtList )
        tgtList.extend( spriteTgtList )
        tgtList.extend( musicTgtList )
    self.KAlias("@build_data", tgtList)
    self.KAlias("@build_all", tgtList)
    
    return tgtList
    
def generate(env, *args, **kw):
    # Create a builders for Data
    textureBld =Builder(action = Action(builder_copy, cmdstr='[texture] $TARGET'), suffix='.tex') #,  src_suffix='.x'
    env.Append(BUILDERS = {'bTexture' :  textureBld})

    soundBld =Builder(action = Action(builder_copy, cmdstr='[sound] $TARGET'), suffix='.tex') #,  src_suffix='.x'
    env.Append(BUILDERS = {'bSound' :  soundBld})
    
    materialBld =Builder(action = Action(builder_copy, cmdstr='[material] $TARGET'), suffix='.mat')
    env.Append(BUILDERS = {'bMaterial' :  materialBld})
    
    meshBld =Builder(action = Action(builder_mesh, cmdstr='[mesh] $TARGET'), suffix='.mesh', src_suffix='.fbx')
    env.Append(BUILDERS = {'bMesh' :  meshBld})
    
    musicBld =Builder(action = Action(builder_music, cmdstr='[music] $TARGET'), suffix='.ogg', src_suffix='.mp3')
    env.Append(BUILDERS = {'bMusic' :  musicBld})
    
    
    spriteBld =Builder(action = Action(builder_sprite, cmdstr='[sprite] $TARGET'), suffix='.spr')
    env.Append(BUILDERS = {'bSprite' :  spriteBld})
    
    env.AddMethod(Data)
    env.AddMethod(Texture)
    env.AddMethod(Sound)
    env.AddMethod(Material)
    env.AddMethod(Mesh)
    env.AddMethod(Music)
    env.AddMethod(Sprite)

def exists():
    print "we exists"
