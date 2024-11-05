from flask import render_template, redirect, url_for, flash, abort, request, make_response
from LandlordRecruitment import App

@App.route("/")
def index():
    # return """<h1>123</h1>"""
    return render_template("index.html")

@App.route("/test")
def test():
    return render_template("test.html")