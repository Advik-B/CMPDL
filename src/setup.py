from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
ext_modules = [

    Extension("source",  ["__main__.py", "backend.py", 'logger.py', 'tree_generator.py'])
]

setup(
    name = 'CMPDL',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules)