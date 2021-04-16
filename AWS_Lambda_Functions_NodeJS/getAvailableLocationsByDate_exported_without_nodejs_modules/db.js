// CONNECTION TO DB

const mongoose = require('mongoose');
mongoose.Promise = global.Promise;
let isConnected;


require('dotenv').config({ path: './variables.env' });

module.exports = connect_to_db = () => {
    if (isConnected) {
        console.log('=> using existing database connection');
        return Promise.resolve();
    }
 
    console.log('=> using new database connection');
    
    return mongoose.connect(process.env.DB, {
        dbName: 'Database_del_Progetto',
        useNewUrlParser: true,
        useUnifiedTopology: true
    }).then(db => { isConnected = db.connections[0].readyState; });
};