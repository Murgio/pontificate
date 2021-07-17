# Create auth for Oxford Dictionaries API
import configparser

config = configparser.ConfigParser()
config.read('webapp/credentials.INI')

def create_auth():
    return {'app_id' : config.get("Section", "clientid"), 'app_key' : config.get("Section", "clientsecret")}
