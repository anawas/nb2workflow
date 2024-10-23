import importlib.metadata

name = "nb2workflow"

def version(print_it=True):
    v = importlib.metadata.version("nb2workflow")
    if print_it:
        print(v)
    
    return v