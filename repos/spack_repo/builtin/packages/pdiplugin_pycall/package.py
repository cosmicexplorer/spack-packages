# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *

from ..pdi.package import Pdi


class PdipluginPycall(CMakePackage):
    """pycall plugin for the PDI library"""

    homepage = "https://pdi.dev"
    git = "https://github.com/pdidev/pdi.git"
    url = "https://github.com/pdidev/pdi/archive/refs/tags/1.8.0.tar.gz"

    license("BSD-3-Clause")

    maintainers("jbigot")


    # only the latest version is supported upstream
    # we also offer the last 2 patch versions of the current minor
    # and the last patch version of the previous 2 minors
    # all the rest is marked as deprecated
    version("develop", branch="main", no_cache=True)
    version("1.10.1", sha256="f2409611310255360867e3c74d44e055f45c87071ef8881665ff30a7940e1449")
    version("1.10.0", sha256="8bda1ed83bdb152a047a45a48f896466e7ebf5163030405c15dbfa4e2e788143")
    version("1.9.3", sha256="ab390e51e3b7298d6b09484a443dc267651aed5978c711f8804848b19ab1527e")
    version(
        "1.9.2",
        sha256="0430d5898980435e5602b67188264621a27f71969ff886efaa2e6d43a45caac4",
        deprecated=True,
    )
    version(
        "1.9.1-fixed",
        sha256="13d052a7d5d53271638382f06e9da0d58b01ed9cfdf9c4fa1e82367b9e1732e1",
        deprecated=True,
    )
    version(
        "1.9.0",
        sha256="04fee7851c4f2a156daddf7eb2c3c3b0132d80d3f0e448cdeebda0b7c4595639",
        deprecated=True,
    )
    version("1.8.3", sha256="df7200289a2a368ec874140039b417abdfe681b57fb1b9f4c52f924952226020")
    version(
        "1.8.2",
        sha256="bb4d1654c97f7ff379067adbff339f8b4117c0cf9432f41f1a5cb20a747cac1a",
        deprecated=True,
    )
    version(
        "1.8.1",
        sha256="43f0c0b2bda5515ecf99da7be1600af2c1f669d6c73e3f309275b14940c7e35c",
        deprecated=True,
    )
    version(
        "1.8.0",
        sha256="5d353bfa64f45ee4715b88bd30330030f79f2020cd6bede0ad9b8f9beddadea9",
        deprecated=True,
    )

    variant("tests", default=False, description="Build tests")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cmake@3.22.1:", type=("build"), when="@1.10.0:")
    depends_on("cmake@3.16.3:", type=("build"))


    depends_on("pdi+python@1.10.1", type=("link", "run"), when="@1.10.1")
    depends_on("pdi+python@1.10.0", type=("link", "run"), when="@1.10.0")
    depends_on("pdi+python@1.9.3", type=("link", "run"), when="@1.9.3")
    depends_on("pdi+python@1.9.2", type=("link", "run"), when="@1.9.2")
    depends_on("pdi+python@1.9.1-fixed", type=("link", "run"), when="@1.9.1-fixed")
    depends_on("pdi+python@1.9.0", type=("link", "run"), when="@1.9.0")
    depends_on("pdi+python@1.8.3", type=("link", "run"), when="@1.8.3")
    depends_on("pdi+python@1.8.2", type=("link", "run"), when="@1.8.2")
    depends_on("pdi+python@1.8.1", type=("link", "run"), when="@1.8.1")
    depends_on("pdi+python@1.8.0", type=("link", "run"), when="@1.8.0")


    depends_on("py-setuptools", type=("build"), when="@1.8.3: ^python@3.12:")
    depends_on("pkgconfig", type=("build"))

    root_cmakelists_dir = "plugins/pycall"

    def url_for_version(self, version):
        return Pdi.version_url(version)

    def cmake_args(self):
        return [
            "-DINSTALL_PDIPLUGINDIR:PATH={:s}".format(self.prefix.lib),
            self.define_from_variant("BUILD_TESTING", "tests"),
        ]

    def setup_run_environment(self, env: EnvironmentModifications) -> None:
        env.prepend_path("PDI_PLUGIN_PATH", self.prefix.lib)
