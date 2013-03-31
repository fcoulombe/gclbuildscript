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
import sys
import SCons.Builder
from SCons.Builder import Builder

import SCons.Action
from SCons.Action import Action

import RunProgram

global modList
global pipelineDir

    
def Data(self, target):
    global modList
    tgtList = []
    for t in target:
        dataPath = t.srcnode().abspath
        if not os.path.exists(dataPath):
            continue
         
        for mod in modList:
            tgt = modList[mod].pipeline.ProcessData(self, t)
            tgtList.extend(tgt)
    self.KAlias("@build_data", tgtList)
    self.KAlias("@build_all", tgtList)
    
    return tgtList
    
def generate(env, *args, **kw):
    global modList
    pipelineDir = env.Dir("#gclbuildscript/site_scons/site_tools/pipelines/").abspath
    sys.path.append(pipelineDir)
    modList = dict()
    # Create a builders for Data
    env.AddMethod(Data)
    for file in os.listdir(pipelineDir):
        if file[-3:] == "pyc":
            continue
        modname = file[0:-3]
        if modname == "Pipeline":
            continue
        mod = __import__(modname)
        modList[modname] = mod
        #print modname
        modList[modname].pipeline.generate(env)

def exists():
    print "we exists"
