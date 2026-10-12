# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.gnu import GNUMirrorPackage

import spack.llnl.util.tty
from spack.package import *
from spack.version import StandardVersion, Version


class Parallel(AutotoolsPackage, GNUMirrorPackage):
    """GNU parallel is a shell tool for executing jobs in parallel using
    one or more computers. A job can be a single command or a small
    script that has to be run for each of the lines in the input.
    """

    homepage = "https://www.gnu.org/software/parallel/"
    gnu_mirror_path = "parallel/parallel-20220522.tar.bz2"

    def _split_ver_components(self, v: Version) -> Version:
        assert type(v) is StandardVersion, v
        if len(v) == 1:
            s = str(v)
            if s.isdigit() and len(s) == 8:
                tty.debug('version %r has a standard 8-digit yyyymmdd CalVer representation, '
                          'much like the upstream gnu mirror',
                          v)
                return v
            else:
                raise SpackError(f"could not parse single-component version {v!r}: "
                                 'expected either yyyymmdd or yyyy.mm.dd CalVer format')
        return v

    def _merge_ver_components(self, v: Version) -> Version:
        assert type(v) is StandardVersion, v
        # Stylishly split the yyyymmdd string in yyyy.mm.dd to disambiguate comparison
        # semantics:
        try:
            yyyy,mm,dd = str(v.dotted).split('.')
        except ValueError:
            raise SpackError(f"expected version {v!r} for package {self.spec.name!r}"
                             "to split into 3 'yyyy.mm.dd' components "
                             f"(num components was: {len(v)})")
        return StandardVersion.from_string(f"{yyyy}{mm}{dd}")

    def url_for_version(self, v: Version) -> str:
        return super().url_for_version(self._merge_ver_components(v))


    license("GPL-3.0-or-later", checked_by="wdconinc")

    version("2026.06.22", sha256="bcdb706d92a9f0a496c05e143d90c26b57e1848f06842c7de419dc3efb56a865")
    version("2024.08.22", sha256="d7bbd95b7631980b172be04cbd2138d5f7d8c063d6da5ad8f9f70dfd88c8309d")
    version("2022.05.22", sha256="bb6395f8d964e68f3bdb26a764d3c48b69bc5b759a92ac3ab2bd1895c7fa8c1f")
    version("2022.04.22", sha256="96e4b73fff1302fc141a889ae43ab2e93f6c9e86ac60ef62ced02dbe70b73ca7")
    version("2022.03.22", sha256="df93ccf6a9f529ad2126b7042aef0486603e938c77b405939c41702d38a4e6d8")
    version("2022.02.22", sha256="f81682b863ead7fb9a114754001e9286f954550a57a3cf36c9003a8047a6a445")
    version("2022.01.22", sha256="b8221a21412bca572ad8445b7981dfd625a3c6d48772cda468dfb5b886337e00")
    version("2021.09.22", sha256="dedca94fc41f2054dbadd9b8361e56015fc8af5d1961c1b982b63e6d86494d66")
    version("2020.08.22", sha256="9654226a808392c365b1e7b8dea91bf4870bc4f306228d853eb700679e21be09")
    version("2019.02.22", sha256="86b1badc56ee2de1483107c2adf634604fd72789c91f65e40138d21425906b1c")
    version("2017.03.22", sha256="f8f810040088bf3c52897a2ee0c0c71bd8d097e755312364b946f107ae3553f6")
    version("2017.01.22", sha256="417e83d9de2fe518a976fcff5a96bffe41421c2a57713cd5272cc89d1072aaa6")
    version("2016.04.22", sha256="065a8f471266361218a9eb45c5f8ab995d73b181cc1180600ee08cc768c9ac42")
    version("2016.03.22", sha256="6430f649ec07243645c955e8d6bee6da1df2e699b1e49b185946d1ab38731b08")

    depends_on("perl", type=("build", "run"))

    def check(self):
        # The Makefile has a 'test' target, but it does not work
        make("check")

    @run_before("install")
    def filter_sbang(self):
        """Run before install so that the standard Spack sbang install hook
        can fix up the path to the perl binary.
        """
        perl = self.spec["perl"].command
        kwargs = {"ignore_absent": False, "backup": False, "string": False}

        with working_dir("src"):
            match = "^#!/usr/bin/env perl|^#!/usr/bin/perl.*"
            substitute = f"#!{perl}"
            files = ["parallel", "niceload", "parcat", "sql"]
            filter_file(match, substitute, *files, **kwargs)
            # Since scripts are run during installation, we need to add sbang
            for file in files:
                filter_shebang(file)
