import os
import Pipeline
import SCons.Builder
from SCons.Builder import Builder
import SCons.Action
from SCons.Action import Action
import RunProgram

pipelineName = "Sprite"
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

class SpritePipeline(Pipeline.Pipeline):
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
            tgtList.extend(env.SpriteBuilder(env.File("%s/%s" % (str(target),d))))
  
        env.AlwaysBuild(tgtList);
        env.KAlias("@build_sprites", tgtList)
        return tgtList

       
    def generate(seld, env):
        spriteBld =Builder(action = Action(builder_sprite, cmdstr='[sprite] $TARGET'), suffix='.spr')
        env.Append(BUILDERS = {'SpriteBuilder' :  spriteBld})
      
pipeline = SpritePipeline()