# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack_repo.builtin.build_systems.cmake import CMakePackage, generator

from spack.package import *


class Brotli(CMakePackage):
    """Brotli is a generic-purpose lossless compression algorithm"""

    homepage = "https://github.com/google/brotli"
    url = "https://github.com/google/brotli/archive/v1.0.7.tar.gz"

    license("MIT")

    executables = [r'^brotli$']

    version("1.2.0", sha256="816c96e8e8f193b40151dad7e8ff37b1221d019dbcb9c35cd3fadbfe6477dfec")

    variant("tools", default=True,
        description="Build the `brotli` executable.")

    variant(
        "libs",
        default="shared",
        values=("shared", "static"),
        description="Build shared libs or static libs (brotli only allows one or the other)",
    )

    depends_on("c", type="build")

    depends_on("cmake@3.15:", type="build")
    generator("make")
    depends_on("gmake", type="build")

    def cmake_args(self) -> list[str]:
        args = [
            self.define("BROTLI_BUILD_FOR_PACKAGE", False),
        ]

        args.append(self.define_from_variant("BROTLI_BUILD_TOOLS", "tools"))

        libs = self.spec.variants['libs'].value
        if libs == 'shared':
            args.append(self.define("BUILD_SHARED_LIBS", True))
        else:
            assert libs == 'static', libs
            args.append(self.define("BUILD_SHARED_LIBS", False))

        return args

    _version_at_eol = re.compile(r'\s+([0-9]+\.[0-9]+(?:\.[0-9]+)?\S*)$')
    @classmethod
    def determine_version(cls, exe):
        exe = Executable(exe)
        m = cls._version_at_eol.search(exe("--version").splitlines()[0])
        if m:
            return m.group(1)
        return None
