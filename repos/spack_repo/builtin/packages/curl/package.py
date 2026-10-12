# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
import sys

from spack_repo.builtin.build_systems.autotools import AutotoolsBuilder, AutotoolsPackage
from spack_repo.builtin.build_systems.cmake import CMakeBuilder, CMakePackage

from spack.package import *
from spack.version import StandardVersion

IS_WINDOWS = sys.platform == "win32"


class Curl(AutotoolsPackage, CMakePackage):
    """cURL is an open source command line tool and library for
    transferring data with URL syntax"""

    homepage = "https://curl.se/"
    url = "https://curl.haxx.se/download/curl-7.78.0.tar.bz2"
    git = "https://github.com/curl/curl.git"

    executables = ["^curl$"]
    tags = ["build-tools", "windows"]

    maintainers("alecbcs")

    license("curl")

    version("8.22.0", sha256="5d956a6a22b3c279f50c421ee5d3c9e9d660cb6f115dcf881b579e952130549c")
    version("8.21.0", sha256="ad6f2f94934b38e31e48272833c99b891d045b4565fe942a53fbd27bd3910e16")
    version("8.20.0", sha256="4be48e69cf467246cb97d369b85d78a08528f2b37cffef2418ee16e6a4eb596e")
    version("8.19.0", sha256="eba3230c1b659211a7afa0fbf475978cbf99c412e4d72d9aa92d020c460742d4")
    version("8.18.0", sha256="ffd671a3dad424fb68e113a5b9894c5d1b5e13a88c6bdf0d4af6645123b31faf")
    version("8.17.0", sha256="230032528ce5f85594d4f3eace63364c4244ccc3c801b7f8db1982722f2761f4")
    version("8.15.0", sha256="699a6d2192322792c88088576cff5fe188452e6ea71e82ca74409f07ecc62563")
    version("8.14.1", sha256="5760ed3c1a6aac68793fc502114f35c3e088e8cd5c084c2d044abdf646ee48fb")

    # TODO: add dependencies for other possible TLS backends

    # common arguments for tls variant definitions
    tls_args = {
        "description": "TLS backend",
        "multi": True,
        "values": (
            # 'amissl',
            # 'bearssl',
            "gnutls",
            "mbedtls",
            # 'mesalink',
            "openssl",
            # 'rustls',
            # 'schannel',
            # secure_transport support was removed in curl 8.15.0
            conditional("secure_transport", when="platform=darwin @:8.14"),
            # 'wolfssl',
            conditional("sspi", when="platform=windows"),
        ),
    }

    variant("tls", default="gnutls", **tls_args)
    variant("tls", default="sspi", when="platform=windows", **tls_args)
    variant("tls", default="secure_transport", when="platform=darwin @:8.14", **tls_args)

    variant("backtrace", default=True, description="build with backtrace support",
            when='build_system=autotools')
    variant("nghttp2", default=True, description="build nghttp2 library")
    variant("nghttp3", default=True, description="build http/3 support")
    variant("ngtcp2", default=True, description="build with QUIC support")
    variant("libssh2", default=True, description="enable libssh2 support")
    # FIXME: deprecate variants!
    variant("libssh", default=False, description="[deprecated] enable libssh support")
    variant("gssapi", default=False, description="enable Kerberos support")
    variant("librtmp", default=False, description="enable Rtmp support")
    variant("ldap", default=False, description="enable ldap support")
    variant("libidn2", default=True, description="enable libidn2 support")
    variant("brotli", default=True, description="build with brotli support",
            when='build_system=autotools')
    variant("zlib", default=True, description="build with zlib-api support")
    variant("zstd", default=True, description="build with zstd support",
            when='build_system=autotools')
    variant("uv", default=True, description="build with libuv support",
            when='build_system=autotools')
    variant(
        "libs",
        default="shared,static" if not IS_WINDOWS else "shared",
        values=("shared", "static"),
        multi=not IS_WINDOWS,
        description="Build shared libs, static libs or both",
    )

    # with when('build_system=autotools'):
    #     variant("debug", default=False, description="Enable debug build flags.")
    #     variant("opt", default=True, description="Enable optimizations.")
    #     variant("verbose", default=True, description="Enable verbose strings.")


    with when("platform=windows build_system=cmake"):
        variant("static-crt", default=False, description="Link to static CRT")
        variant("unicode", default=False, description="Use the unicode version of Windows API")

    requires("platform=darwin", when="tls=secure_transport", msg="Only supported on macOS")

    depends_on("c", type="build")

    depends_on("pkg-config", type="build", when="platform=darwin")
    depends_on("pkg-config", type="build", when="platform=linux")
    depends_on("pkg-config", type="build", when="platform=freebsd")

    # CMake 4.0: is not compatible with CMake systems requiring
    # 3.0, which curl@7.63 requires
    depends_on("cmake@:3", type="build", when="build_system=cmake @:7.63")

    depends_on("gnutls@3.6.5:", when="tls=gnutls @8.18:", type=("link", "run"))
    depends_on("gnutls", when="tls=gnutls", type=("link", "run"))
    depends_on("mbedtls@3: +pic", when="tls=mbedtls @8.17:")
    depends_on("mbedtls@2: +pic", when="tls=mbedtls")
    depends_on("openssl@3:", when="tls=openssl @8.18:")
    depends_on("openssl", when="tls=openssl")

    depends_on("libidn2", when="+libidn2", type="link")
    depends_on("zlib-api", when="+zlib", type="link")
    depends_on("nghttp2", when="+nghttp2", type="link")
    depends_on("nghttp3", when="+nghttp3", type="link")
    depends_on("ngtcp2", when="+ngtcp2", type="link")
    depends_on("libssh2", when="+libssh2")
    depends_on("libssh", when="+libssh")
    depends_on("krb5", when="+gssapi")
    depends_on("rtmpdump", when="+librtmp")
    depends_on("zstd", when="+zstd", type=("link", "run"))
    depends_on("brotli", when="+brotli", type="link")
    depends_on("libbacktrace", when="+backtrace", type="link")
    depends_on("libbacktrace+shared", when="+backtrace libs=shared", type="link")
    depends_on("libuv", when="+uv", type="link")

    depends_on("c-ares", when="build_system=autotools", type=("link", "run"))

    build_system(
        "autotools",
        "cmake",
        default="cmake" if IS_WINDOWS else "autotools",
    )


    with default_args(type="build", when="build_system=autotools"):
        depends_on("autoconf@2.59:")
        depends_on("automake@1.16:")
        depends_on("libtool")
        depends_on("ca-certificates-mozilla@2026:")

    @classmethod
    def determine_version(cls, exe):
        curl = Executable(exe)
        output = curl("--version", output=str, error=str)
        match = re.match(r"curl ([\d.]+)", output)
        return match.group(1) if match else None

    @classmethod
    def determine_variants(cls, exes, version):
        for exe in exes:
            variants = ""
            curl = Executable(exe)
            output = curl("--version", output=str, error=str)
            if "nghttp2" in output:
                variants += "+nghttp2"
            protocols_match = re.search(r"Protocols: (.*)\n", output)
            if protocols_match:
                protocols = protocols_match.group(1).strip().split(" ")
                if "ldap" in protocols:
                    variants += "+ldap"
            features_match = re.search(r"Features: (.*)\n", output)
            if features_match:
                features = features_match.group(1).strip().split(" ")
                if "GSS-API" in features:
                    variants += "+gssapi"
            # TODO: Determine TLS backend if needed.
            # TODO: Determine more variants.
            return variants

    @property
    def command(self):
        return Executable(self.prefix.bin.join("curl-config"))

    def flag_handler(self, name, flags):
        build_system_flags = []
        spec = self.spec
        if name == "cflags" and (spec.satisfies("%intel") or spec.satisfies("%oneapi")):
            build_system_flags = ["-we147"]
        return flags, None, build_system_flags


