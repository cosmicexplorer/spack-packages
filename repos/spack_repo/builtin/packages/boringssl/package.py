# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Boringssl(CMakePackage):
    """BoringSSL is a fork of OpenSSL that is developed by Google to meet Google's needs and is
    generally considered more performant and secure than OpenSSL.

    The ngtcp2 project has recommended at least a particular commit hash at one point,
    making it slightly easier to trust:
    <https://github.com/ngtcp2/ngtcp2/blob/713151dcef2b48e3f2d7977d091d8c92c0e9171d/README.rst>
    """
    docstring_has_extended_text = True

    homepage = "https://boringssl.googlesource.com/boringssl"
    git = "https://boringssl.googlesource.com/boringssl.git"

    provides("tls")

    maintainers("ta7mid")

    license("Apache-2.0", checked_by="ta7mid")

    version("main", branch="main")
    version("ngtcp2-recommended", commit="3c6315e00ab02d7bc9b8922aff1f85d8f81ee130",
            preferred=True)

    variant(
        "no_asm",
        default=False,
        description="Disable the use of assembly code, losing significant performance benefits",
    )
    variant("small", default=False, description="Reduce binary size at some performance cost")
    variant("shared", default=False, description="Build shared libraries")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    def cmake_args(self):
        return [
            self.define_from_variant("OPENSSL_NO_ASM", "no_asm"),
            self.define_from_variant("OPENSSL_SMALL", "small"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define("BUILD_TESTING", False),
        ]
