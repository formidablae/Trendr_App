const mongoose = require('mongoose');

const locations_schema = new mongoose.Schema({
    created_at: String,
    locations_name: String,
    location_type: String,
    locations_woeid: Number,
    parent_id: Number,
    parent_name: String
}, { collection: 'Available_locations' });

module.exports = mongoose.model('location', locations_schema);