## Overview

The repository contains the source code for required Django app. When there's a new commit, the code is automatically transferred to remote server and it will trigger docker image rebuild and container re-creation. A demo sever is setup and the Django app runs behind caddy reverse proxy. The PostgreSQL is also configured at docker-compose file, which will be deployed at remote server.

There are three main directories:

-   `backtest` -- BackTest module
-   `fetch_data` -- module that fetch data from external API
-   `predict_data` -- module that apply ML model on history stock price

Since the API Key has strict limit of queries, I cached one stock's data(AAPL).

Demo API Endpoint:

### Fetch financial data

https://block-house-trial.renas.dev/fetch-data?symbol=AAPL

### Predict future stock price

https://block-house-trial.renas.dev/predict?symbol=AAPL&duration=10

-   `duration`: days to predict

### Visualize the prediction

https://block-house-trial.renas.dev/predict_and_visualize?symbol=AAPL&duration=200

-   `duration`: In order to compare real and predict value, the test is operated on history data. For example, when `duration=200`, the last 200 days of data is used to visualize the prediction result.

### Backtesting module

https://block-house-trial.renas.dev/backtest?symbol=AAPL&short_window=50&long_window=200&initial_invest_amount=10000

-   Buy when the stock price is smaller than the average price of last `short_window` days.
-   Sell when the stock price is larger than the average price of last `long_window` days.

## Deploy Guide

### Setting up secrets used for Github Action

-   `DEPLOY_PRIVATE_KEY`
-   `SERVER_HOST`
-   `SSH_PORT`
-   `SERVER_USER`

Also, the public key should be configured at remote server.

### Caddyfile used

```
acme_ca https://acme.zerossl.com/v2/DV90
email {{ email }}
acme_dns cloudflare {{ cf-token }}

{{ DOMAIN_NAME_USED }} {
	reverse_proxy localhost:8123
}
```

### Configure `.env` file manually

see `.env.example`
