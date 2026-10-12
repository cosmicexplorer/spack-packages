# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Acl(AutotoolsPackage):
    """Commands for Manipulating POSIX Access Control Lists."""

    homepage = "https://savannah.nongnu.org/projects/acl"
    url = "https://download.savannah.nongnu.org/releases/acl/acl-2.4.0.tar.gz"

    license("LGPL-2.1-or-later AND GPL-2.0-or-later", checked_by="tgamblin")

    version("2.4.0", sha256="73c853c3d44e1f693e5a96a986f1bd19d3d0dac2c7d453e796177774bc4e5f6a")
    version("2.2.53", sha256="9e905397ac10d06768c63edd0579c34b8431555f2ea8e8f2cee337b31f856805")
    version("2.2.52", sha256="f3f31d2229c903184ff877aa0ee658b87ec20fec8aebb51e65eaa68d7b24e629")
    version("2.2.51", sha256="31a43d96a274a39bfcb805fb903d45840515344884d224cef166b482693a9f48")
    version("2.2.50", sha256="39e21d623a9f0da8c042cde346c01871b498d51400e92c2ab1490d5ffd724401")
    version("2.2.49", sha256="c6e01460cac4e47673dd60a7f57b970b49f6998bb564eff141cca129aa8940d1")
    version("2.2.48", sha256="877eaeccc1500baec58391935b46ac7dfc5ffd8c54fbc0385ccd8b2b18ac3fa6")

    depends_on("c", type="build")  # generated

    depends_on("autoconf@2.65:", type="build")
    depends_on("automake@2:", type="build")
    depends_on("libtool@2.1:", type="build")
    depends_on("attr")
    depends_on("gettext", type=("build", "link"))

    def flag_handler(self, name, flags):
        if name == "ldlibs" and "intl" in self.spec["gettext"].libs.names:
            flags.append("-lintl")
        return self.build_system_flags(name, flags)

    @when("@2.2")
    def autoreconf(self, spec, prefix):
        bash = which("bash", required=True)
        bash("./autogen.sh")
