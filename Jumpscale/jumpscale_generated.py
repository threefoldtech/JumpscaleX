
# from Jumpscale.core.JSBase import JSBase
import os
import sys
from Jumpscale import j


if "/sandbox/lib/jumpscale" not in sys.path:
    sys.path.append("/sandbox/lib/jumpscale")

class JSGroup():
    pass



class group_kosmos(JSGroup):
    def __init__(self):
        
        self._zos = None

    
    @property
    def zos(self):
        if self._zos is None:
            from DigitalMe.kosmos.zos.ZOSFactory import ZOSCmdFactory
            self._zos =  ZOSCmdFactory()
        return self._zos

j.kosmos = group_kosmos()
j.core._groups["kosmos"] = j.kosmos


class group_world(JSGroup):
    def __init__(self):
        
        self._system = None
        self._hypervisor = None

    
    @property
    def system(self):
        if self._system is None:
            from DigitalMe.tools.kosmos.WorldSystem import WorldSystem
            self._system =  WorldSystem()
        return self._system
    @property
    def hypervisor(self):
        if self._hypervisor is None:
            from DigitalMe.tools.kosmos.world_example.HyperVisorCoordinator.CoordinatorHypervisor import CoordinatorHypervisor
            self._hypervisor =  CoordinatorHypervisor()
        return self._hypervisor

j.world = group_world()
j.core._groups["world"] = j.world


