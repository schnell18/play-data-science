from pygobuildinfo import get_go_mod
from os import listdir
from os.path import isfile, join, isdir
from pathlib import Path

__all__ = [
    "parse_deps"
]


def persist_deps(module, version, deps, f):
    for pair in deps:
        f.write(f"{module},{pair[0]},{version},{pair[1]},{pair[2]}\n")

    
def parse_deps(base_dir="mod-info", deps_file="dependencies.csv", trace=False):
    # persist mod dependencies
    deps_path = join(base_dir, deps_file)
    sub = Path(deps_path[0:-len(deps_file)])
    sub.mkdir(parents=True, exist_ok=True)
    if not Path(deps_path).exists():
        with open(deps_path, 'w') as f:
            f.write("full_name,public_name,version,dep_module,dep_version\n")
        
    with open(deps_path, 'a') as f:
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


