import warnings
from dotenv import load_dotenv

try:
    load_dotenv(".env")
except FileNotFoundError:
    warnings.warn(".env file not found")

