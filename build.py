# Simple automatization for building an addon

import sys
import os
import shutil

class Const:
    ANKI = 0
    ZIP = 1
    CLEAR = 3

addonIndex = None
mode = None
target = None

acceptedArgs = ('-source', '-dist', '-dev', '-clear')
existingAddons = ('schedule_priority', 'anki_web_browser')

print ('====================== Building RSS Addon =====================')

for index, value in enumerate(sys.argv):
    if value not in acceptedArgs:
        continue

    if value == acceptedArgs[0]: #source
        if (index + 1) > len(sys.argv) - 1:
            raise IOError('Incorrect parameters. After "-source" there must be a value ')
        addonIndex = sys.argv[index + 1]
    elif value == acceptedArgs[1]:
        mode = Const.ZIP      # dist
        target = '/dist'
    elif value == acceptedArgs[2]:
        if mode:
            print('Already set to dist mode. Ignoring -dev')
        else:
            mode = Const.ANKI
            target = './dist' #os.environ['anki_addon']
    elif value == acceptedArgs[3]:  # clear
        mode = Const.CLEAR
        target = './dist' #os.environ['anki_addon']

# -----------------------------------------------------------

print ('Choose an addon to be processed ===============================')

for index, name in enumerate(existingAddons):
    print('{} - {}'.format(index, name))

print ('-'*60)

addonIndex = int(input('> '))

if not addonIndex or addonIndex > len(existingAddons):
    raise IOError('It was not possible to determine a valid addon as input')

addon = existingAddons[addonIndex]

if not target:
    raise IOError('No mode was informed. Choose either -dev or -dist')
# -----------------------------------------------------------

currentDir = os.path.dirname(os.path.realpath(__file__))

if mode == Const.ZIP:
    if os.path.exists('dist'):
        print('Cleaning dist directory')
        shutil.rmtree('dist/')
    print('Copying files')    
    shutil.copytree(currentDir + '/' + addon.replace('_', '-'),  './dist', 
    ignore=shutil.ignore_patterns('tests', 'doc', '*_test*', '__pycache__'))
    
    print('Creating binary')
    shutil.make_archive(addon, format = 'zip', 
    root_dir='dist')

# copies to anki's addon folder - test integrated
elif mode == Const.ANKI:
    if os.path.exists(target + '/' + addon + '.py'):
        print('Removing old files: {}'.format(target + '/' + addon))
        shutil.rmtree(target + '/' + addon)
        os.remove(target + '/' + addon + '.py')

    print('Copying files to anki directory')
    shutil.copytree(currentDir + '/' + addon.replace('_', '-') + '/',  target + '/' + addon, 
    ignore=shutil.ignore_patterns('tests', 'doc', '*_test*', '__pycache__'))

# Deletes from anki addons
elif mode == Const.CLEAR:
    if os.path.exists(target + '/' + addon):
        print('Removing old files: {}'.format(target + '/' + addon))
        shutil.rmtree(target + '/' + addon)
        os.remove(target + '/' + addon + '.py')
    else:
        print('Addon was not found on the target path: {}'.format(target + '/' + addon + '.py'))