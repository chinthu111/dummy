import os

def get_env(key, default_val):
    return os.getenv(key, default_val)

def get_env_float(key, default_val):
    try:
        return float(os.getenv(key, default_val))
    except:
        return default_val
