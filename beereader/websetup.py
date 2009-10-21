"""Setup the beereader application"""
import logging

from beereader.config.environment import load_environment

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup beereader here"""
    environ = load_environment(conf.global_conf, conf.local_conf)

    from beereader.model import context as ctx
    from melkman.db import Composite

    log.info('bootstrapping database and plugins')
    ctx.bootstrap() # XXX accept a flag to possibly pass purge=True

    bucketid = 'site_index'
    if bucketid not in ctx.db:
        log.info('creating main bucket at %s' % bucketid)
        index = Composite.create(ctx, bucketid)
        index.save()

    cmd = 'curl -T <opmlfile> %s:%s/api/composite/%s/opml' % (
        'localhost', '5000', bucketid) # XXX get from config
    log.info('run "%s" or similar to add some feeds' % cmd)
