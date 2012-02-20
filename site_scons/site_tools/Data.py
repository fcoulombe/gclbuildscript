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
        stdout, stderr = RunProgram.RunProgram(cmdLine)
        
        if stderr and len(stderr):
            print stderr
            return -1
    return 0


def builder_texture(target, source, env):
    for t in target:
        rsync = "/usr/bin/rsync --times --force --recursive --update --delete --progress"
        cmdLine = "%s  %s %s" % (rsync, source[0].abspath, t.abspath) 
        #print  cmdLine
        stdout, stderr = RunProgram.RunProgram(cmdLine)
        
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

def builder_material(target, source, env):
    for t in target:
        rsync = "/usr/bin/rsync --times --force --recursive --update --delete --progress"
        cmdLine = "%s  %s %s" % (rsync, source[0].abspath, t.abspath+source[0].abspath[-9:]) 
        #print  cmdLine
        stdout, stderr = RunProgram.RunProgram(cmdLine)
        
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
    for t in target:
        rsync = "/usr/bin/rsync --times --force --recursive --update --delete --progress"
        cmdLine = "%s  %s %s" % (rsync, t.srcnode().abspath, os.path.dirname(t.abspath)) 
        #print  cmdLine
        stdout, stderr = RunProgram.RunProgram(cmdLine)
        
        if stderr and len(stderr):
            print stderr
            return -1
    return 0

def Mesh(self, target):
    t = target.srcnode().abspath
    
    tgtList = []
    if not os.path.exists(t):
        return tgtList
        
    dirList = os.listdir(str(t))
    
    for d in dirList:
        tgtList.extend(self.bMesh(self.File("%s/%s" % (str(target),d))))
    return tgtList
    

def builder_sprite_old(target, source, env):
    for t in target:
        rsync = "/usr/bin/rsync --times --force --recursive --update --delete --progress"
        cmdLine = "%s  %s %s" % (rsync, t.srcnode().abspath, os.path.dirname(t.abspath)) 
        #print  cmdLine
        stdout, stderr = RunProgram.RunProgram(cmdLine)
        
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
        for tex in textures.getchildren():
            textureFilename = tex.get("filename")
            textureList.append(textureFilename)
            
            
        #binary writing
        f = open(t.abspath, "wb+")
        #print "width: %d" % int(width)
        #print "height: %d" % int(height)
        #print "frameCount: %d" % int(frameCount)
        #print "textureCount: %d" % int(textureCount)
        
        binaryData = struct.pack("HHLL", int(width), int(height), int(frameCount), int(textureCount))
        f.write(binaryData)
        for tex in textureList:
            f.write(struct.pack("L", len(tex)))
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
        self.KAlias("@build_texture", textureTgtList)
        materialTgtList = self.Material(self.Dir(str(t)+"/Material"))
        self.KAlias("@build_material", materialTgtList)
        meshTgtList = self.Mesh(self.Dir(str(t)+"/Mesh"))
        self.KAlias("@build_mesh", meshTgtList)
        spriteTgtList = self.Sprite(self.Dir(str(t)+"/Sprite"))
        self.KAlias("@build_sprite", spriteTgtList)
        tgtList = textureTgtList
        tgtList.extend( materialTgtList)
        tgtList.extend( meshTgtList )
        tgtList.extend( spriteTgtList )
    self.KAlias("@build_data", tgtList)
    self.KAlias("@build_all", tgtList)
    
    return tgtList
    
def generate(env, *args, **kw):
    # Create a builders for Data
    textureBld =Builder(action = Action(builder_copy, cmdstr='[texture] $TARGET'), suffix='.tex') #,  src_suffix='.x'
    env.Append(BUILDERS = {'bTexture' :  textureBld})
    
    materialBld =Builder(action = Action(builder_copy, cmdstr='[material] $TARGET'), suffix='.mat')
    env.Append(BUILDERS = {'bMaterial' :  materialBld})
    
    meshBld =Builder(action = Action(builder_copy, cmdstr='[mesh] $TARGET'), suffix='.mesh')
    env.Append(BUILDERS = {'bMesh' :  meshBld})
    
    spriteBld =Builder(action = Action(builder_sprite, cmdstr='[sprite] $TARGET'), suffix='.spr')
    env.Append(BUILDERS = {'bSprite' :  spriteBld})
    
    env.AddMethod(Data)
    env.AddMethod(Texture)
    env.AddMethod(Material)
    env.AddMethod(Mesh)
    env.AddMethod(Sprite)

def exists():
    print "we exists"