class group_tools(JSGroup):
    def __init__(self):
        
        self._kosmos = None
        self._open_publish = None
        self._tfbot = None
        self._threefold_directory = None
        self._threefoldgrid = None
        self._objectinspector = None
        self._fixer = None
        self._jinja2 = None
        self._logger = None
        self._dash = None
        self._tmux = None
        self._startupcmd = None
        self._expect = None
        self._cython = None
        self._markdowndocs = None
        self._performancetrace = None
        self._formatters = None
        self._aggregator = None
        self._realityprocess = None
        self._code = None
        self._codeloader = None
        self._code = None
        self._notapplicableyet = None
        self._sandboxer = None
        self._reportlab = None
        self._timer = None
        self._capacity = None
        self._storybot = None
        self._imagelib = None
        self._typechecker = None
        self._path = None
        self._dnstools = None
        self._memusagetest = None
        self._offliner = None
        self._rexplorer = None
        self._googleslides = None
        self._console = None
        self._legal_contracts = None
        self._executorLocal = None
        self._executor = None
        self._team_manager = None
        self._syncer = None
        self._bash = None
        self._tarfile = None
        self._issuemanager = None
        self._numtools = None
        self._zipfile = None
        self._email = None
        self._flist = None

    
    @property
    def kosmos(self):
        if self._kosmos is None:
            from DigitalMe.tools.kosmos.kosmos_OLD.Kosmos import Kosmos
            self._kosmos =  Kosmos()
        return self._kosmos
    @property
    def open_publish(self):
        if self._open_publish is None:
            from DigitalMe.tools.openpublish.OpenPublishFactory import OpenPublishFactory
            self._open_publish =  OpenPublishFactory()
        return self._open_publish
    @property
    def tfbot(self):
        if self._tfbot is None:
            from DigitalMe.tools.tfbot.TFBotFactory import TFBotFactory
            self._tfbot =  TFBotFactory()
        return self._tfbot
    @property
    def threefold_directory(self):
        if self._threefold_directory is None:
            from DigitalMe.tools.threefolddirectory.ThreeFoldDirectory import ThreeFoldDirectory
            self._threefold_directory =  ThreeFoldDirectory()
        return self._threefold_directory
    @property
    def threefoldgrid(self):
        if self._threefoldgrid is None:
            from DigitalMe.tools.threefolddirectory._archive.FarmerFactory import FarmerFactory
            self._threefoldgrid =  FarmerFactory()
        return self._threefoldgrid
    @property
    def objectinspector(self):
        if self._objectinspector is None:
            from Jumpscale.tools.objectinspector.ObjectInspector import ObjectInspector
            self._objectinspector =  ObjectInspector()
        return self._objectinspector
    @property
    def fixer(self):
        if self._fixer is None:
            from Jumpscale.tools.fixer.Fixer import Fixer
            self._fixer =  Fixer()
        return self._fixer
    @property
    def jinja2(self):
        if self._jinja2 is None:
            from Jumpscale.tools.jinja2.Jinja2 import Jinja2
            self._jinja2 =  Jinja2()
        return self._jinja2
    @property
    def logger(self):
        if self._logger is None:
            from Jumpscale.tools.logger.LoggerFactory import LoggerFactory
            self._logger =  LoggerFactory()
        return self._logger
    @property
    def dash(self):
        if self._dash is None:
            from Jumpscale.tools.dash.DASH import DASH
            self._dash =  DASH()
        return self._dash
    @property
    def tmux(self):
        if self._tmux is None:
            from Jumpscale.tools.tmux.Tmux import Tmux
            self._tmux =  Tmux()
        return self._tmux
    @property
    def startupcmd(self):
        if self._startupcmd is None:
            from Jumpscale.tools.startupcmd.StartupCMDFactory import StartupCMDFactory
            self._startupcmd =  StartupCMDFactory()
        return self._startupcmd
    @property
    def expect(self):
        if self._expect is None:
            from Jumpscale.tools.expect.Expect import ExpectTool
            self._expect =  ExpectTool()
        return self._expect
    @property
    def cython(self):
        if self._cython is None:
            from Jumpscale.tools.cython.CythonFactory import CythonFactory
            self._cython =  CythonFactory()
        return self._cython
    @property
    def markdowndocs(self):
        if self._markdowndocs is None:
            from Jumpscale.tools.markdowndocs.MarkDownDocs import MarkDownDocs
            self._markdowndocs =  MarkDownDocs()
        return self._markdowndocs
    @property
    def performancetrace(self):
        if self._performancetrace is None:
            from Jumpscale.tools.performancetrace.PerformanceTrace import PerformanceTraceFactory
            self._performancetrace =  PerformanceTraceFactory()
        return self._performancetrace
    @property
    def formatters(self):
        if self._formatters is None:
            from Jumpscale.tools.formatters.FormattersFactory import FormattersFactory
            self._formatters =  FormattersFactory()
        return self._formatters
    @property
    def aggregator(self):
        if self._aggregator is None:
            from Jumpscale.tools.aggregator.Aggregator import Aggregator
            self._aggregator =  Aggregator()
        return self._aggregator
    @property
    def realityprocess(self):
        if self._realityprocess is None:
            from Jumpscale.tools.aggregator.RealityProcess import RealitProcess
            self._realityprocess =  RealitProcess()
        return self._realityprocess
    @property
    def code(self):
        if self._code is None:
            from Jumpscale.tools.codetools.CodeTools import CodeTools
            self._code =  CodeTools()
        return self._code
    @property
    def codeloader(self):
        if self._codeloader is None:
            from Jumpscale.tools.codeloader.CodeLoader import CodeLoader
            self._codeloader =  CodeLoader()
        return self._codeloader
    @property
    def code(self):
        if self._code is None:
            from Jumpscale.tools.codeloader.CodeTools import CodeTools
            self._code =  CodeTools()
        return self._code
    @property
    def notapplicableyet(self):
        if self._notapplicableyet is None:
            from Jumpscale.tools.builder.Builder import Builder
            self._notapplicableyet =  Builder()
        return self._notapplicableyet
    @property
    def sandboxer(self):
        if self._sandboxer is None:
            from Jumpscale.tools.sandboxer.Sandboxer import Sandboxer
            self._sandboxer =  Sandboxer()
        return self._sandboxer
    @property
    def reportlab(self):
        if self._reportlab is None:
            from Jumpscale.tools.reportlab.ReportlabFactory import ReportlabFactory
            self._reportlab =  ReportlabFactory()
        return self._reportlab
    @property
    def timer(self):
        if self._timer is None:
            from Jumpscale.tools.timer.Timer import TIMER
            self._timer =  TIMER()
        return self._timer
    @property
    def capacity(self):
        if self._capacity is None:
            from Jumpscale.tools.capacity.Factory import Factory
            self._capacity =  Factory()
        return self._capacity
    @property
    def storybot(self):
        if self._storybot is None:
            from Jumpscale.tools.storybot.StoryBotFactory import StoryBotFactory
            self._storybot =  StoryBotFactory()
        return self._storybot
    @property
    def imagelib(self):
        if self._imagelib is None:
            from Jumpscale.tools.imagelib.ImageLib import ImageLib
            self._imagelib =  ImageLib()
        return self._imagelib
    @property
    def typechecker(self):
        if self._typechecker is None:
            from Jumpscale.tools.typechecker.TypeChecker import TypeCheckerFactory
            self._typechecker =  TypeCheckerFactory()
        return self._typechecker
    @property
    def path(self):
        if self._path is None:
            from Jumpscale.tools.path.PathFactory import PathFactory
            self._path =  PathFactory()
        return self._path
    @property
    def dnstools(self):
        if self._dnstools is None:
            from Jumpscale.tools.dnstools.DNSTools import DNSTools
            self._dnstools =  DNSTools()
        return self._dnstools
    @property
    def memusagetest(self):
        if self._memusagetest is None:
            from Jumpscale.tools.memusagetest.MemUsageTest import MemUsageTest
            self._memusagetest =  MemUsageTest()
        return self._memusagetest
    @property
    def offliner(self):
        if self._offliner is None:
            from Jumpscale.tools.offliner.Offliner import Offliner
            self._offliner =  Offliner()
        return self._offliner
    @property
    def rexplorer(self):
        if self._rexplorer is None:
            from Jumpscale.tools.offliner.Rexplorer import Rexplorer
            self._rexplorer =  Rexplorer()
        return self._rexplorer
    @property
    def googleslides(self):
        if self._googleslides is None:
            from Jumpscale.tools.googleslides.GoogleSlides import GoogleSlides
            self._googleslides =  GoogleSlides()
        return self._googleslides
    @property
    def console(self):
        if self._console is None:
            from Jumpscale.tools.console.Console import Console
            self._console =  Console()
        return self._console
    @property
    def legal_contracts(self):
        if self._legal_contracts is None:
            from Jumpscale.tools.legal_contracts.LegalContractsFactory import LegalContractsFactory
            self._legal_contracts =  LegalContractsFactory()
        return self._legal_contracts
    @property
    def executorLocal(self):
        if self._executorLocal is None:
            from Jumpscale.tools.executor.ExecutorLocal import ExecutorLocal
            self._executorLocal =  ExecutorLocal()
        return self._executorLocal
    @property
    def executor(self):
        if self._executor is None:
            from Jumpscale.tools.executor.ExecutorFactory import ExecutorFactory
            self._executor =  ExecutorFactory()
        return self._executor
    @property
    def team_manager(self):
        if self._team_manager is None:
            from Jumpscale.tools.teammgr.Teammgr import Teammgr
            self._team_manager =  Teammgr()
        return self._team_manager
    @property
    def syncer(self):
        if self._syncer is None:
            from Jumpscale.tools.syncer.SyncerFactory import SyncerFactory
            self._syncer =  SyncerFactory()
        return self._syncer
    @property
    def bash(self):
        if self._bash is None:
            from Jumpscale.sal.bash.BashFactory import BashFactory
            self._bash =  BashFactory()
        return self._bash
    @property
    def tarfile(self):
        if self._tarfile is None:
            from Jumpscale.data.tarfile.TarFile import TarFileFactory
            self._tarfile =  TarFileFactory()
        return self._tarfile
    @property
    def issuemanager(self):
        if self._issuemanager is None:
            from Jumpscale.data.issuemanager.IssueManager import IssueManager
            self._issuemanager =  IssueManager()
        return self._issuemanager
    @property
    def numtools(self):
        if self._numtools is None:
            from Jumpscale.data.numtools.NumTools import NumTools
            self._numtools =  NumTools()
        return self._numtools
    @property
    def zipfile(self):
        if self._zipfile is None:
            from Jumpscale.data.zip.ZipFile import ZipFileFactory
            self._zipfile =  ZipFileFactory()
        return self._zipfile
    @property
    def email(self):
        if self._email is None:
            from Jumpscale.data.email.Email import EmailTool
            self._email =  EmailTool()
        return self._email
    @property
    def flist(self):
        if self._flist is None:
            from Jumpscale.data.flist.FListFactory import FListFactory
            self._flist =  FListFactory()
        return self._flist

j.tools = group_tools()
j.core._groups["tools"] = j.tools


