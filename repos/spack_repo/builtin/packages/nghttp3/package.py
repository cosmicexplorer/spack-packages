# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Nghttp3(AutotoolsPackage):
    """nghttp3 is a thin HTTP/3 layer over an underlying QUIC stack."""
    homepage = "https://nghttp2.org/nghttp3/"
    url = "https://github.com/ngtcp2/nghttp3/releases/download/v1.17.0/nghttp3-1.17.0.tar.xz"
    git = "https://github.com/ngtcp2/nghttp3.git"
    submodules = True

    supplier = "ngtcp2"

    maintainers("cosmicexplorer")

    license("MIT", checked_by="cosmicexplorer")

    version("1.17.0", sha256="e8b798272b9282045cb83577dcf7bd7fcd22bb3a43aec0eb1a24f675b4cef0b8")
    version("1.16.0", sha256="776f59a99905c9a348846807b2e5ac9bb3485fc0f8c0250ba803018d5238a16e")
    version("1.15.0", sha256="6da0cd06b428d32a54c58137838505d9dc0371a900bb8070a46b29e1ceaf2e0f")
    version("1.14.0", sha256="b3083dae2ff30cf00d24d5fedd432479532c7b17d993d384103527b36c1ec82d")
    version("1.13.1", sha256="020836668c711d5c166969f8b165fbfd989e6967d0601947bf608f29e2158518")

    depends_on("c", type="build")

    def configure_args(self):
        return [
            '--enable-lib-only',
            '--enable-year2038',
        ]
