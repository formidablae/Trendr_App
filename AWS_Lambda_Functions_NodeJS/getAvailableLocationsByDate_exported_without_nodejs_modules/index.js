const connect_to_db = require('./db');

const location = require('./locations');

module.exports.handler = (event, context, callback) => {
    context.callbackWaitsForEmptyEventLoop = false;
    console.log('Received event:\n', JSON.stringify(event, null, 2));
    
    // set default
    if(!event.date) {
        callback(null, {
            statusCode: 500, headers: { 'Content-Type': 'text/plain' },
            body: 'Could not fetch the locations. Date is null.'
        })
    }
    
    connect_to_db().then(() => {
        console.log('=> get all available locations that have trends in that date');
        location.find({dateTime: new RegExp(event.date)}, {_id: 0})
            .then(
                locations => {
                    callback(null, {
                        statusCode: 200,
                        body: {locations}
                    })
                }
            )
            .catch(err =>
                callback(null, {
                    statusCode: err.statusCode || 500,
                    headers: { 'Content-Type': 'text/plain' },
                    body: 'Could not fetch the locations.'
                })
            );
    });
};
