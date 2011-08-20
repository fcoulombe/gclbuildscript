import subprocess

def RunProgram(cmdLine):
    p = subprocess.Popen(cmdLine, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout = []
    for line in p.stdout.readlines():
        stdout.append(line)
    retval = p.wait()
    return stdout