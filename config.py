from environs import Env


env = Env()
env.read_env()

SUFFIX = env.str('SUFFIX')
PROJECT_ID = env.str('PROJECT_ID')
SESSION_ID = env.int('SESSION_ID')
LANGUAGE_CODE = env.str('LANGUAGE_CODE')
TG_BOT_API_KEY = env.str('TG_BOT_API_KEY')
VK_API_KEY = env.str('VK_API_KEY')