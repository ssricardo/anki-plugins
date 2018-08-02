# Simple automatization for building an addon
# TODO yet

import sys
import os

print(sys.argv)

class Const:
    ANKI = 0
    ZIP = 1

addon = None
mode = None
target = None

acceptedArgs = ('-source', '-dist', '-dev')
existingAddons = ('schedule-priority', 'anki-web-browser')

print ('========================= Building RSS Addon ========================')

for index, value in enumerate(sys.argv):
    if value not in acceptedArgs:
        continue

    if value == acceptedArgs[0]: #source
        if (index + 1) > len(sys.argv) - 1:
            raise IOError('Incorrect parameters. After "-source" there must be a value ')
        addon = sys.argv[index + 1]
    elif value == acceptedArgs[1]:
        mode = Const.ZIP      # dist
        target = '/dist'
    elif value == acceptedArgs[2]:
        if mode:
            print('Already set to dist mode. Ignoring -dev')
        else:
            mode = Const.ANKI
            target = 'D:\\dev\\git\\anki-plugins\\dist' #os.environ['anki_addon']

print (addon)

if not addon or addon not in existingAddons:
    raise IOError('It was not possible to determine a valid addon as input')

import shutil
import os

currentDir = os.path.dirname(os.path.realpath(__file__))

if mode == Const.ZIP:
    if os.path.exists('dist'):
        print('Cleaning dist directory')
        shutil.rmtree('dist/')
    print('Copying files')    
    shutil.copytree(currentDir + '/' + addon,  './dist', 
    ignore=shutil.ignore_patterns('tests', 'doc', '*_test*'))
    
    print('Creating binary')
    shutil.make_archive(addon, format = 'zip', 
    root_dir='dist')
else:
    if os.path.exists(target + '/' + addon):
        print('Removing old files')
        shutil.rmtree(target + '/' + addon)
    print('Copying files to anki directory')
    shutil.copytree(currentDir + '/' + addon + '/',  target + '/' + addon, 
    ignore=shutil.ignore_patterns('tests', 'doc', '*_test*'))