class AutotoolsBuilder(AutotoolsBuilder):
    def configure_args(self) -> list[str]:
        spec = self.spec

        args = [
            # Prevent unintentional linking against system libraries: we could
            # add variants for these in the future
            "--without-libgsasl",
            "--without-libpsl",
            "--enable-docs",
            "--enable-manual",
        ]

        args.extend(self.enable_or_disable("libs"))

        if spec.satisfies('tls=gnutls'):
            args.extend([
                '--with-default-ssl-backend=gnutls',
                '--without-ca-bundle',
                '--without-ca-path',
                '--without-ca-fallback',
                f"--with-ca-embed={mozilla_ca_bundle}",
                '--enable-websockets',
                '--enable-hsts',
                '--enable-headers-api',
                '--enable-alt-svc',
                '--enable-get-easy-options',
                '--enable-dnsshuffle',
                '--enable-sha512-256',
                '--enable-progress-meter',
                '--enable-netrc',
                '--enable-dateparse',
                '--enable-form-api',
                '--enable-bindlocal',
                '--enable-mime',
                '--enable-doh',
                '--enable-http-auth',
                '--enable-socketpair',
                '--enable-cookies',
                '--enable-unix-sockets',
                '--enable-tls-srp',
                '--enable-ntlm',
                '--enable-aws',
                '--enable-negotiate-auth',
                '--enable-kerberos-auth',
                '--enable-digest-auth',
                '--enable-basic-auth',
                '--enable-bearer-auth',
                '--enable-sspi',
                '--enable-typecheck',
                # this is redundant with c-ares apparently? the docs are useless:
                # https://circumstances.run/@hipsterelectron/116948221193996710
                # '--enable-threaded-resolver',
                '--enable-versioned-symbols',
                # FIXME!
                '--enable-ca-search-safe',
                '--enable-ca-native',
                '--disable-openssl-auto-load-config',
                '--enable-ipv6',
                '--enable-libcurl-option',
                '--enable-mqtt',
                '--enable-gopher',
                '--enable-smtp',
                '--enable-smb',
                '--enable-imap',
                '--enable-pop3',
                '--enable-tftp',
                '--enable-telnet',
                '--enable-dict',
                '--enable-proxy',
                '--enable-rtsp',
                '--enable-ipfs',
                '--enable-file',
                '--enable-ftp',
                '--enable-http',
                '--enable-unity',
                '--enable-largefile',
                '--enable-year2038',
                # apparently this only works with openssl?
                # despite openssl not supporting http/3 itself?
                # '--enable-proxy-http3',
                '--enable-ssls-export',
                # marked "experimental" for the last 3 years:
                # https://github.com/curl/curl/blob/master/docs/ECH.md
                # gnutls was stonewalled by cloudflare when they tried to implement:
                # https://gitlab.com/gnutls/gnutls/-/work_items/595#note_1390322559
                # but the EFF and senators love ECH apparently
                # '--enable-ech',
                # '--enable-httpsrr',
                '--enable-optimize',
                '--enable-warnings',
                '--enable-verbose',
                '--disable-rt',
                f"--with-zsh-functions-dir={self.prefix}"
            ])
        args.append(f"--enable-ares={self.spec['c-ares'].prefix}")

        # Make gnutls / openssl decide what certs are trusted.
        # TODO: certs for other tls options.
        if spec.satisfies("@:8.20 tls=gnutls") or spec.satisfies("tls=openssl"):
            args.extend(["--without-ca-bundle", "--without-ca-path", "--with-ca-fallback"])

        if spec.satisfies("+gssapi"):
            args.append("--with-gssapi=" + spec["krb5"].prefix)
        else:
            args.append("--without-gssapi")

        args.extend(self.with_or_without("tls"))
        args.extend(self.with_or_without("libidn2", activation_value="prefix"))
        args.extend(self.with_or_without("librtmp"))
        args.extend(self.with_or_without("nghttp2", activation_value="prefix"))
        args.extend(self.with_or_without("nghttp3", activation_value="prefix"))
        args.extend(self.with_or_without("ngtcp2", activation_value="prefix"))
        args.extend(self.with_or_without("libssh2", activation_value="prefix"))
        args.extend(self.with_or_without("libssh", activation_value="prefix"))
        if '+ldap' in spec:
            args.extend(['--enable-ldap', '--enable-ldaps'])
        else:
            args.extend(['--disable-ldap', '--disable-ldaps'])
        args.extend(self.with_or_without('brotli'))
        if spec.satisfies('+zlib'):
            args.append(f"--with-zlib={spec['zlib-api'].prefix}")
        args.extend(self.with_or_without('zstd'))
        if '+backtrace' in spec:
            args.append('--enable-backtrace')
        if self.spec.satisfies('%c=gcc'):
            args.append('--with-libgcc')

        return filter(None, args)

    def with_or_without_librtmp(self, activated):
        if activated:
            return f"--with-librtmp={self.spec['librtmp'].prefix}"
        elif self.spec.version < StandardVersion.from_string("8.21"):
            return '--without-librtmp'

    def with_or_without_gnutls(self, activated):
        if activated:
            return "--with-gnutls=" + self.spec["gnutls"].prefix
        else:
            return "--without-gnutls"

    def with_or_without_mbedtls(self, activated):
        if activated:
            return "--with-mbedtls=" + self.spec["mbedtls"].prefix
        else:
            return "--without-mbedtls"

    def with_or_without_openssl(self, activated):
        if activated:
            return "--with-openssl=" + self.spec["openssl"].prefix
        else:
            return "--without-openssl"

    def with_or_without_sspi(self, activated):
        if activated:
            return f"--with-sspi={self.spec['sspi'].prefix}"
        elif self.spec.version < StandardVersion.from_string("8.21"):
            return '--without-sspi'

    def with_or_without_secure_transport(self, activated):
        if activated:
            return "--with-secure-transport"
        elif self.spec.version < StandardVersion.from_string("8.21"):
            return "--without-secure-transport"


