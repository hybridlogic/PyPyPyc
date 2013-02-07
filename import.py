import sys, imp, os

"""
Teach PyPy about loading .pyc files; it seems to have forgotten.
"""

if 'PyPy' in sys.version:
    class PycImporter(object):
        SUFFIX = ('.pyc', 'rb', imp.PY_COMPILED)

        def _findModule(self, fullname, path=None):
            print "_findModule called with:", fullname, path
            fullname = fullname.replace(".", "/") # e.g. module/b

            fullpath = "%s.pyc" % (fullname,) # e.g. module/b.pyc
            if path is not None:
                fullpath = "%s/%s" % (path, fullpath) # e.g. /usr/local/lib/python-foo/module/b.pyc?

            if os.path.exists(fullpath):
                return fullpath, False

            maybeModule = "%s/__init__.pyc" % (fullname,)
            if os.path.exists(maybeModule):
                return maybeModule, True

            return None


        def find_module(self, fullname, path=None):
            """
            We can be used to load a module if:

            a) the pyc file exists, or
            b) it's a module for which an __init__.pyc file exists.
            """
            print "find_module called with:", fullname, path
            result = self._findModule(fullname, path)
            if result is not None:
                return self # We can find it...
            else:
                return None


        def load_module(self, fullname):
            print "load_module called with:", fullname
            filename, isPackage = self._findModule(fullname)
            print "load_module using", filename, isPackage
            fp = open(filename, 'rb')
            return imp.load_module(fullname, fp, filename, self.SUFFIX)


    importer = PycImporter()
    sys.meta_path.append(importer)


import a
print 'a.a is %s' % (a.a,)

from module import b
print 'b.b is %s' % (b.b,)


"""
            # Look for pyc files in the current path to start with.
            print "looking for", fullname
            maybePyc = "%s.pyc" % (fullname,)
            # Seems like returning None 
            if os.path.exists(maybePyc):
                return (open(maybePyc, 'rb'), maybePyc, 
"""
