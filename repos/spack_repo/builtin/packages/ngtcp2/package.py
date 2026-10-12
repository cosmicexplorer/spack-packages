# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Ngtcp2(AutotoolsPackage):
    """ngtcp2 project is an effort to implement IETF QUIC protocol."""

    homepage = "https://nghttp2.org/ngtcp2/"
    url = "https://github.com/ngtcp2/ngtcp2/releases/download/v1.24.0/ngtcp2-1.24.0.tar.xz"
    git = "https://github.com/ngtcp2/ngtcp2.git"
    submodules = True

    supplier = "ngtcp2"

    maintainers("cosmicexplorer")

    license("MIT", checked_by="cosmicexplorer")

    version("1.24.0", sha256="7fa5ec2be0f0cbed8bc4ec89c0787dfa9d8ce678f1ed9477c52f30eb1a591207")
    version("1.23.0", sha256="59d5b4211e96970f2d3d5e6876f73dce03414800ba04aa56835b132fce8de730")
    version("1.22.1", sha256="dfd2c68bd64b89847c611425b9487105c46e8447b5c21e6aeb00642c8fbe2ca8")
    version("1.22.0", sha256="75c1d6f5c7936b23bfab9c143c8e9f1cca1acf3ab66dba705306ec7dac6fe0f1")
    version("1.21.0", sha256="2d1c07e6aa509c017516c08307b0b707cd165a17275ab5f1caff9aaa0e3b6c7d")

    variant("tls",
            values=(any_combination_of("gnutls", "boringssl", "libressl", "openssl")
                    .allow_empty_set()
                    .with_default("gnutls")),
            description="build in crypto support, including library-specific API functions.\n"
            "However, it remains possible to implement by hand.\n"
            "See the website for further discussion:\n"
            "<https://nghttp2.org/ngtcp2/programmers-guide.html#tls-integration>")
    variant("memdebug", default=False,
            description="Whether to write debug messages to stderr upon each memory allocation.")
    variant("mempool", default=False,
            description="Whether to pool memory across streams while the library is in use.\n"
            "See example usage at:\n"
            "<https://github.com/ngtcp2/ngtcp2/blob/713151dcef2b48e3f2d7977d091d8c92c0e9171d/lib/ngtcp2_ksl.c#L112-L139>")


    # FIXME: break these out into generic traits!!! possibly memdebug too!!! and tls!!!
    variant("debug", default=False,
            description="Whether to write protocol debug messages to stderr.")
    variant("jemalloc", default=False,
            description="Use the jemalloc allocator.")
    variant("asan", default=False,
            description="Enable address sanitization.")
    variant("libs", values=(any_combination_of("static", "shared")
                            .prohibit_empty_set()
                            .with_default("static,shared")),
            description="build shared and/or static libraries")
    variant("pic", values=(any_combination_of("yes", "no")
                           .prohibit_empty_set()
                           .with_default("yes,no")))

    depends_on("c", type="build")

    depends_on("pkg-config@0.20:", type="build")
    depends_on("autoconf@2.61:", type="build")
    depends_on("automake@1.18:", type="build")
    depends_on("libtool@2.2.6:", type="build")

    depends_on("gnutls@3.7.5:", when="tls=gnutls")
    depends_on("boringssl@ngtcp2-recommended:", when="tls=boringssl")
    depends_on("libressl@3.9.2:", when="tls=libressl")
    depends_on("openssl@3.5.0:", when="tls=openssl")
    depends_on("jemalloc", when="+jemalloc")

    def configure_args(self):
        args = [
            '--enable-lib-only',
            '--enable-year2038',
            # This is also the only way to enable any warnings at all.
            # We can trust spack to stop this from actually engaging -Werror.
            '--enable-werror',
        ]

        # Dependencies.
        tls = self.spec.variants['tls'].value
        if 'gnutls' in tls:
            args.append(f"--with-gnutls={self.spec['gnutls'].prefix}")
        elif 'boringssl' in tls:
            args.append(f"--with-boringssl={self.spec['boringssl'].prefix}")
        elif 'libressl' in tls:
            args.append(f"--with-openssl={self.spec['libressl'].prefix}")
        elif 'openssl' in tls:
            args.append(f"--with-openssl={self.spec['openssl'].prefix}")
        else:
            args.append('--without-openssl')

        args.extend(self.with_or_without("jemalloc"))

        # Debugging.
        args.extend(self.enable_or_disable("debug"))
        args.extend(self.enable_or_disable("memdebug"))
        args.extend(self.enable_or_disable('asan'))

        # Memory and performance optimizations.
        args.extend(self.enable_or_disable("mempool"))

        # Library build scenarios.
        args.extend(self.enable_or_disable('libs'))

        pic = self.spec.variants['pic'].value
        if pic == 'yes':
            args.append('--enable-pic')
        elif pic == 'no':
            args.append('--disable-pic')

        return args
