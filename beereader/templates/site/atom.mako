<%namespace name="feeder" file="/feeder/init.mako" />\
${feeder.atom_feed_from_bucket(c.default_bucket_id)}