class group_data(JSGroup):
    def __init__(self):
        
        self._nltk = None
        self._serializers = None
        self._capnp = None
        self._inifile = None
        self._bcdb = None
        self._idgenerator = None
        self._indexfile = None
        self._worksheets = None
        self._docs = None
        self._latex = None
        self._regex = None
        self._schema = None
        self._hash = None
        self._randomnames = None
        self._cachelru = None
        self._rivine = None
        self._html = None
        self._markdown = None
        self._nacl = None
        self._encryption = None
        self._treemanager = None
        self._dict_editor = None
        self._types = None
        self._time = None
        self._timeinterval = None

    
    @property
    def nltk(self):
        if self._nltk is None:
            from DigitalMe.data.nltk.NLTK import NLTKFactory
            self._nltk =  NLTKFactory()
        return self._nltk
    @property
    def serializers(self):
        if self._serializers is None:
            from Jumpscale.data.serializers.SerializersFactory import SerializersFactory
            self._serializers =  SerializersFactory()
        return self._serializers
    @property
    def capnp(self):
        if self._capnp is None:
            from Jumpscale.data.capnp.Capnp import Capnp
            self._capnp =  Capnp()
        return self._capnp
    @property
    def inifile(self):
        if self._inifile is None:
            from Jumpscale.data.inifile.IniFile import InifileTool
            self._inifile =  InifileTool()
        return self._inifile
    @property
    def bcdb(self):
        if self._bcdb is None:
            from Jumpscale.data.bcdb.BCDBFactory import BCDBFactory
            self._bcdb =  BCDBFactory()
        return self._bcdb
    @property
    def idgenerator(self):
        if self._idgenerator is None:
            from Jumpscale.data.idgenerator.IDGenerator import IDGenerator
            self._idgenerator =  IDGenerator()
        return self._idgenerator
    @property
    def indexfile(self):
        if self._indexfile is None:
            from Jumpscale.data.indexFile.IndexFiles import IndexDB
            self._indexfile =  IndexDB()
        return self._indexfile
    @property
    def worksheets(self):
        if self._worksheets is None:
            from Jumpscale.data.worksheets.Sheets import Sheets
            self._worksheets =  Sheets()
        return self._worksheets
    @property
    def docs(self):
        if self._docs is None:
            from Jumpscale.data.docs.DocsFactory import DocsFactory
            self._docs =  DocsFactory()
        return self._docs
    @property
    def latex(self):
        if self._latex is None:
            from Jumpscale.data.latex.Latex import Latex
            self._latex =  Latex()
        return self._latex
    @property
    def regex(self):
        if self._regex is None:
            from Jumpscale.data.regex.RegexTools import RegexTools
            self._regex =  RegexTools()
        return self._regex
    @property
    def schema(self):
        if self._schema is None:
            from Jumpscale.data.schema.SchemaFactory import SchemaFactory
            self._schema =  SchemaFactory()
        return self._schema
    @property
    def hash(self):
        if self._hash is None:
            from Jumpscale.data.hash.HashTool import HashTool
            self._hash =  HashTool()
        return self._hash
    @property
    def randomnames(self):
        if self._randomnames is None:
            from Jumpscale.data.random_names.RandomNames import RandomNames
            self._randomnames =  RandomNames()
        return self._randomnames
    @property
    def cachelru(self):
        if self._cachelru is None:
            from Jumpscale.data.cachelru.LRUCacheFactory import LRUCacheFactory
            self._cachelru =  LRUCacheFactory()
        return self._cachelru
    @property
    def rivine(self):
        if self._rivine is None:
            from Jumpscale.data.rivine.RivineDataFactory import RivineDataFactory
            self._rivine =  RivineDataFactory()
        return self._rivine
    @property
    def html(self):
        if self._html is None:
            from Jumpscale.data.html.HTMLFactory import HTMLFactory
            self._html =  HTMLFactory()
        return self._html
    @property
    def markdown(self):
        if self._markdown is None:
            from Jumpscale.data.markdown.MarkdownFactory import MarkdownFactory
            self._markdown =  MarkdownFactory()
        return self._markdown
    @property
    def nacl(self):
        if self._nacl is None:
            from Jumpscale.data.nacl.NACLFactory import NACLFactory
            self._nacl =  NACLFactory()
        return self._nacl
    @property
    def encryption(self):
        if self._encryption is None:
            from Jumpscale.data.encryption.EncryptionFactory import EncryptionFactory
            self._encryption =  EncryptionFactory()
        return self._encryption
    @property
    def treemanager(self):
        if self._treemanager is None:
            from Jumpscale.data.treemanager.Treemanager import TreemanagerFactory
            self._treemanager =  TreemanagerFactory()
        return self._treemanager
    @property
    def dict_editor(self):
        if self._dict_editor is None:
            from Jumpscale.data.dicteditor.DictEditor import DictEditorFactory
            self._dict_editor =  DictEditorFactory()
        return self._dict_editor
    @property
    def types(self):
        if self._types is None:
            from Jumpscale.data.types.Types import Types
            self._types =  Types()
        return self._types
    @property
    def time(self):
        if self._time is None:
            from Jumpscale.data.time.Time import Time_
            self._time =  Time_()
        return self._time
    @property
    def timeinterval(self):
        if self._timeinterval is None:
            from Jumpscale.data.time.TimeInterval import TimeInterval
            self._timeinterval =  TimeInterval()
        return self._timeinterval

j.data = group_data()
j.core._groups["data"] = j.data


