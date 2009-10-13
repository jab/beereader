<%inherit file="/base.mako" />

##
## This is the front page of the site.
##

<%namespace name="reader" file="/reader/init.mako" />

<%def name="extra_javascripts()">
  ${reader.extra_javascripts()}
</%def>

## set what 'bucket' should be shown to this user
${reader.init_with_bucket('luke/street')}

## the body of the front page ...
${reader.entries()}

${reader.page_controls()}