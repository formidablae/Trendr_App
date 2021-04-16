const mongoose = require('mongoose');

const trends_schema = new mongoose.Schema({
    as_of: String,
    created_at: String,
    name: String,
    url: String,
    tweet_volume: String,
    locations_name: String,
    locations_woeid: Number
}, { collection: 'Trending_Topics' });

module.exports = mongoose.model('trend', trends_schema);