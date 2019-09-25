from app import app
from bs4 import BeautifulSoup
import requests,lxml
from selenium import webdriver
import time
import json
from functools import wraps
from flask import request
import jwt
from models import *
secret=app.config['SECRET_KEY']
