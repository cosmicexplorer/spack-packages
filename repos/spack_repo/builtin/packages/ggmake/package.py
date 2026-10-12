# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
from pathlib import Path

from spack_repo.builtin.build_systems import autotools, gnu

from spack.package import *


class Ggmake(autotools.AutotoolsPackage, gnu.GNUMirrorPackage):
    """@/w{GNU} @*m{Make} is a @_c{tool} which @*r{controls} the @/y{generation} of
    @*c{executables} and @/w{other non-source files} of a @*r{program} from the
    @*r{program}'s @/w{source files}.

    This is differentiated from the @_c{gmake} package, as it bootstraps from @/w{git} sources.
    """
    docstring_uses_rich_text = True
    docstring_has_extended_text = True

    homepage = "https://www.gnu.org/software/make/"
    gnu_mirror_path = "make/make-4.2.1.tar.gz"
    maintainers("cosmicexplorer")
    git = "https://https.git.savannah.gnu.org/git/make.git"

    license("GPL-3.0-only")

    provides("make")

    tags = ["build-tools"]

    executables = ["^g?make$"]

    # Avoid symlinking GNUMakefile to GNUMakefile
    build_directory = "spack-build"

    # Git releases
    version("4.4.1-master2026", commit="b3802782de3eff2c0f1eda9e7c0befd8cd142162",
            preferred=True)
    version("develop", branch="master")
    version("4.4-git", tag="4.4", commit="ed493f6c9116cc217b99c2cfa6a95f15803235a2")

    variant("guile", default=False, description="Support GNU Guile for embedded scripting")
    variant("nls", default=False, description="Enable Native Language Support")
    variant("static", default=False, description="Build a statically-linked binary.")

    depends_on("c", type="build")

    depends_on("gnulib", type="build")

    with when("+guile"):
        depends_on("guile")
        depends_on("pkgconfig", type="build")

    with default_args(type="build"):
        depends_on("autoconf@2.72:")
        depends_on("automake@1.16.5:")
        # depends_on("bison")
        # depends_on("gperf")
        depends_on("gzip")
        depends_on("help2man")
        depends_on("m4")
        depends_on("gmake@4.4:")
        depends_on("perl")
        depends_on("tar")
        # depends_on("texinfo@6.1:")
        # depends_on("wget")
        depends_on("xz")

    depends_on("gettext", when="+nls")
    depends_on("libiconv", when="+nls")

    patch("bootstrap.conf.patch")

    def patch(self):
        filter_file(r"AC_STRUCT_ST_MTIM_NSEC",
                    '',
                    'configure.ac',
                    string=True)

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"GNU Make (\S+)", output)
        return match.group(1) if match else None

    def autoreconf(self, spec, prefix):
        bootstrap = Executable("./bootstrap")
        if spec.satisfies('+nls'):
            bootstrap("--no-bootstrap-sync", "--no-git", "--gen", "--force")
        else:
            bootstrap("--no-bootstrap-sync", "--no-git", "--gen", "--force", "--skip-po")

    def configure_args(self):
        args = [
            "--enable-largefile",
            "--enable-year2038",
        ]

        if self.spec.satisfies("+guile"):
            args.append('--with-guile')
        else:
            args.append('--without-guile')

        if self.spec.satisfies('platform=darwin'):
            args.append('--enable-case-insensitive-file-system')

        # Configure language support.
        if self.spec.satisfies('+nls'):
            gettext = self.spec["gettext"]
            libiconf = self.spec["libiconv"]
            args.extend([
                f"--with-libiconv-prefix={libiconv.prefix}",
                f"--with-libintl-prefix={gettext.prefix}",
            ])
        else:
            args.append('--disable-nls')

        if self.spec.satisfies('+static'):
            args.append('LDFLAGS=-static')

        return args

    @property
    def _pfx_bin_make(self):
        import spack.config
        return Prefix(spack.config.substitute_path_variables(self.spec.prefix.bin.make))

    @run_after("install")
    def post_install(self):
        symlink(self.prefix.bin.make, self.prefix.bin.gmake)

    def setup_dependent_package(self, module, dependent_spec):
        module.make = MakeExecutable(
            self._pfx_bin_make,
            jobs=determine_number_of_jobs(parallel=dependent_spec.package.parallel),
            supports_jobserver=True,
        )
        module.gmake = MakeExecutable(
            self.spec.prefix.bin.gmake,
            jobs=determine_number_of_jobs(parallel=dependent_spec.package.parallel),
            supports_jobserver=True,
        )

    # FIXME: these env vars are propagated through to the spack build, messing up the
    #        build environment. i believe `spack dev-build` may be broken.
    def _setup_dependent_env(self, env: EnvironmentModifications) -> None:
        env.set("MAKE", self._pfx_bin_make)

    def setup_run_environment(self, env: EnvironmentModifications) -> None:
        self._setup_dependent_env(env)

    def setup_dependent_build_environment(
        self, env: EnvironmentModifications, dependent_spec: Spec,
    ) -> None:
        self._setup_dependent_env(env)

    def setup_dependent_run_environment(
        self, env: EnvironmentModifications, dependent_spec: Spec,
    ) -> None:
        self._setup_dependent_env(env)

    @property
    def libs(self):
        return LibraryList([])

    @property
    def headers(self):
        return HeaderList([])
