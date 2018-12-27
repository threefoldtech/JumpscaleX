from Jumpscale import j
from .TLS import TLS

JSBASE = j.application.JSBaseClass


class TLSFactory(j.application.JSBaseClass):
    """Factory class to deal with TLS, key and certificate generation"""

    def __init__(self):
        self.__jslocation__ = "j.sal.tls"
        JSBASE.__init__(self)

    def get(self, path=None):
        """Get an instance of the TLS class
            This module use the cfssl AYS.

        :param path: Path is the working directory where the certificate and key will be generated, defaults to None
        :type path: string, optional
        :return: TLS instance
        :rtype: TLS class
        """
        return TLS(path=path)
