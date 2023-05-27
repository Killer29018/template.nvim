import os
import shutil
import re

import pynvim

folderName = ".templates"
filePath = os.path.abspath(os.getenv("HOME") + "/" + folderName)
# cwd = os.getcwd()

templates = []

def nvim_clear(nvim):
    nvim.command("redraw | echo")

def nvim_write(nvim, msg):
    nvim.command("redraw | echo")
    nvim.out_write(msg)

def nvim_input(nvim, msg):
    return nvim.eval(f'input("{msg}")')

ignore = shutil.ignore_patterns(".git*")

@pynvim.plugin
class Template(object):

    def __init__(self, nvim):
        self.templates = []
        self.nvim = nvim

    def _load_templates(self):
        self.templates = []

        if not os.path.exists(filePath):
            os.mkdir(filePath)

        with os.scandir(filePath) as it:
            for file in it:
                if file.is_dir():
                    self.templates.append(file)

    def _get_template(self, name):
        for template in self.templates:
            if template.name == name:
                return template, True

        return None, False

    @pynvim.function("TemplateList", sync=True)
    def list_templates(self, args):
        self._load_templates()

        output = ["".join(x.name) for x in self.templates]

        return output

    @pynvim.function("TemplateUse", sync=True)
    def use_template(self, args):
        # args[0] : name

        cwd = self.nvim.command_output("pwd")
        confirm = nvim_input(self.nvim, "Are you sure y/N: ")
        if confirm.lower() != 'y':
            nvim_write(self.nvim, "Cancelled")
            return

        name = args[0]
        template, found = _get_template(name)

        if not found:
            nvim_write(self.nvim, f"Unable to use the template {template.name}")
            return

        nvim_write(self.nvim, f"Used the template {template.name}\n")
        shutil.copytree(template.path, cwd, dirs_exist_ok=True)

    @pynvim.command("TemplateCreate", sync=True)
    def create_template(self):
        name = nvim_input(self.nvim, "Please enter the name of the template: ")

        cwd = self.nvim.command_output("pwd")

        output = filePath + "/" + name
        if os.path.isdir(output):
            self.nvim.command("redraw | echo")
            overwrite = nvim_input(self.nvim, f"Template {name} already exists. Do you want to overwrite (y/N): ")

            if overwrite.lower() != "y":
                nvim_write(self.nvim, "Cancelled\n")
                return

        shutil.copytree(cwd, filePath + "/" + name, dirs_exist_ok=True, ignore=ignore)
        nvim_write(self.nvim, f"Created template {name}\n")

    @pynvim.function("TemplateRemove", sync=True)
    def remove_template(self, args):
        # args[0] : name
        remove = nvim_input(self.nvim, 'Are you sure (y/N): ')

        if (remove.lower() != "y"):
            self.nvim.out_write('Cancelled\n')
            return False

        name = args[0]
        template, found = _get_template(name)
        if not found:
            return False

        shutil.rmtree(filePath + "/" + name)
        nvim_write(self.nvim, f"Removed the template {template}\n")
        return True

    @pynvim.function("TemplateFiles", sync=True)
    def template_files(self, args):
        # args[0] : name

        args[0]
        template, found = self._get_template(args[0])
        if not found:
            return []

        output = []

        files = []

        if template is None or template.path is None:
            return []

        with os.scandir(template.path) as it:
            for file in it:
                files.append(file)

        directories = [x for x in files if x.is_dir()]
        files = [x for x in files if not x.is_dir()]

        directories.sort(key=lambda x: x.name)
        files.sort(key=lambda x: x.name)

        for x in directories:
            output.append(f" {x.name}")

        for x in files:
            extension = ""

            temp = re.findall("\.[A-Za-z]+", x.name)

            if temp.length > 0:
                extension = temp[0][:1]

            icon = self.nvim.command_output(f"lua print(require'nvim-web-devicons'.get_icon('{x.name}', '{extension}'))")[0]

            output.append(f"{icon} {x.name}")

        return output

