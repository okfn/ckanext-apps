# this is a namespace package
try:
    import pkg_resources
    pkg_resources.declare_namespace(__name__)
except ImportError:
    import pkgutil
    __path__ = pkgutil.extend_path(__path__, __name__)

import meta

from .idea import *
from .application import *

def init_model(engine):
    meta.Session.configure(bind=engine)
    meta.engine = engine
    meta.metadata.bind = engine
    meta.metadata.create_all(bind=meta.metadata.bind)
    #meta.metadata.reflect()

