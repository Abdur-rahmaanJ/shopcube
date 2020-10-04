import os
import importlib

def autoload_models():
    print('Auto importing models')
    for module in os.listdir("modules"):
        if module.startswith("__"):
            continue
        try:
            to_load = "modules.{}.models".format(module)
            importlib.import_module(to_load)
            print('[x]', 'imported', to_load)
        except Exception as e:
            print('[ ]', e)
