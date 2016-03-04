"""
    packager.py lets you make zippable packages out of source code, and lets you
    delete unnecessary source code files.
"""

# pylint: disable-msg=C0103

import json, os, sys, shutil, traceback

print "\033[1;32m"
print "#########################################################################"
print "#                                                                       #"
print "#                               This is                                 #"
print "#                             Packager.py                               #"
print "#                                                                       #"
print "#########################################################################"
print "\033[0m"

errors = []

try:
    if not isinstance(sys.argv[1], basestring) or not os.path.isdir(sys.argv[1]):
        errors.append('the first argument must be a string directory name')

    if not isinstance(sys.argv[2], basestring):
        errors.append('the second argument must be a string destination name')

    print "reading \033[1;33mpackager.json\033[0m...\n"

    """
        packager.json should be in the source dir.
    """
    try:
        packageFiles = json.loads(open(os.path.join(sys.argv[1], 'packager.json'), 'r').read())
    except IOError:
        errors.append('\033[1;33mpackager.json\033[0m not found')
    except ValueError:
        errors.append('\033[1;33mpackager.json\033[0m formatted incorrectly')

except IndexError:
    errors.append('\033[1;33mpackager.py\033[0m expects two arguments.')

if len(errors):
    print "\033[1;31mERRORS!"

    for value in errors:
        print value
    print "\033[0m"

    print """Usage instructions: \npython \033[1;33mpackager.py\033[0m \033[1;34m[string source] [string destination]\033[0m\n"""

    exit()

src = sys.argv[1]
dest = sys.argv[2]

proceedConf = ''

if os.path.isdir(dest):
    proceedConf = raw_input('''\033[1;34m%s\033[0m already exists, do you want
                            to overwrite it? Type "\033[0;32myes\033[0m" or
                            "\033[0;32my\033[0m" to proceed: ''' % (dest))

    if proceedConf != 'yes' and proceedConf != 'y':
        print "\n\033[1;31mABORTING\033[0m\n"
        exit()

if proceedConf != '':
    print "\033[1;33mremoving\033[0m\n"

    shutil.rmtree(dest)

print """\033[1;32mcopying\033[0m \033[1;34m%s\033[0m to \033[1;34m%s\033[0m
      \n""" % (src, dest)

shutil.copytree(src, dest)

print "\033[1;32msuccess\033[0m\n"

print "\033[1;32mapplying actions\033[0m\n"

try:
    for item in packageFiles['delete']['dir']:
        shutil.rmtree(os.path.join(dest, item))
    for item in packageFiles['delete']['file']:
        os.remove(os.path.join(dest, item))

    for index in range(0, len(packageFiles['move']['target'])):
        if os.path.exists(os.path.join(dest, packageFiles['move']['destination'][index])):
            if os.path.isdir(os.path.join(dest, packageFiles['move']['destination'][index])):
                shutil.rmtree(os.path.join(dest, packageFiles['move']['destination'][index]))
            else:
                os.remove(os.path.join(dest, packageFiles['move']['destination'][index]))

        shutil.move(
            os.path.join(dest, packageFiles['move']['target'][index]),
            os.path.join(dest, packageFiles['move']['destination'][index])
        )

    for item in packageFiles['create']['dir']:
        os.mkdir(os.path.join(dest, item))

except OSError:
    print "\033[1;31mSomething's gone wrong!"

    traceback.print_exc()

    print "cleaning up \033[0m"
    shutil.rmtree(dest)

print "\033[1;32mDone!\033[0m\n"
