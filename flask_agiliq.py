from flask import Flask,redirect,session,request,abort,render_template
from requests import Request
import requests
import uuid
from wtforms import Form, StringField, FileField, SubmitField, validators

app = Flask(__name__)
app.debug = True
app.secret_key = 'hello'

class ResumeForm(Form):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    projects_url = StringField('Projects Url')
    code_url = StringField('Code Url')
    resume = FileField('Resume')
    submit = SubmitField()

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

@app.route('/callback',methods=['GET','POST'])
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
    session['access_token'] = access_token
    return redirect('res_form')
    
@app.route('/res_form',methods=['GET','POST'])
def res_form():
    form = ResumeForm()
    if request.method == 'POST' and form.validate():
        
        return "HEllo"
    return render_template('res_form.html',form=form,access_token=session['access_token'])
    

if __name__ == '__main__':
    app.run()
