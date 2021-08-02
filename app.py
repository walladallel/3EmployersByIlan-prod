import json
from flask import Flask, render_template, request
from datetime import datetime

#Home Work No. 4 - Ilan Elkayam 21/0/7/2021
app = Flask(__name__)


workers_dict = {}
# load workers from the data file
with open('data.txt','r') as file:
    data = file.read()
    # take care of file in case the file is empty
    if data:
        workers_dict = eval(data)


# file synchronized update with html table
def update_workers_file():
    with open('data.txt', 'w') as file:
        file.write(str(workers_dict))


# creates a base route and accepts both GET and POST
@app.route("/", methods = ['GET','POST'])
def index():
    # handle the form data
    if request.method == 'POST':
        data = request.form
        
        # first and last name validation
        first_name = data['first_name'].capitalize()
        last_name = data['last_name'].capitalize()

        # is_smoking checkbox logic
        # it is required for the checkbox to work properly
        is_smoking = False
        if('is_smoking' in data.keys()):
            is_smoking = True
        
        # id formatting and validation
        id = data['ID']
        # try to convert it into a number
        try:
            int(id)
            id = id[:9]
            if(len(id) < 9):
                while len(id) != 9:
                    id = '0' + id
        except Exception:
            print("value isn't a number")
        
        # date formatting and validation
        date = datetime.strptime(data['datetime'],'%Y-%m-%d')
        date = date.strftime('%d/%m/%Y')

        # adds worker to nested dict
        workers_dict[id] = {
            'ID':id,
            'first_name': first_name,
            'last_name': last_name,
            'is_smoking': is_smoking,
            'birthday':date 
        }

        update_workers_file()
        
    # render the page with the workers in the table
    return render_template('index.html',workers_dict=workers_dict)


if __name__ == '__main__':
    app.run(debug=True)