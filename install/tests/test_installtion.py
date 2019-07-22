import os.path
from .base_test import BaseTest

class Test_instaltion(BaseTest):
    def setUp(self):
        pass

    @classmethod
    def tearDownClass(cls):
        self = cls()
        self.info("Delete jumpscale created container.")
        if not self.check_js_installtion():
            pass
        command = "/tmp/jsx container_delete"
        output, error = self.linux_os(command)
        command = "docker ps -a | grep {}".format(self.js_container)
        output, error = self.linux_os(command)
        self.assertFalse(output)

    def test01_install_jumpscale_on_linux_inside_docker(self):
        """
        test TCR337
        *Test libs builers sandbox*
        #. Install jumpscale from specific branch
        #. Run container_kosmos ,should succeed
        """

        self.info("Install jumpscale from {} branch".format(self.js_branch))
        output, error = self.jumpscale_installtion()
        self.assertIn("install succesfull", output)

        self.info(" Run container_kosmos ,should succeed")
        command = "/tmp/jsx container_kosmos"
        output, error = self.linux_os(command)
        self.assertIn("BCDB INIT DONE", output)
        self.assertFalse(error)

    def Test02_container_stop_and_container_start_options_Linux_os(self):
        """
        test TCR338
        #. Check that js container exist ,should succeed.
        #. Run container stop.
        #. Check that container stopped successfully.
        #. Run container started.
        #. Check that container started successfully

        """
        self.info(" Check that js container exist ,should succeed")
        self.assertTrue(self.check_js_installtion())

        self.info("Run container stop ")
        command = "/tmp/jsx container_stop"
        output, error = self.linux_os(command)

        self.info("Check that container stopped successfully")
        command = "docker ps -a -f status=running  | grep {}".format(self.js_container)
        output, error = self.linux_os(command)
        self.assertFalse(output)

        self.info("Run container started ")
        command = "/tmp/jsx container_start"
        output, error = self.linux_os(command)

        self.info("Check that container started successfully")
        command = "docker ps -a -f status=running  | grep {}".format(self.js_container)
        output, error = self.linux_os(command)
        self.assertIn(self.js_container, output.decode())

    def Test03_jumpscale_installtion_inside_jumpscale_docker_Linux_os(self):
        """
        test TCR339
        #. Run kosmos command inside docker, should start kosmos shell .
        #. Run js_init generate command inside docker, sshould run successfully.
        #. Check the branch of jumpscale code, should be same as installtion branch.
        """

        self.info(" Check that js container exist ,should succeed")
        self.assertTrue(self.check_js_installtion())

        self.info("Run kosmos command inside docker,should start kosmos shell")
        command = "docker exec -i {} /bin/bash -c 'source /sandbox/env.sh && kosmos'".format(self.js_container)
        output, error = self.linux_os(command)
        self.assertIn("BCDB INIT DONE", output)
        self.info("Run js_init generate ")
        command = "docker exec -i {} /bin/bash -c 'source /sandbox/env.sh && js_init generate'".format(
            self.js_container
        )
        output, error = self.linux_os(command)
        self.assertIn("process", output.decode())
        self.assertFalse(error)

        self.info(" Check the branch of jumpscale code, should be same as installtion branch.")
        command = "docker exec -i {} /bin/bash -c 'cd /sandbox/code/github/threefoldtech/jumpscaleX && cat .git/HEAD'".format(
            self.js_container
        )
        output, error = self.linux_os(command)
        branch = output.decode()[output.decode().find("head") + 6 : -2]
        self.assertEqual(branch, self.js_branch)

    def Test04_loaded_ssh_key_inside_jumpscale_docker_linux_os(self):
        """
        test TCR340
        #. check  that ssh-key loaded in docker  successfully.
        """
        self.info(" Check that js container exist ,should succeed")
        self.assertTrue(self.check_js_installtion())

        self.info("check  that ssh-key loaded in docker  successfully")
        command = "docker exec -i {} /bin/bash -c 'cat /root/.ssh/authorized_keys'".format(self.js_container)
        output, error = self.linux_os(command)
        self.assertEqual(output.decode().strip("\n"), self.ssh_key)


class Test_instaltion_insystem(BaseTest):
    @classmethod
    def setUpClass(cls):
        """
        Setup
        *clean old installation*
        #. remove sandbox /tmp/jsx, /tmp/jumpscale/, /tmp/InstallTools.py
        #. install click python package
        """
        self = cls()
        self.info("Clean old installation")
        command = "rm -rf ~/sandbox/ /tmp/jsx /tmp/jumpscale/ /tmp/InstallTools.py"
        output, error = self.linux_os(command)
        os.path.isfile("/tmp/jsx")

        self.info("install click python package")
        command = "pip3 install click"
        output, error = self.linux_os(command)
        self.assertIn("Successfully installed", output.decode())

    @classmethod
    def tearDownClass(cls):
        pass 

    def test01_install_jumpscale_insystem_no_interactive(self):
        """
        test TC63
        *Test installation of Jumpscale*
        #. Install jumpscale from specific branch
        #. Run kosmos ,should succeed
        """

        self.info("Install jumpscale from {} branch on {}".format(self.js_branch, self.os_type))
        output, error = self.jumpscale_installtion()
        self.assertIn("install succesfull", output)

        self.info(" Run kosmos shell,should succeed")
        command = " . /sandbox/env.sh; kosmos"
        output, error = self.linux_os(command)
        self.assertIn("BCDB INIT DONE", output)
        self.assertFalse(error)


