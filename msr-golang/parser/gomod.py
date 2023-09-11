#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


class ModuleReference:
    def __init__(self, module, version):
        self._module = module
        self._version = version

    @property
    def module(self):
        return self._module

    @property
    def version(self):
        return self._version

    def __repr__(self):
        return f"mod: {self.module}, version: {self.version}"

    def __str__(self):
        return f"{self.module} {self.version}"


class Require(ModuleReference):

    def __init__(self, module, version, indirect):
        super().__init__(module, version)
        self._indirect = indirect

    @property
    def indirect(self):
        return self._indirect

    def __repr__(self):
        return f"{super().__repr__()}, indirect: {self.indirect}"

    def __str__(self):
        return f"{super().__str__()}{' //indirect' if self.indirect else ''}"


class Replace:
    def __init__(self, left, right):
        self._left = left
        self._right = right

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    def __repr__(self):
        return f"{self.left.__repr__()} => {self.right.__repr__()}"

    def __str__(self):
        return f"{self.left.__str__()} => {self.right.__str__()}"


class Retract:
    def __init__(self, versions):
        self._versions = versions

    @property
    def versions(self):
        return self._versions

    def __repr__(self):
        return f"{[v for v in versions]}"

    def __str__(self):
        return f"{[v for v in versions]}"


class GoMod:
    ModulePathDirectivePat = re.compile("module\s+(.*)")
    GoVersionDirectivePat  = re.compile("go\s+(.*)")
    ToolchainDirectivePat  = re.compile("tailchain\s+(.*)")
    RequireDirectivePat1   = re.compile("^\s*require\s+(.*?)\s+(v.+)$", re.MULTILINE)
    RequireDirectivePat2   = re.compile("require\s+\(\s*\n\s*(?:.*\s+v.+\n)+\)")
    RequireDirectivePat21  = re.compile("^\s*(\w+(?:.*?))\s+(v.+)$", re.MULTILINE)
    #ReplaceDirectivePat1   = re.compile("replace\s+(.*?)\s+(v.+)?\s*=>\s*(.*)\s+(v.+)?")
    ReplaceDirectivePat1   = re.compile("replace\s+(\w+(?:.*?))\s+(v.+)?\s*=>\s*((?:\.|/|-|\w)+)\s*(v.+)?")
    ReplaceDirectivePat2   = re.compile("replace\s+\(\s*\n\s*(?:.*\n)+\)")
    # ReplaceDirectivePat21  = re.compile("^\s*(\w+(?:.*?))\s+(v.+)?\s*=>\s*(\w+(?:.*?))\s*(v.+)?", re.MULTILINE)
    ReplaceDirectivePat21  = re.compile("^\s*(\w+(?:.*?))\s+(v.+)?\s*=>\s*((?:\.|/|-|\w)+)\s*(v.+)?$", re.MULTILINE)
    RetractDirectivePat1   = re.compile("retract\s+(v.+)")
    RetractDirectivePat2   = re.compile("retract\s+(v.+(?:v.+,)*)")

    def __init__(self, content):
        self._module_path = ""
        self._go_version  = ""
        self._toolchain   = ""
        self._excludes    = []
        self._retract     = []

        self._parse(content)

    def _parse(self, content):
        # strip pure comment lines

        lines = content.split("\n")
        content = "\n".join([line for line in lines if not re.match(r"^\s*//.*", line)])

        m = re.search(GoMod.ModulePathDirectivePat, content)
        if m: self._module_path = m.group(1)

        m = re.search(GoMod.GoVersionDirectivePat, content)
        if m: self._go_version = m.group(1)

        m = re.search(GoMod.ToolchainDirectivePat, content)
        if m: self._toolchain = m.group(1)

        requires = []
        # parse module dependency
        for m in re.finditer(GoMod.RequireDirectivePat1, content):
            requires.append(self._parse_require(m.group(1), m.group(2)))

        for m1 in re.finditer(GoMod.RequireDirectivePat2, content):
            for m2 in re.finditer(GoMod.RequireDirectivePat21, m1.group(0)):
                requires.append(self._parse_require(m2.group(1), m2.group(2)))
        self._requires = requires

        # parse replace
        replaces = []
        # parse module dependency
        for m in re.finditer(GoMod.ReplaceDirectivePat1, content):
            replaces.append(self._parse_replace(*m.groups()))

        for m1 in re.finditer(GoMod.ReplaceDirectivePat2, content):
            for m2 in re.finditer(GoMod.ReplaceDirectivePat21, m1.group(0)):
                replaces.append(self._parse_replace(*m2.groups()))
        self._replaces = replaces

        #TODO: parse exclude
        #TODO: parse retract

    def _parse_require(self, module, version_str):
        indirect = False
        version = ""
        if version_str.find("//") > 0:
            ver, comment = version_str.split('//', 1)
            indirect = comment.find("indirect") > 0
            version = ver.lstrip().rstrip()
        else:
            version = version_str.lstrip().rstrip()

        return Require(module, version, indirect)

    def _parse_replace(self, left_mod, left_ver, right_mod, right_ver):
        if left_ver is None: left_ver = ''
        if right_ver is None: right_ver = ''

        return Replace(
            ModuleReference(left_mod, left_ver),
            ModuleReference(right_mod, right_ver),
        )

    @property
    def module_path(self):
        return self._module_path 

    @property
    def go_version(self):
        return self._go_version  

    @property
    def toolchain(self):
        return self._toolchain   

    @property
    def requires(self):
        return self._requires    

    @property
    def excludes(self):
        return self._excludes    

    @property
    def replaces(self):
        return self._replaces    

    @property
    def retract(self):
        return self._retract    

    @property
    def requires(self):
        return self._requires    

    def __repr__(self):
        requires = "\n".join([req.__repr__() for req in self.requires])
        return f"module-path: {self.module_path} go-version: {self.go_version} toolchain: {self.toolchain} \n{requires}\n {self.excludes}\n{self.replaces}\n{self.retract}"

    def __str__(self):
        requires = "\n".join([req.__str__() for req in self.requires])
        replaces = "\n".join([req.__str__() for req in self.replaces])
        return f"{self.module_path} {self.go_version}\n{requires}\n{self.excludes}\n{replaces}\n{self.retract}"

if __name__ == "__main__":
    pass
    s = """
replace (
    // k8s.io/api => k8s.io/api v0.28.0
    k8s.io/api => k8s.io/api v0.28.1
    k8s.io/apimachinery => k8s.io/apimachinery v0.28.1
    k8s.io/client-go => k8s.io/client-go v0.28.1
    k8s.io/component-base => k8s.io/component-base v0.28.1
    golang.org/x/net v1.2.3 => ./fork/net
    golang.org/x/net => ./fork/net
)
"""

    for m in re.finditer(GoMod.ReplaceDirectivePat21, s):
        print(m.groups())
