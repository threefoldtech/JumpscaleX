from Jumpscale import j

builder_method = j.builder.system.builder_method


class BuilderPostgresql(j.builder.system._BaseClass):
    NAME = "psql"

    def _init(self):
        self.DOWNLOAD_DIR = self.tools.joinpaths(self.DIR_BUILD, "build")
        self.DATA_DIR = self._replace("{DIR_BASE}/apps/psql/data")

    @builder_method()
    def build(self):
        postgres_url = "https://ftp.postgresql.org/pub/source/v9.6.13/postgresql-9.6.13.tar.gz"
        j.builder.tools.file_download(postgres_url, to=self.DOWNLOAD_DIR, overwrite=False, expand=True)
        j.builder.system.package.ensure(["build-essential", "zlib1g-dev", "libreadline-dev"])

        cmd = self._replace(
            """
            cd {DOWNLOAD_DIR}/postgresql-9.6.13
            ./configure --prefix={DIR_BASE}
            make
        """
        )
        self._execute(cmd)

    def _group_exists(self, groupname):
        return groupname in self._read("/etc/group")

    @builder_method()
    def install(self, port=5432):
        cmd = self._replace(
            """
            cd {DOWNLOAD_DIR}/postgresql-9.6.13
            make install
        """
        )
        self._execute(cmd)

        if not self._group_exists("postgres"):
            self._execute(
                'adduser --system --quiet --home {DIR_BASE} --no-create-home \
        --shell /bin/bash --group --gecos "PostgreSQL administrator" postgres'
            )

        self._remove(self.DATA_DIR)

        c = self._replace(
            """
            cd {DIR_BASE}
            mkdir -p log
            mkdir -p {DATA_DIR}
            chown -R postgres {DATA_DIR}
            sudo -u postgres {DIR_BIN}/initdb -D {DATA_DIR} -E utf8 --locale=en_US.UTF-8
        """
        )

        self._execute(c)

    @property
    def startup_cmds(self):
        cmd = j.tools.startupcmd.get(
            "postgres", self._replace("sudo -u postgres {DIR_BIN}/postgres -D {DATA_DIR}"), path="/sandbox/bin"
        )
        return [cmd]
