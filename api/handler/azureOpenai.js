/**
 * Azure OpenAI API calls
 */

const axios = require('axios');
const logger = require('tracer').console();

const prompt = require('../handler/prompt');
const utils = require('../handler/utils');
const config = require('../config');

module.exports = {
    /**
     * Evaluates a question and answer using Azure OpenAI's GPT-3 model.
     *
     * @param {string} question - The question to be evaluated.
     * @param {string} answer - The answer to the question.
     * @return {Promise<Object>} The evaluation result as a JSON object.
     * @throws {Error} If the evaluation fails due to missing content or an error.
     */
    async evaluate(question, answer) {
        const { gptUrl, headers } = config.azureOpenai;
        const results = await this.aisearch(question);
        let resObj = {};

        const hints = results.map(v => v.content).join('\n\n');
        const files = results.map(v => v.file).join(',');
        logger.log('******************', 'evaluate hints..', hints.length, files);

        const body = {
            messages: prompt.evalgpt(question, answer, hints),
            temperature: 0,
            top_p: 1,
            // max_tokens: 800,
            response_format: { type: 'json_object' }
        };

        logger.log('******************', 'evaluate body..', JSON.stringify({ body }));
        // when no hints from RAG search
        // if (!hints) return resObj;

        // api call to azure openai
        const { data } = await axios.post(gptUrl, body, { headers }) || {};
        const content = utils.getNested(data, 'choices.0.message.content');
        if (!content || data.error) throw new Error(content ? content.error : 'missing content!');

        logger.log('******************', 'evaluate content..', content);

        try {
            resObj = JSON.parse(content);
            resObj.reference = files;
        } catch (error) {
            resObj.data = content;
            resObj.error = error.message || error;
            logger.error('******************', resObj.error, content);
        }

        return resObj;
    },

    /**
     * Asynchronously searches for answers using Azure AI Search.
     *
     * @param {string} question - The question to search for answers to.
     * @return {Promise<string>} A string containing the answers to the question, separated by double newlines.
     * @throws {Error} If the search data is missing or the API call fails.
     */
    async aisearch(question) {
        const { searchUrl, headers, params } = config.aiSearch;
        params.search = question;
        logger.log('******************', 'aisearch params..', JSON.stringify({ params }));

        // api call to azure ai search
        const { data } = await axios.get(searchUrl, { params, headers }) || {};
        if (!data || !data.value) throw new Error('missing search data!');
        const values = [];

        // append matching top 2 search results
        for (const obj of data.value) {
            if (obj['@search.rerankerScore'] > 1 && values.length < 2) {
                values.push({
                    content: obj.content,
                    file: obj.metadata_storage_name
                });
            }
        }

        logger.log('******************', 'aisearch values..', values.length);
        return values;
    }
};
