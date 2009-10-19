<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">    
##
## This template is inherited by most other user 
## facing templates -- it defines the wrapper that 
## encloses most pages and slots that can be overridden.
##
## the following globals are available to all templates:
##
## c.site_title - configured title of this site
## c.site_url - URL of front page of site
## c.this_url - URL of the current page being viewed
## c.google_ajax_api_key - configured google api key for domain
## c.local_resources_only - configured boolean to disable offsite scripts/etc.
##

## default title for any given page, override this 
## in inheriting templates 
<%def name="title()">
${c.site_title}
</%def>

## default page header
## override this to use a different header
<%def name="header()">
<%include file="/header.mako" />
</%def>

## default page footer
## override this to use a different footer
<%def name="footer()">
<%include file="/footer.mako" />
</%def>

## hook to include extra javascript
## override this to place extra scripts 
## at the bottom of the page
<%def name="extra_javascripts()">
</%def>

## hook to include extra stuff in
## the head of the document (e.g stylesheets)
<%def name="extra_head()">
</%def>

## hook for arbitrary page initialization
<%def name="page_init()">
</%def>


${self.page_init()}
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <title>${self.title()}</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <meta http-equiv="Content-Language" content="en-us" />
    
    ## stylesheets
    <link rel="stylesheet" href="${h.url_for('/stylesheets/blueprint/screen.css')}" type="text/css" media="screen, projection" />
    <link rel="stylesheet" href="${h.url_for('/stylesheets/blueprint/print.css')}" type="text/css" media="print" />
    <link rel="stylesheet" href="${h.url_for('/stylesheets/theme.css')}" type="text/css" />
    <!--[if IE]>
    	<link rel="stylesheet" href="/stylesheets/blueprint/ie.css" type="text/css" media="screen, projection" />
    	<![endif]-->
    	<!--[if (lt IE 7)&(gt IE 5.5)]>
    	<link rel="stylesheet" type="text/css" href="${h.url_for('/stylesheets/fixes-old-ie.css')}" />
    <![endif]-->
    ${self.extra_head()}
  </head>

  <body>
    <div id="header">
        ${self.header()}
    </div>
  	<div id="page-body">
  	    ## contents of inherting template
  	    ${next.body()}
  	</div>
    <div id="footer">
    		${self.footer()}
    </div>

    ##
    ## scripts
    ##
    %if c.local_resources_only == True:
      ## use offline scripts
      <script src="${h.url_for('/javascripts/jquery-1.3.2.min.js')}"></script>
    %else:
      ## use google hosted scripts
      <script src="http://www.google.com/jsapi?key=${c.google_ajax_api_key}"></script>
      <script>
        google.load("jquery", "1.3.2");
      </script>
    %endif
    ${self.extra_javascripts()}
  </body>
</html>
