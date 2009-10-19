if (typeof reader == 'undefined') {
    var reader = {};
}

reader.init = function() {
    // take control of the 'more' button
    $('a.reader-more-button').click(
        function(evt) {
            var source_url = evt.target.href;
            reader.load_more(source_url);
            return false;
        });
};

reader.display_error = function(message) {
    $('#error').text = message;
};

reader.disable_more_button = function(disabledtext) {
    $('a.reader-more-button').text(disabledtext).attr('href', '').removeClass('enabled');
};

reader.enable_more_button = function(enabledtext, url) {
    $('a.reader-more-button').text(enabledtext).attr('href', url).addClass('enabled');
};

reader.load_more = function(source_url) {
    if (!source_url)
        return;

    reader.disable_more_button('please wait...');

    $.ajax({
        url: source_url,
        dataType: 'json',
        timeout: 2000,
        success: function(data) {
            var batch = data.content;
            reader.append_batch(batch);
            if (batch.next) {
              reader.enable_more_button('more', batch.next);
            } else {
              reader.disable_more_button('no more');
            }
        },
        error: function() {
            // signal error message
            reader.display_error('Error loading more articles.')
            // restore more button to last...
            reader.enable_more_button('more', source_url);
        }
    });
};

reader.append_batch = function(batch) {
    for (var i=0; i < batch.html.length; ++i) {
        var entry_html = batch.html[i];
        if (entry_html) {
            $('#reader-entries').append(entry_html);
        }
    }
};
