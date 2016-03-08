import os
import hashlib

from app import db

def process_media(m):
    if os.path.exists(m.path):
    else:
        raise FileNotFoundError 