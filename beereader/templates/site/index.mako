<%inherit file="/base.mako" />

##
## This is the front page of the site.
##

<%namespace name="reader" file="/reader/init.mako" />

<%def name="page_init()">
  ${reader.init_with_bucket('site_index')}
</%def>

<%def name="extra_head()">
  ${reader.extra_head()}
</%def>

<%def name="extra_javascripts()">
  ${reader.extra_javascripts()}
</%def>

## the body of the front page ...
${reader.entries()}

${reader.page_controls()}
