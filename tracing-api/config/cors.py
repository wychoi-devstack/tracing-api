from oslo_config import cfg

GROUP_NAME = __name__.split('.')[-1]

ALL_OPTS = [cfg.StrOpt('allow_origins', default='*')]

def register_opts(conf):
    conf.register_opts(ALL_OPTS, group=GROUP_NAME)
