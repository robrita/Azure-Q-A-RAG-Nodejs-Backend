const { SecretClient } = require('@azure/keyvault-secrets');
const { DefaultAzureCredential } = require('@azure/identity');
const utils = require('./handler/utils');

// Replace with your Key Vault name
const keyVaultName = process.env.KEY_VAULT_NAME;
const vaultUrl = `https://${ keyVaultName }.vault.azure.net`;

// Create a new secret client using the DefaultAzureCredential
const credential = new DefaultAzureCredential();
const client = new SecretClient(vaultUrl, credential);
// invoke "az login" for this to work

module.exports = {
    port: process.env.PORT || 3000,
    appKey: process.env.APP_KEY,
    vault: async () => {
        return utils.getNested(await client.getSecret('AI-Services-Key'), 'value');
    },
    azureOpenai: {
        gptUrl: `${ process.env.AZURE_OPENAI_ENDPOINT }/openai/deployments/${ process.env.AZURE_OPENAI_CHAT_DEPLOYMENT }/chat/completions?api-version=${ process.env.AZURE_OPENAI_API_VERSION }`,
        headers: {
            'api-key': process.env.AZURE_OPENAI_KEY,
            'Content-Type': 'application/json'
        }
    },
    aiSearch: {
        searchUrl: `${ process.env.AZURE_AI_SEARCH_ENDPOINT }/indexes/${ process.env.AZURE_AI_SEARCH_INDEX }/docs`,
        headers: {
            'api-key': process.env.AZURE_AI_SEARCH_KEY
        },
        params: {
            'api-version': process.env.AZURE_AI_SEARCH_API_VERSION,
            queryType: 'semantic',
            semanticConfiguration: 'default',
            captions: 'extractive',
            answers: 'extractive|count-3',
            queryLanguage: 'id-ID'
        }
    }
};
