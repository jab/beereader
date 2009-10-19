<%inherit file="/base.mako" />

##
## This is the front page of the site.
##

<%namespace name="reader" file="/reader/init.mako" />

<%def name="page_init()">
  ## set what 'bucket' should be shown to this user
  ${reader.init_with_bucket('melk:c8a8d880-b18c-6569-749d-66d0045c58fa')}
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
