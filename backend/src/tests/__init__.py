from app.factory import SETTINGS

if SETTINGS.SETTINGS_NAME != "test":
    print('>' * 100)
    print('\t\t\t change SOCIAL_NETWORK_CONFIG to test')
    print('>' * 100)
    raise BaseException('CHECK .env file: SOCIAL_NETWORK_CONFIG != test')
