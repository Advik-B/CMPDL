from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
ext_modules = [

    Extension("backend",  ["backend.py"]),
    Extension("logger", ["logger.py"]),
    Extension('tree_generator', ['tree_generator.py']),
]

setup(
    name = 'CMPDL',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules)