# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
from textwrap import dedent

from spack_repo.builtin.build_systems.compiler import CompilerPackage

from spack.package import *


class Emscripten(Package, CompilerPackage):
    """An LLVM-to-WebAssembly Compiler."""

    homepage = "https://emscripten.org"
    git = "https://github.com/emscripten-core/emscripten.git"
    url = "https://github.com/emscripten-core/emscripten/archive/refs/tags/4.0.12.tar.gz"
    maintainers("cosmicexplorer")

    license("MIT AND NCSA", checked_by="cosmicexplorer")

    provides("c", "cxx")

    compiler_prefixes = []
    compiler_version_argument = "-dumpversion"
    compiler_version_regex = re.compile("([0-9]+\.[0-9]+\.[0-9]+(?:\-git)?)$",
                                        flags=re.MULTILINE)
    compiler_languages = ["c", "cxx"]
    c_names = ["emcc"]
    cxx_names = ["em++"]
    compiler_wrapper_link_paths = {
        "c": os.path.join("emscripten", "emcc"),
        "cxx": os.path.join("emscripten", "em++"),
    }
    opt_flags = ["-O0", "-O1", "-O2", "-O3", "-Os", "-Oz", "-Og", "-Ofast"]
    debug_flags = ["-g", "-g0", "-g1", "-g2", "-g3", "-gz"]

    @classmethod
    def compiler_bindir(cls, prefix):
        """Tools like emcc are at the prefix root instead of /bin, and they don't seem to like being
        symlinked into /bin."""
        return prefix

    version("latest", branch="main")
    version("4.0.12", sha256="a177867ccc704e466683e3a72e43be197d6ba741cf775f9302e5cbff304b34de")

    phases = ["build", "install", "test"]

    variant(
        "create-standard-executables",
        default=True,
        description="Apply some patches to executable-type output files "
        "in order to make them executable by default.",
    )
    variant(
        "closure",
        default=False,
        description="Include java in order to run the Closure compiler.",
    )

    # Need f-strings to run emcc, so 3.7+ (annoying that their docs say 3.6).
    depends_on("python@3.7:")
    # Version 22 is what the google chromium repo apparently tests against. Let's see if 20 works!
    # FIXME: misspelling this as node_js produces an internal solver error with 0 unsat
    #        cores--FIX THIS!
    depends_on("node-js@20:")
    # There is no build step, but instead a single install step.
    depends_on("npm", type="build")
    # The instructions say "close to top-of-tree" (unhelpful), so let's try at least 20.
    # LLVM externals can't detect targets=webassembly, and it's unlikely that distros will provide
    # this in any case, so we will probably have to build it ourselves.
    depends_on("llvm@20:+lld+clang targets=webassembly")

    # Only necessary for tests, but not that onerous of a dep to require in all cases.
    depends_on("git", type="build")

    # Unclear how often this will be used.
    depends_on("java", when="+closure")

    # It used to be the case that each emscripten release was only compatible with a single binaryen
    # version, but their current build instructions make no mention of this.
    depends_on("binaryen")

    # with when("+create-standard-executables"):
    #     # Ensure the output has a hashbang and is marked executable with chmod.
    #     patch("executable-result.patch")
    #     # Ensure the output has access to node raw fs APIs.
    #     patch("force-fs.patch")
    #     # Ensure that executables have sufficient initial memory, and can grow the
    #     # memory at runtime.
    #     patch("initial-memory.patch")

    # executables = ["^{}$".format(re.escape(exe)) for exe in [
    #     "emscons",
    #     "embuilder",
    #     "emprofile",
    #     "emconfigure",
    #     "em++",
    #     "emcc",
    #     "emnm",
    #     "emrun",
    #     "em-config",
    #     "emcmake",
    #     "emdump",
    #     "emranlib",
    #     "emar",
    #     "emsize",
    #     "emdwp",
    #     "emmake",
    # ]]

    @run_before("build")
    def add_submodules(self):
        if self.run_tests:
            git = which("git")
            git("submodule", "update", "--init")

    def build(self, spec, prefix):
        bootstrap = Executable("./bootstrap")
        bootstrap("-v")

    @run_before("install")
    def create_config_dotfile(self):
        config_string = dedent(
            """\
            NODE_JS = '{node_js}'
            LLVM_ROOT = '{llvm}'
            BINARYEN_ROOT = '{binaryen}'
            EMSCRIPTEN_ROOT = '{emscripten}'
            COMPILER_ENGINE = NODE_JS
            JS_ENGINES = [NODE_JS]
            """.format(
                node_js=str(which("node")),
                llvm=str(self.spec["llvm"].prefix),
                # Not sure why it was like this previously, but this seems wildly wrong because this
                # should just point to the binaryen installation.
                # llvm=os.path.dirname(str(which("wasm-ld"))),
                binaryen=str(self.spec["binaryen"].prefix),
                emscripten=str(prefix),
            )
        )
        if self.spec.satisfies("^java"):
            config_string += dedent(
                """\
                JAVA = '{java}'
                """.format(java=str(which("java")))
            )

        with open(".emscripten", "w") as f:
            f.write(config_string)

    def install(self, spec, prefix):
        install_tree(".", str(prefix))

    def setup_run_environment(self, env):
        # Tools like emcc are at the prefix root instead of /bin, and they don't seem to
        # like being symlinked into /bin.
        env.prepend_path("PATH", self.prefix)

    _check_description = "shared:INFO: (Emscripten: Running sanity checks)"
    _check_line = re.compile(r"^{}$".format(re.escape(_check_description)), flags=re.MULTILINE)

    def test(self):
        self.run_test(
            "emcc",
            options=["--check"],
            expected=[self._version_pattern, self._check_line],
            installed=True,
            purpose="test: validating emscripten installation",
            skip_missing=False,
        )
