<%inherit file="/base.mako" />

##
## This template is an example of using the reader inside
## a full page. 
##

<%namespace name="reader" file="/reader/init.mako" />

<%def name="extra_javascripts()">
  ${reader.extra_javascripts()}
</%def>

${reader.entries()}

${reader.page_controls()}
