<%page args="entry" />

##
## This template renders an article.
## The format conforms mostly to the 
## hAtom entry spec, except where
## noted otherwise.
## See: http://microformats.org/wiki/hatom
##
## The template is provided an object
## called 'entry' with the following
## properties:
##
## item_id
## title
## link
## source_title
## source_url
## author
## summary
## timestamp (datetime)
## tags (list)
##
## (not used:)
## bucket_id
## add_time
## document_types
##

<li id="${entry.item_id}" class="hentry">
  
  ## title and link
  <h2 class="entry-title">
    <% 
    entry_title = entry.title or 'Untitled Article'
    %>
    %if entry.link:
      <a href="${entry.link}" rel="bookmark">
        ${entry_title | n, unicode }
      </a>
    %else:
      ${entry_title | n, unicode }
    %endif
  </h2>


  ## item source
  <div class="entry-source">
    <a href="${entry.source_url}">${entry.source_title or 'Untitled Source' | n, unicode}</a>
  </div>

  <div class="entry-content">
    ${entry.content or entry.summary or '[Article has no text summary]' | n, unicode}
  </div> <!-- /.entry-content -->
  
  ## assorted meta-data
  <div class="entry-metadata">
    %if entry.timestamp:
      <abbr class="updated" title="${h.iso8601_date(entry.timestamp)}">
        ${h.pretty_date(entry.timestamp)}
      </abbr>
    %endif
    
    ## author
    <div class="author vcard">
      <span class="fn">${entry.author or 'Unknown Author' | n, unicode}</span>
    </div> <!-- /.author  -->
    
    ## tags
    %if 'tags' in entry:
      <ul class="tags">
        ## XXX here we diverge from hAtom, because they want tags to be links to  
        ## something which is odd and has no concrete meaning in the page.
        %for tag in entry.tags:
          <li class="tag">
            ## <a href="http://www.example.org/tags/${tag}" rel="tag">${tag | n, unicode}</a>
            ${tag}</li>
        %endfor
      </ul> <!-- /.tags -->
    %endif
  
  </div> <!-- /.entry-metadata -->

</li> <!-- /.hentry -->
