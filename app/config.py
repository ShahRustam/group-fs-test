#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, jsonify, make_response, request, redirect, session
from flask.views import MethodView
from pymongo import MongoClient
import collections
from functools import wraps
from validate_email import validate_email
from uuid import uuid4
from hashlib import sha512
from time import time
import sqlparse
import re
from flask.ext.htmlmin import HTMLMIN


client = MongoClient("db",27017)
secret_key = "c2e8821a52e088c830870b23c1a5be5967a0daed39abbabec7800393a9b5b392b9bdc396f6fa85bd9eb1be431469138085e965add83ccd978de53f1cf5824d32"