class group_clients(JSGroup):
    def __init__(self):
        
        self._gedis_backend = None
        self._multicast = None
        self._gedis = None
        self._git = None
        self._traefik = None
        self._zdb = None
        self._gitea = None
        self._oauth = None
        self.__template = None
        self._redis_config = None
        self._itsyouonline = None
        self._tfmux = None
        self._logger = None
        self._threefold_directory = None
        self._btc_alpha = None
        self._credis_core = None
        self._redis = None
        self._zboot = None
        self._google_compute = None
        self._ipmi = None
        self._racktivity = None
        self._http = None
        self._ovh = None
        self._zhub = None
        self._tarantool = None
        self._openvcloud = None
        self._portal = None
        self._zerotier = None
        self._etcd = None
        self._sonic = None
        self._mysql = None
        self._mongodb = None
        self._mongoengine = None
        self._packetnet = None
        self._kraken = None
        self._zos = None
        self._ssh = None
        self._email = None
        self._sendgrid = None
        self._kubernetes = None
        self._telegram_bot = None
        self._s3 = None
        self._sshkey = None
        self._freeflowpages = None
        self._currencylayer = None
        self._gdrive = None
        self._peewee = None
        self._influxdb = None
        self._intercom = None
        self._github = None
        self._sendgrid = None
        self._syncthing = None
        self._grafana = None
        self._tfchain = None
        self._btc_electrum = None
        self._zhubdirect = None
        self._rogerthat = None
        self._sqlalchemy = None
        self._trello = None
        self._coredns = None
        self._graphite = None
        self._postgres = None
        self._sshagent = None
        self._zerostor = None
        self._zstor = None
        self._virtualbox = None
        self._webgateway = None

    
    @property
    def gedis_backend(self):
        if self._gedis_backend is None:
            from DigitalMe.clients.gedis_backends.GedisBackendClientFactory import GedisBackendClientFactory
            self._gedis_backend =  GedisBackendClientFactory()
        return self._gedis_backend
    @property
    def multicast(self):
        if self._multicast is None:
            from DigitalMe.clients.multicast.MulticastFactory import MulticastFactory
            self._multicast =  MulticastFactory()
        return self._multicast
    @property
    def gedis(self):
        if self._gedis is None:
            from DigitalMe.clients.gedis.GedisClientFactory import GedisClientFactory
            self._gedis =  GedisClientFactory()
        return self._gedis
    @property
    def git(self):
        if self._git is None:
            from Jumpscale.clients.git.GitFactory import GitFactory
            self._git =  GitFactory()
        return self._git
    @property
    def traefik(self):
        if self._traefik is None:
            from Jumpscale.clients.traefik.TraefikFactory import TraefikFactory
            self._traefik =  TraefikFactory()
        return self._traefik
    @property
    def zdb(self):
        if self._zdb is None:
            from Jumpscale.clients.zdb.ZDBFactory import ZDBFactory
            self._zdb =  ZDBFactory()
        return self._zdb
    @property
    def gitea(self):
        if self._gitea is None:
            from Jumpscale.clients.gitea.GiteaFactory import GiteaFactory
            self._gitea =  GiteaFactory()
        return self._gitea
    @property
    def oauth(self):
        if self._oauth is None:
            from Jumpscale.clients.oauth.OauthFactory import OauthFactory
            self._oauth =  OauthFactory()
        return self._oauth
    @property
    def _template(self):
        if self.__template is None:
            from Jumpscale.clients.TEMPLATE.TemplateGrafanaFactory import GrafanaFactory
            self.__template =  GrafanaFactory()
        return self.__template
    @property
    def redis_config(self):
        if self._redis_config is None:
            from Jumpscale.clients.redisconfig.RedisConfigFactory import RedisConfigFactory
            self._redis_config =  RedisConfigFactory()
        return self._redis_config
    @property
    def itsyouonline(self):
        if self._itsyouonline is None:
            from Jumpscale.clients.itsyouonline.IYOFactory import IYOFactory
            self._itsyouonline =  IYOFactory()
        return self._itsyouonline
    @property
    def tfmux(self):
        if self._tfmux is None:
            from Jumpscale.clients.tfmux.TFMuxFactory import TFMuxClientFactory
            self._tfmux =  TFMuxClientFactory()
        return self._tfmux
    @property
    def logger(self):
        if self._logger is None:
            from Jumpscale.clients.logger.LoggerFactory import LoggerFactory
            self._logger =  LoggerFactory()
        return self._logger
    @property
    def threefold_directory(self):
        if self._threefold_directory is None:
            from Jumpscale.clients.threefold_directory.GridCapacityFactory import GridCapacityFactory
            self._threefold_directory =  GridCapacityFactory()
        return self._threefold_directory
    @property
    def btc_alpha(self):
        if self._btc_alpha is None:
            from Jumpscale.clients.btc_alpha.BTCFactory import GitHubFactory
            self._btc_alpha =  GitHubFactory()
        return self._btc_alpha
    @property
    def credis_core(self):
        if self._credis_core is None:
            from Jumpscale.clients.redis.RedisCoreClient import RedisCoreClient_old
            self._credis_core =  RedisCoreClient_old()
        return self._credis_core
    @property
    def redis(self):
        if self._redis is None:
            from Jumpscale.clients.redis.RedisFactory import RedisFactory
            self._redis =  RedisFactory()
        return self._redis
    @property
    def zboot(self):
        if self._zboot is None:
            from Jumpscale.clients.zero_boot.ZerobootFactory import ZerobootFactory
            self._zboot =  ZerobootFactory()
        return self._zboot
    @property
    def google_compute(self):
        if self._google_compute is None:
            from Jumpscale.clients.google_compute.GoogleComputeFactory import GoogleComputeFactory
            self._google_compute =  GoogleComputeFactory()
        return self._google_compute
    @property
    def ipmi(self):
        if self._ipmi is None:
            from Jumpscale.clients.ipmi.IpmiFactory import IpmiFactory
            self._ipmi =  IpmiFactory()
        return self._ipmi
    @property
    def racktivity(self):
        if self._racktivity is None:
            from Jumpscale.clients.racktivity.RacktivityFactory import RacktivityFactory
            self._racktivity =  RacktivityFactory()
        return self._racktivity
    @property
    def http(self):
        if self._http is None:
            from Jumpscale.clients.http.HttpClient import HttpClient
            self._http =  HttpClient()
        return self._http
    @property
    def ovh(self):
        if self._ovh is None:
            from Jumpscale.clients.ovh.OVHFactory import OVHFactory
            self._ovh =  OVHFactory()
        return self._ovh
    @property
    def zhub(self):
        if self._zhub is None:
            from Jumpscale.clients.zero_hub.ZeroHubFactory import ZeroHubFactory
            self._zhub =  ZeroHubFactory()
        return self._zhub
    @property
    def tarantool(self):
        if self._tarantool is None:
            from Jumpscale.clients.tarantool.TarantoolFactory import TarantoolFactory
            self._tarantool =  TarantoolFactory()
        return self._tarantool
    @property
    def openvcloud(self):
        if self._openvcloud is None:
            from Jumpscale.clients.openvcloud.OVCFactory import OVCClientFactory
            self._openvcloud =  OVCClientFactory()
        return self._openvcloud
    @property
    def portal(self):
        if self._portal is None:
            from Jumpscale.clients.portal.PortalClientFactory import PortalClientFactory
            self._portal =  PortalClientFactory()
        return self._portal
    @property
    def zerotier(self):
        if self._zerotier is None:
            from Jumpscale.clients.zerotier.ZerotierFactory import ZerotierFactory
            self._zerotier =  ZerotierFactory()
        return self._zerotier
    @property
    def etcd(self):
        if self._etcd is None:
            from Jumpscale.clients.etcd.EtcdFactory import EtcdFactory
            self._etcd =  EtcdFactory()
        return self._etcd
    @property
    def sonic(self):
        if self._sonic is None:
            from Jumpscale.clients.sonic.SonicFactory import SonicFactory
            self._sonic =  SonicFactory()
        return self._sonic
    @property
    def mysql(self):
        if self._mysql is None:
            from Jumpscale.clients.mysql.MySQLFactory import MySQLFactory
            self._mysql =  MySQLFactory()
        return self._mysql
    @property
    def mongodb(self):
        if self._mongodb is None:
            from Jumpscale.clients.mongodbclient.MongoFactory import MongoFactory
            self._mongodb =  MongoFactory()
        return self._mongodb
    @property
    def mongoengine(self):
        if self._mongoengine is None:
            from Jumpscale.clients.mongodbclient.MongoEngineFactory import MongoEngineFactory
            self._mongoengine =  MongoEngineFactory()
        return self._mongoengine
    @property
    def packetnet(self):
        if self._packetnet is None:
            from Jumpscale.clients.packetnet.PacketNetFactory import PacketNetFactory
            self._packetnet =  PacketNetFactory()
        return self._packetnet
    @property
    def kraken(self):
        if self._kraken is None:
            from Jumpscale.clients.kraken.KrakenFactory import KrakenFactory
            self._kraken =  KrakenFactory()
        return self._kraken
    @property
    def zos(self):
        if self._zos is None:
            from Jumpscale.clients.zero_os.ZeroOSClientFactory import ZeroOSFactory
            self._zos =  ZeroOSFactory()
        return self._zos
    @property
    def ssh(self):
        if self._ssh is None:
            from Jumpscale.clients.ssh.SSHClientFactory import SSHClientFactory
            self._ssh =  SSHClientFactory()
        return self._ssh
    @property
    def email(self):
        if self._email is None:
            from Jumpscale.clients.mail.EmailFactory import EmailFactory
            self._email =  EmailFactory()
        return self._email
    @property
    def sendgrid(self):
        if self._sendgrid is None:
            from Jumpscale.clients.mail.sendgrid.SendGridClient import SendGridClient
            self._sendgrid =  SendGridClient()
        return self._sendgrid
    @property
    def kubernetes(self):
        if self._kubernetes is None:
            from Jumpscale.clients.kubernetes.KubernetesFactory import KubernetesFactory
            self._kubernetes =  KubernetesFactory()
        return self._kubernetes
    @property
    def telegram_bot(self):
        if self._telegram_bot is None:
            from Jumpscale.clients.telegram_bot.TelegramBotFactory import TelegramBotFactory
            self._telegram_bot =  TelegramBotFactory()
        return self._telegram_bot
    @property
    def s3(self):
        if self._s3 is None:
            from Jumpscale.clients.s3.S3Factory import S3Factory
            self._s3 =  S3Factory()
        return self._s3
    @property
    def sshkey(self):
        if self._sshkey is None:
            from Jumpscale.clients.sshkey.SSHKeys import SSHKeys
            self._sshkey =  SSHKeys()
        return self._sshkey
    @property
    def freeflowpages(self):
        if self._freeflowpages is None:
            from Jumpscale.clients.freeflow.FreeFlowFactory import FreeFlowFactory
            self._freeflowpages =  FreeFlowFactory()
        return self._freeflowpages
    @property
    def currencylayer(self):
        if self._currencylayer is None:
            from Jumpscale.clients.currencylayer.CurrencyLayer import CurrencyLayerSingleton
            self._currencylayer =  CurrencyLayerSingleton()
        return self._currencylayer
    @property
    def gdrive(self):
        if self._gdrive is None:
            from Jumpscale.clients.gdrive.GDriveFactory import GDriveFactory
            self._gdrive =  GDriveFactory()
        return self._gdrive
    @property
    def peewee(self):
        if self._peewee is None:
            from Jumpscale.clients.peewee.PeeweeFactory import PeeweeFactory
            self._peewee =  PeeweeFactory()
        return self._peewee
    @property
    def influxdb(self):
        if self._influxdb is None:
            from Jumpscale.clients.influxdb.InfluxdbFactory import InfluxdbFactory
            self._influxdb =  InfluxdbFactory()
        return self._influxdb
    @property
    def intercom(self):
        if self._intercom is None:
            from Jumpscale.clients.intercom.IntercomFactory import Intercom
            self._intercom =  Intercom()
        return self._intercom
    @property
    def github(self):
        if self._github is None:
            from Jumpscale.clients.github.GitHubFactory import GitHubFactory
            self._github =  GitHubFactory()
        return self._github
    @property
    def sendgrid(self):
        if self._sendgrid is None:
            from Jumpscale.clients.sendgrid.SendgridFactory import SendgridFactory
            self._sendgrid =  SendgridFactory()
        return self._sendgrid
    @property
    def syncthing(self):
        if self._syncthing is None:
            from Jumpscale.clients.syncthing.SyncthingFactory import SyncthingFactory
            self._syncthing =  SyncthingFactory()
        return self._syncthing
    @property
    def grafana(self):
        if self._grafana is None:
            from Jumpscale.clients.grafana.GrafanaFactory import GrafanaFactory
            self._grafana =  GrafanaFactory()
        return self._grafana
    @property
    def tfchain(self):
        if self._tfchain is None:
            from Jumpscale.clients.blockchain.tfchain.TFChainClientFactory import TFChainClientFactory
            self._tfchain =  TFChainClientFactory()
        return self._tfchain
    @property
    def btc_electrum(self):
        if self._btc_electrum is None:
            from Jumpscale.clients.blockchain.electrum.ElectrumClientFactory import ElectrumClientFactory
            self._btc_electrum =  ElectrumClientFactory()
        return self._btc_electrum
    @property
    def zhubdirect(self):
        if self._zhubdirect is None:
            from Jumpscale.clients.zero_hub_direct.HubDirectFactory import HubDirectFactory
            self._zhubdirect =  HubDirectFactory()
        return self._zhubdirect
    @property
    def rogerthat(self):
        if self._rogerthat is None:
            from Jumpscale.clients.rogerthat.RogerthatFactory import RogerthatFactory
            self._rogerthat =  RogerthatFactory()
        return self._rogerthat
    @property
    def sqlalchemy(self):
        if self._sqlalchemy is None:
            from Jumpscale.clients.sqlalchemy.SQLAlchemyFactory import SQLAlchemyFactory
            self._sqlalchemy =  SQLAlchemyFactory()
        return self._sqlalchemy
    @property
    def trello(self):
        if self._trello is None:
            from Jumpscale.clients.trello.TrelloFactory import Trello
            self._trello =  Trello()
        return self._trello
    @property
    def coredns(self):
        if self._coredns is None:
            from Jumpscale.clients.coredns.CoreDNSFactory import CoreDnsFactory
            self._coredns =  CoreDnsFactory()
        return self._coredns
    @property
    def graphite(self):
        if self._graphite is None:
            from Jumpscale.clients.graphite.GraphiteFactory import GraphiteFactory
            self._graphite =  GraphiteFactory()
        return self._graphite
    @property
    def postgres(self):
        if self._postgres is None:
            from Jumpscale.clients.postgresql.PostgresqlFactory import PostgresqlFactory
            self._postgres =  PostgresqlFactory()
        return self._postgres
    @property
    def sshagent(self):
        if self._sshagent is None:
            from Jumpscale.clients.sshagent.SSHAgent import SSHAgent
            self._sshagent =  SSHAgent()
        return self._sshagent
    @property
    def zerostor(self):
        if self._zerostor is None:
            from Jumpscale.clients.zero_stor.ZeroStorFactoryDeprecated import ZeroStorFactoryDeprecated
            self._zerostor =  ZeroStorFactoryDeprecated()
        return self._zerostor
    @property
    def zstor(self):
        if self._zstor is None:
            from Jumpscale.clients.zero_stor.ZeroStorFactory import ZeroStorFactory
            self._zstor =  ZeroStorFactory()
        return self._zstor
    @property
    def virtualbox(self):
        if self._virtualbox is None:
            from Jumpscale.clients.virtualbox.VirtualboxFactory import VirtualboxFactory
            self._virtualbox =  VirtualboxFactory()
        return self._virtualbox
    @property
    def webgateway(self):
        if self._webgateway is None:
            from Jumpscale.clients.webgateway.WebGatewayFactory import WebGatewayFactory
            self._webgateway =  WebGatewayFactory()
        return self._webgateway

