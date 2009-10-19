<?xml version="1.0" encoding="utf-8" ?>

<%page args="feed, alt_url=None" />
##
## renders an Atom feed
##
## The template is provided an object
## called 'feed' with the following
## properties:
##
## id 
## title 
## timestamp (datetime)
## entries - list of entries as described below
## 
## each entry contains the following properties:
## title
## item_id
## link
## source_title
## source_url
## author
## summary
## timestamp (datetime)
## tags (list)
##
## alt_url may be specified to provide a link to (for example)
## a human readable view of the feed's source
##

<feed xmlns="http://www.w3.org/2005/Atom">
  <id>${c.this_url}</id>
  
  <link rel="self" href="${c.this_url}" />
  %if alt_url:
  <link rel="alternate" href="${source_url}" />
  %endif

  <title type="html">
    <![CDATA[${feed.title or 'Untitled Feed' | n, unicode }]]>
  </title>

  <updated>${feed.timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')}</updated>
  
  %for entry in feed.entries:
  <entry>
    <id>${entry.item_id}</id>
    
    <title type="html">
      <![CDATA[${entry.title or 'Untitled Article' | n, unicode }]]>
    </title>

    %if entry.timestamp:
      <updated>${entry.timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')}</updated>
    %endif

    %if entry.author:
      <author>
        <name>${entry.author | n, unicode }</name>
      </author>
    %endif

    <link rel="alternate" href="${entry.link}" />
    
    ## XXX NewsItemRefs don't have tags
    %if 'tags' in entry:
      %for tag in entry.tags:
      <category scheme="${c.site_url}" term="${tag | n, unicode }" />
      %endfor
    %endif
    
    <summary type="html">
     <![CDATA[${entry.summary | n, unicode }]]>
    </summary>
  
  </entry>
  %endfor
</feed>
