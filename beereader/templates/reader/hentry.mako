<%page args="entry" />

##
## This template renders an article.
## The format conforms mostly to the 
## hAtom entry spec.
## See: http://microformats.org/wiki/hatom
##
## The template is provided an object
## called 'entry' with the following
## properties:
##
## title
## id
## permalink
## source_name
## source_url
## author_name
## content
## timestamp (datetime)
## tags (list)
##

<li id="${entry.id}" class="hentry">
  
  ## title and permalink
  <h2 class="entry-title">
    <% 
    entry_title = entry.title or 'Untitled Article'
    %>
    %if entry.permalink:
      <a href="${entry.permalink}" rel="bookmark">
        ${entry_title | n, unicode }
      </a>
    %else:
      ${entry_title | n, unicode }
    %endif
  </h2>


  ## item source
  <a class="entry-source" href="${entry.source_url}">
    ${entry.source_name or 'Untitled Source' | n, unicode}
  </a>

  ## content of article
  <div class="entry-content">
    ${entry.content or '[Article has no text content]' | n, unicode}
  </div> <!-- /.entry-content -->
  
  ## assorted meta-data
  <div class="entry-metadata">
    
    ## last update time
    %if entry.timestamp:
      <abbr class="updated" title="${h.iso8601_date(entry.timestamp)}">
        ${h.pretty_date(entry.timestamp)}
      </abbr>
    %endif
    
    ## author
    <div class="author vcard">
      <span class="fn">${entry.author_name or 'Unknown Author' | n, unicode}</span>
    </div> <!-- /.author  -->
    
    ## tags
    %if 'tags' in entry:
      <ul class="entry-tags">
        ## XXX here we diverge from hAtom, because they want tags to be links to  
        ## something which is odd and has no concrete meaning in the page.
        %for tag in entry.tags:
          <li class="entry-tag">
            ## <a href="http://www.example.org/tags/${tag}" rel="tag">${tag | n, unicode}</a>
            ${tag}
          </li>
        %endfor
      </ul> <!-- /.entry-tags -->
    %endif
  
  </div> <!-- /.entry-metadata -->

</li> <!-- /.hentry -->
