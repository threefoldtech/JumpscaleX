from Jumpscale import j

builder_method = j.builder.system.builder_method


class BuilderRestic(j.builder.system._BaseClass):

    NAME = "restic"

    def _init(self):
        self.DIR_BUILD = self._replace("{DIR_VAR}/build/restic")
        self.tools.dir_ensure(self.DIR_BUILD)

    @builder_method()
    def build(self):

        # install golang dependancy
        j.builder.runtimes.golang.install()

        # clone the repo
        C = """
        cd {}
        git clone --depth 1 https://github.com/restic/restic.git
        """.format(
            self.DIR_BUILD
        )
        self._execute(C, timeout=1200)

        # build binaries
        build_cmd = "cd {dir}/restic; go run build.go -k -v; make".format(dir=self.DIR_BUILD)
        self._execute(build_cmd, timeout=1000)

    @builder_method()
    def install(self):
        """
        download, install, move files to appropriate places, and create relavent configs
        """
        self._copy("{DIR_BUILD}/restic/restic", "{DIR_BIN}")

    @builder_method()
    def sandbox(self, zhub_client=None, flist_create=True, merge_base_flist=""):
        bin_dest = j.sal.fs.joinPaths(self.DIR_SANDBOX, "sandbox", "bin")
        self.tools.dir_ensure(bin_dest)
        self._copy("{DIR_BIN}/restic", bin_dest)

    @builder_method()
    def clean(self):
        self._remove(self.DIR_BUILD)

    @builder_method()
    def reset(self):
        super().reset()
        self.clean()

    @builder_method()
    def test(self):
        return_code, _, _ = self._execute("restic version")
        assert return_code == 0
        print("TEST OK")


# class ResticRepository:
#     '''This class represent a restic repository used for backup'''

#     def __init__(self, path, password, prefab, repo_env=None):
#         self.path = path
#         self.__password = password
#         self.repo_env = repo_env
#         self.prefab = prefab

#         if not self._exists():
#             self.initRepository()

#     def _exists(self):
#         rc, _, _ = self._run('{DIR_BIN}/restic snapshots > /dev/null', die=False)
#         if rc > 0:
#             return False
#         return True

#     def _run(self, cmd, env=None, die=True, showout=True):
#         env_vars = {
#             'RESTIC_REPOSITORY': self.path,
#             'RESTIC_PASSWORD': self.__password
#         }
#         if self.repo_env:
#             env_vars.update(self.repo_env)
#         if env:
#             env_vars.update(env)
#         return j.sal.process.execute(cmd=cmd, env=env_vars, die=die, showout=showout)

#     def initRepository(self):
#         '''
#         initialize the repository at self.path location
#         '''
#         cmd = '{DIR_BIN}/restic init'
#         self._run(cmd)

#     def snapshot(self, path, tag=None):
#         '''
#         @param path: directory/file to snapshot
#         @param tag: tag to add to the snapshot
#         '''
#         cmd = '{DIR_BIN}/restic backup {} '.format(path)
#         if tag:
#             cmd += ' --tag {}'.format(tag)
#         self._run(cmd)

#     def restore_snapshot(self, snapshot_id, dest):
#         '''
#         @param snapshot_id: id of the snapshot to restore
#         @param dest: path where to restore the snapshot to
#         '''
#         cmd = '{DIR_BIN}/restic restore --target {dest} {id} '.format(dest=dest, id=snapshot_id)
#         self._run(cmd)

#     def list_snapshots(self):
#         '''
#         @return: list of dict representing a snapshot
#         { 'date': '2017-01-17 16:15:28',
#           'directory': '/optvar/cfg',
#           'host': 'myhost',
#           'id': 'ec853b5d',
#           'tags': 'backup1'
#         }
#         '''
#         cmd = '{DIR_BIN}/restic snapshots'
#         _, out, _ = self._run(cmd, showout=False)

#         snapshots = []
#         for line in out.splitlines()[2:-2]:
#             ss = list(self._chunk(line))

#             snapshot = {
#                 'id': ss[0],
#                 'date': ' '.join(ss[1:3]),
#                 'host': ss[3]
#             }
#             if len(ss) == 6:
#                 snapshot['tags'] = ss[4]
#                 snapshot['directory'] = ss[5]
#             else:
#                 snapshot['tags'] = ''
#                 snapshot['directory'] = ss[4]
#             snapshots.append(snapshot)

#         return snapshots

#     def check_repo_integrity(self):
#         '''
#         @return: True if integrity is ok else False
#         '''
#         cmd = '{DIR_BIN}/restic check'
#         rc, _, _ = self._run(cmd)
#         if rc != 0:
#             return False
#         return True

#     def _chunk(self, line):
#         '''
#         passe line and yield each word separated by space
#         '''
#         word = ''
#         for c in line:
#             if c == ' ':
#                 if word:
#                     yield word
#                     word = ''
#                 continue
#             else:
#                 word += c
#         if word:
#             yield word