j.clients = group_clients()
j.core._groups["clients"] = j.clients


class group_servers(JSGroup):
    def __init__(self):
        
        self._myjobs = None
        self._digitalme = None
        self._dns = None
        self._raftserver = None
        self._gedis = None
        self._errbot = None
        self._zdb = None
        self._openresty = None
        self._jsrun = None
        self._web = None
        self._etcd = None
        self._capacity = None

    
    @property
    def myjobs(self):
        if self._myjobs is None:
            from DigitalMe.servers.myjobs.MyJobs import MyJobs
            self._myjobs =  MyJobs()
        return self._myjobs
    @property
    def digitalme(self):
        if self._digitalme is None:
            from DigitalMe.servers.digitalme.DigitalMe import DigitalMe
            self._digitalme =  DigitalMe()
        return self._digitalme
    @property
    def dns(self):
        if self._dns is None:
            from DigitalMe.servers.dns.DNSServerFactory import DNSServerFactory
            self._dns =  DNSServerFactory()
        return self._dns
    @property
    def raftserver(self):
        if self._raftserver is None:
            from DigitalMe.servers.raft.RaftServerFactory import RaftServerFactory
            self._raftserver =  RaftServerFactory()
        return self._raftserver
    @property
    def gedis(self):
        if self._gedis is None:
            from DigitalMe.servers.gedis.GedisFactory import GedisFactory
            self._gedis =  GedisFactory()
        return self._gedis
    @property
    def errbot(self):
        if self._errbot is None:
            from Jumpscale.servers.errbot.ErrBotFactory import ErrBotFactory
            self._errbot =  ErrBotFactory()
        return self._errbot
    @property
    def zdb(self):
        if self._zdb is None:
            from Jumpscale.servers.zdb.ZDBServer import ZDBServer
            self._zdb =  ZDBServer()
        return self._zdb
    @property
    def openresty(self):
        if self._openresty is None:
            from Jumpscale.servers.openresty.OpenRestyFactory import OpenRestyFactory
            self._openresty =  OpenRestyFactory()
        return self._openresty
    @property
    def jsrun(self):
        if self._jsrun is None:
            from Jumpscale.servers.jsrun.JSRun import JSRun
            self._jsrun =  JSRun()
        return self._jsrun
    @property
    def web(self):
        if self._web is None:
            from Jumpscale.servers.webserver.JSWebServers import JSWebServers
            self._web =  JSWebServers()
        return self._web
    @property
    def etcd(self):
        if self._etcd is None:
            from Jumpscale.servers.etcd.EtcdServer import EtcdServer
            self._etcd =  EtcdServer()
        return self._etcd
    @property
    def capacity(self):
        if self._capacity is None:
            from Jumpscale.servers.grid_capacity.CapacityFactory import CapacityFactory
            self._capacity =  CapacityFactory()
        return self._capacity

