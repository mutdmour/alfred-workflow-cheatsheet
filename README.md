Cheatsheet
----------

Alfred workflow that gets shortcuts for applications, websites, tools and others

If you have any questions or issues, checkout the discussion at [the alfred forum here](https://www.alfredforum.com/topic/10830-cheatsheet-shortcuts-for-your-tools/).
Or create an issue if you cannot find an answer.

Supported
---------
- Alfred
- AutoMute Chrome extension
- Evernote
- Finder
- Firefox
- Github.com
- Google Chrome
- inbox.google.com
- IntelliJ Idea (default Mac OS X)
- iTerm2
- Mac OSX
- Microsoft Word
- Outlook
- Reddit Enhancement Suite
- Safari
- Slack
- Sublime Text
- Terminal
- Trello.com
- Things
- Video Speed Controller chrome extension
- Vim
- Vintage Sublime
- Youtube.com

Ready for next release
----------------------
- Google Sheets

Requested To add
----------------
- Airmail
- Asana
- Atom
- Default Folder X
- Forklift
- Google Docs
- Illustrator
- Keyboard Maestro
- Microsoft Excel
- Opera
- Photoshop
- Pixelmator
- Sibelius
- Sketch
- Stickies
- TextExpander
- Things
- Transcribe!
- VLC
- VS Code
- Vimeo
- Xcode

To download
-----------
Download [workflow file](https://github.com/mutdmour/alfred-workflow-cheatsheet/raw/master/Cheatsheet.alfredworkflow)

To do
------
- more and better testing
- merge Sublime and Sublime vintage
- standarize shortcuts with symbols

To add more apps
----------------
- add it yourself to [custom.json] in your data directory. Open up the cheatsheet and enter the first option to open the directory.
- to overwrite any default, ^⏎ on any shortcut in the app.
- to share with everyone, create a PR with the app shortcuts you want to add [/src/shortcuts.py]. Please also include the app icon (`src/apps/icons/%APP NAME%.png`).
- create an issue requesting the tool you want us to add

To show or hide apps in search results
----------------
Open `settings.json` in your data directory.
To show only some specific apps in the search results list them in `show_only_apps` parameter:
```json
{
  "__workflow_last_version": "1.3.0",
  "show_only_apps": [
    "Alfred",
    "Mac OSX",
    "Terminal"
  ]
}
```
All other apps would be hidden then.


To hide some apps in the search results list them in `hide_apps` parameter:
```json
{
  "__workflow_last_version": "1.3.0",
  "hide_apps": [
    "Microsoft Word",
    "Video Speed Controller chrome extension"
  ]
}
```





Steps to release workflow:
----------------
1. pull latest changes from master
2. `cd src` and `python shortcuts.py` to update pkl file
3. import plugin into alfred (you can copy and paste the `src/` folder into Alfred.alfredpreferences/workflows)
4. test workflow with added profiles
5. right click on workflow in alfred preferences and hit export
6. replace the `Cheatsheet.alfredworkflow` file in the repo
7. push changes
8. go to releases tab in github repo
9. hit `Draft a new release`
10. insert `Cheatsheet.alfredworkflow` to selected binaries
11. update tag to be more than current release
