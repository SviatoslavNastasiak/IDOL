from distutils.core import setup, Extension

getter_module = Extension('_getter', sources = ['getter_wrap.c', 'getter.c'])
setup(name = 'getter', ext_modules = [getter_module], py_modules = ["getter"])
