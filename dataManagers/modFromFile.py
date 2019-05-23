import runpy
import imp

def loadPath(mod_name, path):
    """Runs the Python code at path, returns a new module with the resulting globals"""
    attrs = runpy.run_path(path, run_name=mod_name)
    mod = imp.new_module(mod_name)
    mod.__dict__.update(attrs)
    return mod