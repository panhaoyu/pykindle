import os
import shutil
import setuptools

print('自动检测到的依赖包：')
[print('\t', package) for package in setuptools.find_packages()]
print()

if os.path.exists('dist'):
    shutil.rmtree('dist')
os.system('python setup.py sdist bdist_wheel')
os.system('twine upload dist/*')
