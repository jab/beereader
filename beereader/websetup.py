"""Setup the beereader application"""
from beereader.config.environment import load_environment
from paste.deploy.converters import asbool
import logging
log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup beereader here"""
    environ = load_environment(conf.global_conf, conf.local_conf)

    from beereader.model import context as ctx
    from melkman.db import Composite

    log.info('bootstrapping database and plugins')
    purge = asbool(conf.get('beereader.purge_on_bootstrap', False))
    ctx.bootstrap(purge=purge)
    log.info('bootstrapped context with purge=%s' % purge)

    bucketid = conf.get('beereader.default_bucket_id', 'site_index')
    buckettitle = conf.get('beereader.default_bucket_title', 'My Daily Bee')
    if bucketid not in ctx.db:
        index = Composite.create(ctx, bucketid, title=buckettitle)
        index.save()
        log.info('created default bucket "%s" at %s' % (buckettitle, bucketid))

    cmd = 'curl -T <opmlfile> %s:%s/api/composite/%s/opml' % (
        'localhost', '5000', bucketid) # XXX get from config
    log.info('run "%s" or similar to add some feeds' % cmd)
