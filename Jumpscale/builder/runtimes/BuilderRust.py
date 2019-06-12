from Jumpscale import j

builder_method = j.builders.system.builder_method


class BuilderRust(j.builders.system._BaseClass):
    NAME = "rust"
    DOWNLOAD_URL = "https://sh.rustup.rs"

    def _init(self):
        self.DIR_BUILD = "/root/.cargo/bin"

    @builder_method()
    def build(self):
        self.profile_sandbox_select()

        # Will download and run the correct version of rustup-init executable for your platform
        self._execute("curl {} -sSf | sh -s -- -y".format(self.DOWNLOAD_URL))

        self.profile.env_set_part("PATH", self.DIR_BUILD)

    @builder_method()
    def install(self):
        self.profile_sandbox_select()
        self.profile.env_set_part("PATH", self.DIR_BUILD)
        self._copy(self.DIR_BUILD, "{DIR_BIN}")

    @builder_method()
    def sandbox(self, reset=False, zhub_client=None, flist_create=False):
        """
        kosmos 'j.builders.runtimes.rust.sandbox()'
        :return:
        """
        dest_path = self.DIR_SANDBOX
        dir_dest = j.sal.fs.joinPaths(dest_path, "sandbox")
        self.tools.dir_ensure(dir_dest)

        bins = [
            "cargo",
            "cargo-clippy",
            "cargo-fmt",
            "_moon.lua",
            "cargo-miri",
            "clippy-driver",
            "rls",
            "rustc",
            "rustdoc",
            "rustfmt",
            "rust-gdb",
            "rust-lldb",
            "rustup",
        ]
        for bin_name in bins:
            dir_src = self.tools.joinpaths(self.DIR_BUILD, bin_name)
            self._copy(dir_src, dir_dest)

    @builder_method()
    def test(self):
        self.install()

        rc, _, _ = self._execute("rustc --V")
        if rc:
            print("TEST Failed")
            return
        print("TEST DONE")
