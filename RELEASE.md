Steps to release workflow:
----------------
1. pull latest changes from master
2. `cd src` and `python shortcuts.py` to update pkl file
3. import plugin into alfred (you can copy and paste the `src/` folder into Alfred.alfredpreferences/workflows)
4. test workflow with added features
5. right click on workflow in alfred preferences and hit export
6. replace the `Cheatsheet.alfredworkflow` file in the repo (keeps download url in readme updated)
7. update `src/version` file with upcoming version
7. push changes
8. go to releases tab in github repo
9. hit `Draft a new release`
10. insert `Cheatsheet.alfredworkflow` to selected binaries
11. update tag to be more than current release