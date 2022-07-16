from flask import Flask, g, jsonify, request
from database import get_database
from functools import wraps

app = Flask(__name__)

# api_username = "admin"
# api_password = "password"

# def protected(f):
#     @wraps
#     def decorated(*args, **kwargs):
#         auth = request.authorization
#         if auth and auth.username == api_username and auth.password ==  api_password:
#             return f(*args, **kwargs)
        
#         return jsonify({"Authentication Message" : "Authentication Failed, Please check your username and password"}), 403

#     return decorated


@app.teardown_appcontext
def closedatabase(error):
    if hasattr(g, 'member_db'):
        g.member_db.close()


@app.route('/getallmembers', methods = ["GET"])
def getallmembers():
    db = get_database()
    allmember_cursor = db.execute("select * from members")
    allmembers = allmember_cursor.fetchall()
    fetched_result = []
    # loop through all the members and append in fetched_result 
    for eachmember in allmembers:
        member_dict = {}
        member_dict['id'] = eachmember['id']
        member_dict['name'] = eachmember['name']
        member_dict['email'] = eachmember['email']
        member_dict['level'] = eachmember['level']
        fetched_result.append(member_dict)
    return jsonify({"All Members" : fetched_result})


@app.route('/getonemembers/<int:memberid>', methods = ["GET"])

def getonemembers(memberid):
    db = get_database()
    member_cursor = db.execute("select * from members where id = ?", [memberid])
    onemember = member_cursor.fetchone()
    return jsonify({"Fetched Member" : {
        "ID" : onemember['id'],
        "Name" : onemember['name'],
         "Email" : onemember['email'],
         "Level" : onemember['level'] 
    }})

@app.route('/addnewmember', methods = ["POST"])

def addnewmember():
    # request all the data from the post man as json data . 
    one_member_data = request.get_json()
    
    name = one_member_data['name']
    email = one_member_data['email']
    level = one_member_data['level']

    # store these 3 detials into the database. 
    db = get_database()
    db.execute("insert into members (name, email, level) values (?,?,?)",[name, email, level])
    db.commit()

    # fetch the newly added member from the database and show it as the output on the post man window. 
    user_cursor = db.execute("select * from members where name = ?", [name])
    onemember = user_cursor.fetchone()

    return jsonify({ "New Member added" : {
        "ID" : onemember['id'], "Name" : onemember['name'] , "Email": onemember['email'], "Level": onemember['level']
    }})

@app.route('/updatememberdetails/<int:memberid>', methods = ["PUT", "PATCH"])

def updatememberdetails(memberid):
    # get the values from the postman which the user will enter in post man using the get_json() function . 
    one_member_data = request.get_json()

    name = one_member_data['name']
    email = one_member_data['email']
    level = one_member_data['level']
    
    # connect to database and update these values in the members table. 
    db = get_database()
    db.execute("update members set name = ?, email =?, level = ? where id = ?", [name, email, level, memberid])
    db.commit()

    # show the updated details of that person on the post man screen as the output. 
    user_cursor = db.execute("select * from members where id = ?", [memberid])
    updateduser = user_cursor.fetchone()
    return jsonify({"Updated member" : {
        "Id" : updateduser['id'], "Name" : updateduser['name'], "Email" : updateduser['email'], "Level" : updateduser['level']
    }})



@app.route('/deletemember/<int:memberid>', methods = ['DELETE'])
def deletemember(memberid):
    db = get_database()
    db.execute("delete from members where id  = ?", [memberid])
    db.commit()
    return jsonify({"Delete Message" : "Member deleted successfully."})

if __name__ == "__main__":
    app.run(debug = True)
