from oslo_config import cfg
from . import default, cors, jaeger

CONF = cfg.CONF

conf_modules = [default, cors, jaeger]


def configure(conf=None, config_file_path='/etc/tracing-api/tracing-api.conf'):
    if conf is None:
        conf = CONF

    for module in conf_modules:
        module.register_opts(conf)

    CONF(['--config-file='+config_file_path], project='tracing-api')
