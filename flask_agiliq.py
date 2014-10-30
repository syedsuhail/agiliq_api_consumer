from flask import Flask,redirect,session,request,abort
from requests import Request
import requests
import uuid

app = Flask(__name__)
app.debug = False
app.secret_key = 'hello'



@app.route('/')
def index():
    state = uuid.uuid4().get_hex()
    session['agiliq_auth_state']= state
    params = {
        'client_id' : 'QmVgYsYlqa2cwg5HmQEmy05QC7J7HExknaj3qXeUHK7eqMFlMR',
        'state' : state,
        'redirect_uri' : 'http://127.0.0.1:5000/callback'
 
    }
    agiliq_auth_url = 'http://join.agiliq.com/oauth/authorize/'
    r = Request('GET',url=agiliq_auth_url,params=params).prepare()
    return redirect(r.url)

@app.route('/callback')
def callback():
    original_state = session.get('agiliq_auth_state')
    if not original_state:
        abort(404)
    del(session['agiliq_auth_state'])

    state = request.args.get('state')
    code = request.args.get('code')

    if not state or not code:
        abort(404)
    if original_state!=state:
        abort(404)

    params = {
        'client_id' : 'QmVgYsYlqa2cwg5HmQEmy05QC7J7HExknaj3qXeUHK7eqMFlMR',
        'client_secret' : 'csgiKjXFDkgm51wCwJ20a4Ag6oLpQ4jzv8O7boNeZsZaTnESG6',
        'code' : code,
        'redirect_uri': 'http://127.0.0.1:5000/callback',
        }
    headers = {'accept':'application/json'}
    url = 'http://join.agiliq.com/oauth/access_token/'

    r = requests.post(url,params=params,headers=headers)
    if not r.ok:
        abort(404) 
    data = r.json()
    access_token = data['access_token']
    params = {
        'access_token':access_token,
        'first_name':'Syed Suhail',
        'last_name':'Ahmed',
        'projects_url':'https://www.github.com/syedsuhail',
        'code_url':'https://github.com/syedsuhail/agiliq_api_consumer/blob/master/flask_agiliq.py',
        'resume':open('suhail_resume2.pdf','rb'),}

    r = requests.post('http://join.agiliq.com/api/resume/upload/',params=params)
    if r.ok:
        return "Successfully posted resume"
    else:
        abort(404)

if __name__ == '__main__':
    app.run()
