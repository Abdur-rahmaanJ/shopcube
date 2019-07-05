from jinja2 import Environment, FileSystemLoader
import json
import os
import random
from pathlib import Path


jload = json.load
path_join = os.path.join

def generate(template_dir, file_in_templates, outpath, **kwargs):
    # template_dir = 'templates/'
    file_loader = FileSystemLoader(template_dir)
    env = Environment(loader=file_loader)
    template = env.get_template(file_in_templates)

    output = template.render(kwargs)
    print(output, file=open(outpath, 'w+', encoding="utf8"))


def get_folders(path):
    return [name for name in os.listdir(path)]


# generate templates

class ModulesLoader:
    def __init__(self, path_now):
        self.path_now = path_now
        self.imports = []
        self.blueprint_regs = []

        self.modules = get_folders(path_join(os.path.sep, path_now, 'modules'))
        self.utils_templates_path = path_join(os.path.sep, path_now, 'utils', 'templates')

    def import_string(self, module_name):
        return 'from views.{0} import {0}_blueprint'.format(module_name)

    def blueprints_reg_string(self, module_name):
        return 'app.register_blueprint({}_blueprint)'.format(module_name)

    def gen_module_info(self, module):
        module_path = path_join(os.path.sep, self.path_now, 'modules', module)
        templates_path = path_join(os.path.sep, self.path_now, 'modules', module, 'templates')
        templates = os.listdir(templates_path)
        info_path = path_join(os.path.sep, module_path, 'info.json')

        self.imports.append(self.import_string(module))
        self.blueprint_regs.append(self.blueprints_reg_string(module))

        # templates
        print('generating templates for module', module)
        for template in templates:
            module_info = jload(open(info_path, encoding='utf8'))
            generate(templates_path, template, 'application/templates/{}_{}'.format(
                module_info['name'], template))
        print('completed!')

        # view file
        print('generating view file for module', module)
        generate(module_path, 'view.py', 'application/views/{}.py'.format(
                module_info['name']))
        print('completed!')

    def gen_appdotpy(self):
        print('generating app.py')
        generate(self.utils_templates_path, 'app.py', 'application/app.py', 
                IMPORTS='\n'.join(self.imports), REGISTER_BLUEPRINTS='\n'.join(self.blueprint_regs))
        print('completed!')

    def gen_module(self, mode):
        if mode == 'all':
            for module in self.modules:
                self.gen_module_info(module)
            self.gen_appdotpy()
        else:
            self.gen_module_info(mode)

        print('Modules Loading Completed Successfully!')

def generate_modules(path_now, mode):
    loader = ModulesLoader(path_now)
    loader.gen_module(mode)