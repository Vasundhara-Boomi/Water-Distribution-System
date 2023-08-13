from flask import Flask, render_template, request, url_for, redirect,session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user
import re
import smtplib
import random
import ssl
import json
import requests
import math
import heapq
import copy
import time
import pandas as pd

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "abc"
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)


db.init_app(app)


with app.app_context():
    db.create_all()
    
with app.app_context():
    users = Users.query.all()
    #d={"id":[],"Username":[],"Password":[]}
    for user in users:
     print(f"User ID: {user.id}")
     print(f"Username: {user.username}")
     print(f"Password: {user.password}")
     print("----------------------")
     """d["id"].append(user.id)
     d["Username"].append(user.username)
     d["Password"].append(user.password)
    df = pd.DataFrame(d)
    print(df)"""
    
     
     
     


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

from flask import flash

@app.route('/register', methods=["GET", "POST"])
def register():
    selected_slide = "signup"  # Default slide is signup

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Check if username is a valid email
        if not is_valid_email(username):
            flash("Invalid email address.", "error")
            
        elif Users.query.filter_by(username=username).first():
            flash("Username already exists.", "error")
        # Check if password meets the requirements
        elif not is_valid_password(password):
            flash("Invalid password.", "error")
        # Check if password and confirm_password match
        elif password != confirm_password:
            flash("Password and confirm password do not match.", "error")
        else:
            user = Users(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            flash("Registration successful. Please log in.", "success")
            return render_template("login.html", selected_slide="login")
    else:
        selected_slide = "signup"  # Default slide is signup

    return render_template("login.html", selected_slide=selected_slide)



def is_valid_email(email):
    # Use regular expression to check if email is valid
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_regex, email) is not None

def is_valid_password(password):
    
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
     
    # compiling regex
    pat = re.compile(reg)
     
    # searching regex                
    return re.search(pat, password)
    



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(username=request.form.get("username")).first()
        if user and user.password == request.form.get("password"):
            login_user(user)
            return render_template("home.html")
        else:
            flash("Username and Password do not match.", "error")
            return render_template("login.html",selected_slide="login")
    return render_template("login.html")

def send_email(sender_email, sender_password, recipient_email, subject, message):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
        server.login(sender_email, sender_password)
        email_message = f"Subject: {subject}\n\n{message}"
        server.sendmail(sender_email, recipient_email, email_message)
        


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        sender_email = "oceanly204@gmail.com"
        sender_password = "lyihkkozuiqofazp"
        recipient_email = request.form['email']
        subject = 'OTP FOR OCEANLY NETWORKS'
        otp = random.randint(100000, 999999)
        message = "YOUR ONE TIME PASSWORD IS {}".format(otp)
        
        send_email(sender_email, sender_password, recipient_email, subject, message)
        
        # Store the OTP and recipient email in session for verification
        session['otp'] = otp
        session['recipient_email'] = recipient_email
        return redirect('/verification')
    
    return render_template('forgot_password.html')

@app.route('/verification', methods=['GET', 'POST'])
def verification():
    if request.method == 'POST':
        entered_otp = request.form['otp']
        
        if session['otp'] == int(entered_otp):
            # OTP verification successful, redirect to home page 
            return render_template('home.html')
        else:
            error = "Invalid OTP. Please try again."
            return render_template('verification.html', error=error)
    
    return render_template('verification.html')
@app.route('/search1')
def search1():
    return render_template("maps3.html")
data=None

@app.route('/search', methods=['POST'])
def search():
    search_input = request.form['searchInput']
   
    search_places(search_input) 
   
    return "Search input received: {}".format(search_input)
   
@app.route('/new')
def new():
    global data
    print(data)
    return render_template('maps.html',data=data)

@app.route("/login.html")
def signout():
    selected_slide = "login"
    return render_template("login.html",selected_slide=selected_slide)


@app.route('/aboutus.html')
def about_us():
    return render_template('aboutus.html')

@app.route('/Confirmm.html')
def update():
    return render_template('Confirmm.html')

@app.route('/help.html')
def help():
    return render_template('help.html')


@app.route("/")
def home():
    selected_slide = "login"
    return render_template("login.html",selected_slide=selected_slide)

@app.route('/go_back')
def go_back():
    # Redirect to the home route using url_for
    return render_template('home.html')

class Node():
        def __init__(self,val):
            self.val=val
        def __lt__(self,other):
            if self.val[2]==other.val[2]:
                return self.val[-1]<other.val[-1]
            else:
                return self.val[2]<other.val[2]
            
