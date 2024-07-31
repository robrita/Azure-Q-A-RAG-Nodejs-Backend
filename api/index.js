// ***************************************************************************
// Q&A RAG Evaluator powered by Azure OpenAI
// https://github.com/robrita/Azure-Q-A-RAG-Nodejs-Backend
// ***************************************************************************

const express = require('express');
const bodyParser = require('body-parser');
const logger = require('tracer').console();
// load env variables
require('dotenv').config('.env');

const azureOpenai = require('./handler/azureOpenai');
const utils = require('./handler/utils');
const config = require('./config');

// Create the Express app & setup middlewares
const app = express();
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// ***************************************************************************

app.get('/', (req, res) => {
    return res.send('Q&A RAG Evaluator');
});

app.get('/vault', async (req, res) => {
    let resObj = {};
    try {
        resObj = await config.vault();
    } catch (error) {
        return res.status(500).send(error.message || error);
    }

    return res.send(resObj);
});

// Q and A RAG Evaluator
app.post('/eval', async (req, res) => {
    let resObj = {};
    logger.log('******************', 'incoming request..', JSON.stringify(req.body));
    if (req.headers['x-api-key'] !== config.appKey) return res.status(401).send('Invalid API key!');

    // retry on error
    for (let i = 0; i < 2; i++) {
        try {
            resObj = await azureOpenai.evaluate(req.body.question, req.body.answer);
            break;
        } catch (error) {
            resObj.error = error.message || error;
            logger.error('******************', 'error in eval..', i, resObj.error);
        }
        // add a delay
        await utils.delay(5000);
    }

    return res.send(resObj);
});

// error handling
app.use((err, req, res, _next) => {
    logger.error('****************', err.message || err);
    return res.status(err.status || 500).send(err.message || err);
});

// Start the server
app.listen(config.port, () => {
    logger.log('Server listening on port', config.port);
});
