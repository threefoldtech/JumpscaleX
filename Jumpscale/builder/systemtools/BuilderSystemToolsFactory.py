from Jumpscale import j
from .BuildersRsync import BuilderRsync
from .BuildersTFMUX import BuildersTFMUX


class BuilderSystemToolsFactory(j.builders.system._BaseFactoryClass):

    __jslocation__ = "j.builders.systemtools"

    def _init(self):
        self.rsync = BuilderRsync()
        self.tfmux = BuildersTFMUX()
