from Jumpscale import j


class BuilderMonitoringFactory(j.builders.system._BaseFactoryClass):

    __jslocation__ = "j.builders.monitoring"

    def _init(self):

        self._smartmon = None
        self._grafana = None

    @property
    def smartmon(self):
        if self._smartmon is None:
            from .BuilderSmartmontools import BuilderSmartmontools

            self._smartmon = BuilderSmartmontools()
        return self._smartmon

    @property
    def grafana(self):
        if self._grafana is None:
            from .BuilderGrafanaFactory import BuilderGrafanaFactory

            self._grafana = BuilderGrafanaFactory()
        return self._grafana
