import RunProgram
import os.path


def SConsWalk(self, dir, ignore):
    out = RunProgram.RunProgram("find . | grep SConscript")
    for line in out:
        script = line.strip()
        if script == ignore:
            continue
         
        env = self.Clone()
        self.Export('env')
        self.SConscript(script, variant_dir='build/'+os.path.dirname(script), duplicate=0)

def generate(env, *args, **kw):
    env.AddMethod(SConsWalk)


def exists():
    print "we exists"