class CMakeBuilder(CMakeBuilder):
    def cmake_args(self):
        args = [
            self.define("BUILD_TESTING", False),
            self.define("CURL_USE_LIBPSL", False),
            # Curl's CMake will turn this off if not building static libcurl
            self.define("BUILD_STATIC_CURL", True),
            # enables install from cmake
            self.define("CURL_DISABLE_INSTALL", False),
            self.define("BUILD_MISC_DOCS", False),
            self.define("BUILD_LIBCURL_DOCS", False),
            self.define("BUILD_EXAMPLES", False),
            self.define("CURL_BROTLI", False),
            self.define("CURL_USE_GSASL", False),
            self.define_from_variant("CURL_ZSTD", "zstd"),
            self.define("ENABLE_CURL_MANUAL", False),
            self.define_from_variant("CURL_USE_LIBSSH2", "libssh2"),
            self.define_from_variant("CURL_USE_LIBSSH", "libssh"),
            self.define_from_variant("CURL_USE_OPENLDAP", "ldap"),
            self.define_from_variant("CURL_DISABLE_LDAP", "ldap"),
            self.define_from_variant("USE_NGHTTP2", "nghttp2"),
            self.define_from_variant("CURL_USE_GSSAPI", "gssapi"),
            self.define_from_variant("USE_LIBRTMP", "librtmp"),
            self.define_from_variant("USE_LIBIDN2", "libidn2"),
        ]

        if self.spec.satisfies("tls=sspi"):
            args.append(self.define("CURL_WINDOWS_SSPI", True))
        if self.spec.satisfies("tls=gnutls"):
            args.append(self.define("CURL_USE_GNUTLS", True))
        if self.spec.satisfies("tls=mbedtls"):
            args.append(self.define("CURL_USE_MBEDTLS", True))
        if self.spec.satisfies("tls=openssl"):
            args.append(self.define("CURL_USE_OPENSSL", True))

        if self.spec.satisfies("platform=windows"):
            args.extend(
                [
                    self.define_from_variant("ENABLE_UNICODE", "unicode"),
                    self.define_from_variant("CURL_STATIC_CRT", "static-crt"),
                ]
            )
            if self.spec.satisfies("+ldap"):
                args.append(self.define("USE_WIN32_LDAP", True))

        if self.spec.satisfies("libs=shared"):
            args.append(self.define("BUILD_SHARED_LIBS", True))
        if self.spec.satisfies("libs=static"):
            args.append(self.define("BUILD_STATIC_LIBS", True))
        return args
