#!/usr/bin/python
# encoding=utf8

update_settings = {
    'github_slug': 'mutdmour/alfred-workflow-cheatsheet',
}

import sys
import os
from workflow import Workflow, ICON_INFO, ICON_WARNING
import cPickle

wf = None
log = None
apps = None
custom = None

nothing_found_error_text = 'Nothing found'

app_icons_dir = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'apps/icons'
)

pkl_file = open('default_cheatsheet.pkl', 'rb')
shortcuts = cPickle.load(pkl_file)

def main(wf):
    log.info(wf.datadir)
    args = wf.args
    run(args)
    wf.send_feedback()
    log.info('Workflow response complete')

def checkUpdate():
    if wf.update_available:
    # Add a notification to top of Script Filter results
        wf.add_item('New version available',
                'Action this item to install the update',
                autocomplete='workflow:update',
                icon=ICON_INFO)

def addEditCustomInfo():
    wf.add_item('Customize your cheatsheet',
            'Edit custom.json to personalize cheatsheet. Edit settings.json to hide apps in search results.',
            arg='opendata',
            valid=True,
            icon=ICON_INFO)

def run(args):
    command = args[0].strip()
    log.info("args")
    log.info(args)
    log.info("")

    checkUpdate()

    if (not command and not u'--search' in args):
        # if no args list all apps
        addEditCustomInfo()
        addApps(apps)
    elif(command == "opendata"):
        wf.open_datadir()
    elif (u'--ctrl' in args):
        app = wf.cached_data("to_search_app")
        if (app in shortcuts or app in custom):
            action = args[0]
            log.info("caching "+app+":"+action)
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
        wf.cache_data("to_search_app",command)
    elif (u'--search' in args):
        app = wf.cached_data("to_search_app")
        if (not app == None):
            log.info("searching for: "+app)
            if (app in shortcuts or app in custom):
                # action = command_opts[1].strip()
                action = command
                log.info("go it "+action)
                if (action == u''):
                    wf.add_item('Customize any shortcut',
                        u'Ctrl ⏎',
                        icon=ICON_INFO)
                    action = ""
                if addShortcuts(app, action) == 0:
                    wf.add_item(nothing_found_error_text, icon=ICON_WARNING)
    elif (u'--search-global' in args):
        shortcuts_added = 0
        for app in apps:
            shortcuts_added += addShortcuts(app, command, True)

        for app in custom:
            shortcuts_added += addShortcuts(app, command, True)

        if shortcuts_added == 0:
            wf.add_item(nothing_found_error_text, icon=ICON_WARNING)
    else:
        filter(command, apps)


def filter(query, items):
    matching = wf.filter(
        query,
        items
    )
    if (len(matching) == 0):
        wf.add_item(nothing_found_error_text, icon=ICON_WARNING)
    else:
        addApps(matching)

# returns a list of the apps available as shortcuts
def getApps():
    built_in_apps = shortcuts.keys()
    custom_apps = custom.keys()
    apps = list(set(built_in_apps) | set(custom_apps))

    if 'show_only_apps' in wf.settings:
        apps = [app for app in apps if app in wf.settings['show_only_apps']]
    elif 'hide_apps' in wf.settings:
        apps = [app for app in apps if app not in wf.settings['hide_apps']]

    return apps

def getAppIconPath(app):
    icon_path = os.path.join(app_icons_dir, app + '.png')
    if not os.path.isfile(icon_path):
        icon_path = ''

    return icon_path

def addApps(items):
    for i in range(0,len(items)):
        item = items[i]
        wf.add_item(item,
                    icon=getAppIconPath(item),
                    uid=item,
                    autocomplete=' '+item,
                    arg=item,
                    valid=True)

def addShortcuts(app, search, include_app_in_search=False):
    actions = {}
    if (app in shortcuts):
        actions = shortcuts[app]
    if (app in custom):
        actions.update(custom[app])

    if include_app_in_search:
        actions_pairs = [(action, shortcut, app + ' ' + action) for action, shortcut in actions.items()]
    else:
        actions_pairs = [(action, shortcut, action) for action, shortcut in actions.items()]

    if search:
        actions_pairs_to_show = wf.filter(search, actions_pairs, key=lambda a: a[2])
    else:
        actions_pairs_to_show = actions_pairs

    icon_path = getAppIconPath(app)
    for action, shortcut, _ in actions_pairs_to_show:
        addShortcut(action, shortcut, app, icon_path)

    return len(actions_pairs_to_show)


def addShortcut(action, shortcut, app, icon_path):
    if (action.strip() and shortcut.strip()):
        wf.add_item(
            action,
            shortcut,
            icon=icon_path,
            largetext=action,
            copytext=shortcut,
            modifier_subtitles={
                u'ctrl': u'Customize this shortcut'
            },
            arg=action
        )

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
                "action":"shortcut"
            }
        }
        wf.store_data('custom',custom)
    apps = getApps()
    sys.exit(wf.run(main, text_errors='--commit' in wf.args))
