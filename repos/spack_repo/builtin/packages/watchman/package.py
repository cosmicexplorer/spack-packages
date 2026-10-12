# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install watchman
#
# You can edit this file again by typing:
#
#     spack edit watchman
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Watchman(CMakePackage):
    """Watchman exists to watch files and record when they change.
    It can also trigger actions (such as rebuilding assets) when matching files change.

    @/m{Note that this is a facebook product.}
    """
    docstring_uses_rich_text = True
    docstring_has_extended_text = True

    homepage = "https://facebook.github.io/watchman/"
    url = "https://github.com/facebook/watchman/releases/download/v2026.06.29.00/watchman-v2026.06.29.00-linux.zip"
    git = "https://github.com/facebook/watchman"

    supplier = "facebook"

    maintainers("cosmicexplorer")

    license("MIT", checked_by="cosmicexplorer")

    version("2026.06.29.00", sha256="4f0dd1317a92c516eed2d4c5ce0f1b9541dd5fda11fae7700d1be82854f6bca0")
    version("2026.06.22.00", sha256="518805368b2bd845f48f333810c5f7eddb82b86280d1778a39b4e7626e676dff")
    version("2026.06.15.00", sha256="ba1e4b9483256a8a84becd9ca0dea2902eddec1820ffae9782589fb6d5c1032f")
    version("2026.06.08.00", sha256="008ef0f73ff441db42206320771bbc1cc3f87e2b9f4edad9214eadf17235dd8f")
    version("2026.05.11.00", sha256="c2660458654145b19869fd8c38e17e6eb9259a502795fe6b4bc1e8c2b0bca76e")
    version("2026.05.04.00", sha256="0498993f6cbf7f2e7a134c284cb2225c21bb1b85f16d0551a1c66bdd5c890a41")
    version("2026.04.27.00", sha256="451e60d2617a3c42aa42f0ee60d298ec0d2e5aadd34d54c0554ffc8797253df0")
    version("2025.06.30.00", sha256="63ec6b1c649bdf67b54333ea2b6432be0508d75e8bef1cee3363a9c27db0c6f0")
    version("2023.10.16.00", sha256="ab4d5579b0d571f87e3ce7986496e1b72a9226871f0ea440405d92c23124fc84")
    version("2022.10.03.00", sha256="91257a67b37af46e7d081b77c228cbbe8d0eadbfbf410ee77e11b0b2f69339dd")
    version("2021.08.23.00", sha256="a15bd0779725d2f2f511e50539ffd0b8a7a61ed793ca93f6300c10ef97b6091f")
    version("2020.07.27.00", sha256="a6649dc40ba24655accd3781097ec0461e964e3ae5fc72b90451b0701551bfef")
    version("2020.07.13.00", sha256="a5c972e9eaf445101734dce8eb6dab6a3291570b8f317590658c85d12d71832b")

    # variant("eden", default=True, description="Add support for the Eden virtual filesystem.")

    depends_on("cxx", type="build")

    requires("%gcc@10:", when="%gcc", msg="needs -fcoroutines")

    # FIXME: Add dependencies if required.
    # depends_on("foo")

    def cmake_args(self):
        # FIXME: Add arguments other than
        # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        # FIXME: If not needed delete this function
        args = [
            self.define("ENABLE_EDEN_SUPPORT", False),
        ]
        return args
