#!/usr/bin/env python3
"""
Python script to display list of installed application in GUI using zenity.
Select and launch app from the list or view its description and exec command.
Built for Ubuntu with Gnome.

"""
import subprocess
import os

dir1 = "/usr/share/applications"
dir2 = "/home/guru/.gnome/apps"

class Apps:
    def __init__(self) -> None:
        self.apps = []
        self.dir = [dir1, dir2]

    def append_app(self, dr, f):
        try:
            content = open(dr+"/"+f).read()
            if not "NoDisplay=true" in content:
                lines = content.splitlines()
                name = [l for l in lines if l.startswith("Name=")][0].replace("Name=", "")
                command = [l for l in lines if l.startswith("Exec=")][0].replace("Exec=", "").replace('"','') ##For MS Edge apps, app-url param of Exec command has additional quotes that need to be removed
                comment = [l for l in lines if l.startswith("Comment=")]
                comment = comment[0].replace("Comment=", "") if comment else "No description"
                self.apps.append([name, comment, command])
        except:
            pass

    def get_app_list(self):
        for dr in self.dir:
            for f in [f for f in os.listdir(dr) if f.endswith(".desktop")]:
                self.append_app(dr,f)

        self.apps.sort(key=lambda x: x[0])
        self.apps = [ap for sublist in self.apps for ap in sublist]
        displ_list = '"'+'" "'.join(self.apps)+'"'
        return displ_list
    
    def display_apps(self):
        disp_list = self.get_app_list()
        while True:
            try:
                chosen = subprocess.check_output([
                    "/bin/bash",
                    "-c",
                    'zenity --list '+\
                    '--column="Applications" '+\
                    '--column="Description" '+\
                    '--column="Commands" '+\
            #        '--hide-column=2 '+\
                    '--height 600 '+\
                    '--width 800 '+\
                    '--print-column=3 '+ disp_list
                    ]).decode("utf-8").split("|")[-1].strip()
                chosen = chosen[:chosen.rfind(" ")] if "%" in chosen else chosen
                print(F'The chosen app: {chosen}')
                subprocess.Popen([
                    "/bin/bash", "-c", chosen
                    ])
            except subprocess.CalledProcessError:
                break
            

if __name__ == '__main__':
    apps = Apps()
    apps.display_apps()