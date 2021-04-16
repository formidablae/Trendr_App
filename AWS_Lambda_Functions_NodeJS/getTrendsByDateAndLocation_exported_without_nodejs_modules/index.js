const connect_to_db = require('./db');

const trend = require('./trends');

module.exports.handler = (event, context, callback) => {
    context.callbackWaitsForEmptyEventLoop = false;
    console.log('Received event:\n', JSON.stringify(event, null, 2));
    
    // set default
    if(!event.date || !event.woeid) {
        callback(null, {
            statusCode: 500, headers: { 'Content-Type': 'text/plain' },
            body: 'Could not fetch the trends. Date or location woeid is null.'
        })
    }
    
    if (!event.docperpage) { event.docperpage = 10 }
    if (!event.page) { event.page = 1 }
    
    connect_to_db().then(() => {
        console.log('=> get all trends');
        trend.find({created_at: new RegExp(event.date), locations_woeid: event.woeid})
            .skip((event.docperpage * event.page) - event.docperpage)
            .limit(event.docperpage)
            .then(trends => {
                    trends = trends.map(trend => ({
                        name: trend.name,
                        url: trend.url,
                        tweetvolume: trend.tweet_volume
                    }));
                    callback(null, {
                        statusCode: 200,
                        body: {
                            date: event.date,
                            woeid: event.woeid,
                            docperpage: event.docperpage,
                            page: event.page,
                            trends: trends
                        }
                    })
                }
            )
            .catch(err =>
                callback(null, {
                    statusCode: err.statusCode || 500,
                    headers: { 'Content-Type': 'text/plain' },
                    body: 'Could not fetch the trends.'
                })
            );
    });
};
