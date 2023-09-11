import pandas as pd
from pygobuildinfo import get_go_mod
from os import listdir
from os.path import isfile, join, isdir
from pathlib import Path
from .gomod import GoMod

__all__ = [
    "parse_deps_from_dir"
    "parse_deps_from_parquet",
]


def persist_deps(module, version, deps, f):
    for pair in deps:
        f.write(f"{module},{pair[0]},{version},{pair[1]},{pair[2]}\n")


def _prepare_csv(deps_file="dependencies.csv"):
    sub = Path(deps_file[0:-len(deps_file)])
    sub.mkdir(parents=True, exist_ok=True)
    if not Path(deps_file).exists():
        with open(deps_file, 'w') as f:
            f.write("full_name,public_name,version,dep_module,dep_version\n")
        

def _parse_record(row, f):
    mod = GoMod(row["content"])
    deps = [(mod.module_path, req.module, req.version) for req in mod.requires if not req.indirect]
    persist_deps(row["repo"], row["version"], deps, f)
    
    
def parse_deps_from_parquet(parquet_file, deps_file="dependencies.csv", trace=False):
    df = pd.read_parquet(parquet_file)
    _prepare_csv(deps_file)
    with open(deps_file, 'a') as f:
        df.apply(lambda row: _parse_record(row, f), axis=1)


def parse_deps_from_dir(base_dir="mod-info", deps_file="dependencies.csv", trace=False):
    # persist mod dependencies
    _prepare_csv(deps_file)
        
    with open(deps_file, 'a') as f:
        for owner in listdir(base_dir):
            if isfile(join(base_dir, owner)): continue
            for repo in listdir(join(base_dir, owner)):
                if isfile(join(base_dir, owner, repo)): continue
                for version in listdir(join(base_dir, owner, repo)):
                    if isfile(join(base_dir, owner, repo, version)): continue
                    gmod_path = join(base_dir, owner, repo, version, "go.mod")   
                    if isfile(gmod_path):
                        # parse go.mod
                        deps = _parse_deps(gmod_path, trace)
                        persist_deps(f"{owner}/{repo}", version, deps, f)
                    else:
                        for subdir in listdir(join(base_dir, owner, repo, version)):
                            if isfile(join(base_dir, owner, repo, version, subdir)): continue
                            gmod_path = join(base_dir, owner, repo, version, subdir, "go.mod")   
                            if isfile(gmod_path):
                                # parse go.mod
                                deps = _parse_deps(gmod_path, trace)
                                persist_deps(f"{owner}/{repo}/{subdir}", version, deps, f)


# Returns: list of depedencies (module, version)
def _parse_deps(gmod_path, trace=False):
    if Path(gmod_path).exists():
        if trace: print(f"Process {gmod_path}")
        dikt = get_go_mod(gmod_path)
        if 'Deps' in dikt:
            return [(dikt.get('Path', ''), d['Path'], d['Version']) for d in dikt['Deps'] if not d['Indirect']]
    return []


