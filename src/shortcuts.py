# coding: utf8

import imp
import os
import importlib
import collections
import cPickle

#https://stackoverflow.com/questions/487971/is-there-a-standard-way-to-list-names-of-python-modules-in-a-package
MODULE_EXTENSIONS = ('.py')#, '.pyc', '.pyo')
def package_contents(package_name):
    file, pathname, description = imp.find_module(package_name)
    if file:
        raise ImportError('Not a package: %r', package_name)
    # Use a set because some may be both source and compiled.
    return set([os.path.splitext(module)[0]
        for module in os.listdir(pathname)
        if module.endswith(MODULE_EXTENSIONS) and module != "__init__.py"])

cheatsheet = {}
apps = package_contents("apps")
for app in apps:
    module = "apps."+app
    app_shortcuts = importlib.import_module(module).shortcuts
    for app_name in app_shortcuts:
        cheatsheet[app_name] = app_shortcuts[app_name]


def convert(data):
    if isinstance(data, basestring):
        return data.decode('utf-8').strip()
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data

unicode_cheatsheet = convert(cheatsheet)

output = open('default_cheatsheet.pkl', 'wb')
cPickle.dump(unicode_cheatsheet, output)
output.close()

print "pkl file updated"