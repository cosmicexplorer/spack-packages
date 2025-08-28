# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack_repo.builtin.build_systems import compiler
from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Binaryen(CMakePackage):
    """Compiler infrastructure and toolchain library for WebAssembly."""

    homepage = "https://github.com/WebAssembly/binaryen"
    git = "https://github.com/WebAssembly/binaryen.git"
    url = "https://github.com/WebAssembly/binaryen/archive/refs/tags/version_123.tar.gz"
    maintainers("cosmicexplorer")

    license("Apache-2.0", checked_by="cosmicexplorer")

    version("main", branch="main")
    version("123", sha256="a1e1caf250cab3a83938713594e55b6762591208e82087e3337f793e8c8eb7ab")

    variant(
        name="assertions",
        default=False,
        description="Enable assertions.",
    )
    variant(
        name="lto",
        default=True,
        description="Build with LTO.",
        when="%clang",
    )
    variant(
        name="llvm-dwarf",
        default=True,
        description="Build with full DWARF support.",
    )
    variant(
        name="tools",
        values=("emscripten-only", "all", "none"),
        default="all",
        multi=False,
        description="Build tools. 'emscripten-only' refers to the tools emscripten needs.",
    )
    variant(
        name="libs",
        values=("shared", "static"),
        default="shared",
        multi=True,
        description="Libraries to build.",
    )
    variant(
        name="mimalloc",
        default=True,
        description="Build with the mimalloc allocator.",
    )

    conflicts("libs=shared", when="platform=windows",
              msg="Binaryen does not support DLL builds on Windows yet.")

    with when("+mimalloc"):
        depends_on("mimalloc libs=shared", when="libs=shared")
        depends_on("mimalloc libs=static", when="libs=static")

    patch("shared-and-static.patch")

    # Specifically requires a C++17-compatible compiler, but we don't have the ability to
    # specify that. We also have no way to enforce that the user not specify std=cxx14 or some other
    # standard incompatible with the source code (unless we individually do conflicts("std=cxx11")
    # or something).
    depends_on("c", "cxx", type="build")

    executables = ["^{}$".format(re.escape(exe)) for exe in [
        "wasm-opt",
        "wasm-as",
        "wasm-dis",
        "wasm2js",
        "wasm-emscripten-finalize",
        "wasm-ctor-eval",
        "wasm-metadce",
        "binaryen.js",
    ]]

    _version_rx = re.compile(r' version ([0-9]+)$')

    @classmethod
    def determine_version(cls, exe_path):
        try:
            exe = Executable(exe_path)
            output = exe("--version", output=str, error=str)
            m = cls._version_rx.search(output)
            if m is None:
                return None
            (v,) = m.groups()
            return Version(v)
        except spack.util.executable.ProcessError:
            return None

    def cmake_args(self):
        return [
            self.define_from_variant("BYN_ENABLE_ASSERTIONS", "assertions"),
            *(
                [self.define_from_variant("BYN_ENABLE_LTO", "lto")]
                if self.spec.satisfies("%clang")
                else []
            ),
            self.define("BUILD_TESTS", False),
            self.define("BUILD_LIT_TESTS", False),
            self.define("BUILD_TOOLS",
                        self.spec.variants["tools"].value != "none"),
            self.define("BUILD_EMSCRIPTEN_TOOLS_ONLY",
                        self.spec.variants["tools"].value == "emscripten-only"),
            self.define_from_variant("BUILD_LLVM_DWARF", "llvm-dwarf"),
            self.define("BUILD_SHARED_LIB",
                        "shared" in self.spec.variants["libs"].value),
            self.define("BUILD_STATIC_LIB",
                        "static" in self.spec.variants["libs"].value),
            self.define_from_variant("BUILD_MIMALLOC", "mimalloc"),
            self.define("ENABLE_WERROR", False),
        ]

    @property
    def headers(self):
        return find_headers("*", self.prefix.include)

    @property
    def libs(self):
        return find_all_libraries(self.prefix.lib)
