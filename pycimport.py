import sys, imp, os

"""
Teach PyPy about loading .pyc files; it seems to have forgotten.
"""

from twisted.python.modules import getModule

if 'PyPy' in sys.version:
    class PycImporter(object):
        SUFFIX = ('.pyc', 'rb', imp.PY_COMPILED)

        def _findModule(self, fullname, path=None):
            # print "_findModule called with:", fullname, path

            mod = getModule(fullname)
            if mod.filePath.path.endswith('.pyc'):
                return mod.filePath.path, mod.isPackage()
            return None


        def find_module(self, fullname, path=None):
            """
            We can be used to load a module if:

            a) the pyc file exists, or
            b) it's a module for which an __init__.pyc file exists.
            """
            # print "find_module called with:", fullname, path
            result = self._findModule(fullname, path)
            if result is not None:
                return self # We can find it...
            else:
                return None


        def load_module(self, fullname):
            # print "load_module called with:", fullname
            filename, isPackage = self._findModule(fullname)
            # print "load_module using", filename, isPackage
            fp = open(filename, 'rb')
            mod = imp.load_module(fullname, fp, filename, self.SUFFIX)
            mod.__path__ = [os.path.dirname(filename)]
            return mod
            
    importer = PycImporter()
    sys.meta_path.append(importer)

# TODO write tests
#import a
#print 'a.a is %s' % (a.a,)

# from module import b
# print 'b.b is %s' % (b.b,)

