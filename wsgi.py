import os
from pathlib import Path

from dotenv import load_dotenv

from apidoc import create_app

dotenv_path = Path(__file__).parent / '.env'

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = create_app('production')
