##
## functions for rendering feeds
##

<%def name="atom_feed_from_bucket(id, alt_url=None)">\
  <%
  from beereader.controllers.bucketfeeder import get_feed_info
  feed = get_feed_info(id)
  %>
  <%include file="atom.mako" args="feed=feed, alt_url=alt_url" />
</%def>
