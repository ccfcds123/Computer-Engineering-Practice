from xgolib import XGO
dog = XGO("xgolite")

version = dog.read_firmware()

if version[0] == 'M':
    print('XGO-MINI')
else:
    print('XGO-LITE')


