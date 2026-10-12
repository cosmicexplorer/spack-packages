# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from pathlib import Path

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.gnu import GNUMirrorPackage

from spack.package import *
from spack.version import StandardVersion, ConcreteVersion


class Nettle(AutotoolsPackage, GNUMirrorPackage):
    """The Nettle package contains the low-level cryptographic library
    that is designed to fit easily in many contexts."""

    homepage = "https://www.lysator.liu.se/~nisse/nettle/"
    gnu_mirror_path = "nettle/nettle-3.3.tar.gz"
    git = "https://gitlab.com/gnutls/nettle.git"

    license("GPL-2.0-or-later OR LGPL-3.0-or-later")

    version("develop", branch="master")
    version("4.0-git", tag="nettle_4.0_release_20260205",
            commit="bf13ee9e5024014cfa6d2fc097923afe087e63ba")

    version("4.0", sha256="3addbc00da01846b232fb3bc453538ea5468da43033f21bb345cb1e9073f5094",
            preferred=True)
    version("3.9.1", sha256="ccfeff981b0ca71bbd6fbcb054f407c60ffb644389a5be80d6716d5b550c6ce3")
    version("3.8.1", sha256="364f3e2b77cd7dcde83fd7c45219c834e54b0c75e428b6f894a23d12dd41cbfe")
    version("3.4.1", sha256="f941cf1535cd5d1819be5ccae5babef01f6db611f9b5a777bae9c7604b8a92ad")
    version("3.4", sha256="ae7a42df026550b85daca8389b6a60ba6313b0567f374392e54918588a411e94")
    version("3.3", sha256="46942627d5d0ca11720fec18d81fc38f7ef837ea4197c1f630e71ce0d470b11e")
    version("3.2", sha256="ea4283def236413edab5a4cf9cf32adf540c8df1b9b67641cfc2302fca849d97")
    version("2.7.1", sha256="bc71ebd43435537d767799e414fce88e521b7278d48c860651216e1fc6555b40")
    version("2.7", sha256="c294ea133c05382cc2effb1734d49f4abeb1ad8515543a333de49a11422cd4d6")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    variant("pic", values=(any_combination_of("yes", "no")
                           .prohibit_empty_set()
                           .with_default("yes,no")),
            description="Compile with position independent code")

    variant(
        "libs",
        default="shared,static",
        values=("shared", "static"),
        multi=True,
        description="Build shared libs, static libs or both",
    )

    depends_on("gmp", when="@:3.9")
    depends_on("m4", type="build", when="@:3.9")

    depends_on("gnulib@2026.06.30-snapshot", type="build", when="@4:")

    @run_before("configure")
    def _bootstrap(self):
        if not Path('./configure').is_file():
            Executable("./.bootstrap")()
        if self.spec.satisfies("@4:"):
            gnulib_tool('--libtool', '--import', 'libgmp', 'libgmp-mpq', 'libgmp-mpz')
            gnulib_tool('--update')

    def flag_handler(self, name, flags):
        if name == "cflags":
            if self.spec.satisfies("@:3.9"):
                flags.append(self.compiler.c99_flag)
        return (flags, None, None)

    def configure_args(self):
        args = ["--disable-openssl"]

        args.extend(self.enable_or_disable("libs"))
        pic = self.spec.variants['pic'].value
        if pic == 'yes':
            args.append('--enable-pic')
        elif pic == 'no':
            args.append('--disable-pic')

        if self.spec.satisfies("@4:"):
            args.append('--enable-mini-gmp')
            if self.spec.target.family == 'x86_64':
                features = self.spec.target.features
                if 'aes' in features:
                    args.append('--enable-x86-aesni')
                    # FIXME: what is the name of this feature?????
                    args.append('--enable-x86-sha-ni')
                if 'pclmulqdq' in features:
                    args.append('--enable-x86-pclmul')
            args.append('--enable-fat')

        return args