j.servers = group_servers()
j.core._groups["servers"] = j.servers


class group_builder(JSGroup):
    def __init__(self):
        
        self.__template = None
        self._monitoring = None
        self.__template = None
        self._db = None
        self._runtimes = None
        self._storage = None
        self._tools = None
        self._system = None
        self._apps = None
        self._libs = None
        self._libs = None
        self._systemtools = None
        self._blockchain = None
        self._web = None
        self._network = None
        self._buildenv = None

    
    @property
    def _template(self):
        if self.__template is None:
            from Jumpscale.builder.monitoring.BuilderGrafanaFactory import BuilderGrafanaFactory
            self.__template =  BuilderGrafanaFactory()
        return self.__template
    @property
    def monitoring(self):
        if self._monitoring is None:
            from Jumpscale.builder.monitoring.BuilderMonitoringFactory import BuilderMonitoringFactory
            self._monitoring =  BuilderMonitoringFactory()
        return self._monitoring
    @property
    def _template(self):
        if self.__template is None:
            from Jumpscale.builder.TEMPLATE.BuilderGrafanaFactory import GrafanaFactory
            self.__template =  GrafanaFactory()
        return self.__template
    @property
    def db(self):
        if self._db is None:
            from Jumpscale.builder.db.BuildDBFactory import BuildDBFactory
            self._db =  BuildDBFactory()
        return self._db
    @property
    def runtimes(self):
        if self._runtimes is None:
            from Jumpscale.builder.runtimes.BuilderRuntimesFactory import BuilderRuntimesFactory
            self._runtimes =  BuilderRuntimesFactory()
        return self._runtimes
    @property
    def storage(self):
        if self._storage is None:
            from Jumpscale.builder.storage.BuilderStorageFactory import BuilderAppsFactory
            self._storage =  BuilderAppsFactory()
        return self._storage
    @property
    def tools(self):
        if self._tools is None:
            from Jumpscale.builder.tools.BuilderTools import BuilderTools
            self._tools =  BuilderTools()
        return self._tools
    @property
    def system(self):
        if self._system is None:
            from Jumpscale.builder.system.BuilderSystemFactory import BuilderSystemPackage
            self._system =  BuilderSystemPackage()
        return self._system
    @property
    def apps(self):
        if self._apps is None:
            from Jumpscale.builder.apps.BuilderAppsFactory import BuilderAppsFactory
            self._apps =  BuilderAppsFactory()
        return self._apps
    @property
    def libs(self):
        if self._libs is None:
            from Jumpscale.builder.libs.BuilderLibs import BuilderLibs
            self._libs =  BuilderLibs()
        return self._libs
    @property
    def libs(self):
        if self._libs is None:
            from Jumpscale.builder.libs.BuilderLibsFactory import BuilderLibsFactory
            self._libs =  BuilderLibsFactory()
        return self._libs
    @property
    def systemtools(self):
        if self._systemtools is None:
            from Jumpscale.builder.systemtools.BuilderSystemToolsFactory import BuilderSystemToolsFactory
            self._systemtools =  BuilderSystemToolsFactory()
        return self._systemtools
    @property
    def blockchain(self):
        if self._blockchain is None:
            from Jumpscale.builder.blockchain.BuilderBlockchainFactory import BuilderBlockchainFactory
            self._blockchain =  BuilderBlockchainFactory()
        return self._blockchain
    @property
    def web(self):
        if self._web is None:
            from Jumpscale.builder.web.BuilderWebFactory import BuilderWebFactory
            self._web =  BuilderWebFactory()
        return self._web
    @property
    def network(self):
        if self._network is None:
            from Jumpscale.builder.network.BuilderNetworkFactory import BuilderNetworkFactory
            self._network =  BuilderNetworkFactory()
        return self._network
    @property
    def buildenv(self):
        if self._buildenv is None:
            from Jumpscale.builder.buildenv.BuildEnv import BuildEnv
            self._buildenv =  BuildEnv()
        return self._buildenv

j.builder = group_builder()
j.core._groups["builder"] = j.builder


