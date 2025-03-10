import pandas as pd

from os import listdir
from os.path import isfile, join, isdir
from pathlib import Path


def _load_gomod_content(gmod_path):
    if Path(gmod_path).exists():
        with open(gmod_path, 'r') as file:
            return file.read()
    return "" 


def snve_as_parquet(base_dir="mod-info", dest_file="gomod.parquet"):
    dikt_list = []
    for owner in listdir(base_dir):
        if isfile(join(base_dir, owner)): continue
        for repo in listdir(join(base_dir, owner)):
            if isfile(join(base_dir, owner, repo)): continue
            for version in listdir(join(base_dir, owner, repo)):
                if isfile(join(base_dir, owner, repo, version)): continue
                gmod_path = join(base_dir, owner, repo, version, "go.mod")   
                if isfile(gmod_path):
                    # parse go.mod
                    content = _load_gomod_content(gmod_path)
                    dikt_list.append({
                        "repo": f"{owner}/{repo}", 
                        "version": version,
                        "sub_path": "",
                        "content": content,
                    })
                else:
                    for subdir in listdir(join(base_dir, owner, repo, version)):
                        if isfile(join(base_dir, owner, repo, version, subdir)): continue
                        gmod_path = join(base_dir, owner, repo, version, subdir, "go.mod")   
                        if isfile(gmod_path):
                            # parse go.mod
                            content = _load_gomod_content(gmod_path)
                            dikt_list.append({
                                "repo": f"{owner}/{repo}", 
                                "version": version,
                                "sub_path": subdir,
                                "content": content,
                            })

    df = pd.DataFrame(dikt_list)
    df.to_parquet(dest_file, compression="snappy", index=False)
