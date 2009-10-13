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

reader.disable_more_button = function() {
    $('a.reader-more-button').attr('href', '');
};

reader.enable_more_button = function(url) {
    $('a.reader-more-button').attr('href', url);
};

reader.load_more = function(source_url) {
    if (!source_url)
        return;

    reader.disable_more_button()

    $.ajax({
        url: source_url,
        dataType: 'json',
        timeout: 2000,
        success: function(data) {
            var batch = data.content;
            reader.append_batch(batch);
            // restore more button
            reader.enable_more_button(batch.next);
        },
        error: function() {
            // signal error message
            reader.display_error('Error loading more articles.')
            // restore more button to last...
            reader.enable_more_button(source_url);
        }
    });
};

reader.append_batch = function(batch) {
    for (var i = 0, iid; iid = batch.entries[i]; i++) {
        var entry_html = batch.html[iid];
        if (entry_html) {
            $('#reader-entries').append(entry_html);
        }
    }
};
