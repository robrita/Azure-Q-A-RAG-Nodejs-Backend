/**
 * generic utility helper functions
 */

module.exports = {
    /**
     * @description Extract deep nested data
     * @param {Object} obj Object being verified.
     * @param {String} params Parameters to be checked if present, i.e. response.0.data
     * @param {String} fallback Fallback response.
     * @returns {String} Extracted data
     */
    getNested(obj, params, fallback = null) {
        if (params) {
            const args = params.split('.');
            return args.reduce((obj, level) => obj && obj[level], obj) || fallback;
        }

        return fallback;
    },

    /**
     * Returns a Promise that resolves after a specified number of milliseconds.
     *
     * @param {number} ms - The number of milliseconds to delay.
     * @return {Promise} A Promise that resolves after the specified delay.
     */
    delay(ms) {
        return new Promise((resolve) => setTimeout(resolve, ms));
    }
};
