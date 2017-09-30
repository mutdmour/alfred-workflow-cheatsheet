#!/usr/bin/python
# coding: utf8

import sys
import re
from shortcuts import shortcuts
from workflow import Workflow


wf = None
log = None
apps = None

def main(wf):
    args = wf.args
    run(args)
    wf.send_feedback()
    log.info('Workflow response complete')

# if no args list all apps
def run(args):
    command = args[0].strip()
    log.info("args")
    log.info(args)
    log.info("")

    if (not command):
        addApps(apps)
    elif (u'--commit' in args):#command in apps):
        # log.info('committing')
        command_opts = command.split(':',1)
        app = command_opts[0]
        action = command_opts[1].strip()
        addShortcuts(app, action)
    else:
        filter(command, apps)


def filter(query, items):
    matching = wf.filter(
        query,
        items
    )
    if (len(matching) == 0):
        wf.add_item('none found')
    else:
        addApps(matching)

# returns a list of the apps available as shortcuts
def getApps():
    apps = shortcuts.keys()
    apps.sort(key=str.lower)
    return apps

def addApps(items):
    for i in range(0,len(items)):
        item = items[i]
        wf.add_item(item, autocomplete=' '+item, arg=item+": ", valid=True)

def addShortcuts(app, search):
    actions = shortcuts[app]
    if (search):
        opts = shortcuts[app].keys()
        matching = wf.filter(search, opts)
        if (len(matching) == 0):
            wf.add_item('none found')
        else:
            for k in matching:
                #TODO handle uft8 chars
                wf.add_item(k, actions[k])
    else:
        for k in actions:
            #TODO handle uft8 chars
            wf.add_item(k, actions[k])

# return the shortcut for an action for an app
def getShortcut(app, key):
    return shortcuts[app][key]

if __name__ == '__main__':
    wf = Workflow()
    apps = getApps()
    log = wf.logger
    sys.exit(wf.run(main, text_errors='--commit' in wf.args))