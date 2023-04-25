# My-PlayList

### Google Sheets
1. Create a Google Sheet 
2. Use the [Google Sheets API](https://developers.google.com/sheets/api/guides/concepts)
3. Obtain the API key

### Github API
1. Use the [GitHub Token](https://github.com/settings/tokens)
2. Create and Obtain the API key

### Update schedule (Two methods)
- Use crontab to run dailyUpdate.sh on a daily basis. (deprecatecurr use)
- AWS (currently in use)
  - Lambda Function: lambdaUpdate.py
  - EventBridge: Execute the lambda function once a day