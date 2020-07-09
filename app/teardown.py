import os
import glob
import shutil

print('hi')

for path in glob.iglob(os.path.join('C:', 'Users', 'admin', 'AppData', 'Local', 'Temp', 'scoped_dir*')):
    print(path)
    shutil.rmtree(path)

for path in glob.iglob(os.path.join('C:', 'Users', 'admin', 'AppData', 'Local', 'Temp', 'chrome_BITS_*')):
    print(path)
    shutil.rmtree(path)

print('bye')