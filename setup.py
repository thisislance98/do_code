import fnmatch
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py as build_py_orig

excluded = ['secret.ini']

class build_py(build_py_orig):
    def find_package_modules(self, package, package_dir):
        modules = super().find_package_modules(package, package_dir)
        return [
            (pkg, mod, file)
            for (pkg, mod, file) in modules
            if not any(fnmatch.fnmatchcase(file, pat=pattern) for pattern in excluded)
        ]

setup(
    name='docode',
    version='0.73',
    #packages=['docode'],
    install_requires=[
        'requests',
        'pickledb'
    ],
    packages=find_packages(exclude=['ez_setup', 'tests', 'tests.*', 'secret.ini']),
    package_data={'docode': ['config.ini']},
    include_package_data=True,
    cmdclass={'build_py': build_py}
)