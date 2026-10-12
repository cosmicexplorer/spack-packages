# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Tpm2Tss(AutotoolsPackage):
    """OSS implementation of the TCG TPM2 Software Stack (TSS2)"""

    homepage = "https://tpm2-software.github.io/"
    url = "https://github.com/tpm2-software/tpm2-tss/archive/3.0.0.tar.gz"
    git = "https://github.com/tpm2-software/tpm2-tss.git"

    license("BSD-2-Clause")

    version("4.1.3", sha256="8a389bda64690910e7af7deaf64703a3faed416dc538c9c3e4f893f24893524d")
    version("4.1.1", sha256="da5b09d5a82d381f7bbd2e1d2db494213f7148659cfaf1b9e423b4df62f48504")
    version("3.0.0", sha256="e88e91aeee2e01ccc45596fb8afcc3b521a660dcebe5a6e1b14ea5e9e5c15cf5")
    version("2.4.2", sha256="1cec5e834a6a750b138cabcd100b3fcd12b16cd21fa4f9103739914743511f75")
    version("2.4.1", sha256="cc6f0691307f3c65d5a1375e2cd22508cc72850dbc70eb820b892f0b3d0cbea2")

    version("develop", branch="master")
    version("4.1.0-git", tag="4.1.0",
            commit="46a1079d5edaaba5268d18e7a7a461f2552c5465")

    depends_on("c", type="build")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool@2.6.0", type="build")
    depends_on("m4", type="build")
    depends_on("autoconf-archive@2019.01.06:", type="build",
               when="@:3")
    depends_on("libtool", type="build")
    depends_on("pkg-config", type="build", when="@:3")
    depends_on("doxygen", type="build", when="@:2.4.2")

    depends_on("openssl@1.1:+docs+shared", type="link")
    depends_on("curl libs=shared", type="link")
    depends_on("acl", type=("build", "link", "run"))
    depends_on("json-c", type="link")

    depends_on("libgcrypt", when="@:2.4.2")

    @when("@:2.4.2")
    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        if self.spec.satisfies("@:2.4.2"):
            env.prepend_path("ACLOCAL_PATH", self.spec["libgcrypt"].prefix.share.aclocal)
        if self.spec.satisfies("@:3"):
            env.prepend_path("ACLOCAL_PATH", self.spec["autoconf-archive"].prefix.share.aclocal)

    @when("@:3")
    def autoreconf(self, spec, prefix):
        sh = which("sh", required=True)
        sh("./bootstrap")
        libtoolize("--verbose", '--install')

    # def edit(self, spec, prefix):
    #     with open('VERSION', mode='w+') as f:
    #         f.write(str(spec.version.dotted) + '\n')
