from Jumpscale import j
import time

CMD_APT_GET = "apt-get "

builder_method = j.builders.system.builder_method


class BuilderSystemPackage(j.builders.system._BaseClass):
    NAME = "SystemPackage"

    @builder_method()
    def _repository_ensure_apt(self, repository):
        self.ensure("python-software-properties")
        j.sal.process.execute("add-apt-repository --yes " + repository)

    def _apt_wait_free(self):
        timeout = time.time() + 300
        while time.time() < timeout:
            _, out, _ = self._execute("fuser /var/lib/dpkg/lock", showout=False, die=False)
            if out.strip():
                time.sleep(1)
            else:
                return
        raise TimeoutError("resource dpkg is busy")

    @builder_method()
    def _apt_get(self, cmd):

        cmd = CMD_APT_GET + cmd
        result = j.sal.process.execute(cmd)
        # If the installation process was interrupted, we might get the following message
        # E: dpkg was interrupted, you must manually j.sal.process.execute 'run
        # dpkg --configure -a' to correct the problem.
        if "run dpkg --configure -a" in result:
            j.sal.process.execute("DEBIAN_FRONTEND=noninteractive dpkg --configure -a")
            result = j.sal.process.execute(cmd)
        return result

    # def upgrade(self, package=None, reset=True):
    #     key = "upgrade_%s" % package
    #     if self._done_check(key, reset):
    #         return
    #     if j.core.platformtype.myplatform.platform_is_ubuntu:
    #         if package is None:
    #             return self._apt_get("-q --yes update")
    #         else:
    #             if type(package) in (list, tuple):
    #                 package = " ".join(package)
    #             return self._apt_get(' upgrade ' + package)
    #     elif j.builders.tools.isAlpine:
    #         j.builders.tools.execute("apk update")
    #         j.builders.tools.execute("apk upgrade")
    #     else:
    #         raise j.exceptions.RuntimeError(
    #             "could not install:%s, platform not supported" % package)
    #     self._done_set(key)

    @builder_method()
    def mdupdate(self):
        """
        update metadata of system
        """
        self._log_info("packages mdupdate")
        if j.core.platformtype.myplatform.platform_is_ubuntu:
            j.sal.process.execute("apt-get update")
        elif j.builders.tools.platform_is_alpine:
            j.builders.tools.execute("apk update")
        elif j.core.platformtype.myplatform.platform_is_osx:
            location = j.builders.tools.command_location("brew")
            # j.sal.process.execute("run chown root %s" % location)
            j.sal.process.execute("brew update")
        elif j.builders.tools.isArch:
            j.sal.process.execute("pacman -Syy")

    @builder_method()
    def upgrade(self, distupgrade=False):
        """
        upgrades system, distupgrade means ubuntu 14.04 will fo to e.g. 15.04
        """
        self.mdupdate()
        self._log_info("packages upgrade")
        if j.core.platformtype.myplatform.platform_is_ubuntu:
            if distupgrade:
                raise NotImplementedError()
                # return self._apt_get("dist-upgrade")
            else:
                self._apt_get("upgrade -y")
        # elif j.builders.tools.isArch:
        #     j.sal.process.execute(
        #         "pacman -Syu --noconfirm;pacman -Sc --noconfirm")
        elif j.core.platformtype.myplatform.platform_is_osx:
            j.sal.process.execute("brew upgrade")
        elif j.builders.tools.isAlpine:
            j.builders.tools.execute("apk update")
            j.builders.tools.execute("apk upgrade")
        elif j.builders.tools.isCygwin:
            return  # no such functionality in apt-cyg
        else:
            raise j.exceptions.RuntimeError("could not upgrade, platform not supported")

    @builder_method()
    def install(self, packages):
        """
        """
        packages = j.core.text.getList(packages, "str")

        if len(packages) == 1:

            package = packages[0]

            self._log_info("package install :%s" % package)
            if j.core.platformtype.myplatform.platform_is_ubuntu:
                cmd = "%s install %s -y" % (CMD_APT_GET, package)

            elif j.builders.tools.platform_is_alpine:
                cmd = "apk add %s" % package

            elif j.builders.tools.platform_is_arch:
                if package.startswith("python3"):
                    package = "extra/python"

                # ignore
                for unsupported in ["libpython3.5-dev", "libffi-dev", "build-essential", "libpq-dev", "libsqlite3-dev"]:
                    if unsupported in package:
                        package = "devel"

                cmd = "pacman -S %s  --noconfirm\n" % package

            elif j.core.platformtype.myplatform.platform_is_osx:
                for unsupported in [
                    "libpython3.4-dev",
                    "python3.4-dev",
                    "libpython3.5-dev",
                    "python3.5-dev",
                    "libffi-dev",
                    "libssl-dev",
                    "make",
                    "build-essential",
                    "libpq-dev",
                    "libsqlite3-dev",
                ]:
                    if "libsnappy-dev" in package or "libsnappy1v5" in package:
                        package = "snappy"

                    if unsupported in package:
                        continue

                if "wget" == package:
                    package = "%s --enable-iri" % package

                cmd = "brew install %s || brew upgrade  %s\n" % (package, package)

            elif j.builders.tools.isCygwin:
                if package in ["run", "net-tools"]:
                    return

                installed = j.sal.process.execute("apt-cyg list&")[1].splitlines()
                if package in installed:
                    return  # means was installed

                cmd = "apt-cyg install %s\n" % package
            else:
                raise j.exceptions.RuntimeError("could not install:%s, platform not supported" % package)

            self._execute(cmd)
        else:
            for package in packages:
                self.install(package)

    @builder_method()
    def ensure(self, packages):
        return self.install(packages)

    @builder_method()
    def clean(self, packages=None, agressive=False):
        """
        clean packaging system e.g. remove outdated packages & caching packages
        @param agressive if True will delete full cache

        """
        packages = j.core.text.getList(packages, "str")

        if len(packages) == 1:

            package = packages[0]

            if j.core.platformtype.myplatform.platform_is_ubuntu:

                if package is not None:
                    return self._apt_get("-y --purge remove %s" % package)
                else:
                    j.sal.process.execute("apt-get autoremove -y")

                self._apt_get("autoclean")
                C = """
                apt-get clean
                rm -rf /bd_build
                rm -rf /var/tmp/*
                rm -f /etc/dpkg/dpkg.cfg.d/02apt-speedup

                find -regex '.*__pycache__.*' -delete
                rm -rf /var/log
                mkdir -p /var/log/apt
                rm -rf /var/tmp
                mkdir -p /var/tmp

                """
                j.sal.process.execute(C)

            # elif j.builders.tools.isArch:
            #     cmd = "pacman -Sc"
            #     if agressive:
            #         cmd += "c"
            #     j.sal.process.execute(cmd)
            #     if agressive:
            #         j.sal.process.execute("pacman -Qdttq", showout=False)

            elif j.core.platformtype.myplatform.platform_is_osx:
                if package:
                    j.sal.process.execute("brew cleanup %s" % package)
                    j.sal.process.execute("brew remove %s" % package)
                else:
                    j.sal.process.execute("brew cleanup")

            elif j.builders.tools.isCygwin:
                if package:
                    j.sal.process.execute("apt-cyg remove %s" % package)
                else:
                    pass

            else:
                raise j.exceptions.RuntimeError("could not package clean:%s, platform not supported" % package)

        else:
            for package in packages:
                self.clean(package, aggresive=agressive)

    @builder_method()
    def remove(self, package, autoclean=False):
        if j.core.platformtype.myplatform.platform_is_ubuntu:
            self._apt_get("remove " + package)
            if autoclean:
                self._apt_get("autoclean")
        elif j.core.platformtype.myplatform.platform_is_osx:
            j.sal.process.execute("brew remove %s 2>&1 > /dev/null|echo " "" % package)
