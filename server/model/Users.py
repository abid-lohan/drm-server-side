from flask import Flask, request
import flask
from flask_sqlalchemy import SQLAlchemy

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))