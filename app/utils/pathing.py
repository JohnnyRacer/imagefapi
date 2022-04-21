from pathlib import Path
import shutil 
import os
import itertools


def mkdirchk(rdir:str,mkdir_if_none=True,**kwargs):
    if 'filep' in list(kwargs.keys()): # If filep argument is passed in, 
        return os.path.isfile(os.path.join(rdir, kwargs.items()['filep']))
    path_exists = os.path.isdir(rdir)
    if not path_exists and mkdir_if_none:
        os.makedirs(rdir, exist_ok=True)
    return path_exists

get_matching = lambda in_rdir,matching='',ftype='',use_regex_match=False :  [ str(e) for e in Path(in_rdir).iterdir() if str(e).lower().endswith(ftype) and (str(e).rfind(matching) if use_regex_match else str(e).find(matching) > 0) ] # Returns 

class CachingStore:
    pass