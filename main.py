import requests
import time
import logging
import os

REQUEST_DELAY = 4
SLEEP_AFTER_ERROR = 10
MAX_MILES_FROM_CITY = 25

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s : %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
)

url = 'https://www.apple.com/shop/fulfillment-messages'

# iPhone 14 Pro, 128GB and 256GB
models = {
    'MQ0E3LL/A': ('DEEP PURPLE', '128GB'),
    'MQ1D3LL/A': ('DEEP-PURPLE', '256GB'),
    # 'MQ063LL/A': ('GOLD', '128GB'),
    # 'MQ163LL/A': ('GOLD', '256GB'),
    'MQ003LL/A': ('SILVER', '128GB'),
    'MQ0X3LL/A': ('SILVER', '256GB'),
    'MPXT3LL/A': ('SPACE BLACK', '128GB'),
    'MQ0N3LL/A': ('SPACE-BLACK', '256GB'),
}

locations = [
    'New York, NY',
    'New Orleans, LA',
    'Chicago, IL',
    'Philadelphia, PA',
    'New Haven, CT',
]

logging.info(f'> Starting script (PID={os.getpid()})...')

while True:

    logging.info('Checking for iPhone 14 Pro availability...')
    attempt = 0

    for model_value, model_display in models.items():
        for location in locations:

            time.sleep(REQUEST_DELAY)
            response = requests.get(url, params={
                'pl': 'true',
                'mts.0': 'regular',
                'cppart': 'UNLOCKED/US',
                'parts.0': model_value,
                'location': location,
            })

            if response.status_code == 200:
                for store in response.json()['body']['content']['pickupMessage']['stores']:
                    if store['partsAvailability'][model_value]['pickupDisplay'] == 'available':
                        if store['storedistance'] > MAX_MILES_FROM_CITY:
                            continue
                        
                        message = f'iPhone 14 Pro {model_display} is available at {store["storeName"]} ({store["city"]})'
                        logging.warning(message)

                        os.system('afplay /System/Library/Sounds/Glass.aiff')
                        for i in range(3):
                            os.system(f'say "{message}"')
                            for i in range(5):
                                os.system('afplay /System/Library/Sounds/Glass.aiff')

            else:
                logging.warning(f'Error {response.status_code} for request: {location} {model_display}')
                time.sleep(SLEEP_AFTER_ERROR)
    
    attempt += 1