def calculate_mst(matrix,places):
  print(places)
  vertices = []
  p = []
  edges = []
  n = len(matrix)
  cyc = [-1] * n
  for i in range(n):
        vertices.append(str(i))
  d1={}
  for i in matrix:
        d1[i]={}
        for j in range(len(matrix[i])):
            if j!=i:
             d1[i][j]=matrix[i][j]
  def cycle(i, j):
    if cyc[i] < 0 and cyc[j] < 0:
        if i != j:
            p.append(1)
            cyc[j] = i
            cyc[i] -= 1
            return
        else:
            p.append(0)
            return
    elif cyc[i] < 0 and cyc[j] >= 0:
        cycle(i, cyc[j])
    elif cyc[i] >= 0 and cyc[j] < 0:
        cycle(cyc[i], j)
    else:
        cycle(cyc[i], cyc[j])


  def prim_mst(g):
        if len(g) == n:
            return g
        else:
            l = []
            for i in g:
                for k in d1[i]:
                    if k not in g:
                        l.append([i, k, d1[i][k]])
            c1 = sorted(l, key=lambda x: x[2])
            for i in c1:
                l = cyc[i[0]]
                k = cyc[i[1]]
                cycle(i[0], i[1])
                if p[-1] != 0:
                    g.append(i[1])
                    edges.append((i[0], i[1],i[2]))
                    break
                else:
                    cyc[i[0]] = l
                    cyc[i[1]] = k
            return prim_mst(g)

  mst = prim_mst([0])
  d2={}
  for i in edges:
        if i[0] in d2 and i[1] in d2:
            d2[i[0]][i[1]]=i[2]
            d2[i[1]][i[0]]=i[2]
        elif i[0] in d2 and i[1] not in d2:
            d2[i[0]][i[1]]=i[2]
            d2[i[1]]={i[0]:i[2]}
        elif i[0] not in d2 and i[1] in d2:
            d2[i[0]]={i[1]:i[2]}
            d2[i[1]][i[0]]=i[2]
        else:
            d2[i[0]]={i[1]:i[2]}
            d2[i[1]]={i[0]:i[2]}
            
            
  priority_queue=[]

   
  def dfs(stack,dest):
        global min_area
        if dest in stack[0]:
            wat=0
            fac=0
            for i in stack[0]:
                if places[i].split()[0]=="RIVER":
                    wat+=1
                elif places[i].split()[0]!="RIVER" and i!=dest:
                    fac+=1
            k=stack[1]
            stack.pop(-1)
            stack.append(wat)
            stack.append(fac)
            stack.append(k)
            heapq.heappush(priority_queue,Node(stack))
            return
        else: 
         for i in d2:
            if i==stack[0][-1]:
                for j in d2[i]:
                    if j not in stack[0]:
                        k=copy.deepcopy(stack)
                        k[0].append(j)
                        k[1]+=d2[i][j]
                        dfs(k,dest)
  dest=places.index("RESIDENTIAL LOCATION")
  sources=[places.index(i) for i in places if "RIVER" in i]
  for i in sources:
        dfs([[i],0],dest)
  blue=[]
  k=priority_queue[0].val[0]
  for i in range(len(k)-1):
      blue.append([k[i],k[i+1]])
  red=[list(edges[i][0:2]) for i in range(len(edges)) 
       if list(edges[i][0:2]) not in blue]
  
  global data
  return mst,blue,red


"""def calculate_distance(lat1, lon1, lat2, lon2):
    api_key = "AIzaSyD4UgJKbfoZZWJCE11UA-4mGRaNc68prDI"
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={lat1},{lon1}&destinations={lat2},{lon2}&key={api_key}"###

    response = requests.get(url)
    data = json.loads(response.text)

   
    if data["status"] == "OK":#atleat one 
      
        if len(data["rows"]) > 0 and len(data["rows"][0]["elements"]) > 0:
            distance = data["rows"][0]["elements"][0]["distance"]["value"]
            distance_km = distance / 1000
            return distance_km
        else:
            raise ValueError("No distance data available.")
    else:
        raise ValueError("Invalid API response.")"""
def calculate_distance(lat1, lon1, lat2, lon2):
    url = f"http://router.project-osrm.org/route/v1/walking/{lon1},{lat1};{lon2},{lat2}"

    response = requests.get(url)
    data = response.json()

    if "routes" in data and len(data["routes"]) > 0:
        distance_m = data["routes"][0]["distance"]
        distance_km = distance_m / 1000
        return distance_km
    else:
        raise ValueError("Invalid API response.")

