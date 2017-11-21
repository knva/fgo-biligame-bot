from flask import Flask
from flask import request
from flask import abort, redirect, url_for
from flask import render_template
import json 
app = Flask(__name__)

@app.route('/')
def main():
    with open("clientinfo.json", 'r') as f:
        data = json.load(f)
    return render_template('hello.html',version=data['version'],dateVersion=data['dateVersion'],dataVersion=data['dataVersion'],appVersion=data['appVersion'])

@app.route('/config',methods=['POST'])
def config():
    version = request.form['version']
    dateVersion = request.form['dateVersion']
    dataVersion = request.form['dataVersion']
    appVersion = request.form['appVersion']
    if(version != "" and dateVersion!= "" and dataVersion != "" and appVersion!= ""):
        processJson("clientinfo.json",version,dateVersion,dataVersion,appVersion)
        return '{"status":"1"}'
    else:
        return '{"status":"0"}'

def processJson(inputJsonFile, version,dateVersion,dataVersion,appVersion):  
    with open(inputJsonFile, 'r') as f:
        data = json.load(f)
        data['version']=version
        data['dateVersion']=dateVersion
        data['dataVersion']=dataVersion
        data['appVersion']=appVersion
        with open(inputJsonFile, 'w') as fn:
            json.dump(data, fn)

@app.route('/account',methods=['put'])
def editOneAcc():
    username =request.form['username']
    userid =request.form['userid']
    usertoken =request.form['usertoken']
    rcode =  addAccount(username,userid,usertoken)
    return '{"status":"'+str(rcode)+'"}'

@app.route('/addaccount',methods=['post'])
def addOneAcc():
    username =request.form['username']
    userid =request.form['userid']
    usertoken =request.form['usertoken']
    rcode =  addAccount(username,userid,usertoken)
    return '{"status":"'+str(rcode)+'"}'


def addAccount(username ,userid,usertoken):
    error = 0
    data={'username':username,'uid':userid,'accessToken':usertoken}
    with open("users.json", 'r') as f:
        jsObj = json.load(f)

        if(len(jsObj)==0):
            jsObj.append(data)
            error=2
            with open("users.json", 'w') as fn:
                json.dump(jsObj, fn)
                return error

        for x in jsObj:
            if x['username']==username:
                x['uid']=userid
                x['accessToken']=usertoken
                error=1
            else:
                error=2
        if error==2:        
            jsObj.append(data)

        with open("users.json", 'w') as fn:
            json.dump(jsObj, fn)
            return error
        
@app.route('/accountList',methods=['get'])
def showAccount():
    with open("users.json", 'r') as f:
        jsObj = json.load(f)
        return json.dumps(jsObj)

@app.route('/removeAccount/<username>',methods=['post','DELETE'])
def delAccount(username=None):
    print(username)
    with open("users.json", 'r') as f:
        jsObj = json.load(f)
        i=0
        for x in jsObj:
            if x['username']==username:
                del jsObj[i]
            i= i+1
        with open("users.json", 'w') as fn:
            json.dump(jsObj, fn)
            return '{"status":"1"}'

if __name__ == '__main__':
    app.debug = True
    app.run("0.0.0.0",5001)