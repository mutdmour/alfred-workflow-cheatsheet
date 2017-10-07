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
user_shortcuts = None

def main(wf):
    # log.info(wf.datadir)
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
        wf.add_item('Add your own config',
                'Edit json file to personalize cheatsheet',
                autocomplete='config',
                icon=ICON_INFO)
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
    user_apps = user_shortcuts.keys()
    return list(set(apps) | set(user_apps))

def addApps(items):
    for i in range(0,len(items)):
        item = items[i]
        wf.add_item(item,
                    autocomplete=' '+item,
                    arg=item+": ",
                    valid=True)

def addShortcuts(app, search):
    actions = shortcuts[app]

    # if (user_shortcuts[app]):
        # actions.update(user_shortcuts[app])

    if (search):
        opts = user_shortcuts[app].keys()
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
            copytext=shortcut,
            # modifier_subtitles={
            #     u'ctrl': u'Change the shortcut'
            # },
            # valid=True
        )

# return the shortcut for an action for an app
def getShortcut(app, key):
    return shortcuts[app][key]

if __name__ == '__main__':
    wf = Workflow(
        libraries=['./lib'],
        update_settings=update_settings)
    wf.data_serializer = 'json'
    log = wf.logger

    user_shortcuts = wf.stored_data('user_shortcuts')
    if (user_shortcuts == None):
        user_shortcuts = {}
        wf.store_data('user_shortcuts',user_shortcuts)

    apps = getApps()

    sys.exit(wf.run(main, text_errors='--commit' in wf.args))