class group_sal(JSGroup):
    def __init__(self):
        
        self._docker = None
        self._nfs = None
        self._bind = None
        self._nic = None
        self._nginx = None
        self._ubuntu = None
        self._netconfig = None
        self._tls = None
        self._disklayout = None
        self._sshd = None
        self._qemu_img = None
        self._openvswitch = None
        self._kvm = None
        self._samba = None
        self._rsync = None
        self._ufw = None
        self._hostsfile = None
        self._nettools = None
        self._fs = None
        self._fswalker = None
        self._unix = None
        self._ssl = None
        self._process = None
        self._windows = None
        self._btrfs = None
        self._dnsmasq = None
        self._coredns = None

    
    @property
    def docker(self):
        if self._docker is None:
            from Jumpscale.tools.docker.Docker import Docker
            self._docker =  Docker()
        return self._docker
    @property
    def nfs(self):
        if self._nfs is None:
            from Jumpscale.sal.nfs.NFS import NFS
            self._nfs =  NFS()
        return self._nfs
    @property
    def bind(self):
        if self._bind is None:
            from Jumpscale.sal.bind.BindDNS import BindDNS
            self._bind =  BindDNS()
        return self._bind
    @property
    def nic(self):
        if self._nic is None:
            from Jumpscale.sal.nic.UnixNetworkManager import UnixNetworkManager
            self._nic =  UnixNetworkManager()
        return self._nic
    @property
    def nginx(self):
        if self._nginx is None:
            from Jumpscale.sal.nginx.Nginx import NginxFactory
            self._nginx =  NginxFactory()
        return self._nginx
    @property
    def ubuntu(self):
        if self._ubuntu is None:
            from Jumpscale.sal.ubuntu.Ubuntu import Ubuntu
            self._ubuntu =  Ubuntu()
        return self._ubuntu
    @property
    def netconfig(self):
        if self._netconfig is None:
            from Jumpscale.sal.netconfig.Netconfig import Netconfig
            self._netconfig =  Netconfig()
        return self._netconfig
    @property
    def tls(self):
        if self._tls is None:
            from Jumpscale.sal.tls.TLSFactory import TLSFactory
            self._tls =  TLSFactory()
        return self._tls
    @property
    def disklayout(self):
        if self._disklayout is None:
            from Jumpscale.sal.disklayout.DiskManager import DiskManager
            self._disklayout =  DiskManager()
        return self._disklayout
    @property
    def sshd(self):
        if self._sshd is None:
            from Jumpscale.sal.sshd.SSHD import SSHD
            self._sshd =  SSHD()
        return self._sshd
    @property
    def qemu_img(self):
        if self._qemu_img is None:
            from Jumpscale.sal.qemu_img.Qemu_img import QemuImg
            self._qemu_img =  QemuImg()
        return self._qemu_img
    @property
    def openvswitch(self):
        if self._openvswitch is None:
            from Jumpscale.sal.openvswitch.NetConfigFactory import NetConfigFactory
            self._openvswitch =  NetConfigFactory()
        return self._openvswitch
    @property
    def kvm(self):
        if self._kvm is None:
            from Jumpscale.sal.kvm.KVM import KVM
            self._kvm =  KVM()
        return self._kvm
    @property
    def samba(self):
        if self._samba is None:
            from Jumpscale.sal.samba.Samba import Samba
            self._samba =  Samba()
        return self._samba
    @property
    def rsync(self):
        if self._rsync is None:
            from Jumpscale.sal.rsync.RsyncFactory import RsyncFactory
            self._rsync =  RsyncFactory()
        return self._rsync
    @property
    def ufw(self):
        if self._ufw is None:
            from Jumpscale.sal.ufw.UFWManager import UFWManager
            self._ufw =  UFWManager()
        return self._ufw
    @property
    def hostsfile(self):
        if self._hostsfile is None:
            from Jumpscale.sal.hostfile.HostFile import HostFile
            self._hostsfile =  HostFile()
        return self._hostsfile
    @property
    def nettools(self):
        if self._nettools is None:
            from Jumpscale.sal.nettools.NetTools import NetTools
            self._nettools =  NetTools()
        return self._nettools
    @property
    def fs(self):
        if self._fs is None:
            from Jumpscale.sal.fs.SystemFS import SystemFS
            self._fs =  SystemFS()
        return self._fs
    @property
    def fswalker(self):
        if self._fswalker is None:
            from Jumpscale.sal.fs.SystemFSWalker import SystemFSWalker
            self._fswalker =  SystemFSWalker()
        return self._fswalker
    @property
    def unix(self):
        if self._unix is None:
            from Jumpscale.sal.unix.Unix import UnixSystem
            self._unix =  UnixSystem()
        return self._unix
    @property
    def ssl(self):
        if self._ssl is None:
            from Jumpscale.sal.ssl.SSLFactory import SSLFactory
            self._ssl =  SSLFactory()
        return self._ssl
    @property
    def process(self):
        if self._process is None:
            from Jumpscale.sal.process.SystemProcess import SystemProcess
            self._process =  SystemProcess()
        return self._process
    @property
    def windows(self):
        if self._windows is None:
            from Jumpscale.sal.windows.Windows import WindowsSystem
            self._windows =  WindowsSystem()
        return self._windows
    @property
    def btrfs(self):
        if self._btrfs is None:
            from Jumpscale.sal.btrfs.BtrfsExtension import BtfsExtensionFactory
            self._btrfs =  BtfsExtensionFactory()
        return self._btrfs
    @property
    def dnsmasq(self):
        if self._dnsmasq is None:
            from Jumpscale.sal.dnsmasq.DnsmasqFactory import DnsmasqFactory
            self._dnsmasq =  DnsmasqFactory()
        return self._dnsmasq
    @property
    def coredns(self):
        if self._coredns is None:
            from Jumpscale.clients.coredns.alternative.CoreDnsFactory import CoreDnsFactory
            self._coredns =  CoreDnsFactory()
        return self._coredns

j.sal = group_sal()
j.core._groups["sal"] = j.sal


class group_tutorials(JSGroup):
    def __init__(self):
        
        self._base = None

    
    @property
    def base(self):
        if self._base is None:
            from Jumpscale.tutorials.base.Tutorial import Tutorial
            self._base =  Tutorial()
        return self._base

j.tutorials = group_tutorials()
j.core._groups["tutorials"] = j.tutorials


class group_data_units(JSGroup):
    def __init__(self):
        
        self._sizes = None

    
    @property
    def sizes(self):
        if self._sizes is None:
            from Jumpscale.data.numtools.units.Units import Bytes
            self._sizes =  Bytes()
        return self._sizes

j.data_units = group_data_units()
j.core._groups["data_units"] = j.data_units


