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
custom = None

pkl_file = open('default_cheatsheet.pkl', 'rb')
shortcuts = cPickle.load(pkl_file)

def main(wf):
    log.info(wf.datadir)
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
        wf.add_item('Customize your cheatsheet',
                'Edit custom.json file to personalize cheatsheet',
                arg='workflow:opendata',
                autocomplete='custom',
                icon=ICON_INFO)
        addApps(apps)
    elif (command == 'custom'):
        wf.open_datadir()
    elif (u'--ctrl' in args):
        command_opts = command.split(':',1)
        app = command_opts[0]
        if (len(command_opts) > 1 and (app in shortcuts or app in custom)):
            action = command_opts[1].strip()
            log.info("caching "+command)
            wf.cache_data("to_update_app",app)
            wf.cache_data("to_update_action",action)
    elif (u'--update' in args):
        app = wf.cached_data("to_update_app")
        action = wf.cached_data("to_update_action")

        if (not app in custom):
            custom[app]={}

        custom[app][action] = command
        wf.store_data("custom",custom)

    elif (u'--commit' in args):
        command_opts = command.split(':',1)
        app = command_opts[0]
        if (len(command_opts) > 1 and (app in shortcuts or app in custom)):
            action = command_opts[1].strip()
            if (action == ""):
                wf.add_item('Customize any shortcut',
                    u'Ctrl ⏎',
                    icon=ICON_INFO)
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
    custom_apps = custom.keys()
    return list(set(apps)|set(custom_apps))

def addApps(items):
    for i in range(0,len(items)):
        item = items[i]
        wf.add_item(item,
                    autocomplete=' '+item,
                    arg=item+": ",
                    valid=True)

def addShortcuts(app, search):
    actions = {}
    if (app in shortcuts):
        actions = shortcuts[app]
    if (app in custom):
        actions.update(custom[app])

    if (search):
        opts = shortcuts[app].keys()
        matching = wf.filter(search, opts)
        if (len(matching) == 0):
            wf.add_item('none found')
        else:
            for k in matching:
                addShortcut(k,actions[k], app)
    else:
        for k in actions:
            addShortcut(k,actions[k], app)

def addShortcut(action, shortcut, app):
    if (action.strip() and shortcut.strip()):
        wf.add_item(
            action,
            shortcut,
            largetext=action,
            copytext=shortcut,
            modifier_subtitles={
                u'ctrl': u'Customize this shortcut'
            },
            arg=app+":"+action
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
    custom = wf.stored_data('custom')
    if (custom == None):
        custom = {
            "custom_app_example":{
                "action":"shortcut [app name and action must be exactly same as default to overwrite any default]"
            }
        }
        wf.store_data('custom',custom)
    apps = getApps()
    sys.exit(wf.run(main, text_errors='--commit' in wf.args))
