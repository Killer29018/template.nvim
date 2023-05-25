import os
import shutil

import pynvim

folderName = ".templates"
filePath = os.path.abspath(os.getenv("HOME") + "/" + folderName)
cwd = os.getcwd()

templates = []

@pynvim.plugin
class Templat(object):

    def __init__(self, nvim):
        self.templates = []
        self.nvim = nvim
    
    @pynvim.function("LoadTemplates", sync=True)
    def load_templates(self):
        self.templates = []

        if not os.path.exists(filePath):
            os.mkdir(filePath)

        with os.scandir(filePath) as it:
            for file in it:
                if file.is_dir():
                    self.templates.append(file)

    @pynvim.function("CreateTemplate", sync=True)
    def create_template(self):
        name = input("Please enter the name of the template: ")

        shutil.copytree(cwd, filePath + "/" + name, dirs_exist_ok=True)
        print("Created new Template")

    @pynvim.function("UseTemplate", sync=True)
    def use_template(self):
        self.load_templates()
        name = input("Please enter the name of the template: ")

        for template in self.templates:
            if template.name.lower() == name.lower():
                shutil.copytree(template.path, cwd, dirs_exist_ok=True)

    @pynvim.function("RemoveTemplate", sync=True)
    def remove_template(self):
        self.load_templates()

        name = input("Please enter the name of the template you want to remove: ")

        for x in self.templates:
            if x.name == name:
                shutil.rmtree(filePath + "/" + name)
                print("Removed " + name)
                return
        else:
            print("Template could not be found")

    def list_templates(self):
        self.load_templates()
        for template in self.templates:
            print(template.name)
