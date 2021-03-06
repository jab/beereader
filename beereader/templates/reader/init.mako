##
## initialization functions for reader pages
##

<%def name="title()">
${c.bucket.title or 'Untitled'} | ${c.site_title}
</%def>

##
## extra stuff to put in the head 
##
<%def name="extra_head()">
  ## link for atom feed
  <link rel="alternate" type="application/atom+xml"
    href="${h.url_for('bucket_latest_entries_atom', id=c.bucket.id)}" />
</%def>

##
## scripts that are necessary to use the reader
##
<%def name="extra_javascripts()">
  <script src="${h.url_for('/javascripts/reader.js')}"></script>
  <script>
    $(document).ready(
      function() {
        reader.init();
      });
  </script>
</%def>

##
## main list of articles
##
<%def name="entries()">
  <ul id="reader-entries">
    ## if initial entries are specified, we immediately render them...
    %for entry in c.reader_initial_entries:
      <%include file="hentry.mako" args="entry=entry" />
    %endfor
  </ul>
</%def>

##
## basic pager
##
<%def name="page_controls()">
  %if c.reader_batch.next:
    <a class="reader-more-button enabled" href="${c.reader_batch.next}">more</a>
  %else:
    <a class="reader-more-button" href="">no more</a>
  %endif
</%def>


##
## a setup function to set up a reader from within a template
##
<%def name="init_with_bucket(id)">
  <%
  from beereader.controllers.bucketreader import get_initial_batch
  from beereader.lib.reader import init_reader_from_batch
  initial_batch = get_initial_batch(id)
  init_reader_from_batch(id, initial_batch)
  %>
</%def>
