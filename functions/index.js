const functions = require('firebase-functions');
const manganelo = require('./datasource/manganelo');

var datasources = {
    'manganelo': manganelo
};

exports.search = functions.https.onRequest(async(request, response) => {
    var searchBody = request.body;
    functions.logger.info("Search", { body: searchBody });
    try {
        var result = await datasources[searchBody.source].search(searchBody.term);
        response.status(200).send(result);
    } catch (error) {
        functions.logger.error(error.message);
        response.status(400).json({ "message": error.message });
    }
});