class group_sal_zos(JSGroup):
    def __init__(self):
        
        self._stats_collector = None
        self._farm = None
        self._traefik = None
        self._disks = None
        self._gateway = None
        self._tfchain = None
        self._ftpclient = None
        self._storagepools = None
        self._ippoolmanager = None
        self._hypervisor = None
        self._sandbox = None
        self._minio = None
        self._zt_bootstrap = None
        self._zrobot = None
        self._bootstrapbot = None
        self._zstor = None
        self._zerodb = None
        self._node = None
        self._capacity = None
        self._influx = None
        self._userbot = None
        self._vm = None
        self._grafana = None
        self._etcd = None
        self._coredns = None
        self._containers = None
        self._mongodb = None
        self._primitives = None
        self._network = None

    
    @property
    def stats_collector(self):
        if self._stats_collector is None:
            from Jumpscale.sal_zos.stats_collector.stats_collector_factory import StatsCollectorFactory
            self._stats_collector =  StatsCollectorFactory()
        return self._stats_collector
    @property
    def farm(self):
        if self._farm is None:
            from Jumpscale.sal_zos.farm.FarmFactory import FarmFactory
            self._farm =  FarmFactory()
        return self._farm
    @property
    def traefik(self):
        if self._traefik is None:
            from Jumpscale.sal_zos.traefik.TraefikFactory import TraefikFactory
            self._traefik =  TraefikFactory()
        return self._traefik
    @property
    def disks(self):
        if self._disks is None:
            from Jumpscale.sal_zos.disks.DisksFactory import DisksFactory
            self._disks =  DisksFactory()
        return self._disks
    @property
    def gateway(self):
        if self._gateway is None:
            from Jumpscale.sal_zos.gateway.gatewayFactory import GatewayFactory
            self._gateway =  GatewayFactory()
        return self._gateway
    @property
    def tfchain(self):
        if self._tfchain is None:
            from Jumpscale.sal_zos.tfchain.TfChainFactory import TfChainFactory
            self._tfchain =  TfChainFactory()
        return self._tfchain
    @property
    def ftpclient(self):
        if self._ftpclient is None:
            from Jumpscale.sal_zos.ftpClient.ftpFactory import FtpFactory
            self._ftpclient =  FtpFactory()
        return self._ftpclient
    @property
    def storagepools(self):
        if self._storagepools is None:
            from Jumpscale.sal_zos.storage.StorageFactory import ContainerFactory
            self._storagepools =  ContainerFactory()
        return self._storagepools
    @property
    def ippoolmanager(self):
        if self._ippoolmanager is None:
            from Jumpscale.sal_zos.ip_pool_manager.IPPoolManagerFactory import IPPoolManagerFactory
            self._ippoolmanager =  IPPoolManagerFactory()
        return self._ippoolmanager
    @property
    def hypervisor(self):
        if self._hypervisor is None:
            from Jumpscale.sal_zos.hypervisor.HypervisorFactory import HypervisorFactory
            self._hypervisor =  HypervisorFactory()
        return self._hypervisor
    @property
    def sandbox(self):
        if self._sandbox is None:
            from Jumpscale.sal_zos.sandbox.ZOSSandboxFactory import ZOSSandboxFactory
            self._sandbox =  ZOSSandboxFactory()
        return self._sandbox
    @property
    def minio(self):
        if self._minio is None:
            from Jumpscale.sal_zos.minio.MinioFactory import MinioFactory
            self._minio =  MinioFactory()
        return self._minio
    @property
    def zt_bootstrap(self):
        if self._zt_bootstrap is None:
            from Jumpscale.sal_zos.zerotier_bootstrap.ZerotierBootstrapFactory import ZerotierBootstrapFactory
            self._zt_bootstrap =  ZerotierBootstrapFactory()
        return self._zt_bootstrap
    @property
    def zrobot(self):
        if self._zrobot is None:
            from Jumpscale.sal_zos.zrobot.ZRobotFactory import ZeroRobotFactory
            self._zrobot =  ZeroRobotFactory()
        return self._zrobot
    @property
    def bootstrapbot(self):
        if self._bootstrapbot is None:
            from Jumpscale.sal_zos.bootstrap_bot.BootstrapBotFactory import BootstrapBotFactory
            self._bootstrapbot =  BootstrapBotFactory()
        return self._bootstrapbot
    @property
    def zstor(self):
        if self._zstor is None:
            from Jumpscale.sal_zos.zstor.ZStorFactory import ZeroStorFactory
            self._zstor =  ZeroStorFactory()
        return self._zstor
    @property
    def zerodb(self):
        if self._zerodb is None:
            from Jumpscale.sal_zos.zerodb.zerodbFactory import ZerodbFactory
            self._zerodb =  ZerodbFactory()
        return self._zerodb
    @property
    def node(self):
        if self._node is None:
            from Jumpscale.sal_zos.node.NodeFactory import PrimitivesFactory
            self._node =  PrimitivesFactory()
        return self._node
    @property
    def capacity(self):
        if self._capacity is None:
            from Jumpscale.sal_zos.capacity.CapacityFactory import CapacityFactory
            self._capacity =  CapacityFactory()
        return self._capacity
    @property
    def influx(self):
        if self._influx is None:
            from Jumpscale.sal_zos.influxdb.influxdbFactory import InfluxDBFactory
            self._influx =  InfluxDBFactory()
        return self._influx
    @property
    def userbot(self):
        if self._userbot is None:
            from Jumpscale.sal_zos.user_bot.UserBotFactory import UserBotFactory
            self._userbot =  UserBotFactory()
        return self._userbot
    @property
    def vm(self):
        if self._vm is None:
            from Jumpscale.sal_zos.vm.ZOS_VMFactory import ZOS_VMFactory
            self._vm =  ZOS_VMFactory()
        return self._vm
    @property
    def grafana(self):
        if self._grafana is None:
            from Jumpscale.sal_zos.grafana.grafanaFactory import GrafanaFactory
            self._grafana =  GrafanaFactory()
        return self._grafana
    @property
    def etcd(self):
        if self._etcd is None:
            from Jumpscale.sal_zos.ETCD.ETCDFactory import ETCDFactory
            self._etcd =  ETCDFactory()
        return self._etcd
    @property
    def coredns(self):
        if self._coredns is None:
            from Jumpscale.sal_zos.coredns.CorednsFactory import CorednsFactory
            self._coredns =  CorednsFactory()
        return self._coredns
    @property
    def containers(self):
        if self._containers is None:
            from Jumpscale.sal_zos.container.ContainerFactory import ContainerFactory
            self._containers =  ContainerFactory()
        return self._containers
    @property
    def mongodb(self):
        if self._mongodb is None:
            from Jumpscale.sal_zos.mongodb.MongodbFactory import MongodbFactory
            self._mongodb =  MongodbFactory()
        return self._mongodb
    @property
    def primitives(self):
        if self._primitives is None:
            from Jumpscale.sal_zos.primitives.PrimitivesFactory import PrimitivesFactory
            self._primitives =  PrimitivesFactory()
        return self._primitives
    @property
    def network(self):
        if self._network is None:
            from Jumpscale.sal_zos.network.NetworkFactory import NetworkFactory
            self._network =  NetworkFactory()
        return self._network

j.sal_zos = group_sal_zos()
j.core._groups["sal_zos"] = j.sal_zos



