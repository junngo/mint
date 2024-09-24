## MINT (Stock Trading Automation System)

This project is a Django-based stock trading automation system that integrates with Korea Investment API.

---

### API Integration
The project interacts with the Korea Investment & Securities API, supporting both real and simulation environments:

- Real Investment Domain: https://openapi.koreainvestment.com:9443
- Simulation Investment Domain: https://openapivts.koreainvestment.com:29443


---

### Available Commands
- Get API Token
To fetch an access token from the Korea Investment API, use the get_token command:

```
python manage.py get_token
```

This command retrieves the access token based on your current environment settings (real or simulated). The environment is controlled via the USE_SIMULATED_API flag in your .env file.

---

### Setup Instructions

#### Prerequisites
- Python 3.12
- Django 5.1.1

#### Installation
- Clone the repository:
```
https://github.com/junngo/mint.git
cd mint
```

- Install the required dependencies:
```
pip install -r requirements.txt
```

- Set up your .env file to manage API keys and environment settings:
```
LIVE_APP_KEY=your_live_app_key
LIVE_APP_SECRET=your_live_app_secret
SIM_APP_KEY=your_sim_app_key
SIM_APP_SECRET=your_sim_app_secret
LIVE_API_DOMAIN=https://openapi.koreainvestment.com:9443
SIM_API_DOMAIN=https://openapivts.koreainvestment.com:29443
USE_SIMULATED_API=True
```

- Apply migrations & Running the Server:
```
python manage.py migrate
python manage.py runserver
```
