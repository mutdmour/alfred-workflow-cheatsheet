#!/usr/bin/python
# encoding=utf8

update_settings = {
    'github_slug': 'mutdmour/alfred-workflow-cheatsheet',
}

import sys
from workflow import Workflow, ICON_INFO
import cPickle

wf = None
log = None
apps = None

pkl_file = open('default_cheatsheet.pkl', 'rb')
shortcuts = cPickle.load(pkl_file)

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

    if wf.update_available:
    # Add a notification to top of Script Filter results
        wf.add_item('New version available',
                'Action this item to install the update',
                autocomplete='workflow:update',
                icon=ICON_INFO)

    if (not command):
        addApps(apps)
    elif (u'--commit' in args):
        command_opts = command.split(':',1)
        app = command_opts[0]
        if (len(command_opts) > 1 and app in shortcuts):
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
                addShortcut(k,actions[k])
    else:
        for k in actions:
            addShortcut(k,actions[k])

def addShortcut(action, shortcut):
    if (action.strip() and shortcut.strip()):
        wf.add_item(
            action,
            shortcut,
            largetext=action,
            copytext=shortcut
        )

# return the shortcut for an action for an app
def getShortcut(app, key):
    return shortcuts[app][key]

if __name__ == '__main__':
    wf = Workflow(
        libraries=['./lib'],
        update_settings=update_settings)
    apps = getApps()
    log = wf.logger
    sys.exit(wf.run(main, text_errors='--commit' in wf.args))
