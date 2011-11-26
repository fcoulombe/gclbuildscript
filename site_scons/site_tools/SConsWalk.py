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

import RunProgram
import os.path

def SConsWalkList(self, list, ignore, variant):
    for line in list:
        script = line.strip()
        if script == ignore:
            continue
         
        #print "Parsing... "+line
        env = self.Clone()
        self.Export('env')
        #env.StampTime("parsing..." + line)
        self.SConscript(script, variant_dir='build/'+variant+'/'+os.path.dirname(script), duplicate=0)

def SConsWalk(self, dir, ignore, variant):
    out = RunProgram.RunProgram("find . | grep SConscript")
    self.SConsWalkList(out, variant)

def generate(env, *args, **kw):
    env.AddMethod(SConsWalk)
    env.AddMethod(SConsWalkList)


def exists():
    print "we exists"