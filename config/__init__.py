from dotenv import dotenv_values

config = dotenv_values(".env")
config = dict(config)