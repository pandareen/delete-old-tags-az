# delete-old-tags-az
Keeping the latest container tags on azure container repository

For usage, refer to `.github/workflows/OIDC_workflow.yml` workflow

This action requires login to the azure cloud services so make sure you have
`AZURE_CREDENTIALS` in your secrets. (more information here https://github.com/Azure/login/tree/v1#sample-workflow-that-uses-azure-login-action-using-oidc-to-run-az-cli-linux)
