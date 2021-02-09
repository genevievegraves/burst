import os, sys, argparse

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--cloudmap", required=True, help="as passed to burst")
parser.add_argument("--testpath", required=True, help="bucket or root directory for tests")
parser.add_argument("--storage-config")
parser.add_argument("--compute-config")
parser.add_argument("--verbosity", type=int, default=1)
args = parser.parse_args()

out1 = "----------------------END-------------------------"

out2 = "123\n456\n"

out3 = "<!DOCTYPE html>"

os.system("rm fulltest.log fulltest.foo fulltest.ports")

os.system("python3 fulltest_ports.py &")

opts = "--verbosity={0} --cloudmap={1}".format(args.verbosity, args.cloudmap)
if args.storage_config:
    opts += " --storage-config={0}".format(args.storage_config)
if args.compute_config:
    opts += " --compute-config={0}".format(args.compute_config)

root = args.cloudmap.split(':')[1]

cmd = "burst -p 6789:80 {0} 'python3 fulltest_command.py --testpath={1}/{2}' 2>&1 | tee fulltest.log".format(opts, root, args.testpath)
print (cmd)
os.system(cmd)

f = open("fulltest.log")
s = f.read()
f.close()

foo = None
if os.path.exists("fulltest.foo"):
    f = open("fulltest.foo")
    foo = f.read()
    f.close()

ports = ""
if os.path.exists("fulltest.ports"):
    f = open("fulltest.ports")
    ports = f.read()
    f.close()

print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TEST COMPLETED~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

if out1 in s:
    print ("PASSED main test")
else:
    print ("FAILED main test")

if out2 == foo:
    print ("PASSED cloudmap test")
else:
    print ("FAILED cloudmap test")

if ports.find(out3)==0:
    print ("PASSED portmap test")
else:
    print ("FAILED portmap test")


