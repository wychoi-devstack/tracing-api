from oslo_config import cfg
import sys

GROUP_NAME = __name__.split('.')[-1]

ALL_OPTS = [
        cfg.StrOpt('url', default='http://localhost:30168'),
        cfg.StrOpt('service_horizon', default='horizon-horizon'),
        cfg.StrOpt('service_cinder', default='cinder-cinder-api'),
        cfg.StrOpt('gap', default='5')
]

def register_opts(conf):
    conf.register_opts(ALL_OPTS, group=GROUP_NAME)