def get_place_coordinates(place):
    
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": place, "key": "AIzaSyCsJp9BP-TpdqL2xrIOwuK-oRdX_rZn2gE"}  ####
    response = requests.get(url, params=params)
    data = response.json()

    
    if data["status"] == "OK":
        location = data["results"][0]["geometry"]["location"]
        latitude = location["lat"]
        longitude = location["lng"]
        return latitude, longitude
    else:
        return None

def search_category(latitude, longitude, category, radius):
   
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{latitude},{longitude}",
        "radius": radius,
        "type": category,
        "key": "AIzaSyCsJp9BP-TpdqL2xrIOwuK-oRdX_rZn2gE" 
    }
    response = requests.get(url, params=params)
    data = response.json()

    # Extract the relevant information from the response
    places = []
    if data["status"] == "OK":
        for result in data["results"]:
            place_name = result["name"]
            place_location = [result["geometry"]["location"]["lat"], result["geometry"]["location"]["lng"]]
            places.append((place_name, place_location))
    return places
def filter_industries(industries):
    freq=len(industries)//8
    new_industries=[]
    for i in range(0,len(industries),freq):
        new_industries.append(industries[i])
    return new_industries    
def filter_water_bodies(water_bodies):
    
    water_bodies = [(name, location) for name, location in water_bodies if any(word in name.lower() for word in ["lake", "pond", "water","river","canal","bay","sea","swamp","cove","moat","marsh","cove","ocean"])]
    water_bodies = [(name, location) for name, location in water_bodies if "temple" not in name.lower()]
    water_bodies = [(name, location) for name, location in water_bodies if "tank" not in name.lower()]
    return water_bodies
def get_water_bodies(latitude, longitude, radius):
    water_bodies = []
    c=0
    while len(water_bodies) < 3:
       if radius>=10000:
           c=1
           break
       if len(water_bodies)<3: 
        water_bodies = search_category(latitude, longitude, "natural_feature", radius)
        radius += 500  
       elif len(water_bodies)  >5:
           water_bodies = search_category(latitude, longitude, "natural_feature", radius)
           radius -= 500
       water_bodies=filter_water_bodies(water_bodies)  
    if c==0:  
     return water_bodies,radius
    else:
        return None,radius

def search_places(place):
    global data
    coordinates = get_place_coordinates(place)
    
    if not coordinates:
        print("Invalid place name or unable to retrieve coordinates.")
        return

    latitude, longitude = coordinates
    print("------",place,latitude,longitude)
    res_location={place:[latitude,longitude]}
  
    radius = 2000  # 2km
    
    water_bodies,radius= get_water_bodies(latitude, longitude, radius)# to change in fromt end
    
    data=json.dumps(data)
    if water_bodies==None:
        data=["no body"]
        data=json.dumps(data)
       
    if water_bodies!=None:    
        water_bodies=filter_water_bodies(water_bodies) 
        industries = search_category(latitude, longitude, "industries", radius)
        industries=filter_industries(industries)
        industries.pop(0)



        industries_dict = {name: location for name, location in industries}
      
        
        water_bodies_dict = {name: location for name, location in water_bodies}
        
        
        
        print("phase2")  
       

        category_list=[]
         
      

        final_dict={}
        
        final_dict.update(water_bodies_dict)
        final_dict.update(industries_dict)
        final_dict.update(res_location)
        
        

          
        
        l=[i for i in final_dict.values()]
        
        node_representation={i:l for i in range(len(l))}
        a=res_location.values()
        
        for i in l:
            
            if i in water_bodies_dict.values():
                category_list.append('RIVER')
            elif i in res_location.values():
                 category_list.append("RESIDENTIAL LOCATION")     
            elif i in industries_dict.values():
                category_list.append('FACTORY') 
           
           
        
        distance={}
        for i,j in node_representation.items():
            li=[]
            for m in (j):
                    dist=calculate_distance(l[i][0],l[i][1],m[0],m[1]) 
                    li.append(math.ceil(dist))
            distance[i]=li   
        dict={}
        
            
        mst,blue,red=calculate_mst(distance,category_list) 
        for i in mst:
            ind=l[i]
        
            a=list(final_dict.keys())    
            b=list(final_dict.values())
            c=b.index(ind)
            d=a[c]
            dict[d]=ind 

        print("L",l)
        print("final_fict",final_dict)
        print("mst: ",mst)
        print("blue: ",blue)
        print("red",red)
        print("dict",dict)
        names=list(final_dict.keys())
        data=[names,l,blue,red]
        print("data",data)
        data=json.dumps(data)
      
        return industries_dict,  water_bodies_dict

    
#data=json.dumps([])
b=time.time()

if __name__ == "__main__":
    """user = Users(username="v1", password="hi")
    db.session.add(user)
    db.session.commit()"""
    app.run()