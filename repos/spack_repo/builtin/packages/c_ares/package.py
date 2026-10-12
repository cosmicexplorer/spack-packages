# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *
from spack.version import ConcreteVersion, StandardVersion


class CAres(AutotoolsPackage):
    """c-ares: A C library for asynchronous DNS requests"""

    homepage = "https://c-ares.haxx.se"
    url = "https://github.com/c-ares/c-ares/releases/download/v1.34.8/c-ares-1.34.8.tar.gz"
    git = "https://github.com/c-ares/c-ares.git"

    license("MIT")

    version("develop", branch="main")
    version("1.34.8", sha256="c222b6d681096f9444d2c4863d2c1174019e27cacca0a4a5c114d36dd7d7bf78")
    version("1.28.1", sha256="e520d971415e48e607819c2f4b377b0aa69044ef6619160bb41bdba15ab4d545")
    version("1.27.0", sha256="de6a839d47b93174ba260187a084027ea681a91ffe12f2d5f20645652eae246c")
    version("1.15.0", sha256="7deb7872cbd876c29036d5f37e30c4cbc3cc068d59d8b749ef85bb0736649f04")
    version("1.13.0", sha256="7c48c57706a38691041920e705d2a04426ad9c68d40edd600685323f214b2d57")

    variant("libs", values=(any_combination_of("shared", "static")
                            .prohibit_empty_set()
                            .with_default("shared,static")),
            description="How to link the resulting library outputs.")
    variant("pic", values=(any_combination_of("yes", "no")
                           .prohibit_empty_set()
                           .with_default("yes,no")))

    depends_on("autoconf@2.69:", type="build")
    depends_on("automake@1.9.6:", type="build")
    depends_on("libtool", type="build")
    depends_on("pkg-config", type="build")

    depends_on("c", type="build")

    _older_url_format = "https://github.com/c-ares/c-ares/archive/cares-{0}.tar.gz"
    _older_threshold = StandardVersion.from_string("1.15")
    def url_for_version(self, version: ConcreteVersion) -> str:
        if version <= self.__class__._older_threshold:
            return self.__class__._older_url_format.format(version.underscored)
        return super().url_for_version(version)

    @property
    def libs(self):
        return find_libraries(["libcares"], root=self.prefix, recursive=True)

    def configure_args(self) -> list[str]:
        args = []

        if self.spec.satisfies('%c=gcc'):
            args.append('--enable-libgcc')

        args.extend(self.enable_or_disable('libs'))
        pic = self.spec.variants['pic'].value
        if pic == 'yes':
            args.append('--enable-pic')
        elif pic == 'no':
            args.append('--disable-pic')

        args.extend([
            '--disable-tests',
            '--enable-cares-threads',
            '--enable-largefile',
            '--enable-year2038',
        ])

        return args
