"""Filename: server.py
Takes input test file from local client, processes it in the server, displays result in webpage and provides
a download link to save as csv.
"""
import warnings
warnings.simplefilter('ignore')
import os
import pandas as pd
from sklearn.externals import joblib
from flask import Flask, jsonify, request, render_template, Response, session
import dill as pickle
from form import TestDataForm


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'a really really really really long secret key'
UPLOAD_FOLDER = 'E:/Projects/naive2legend/deploy_ml/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/downloads")
def downloads():
    # On requesting download, download the results as CSV file.
    return Response(session.get('an_object'),
                       mimetype="text/csv",
                       headers={"Content-Disposition":
                                    "attachment;filename=results.csv"})

@app.route('/', methods=['post', 'get'])
def index():
    """API Call

    Pandas dataframe (sent as a payload) from API Call
    """
    # On the first run (a get request) of render_template(data = null) will display 
    # the file_form (choose file box)
    data = ""
    file_form = TestDataForm()
    # if form.validate_on_submit():
    if request.method == 'POST' :
        # Load an already uploaded test file on the server
        # test = pd.read_csv('data/test.csv', encoding="utf-8-sig")

        # as defined in form.py
        file = request.files['File']

        # You can either save a file or read a file
        # Save the file which was uploaded through form, on server
        # filename = "testtttt"
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))     
        # Read the file uploaded from client into a dataframe
        test = pd.read_csv(file)
             
        # To resolve the issue of TypeError: Cannot compare types 'ndarray(dtype=int64)' and 'str'
        # test['Dependents'] = [str(x) for x in list(test['Dependents'])]

        #Getting the Loan_IDs separated out
        loan_ids = test['Loan_ID']
 
        clf = 'model_v1.pk'
    
        print("Loading the model...")
        loaded_model = None
        with open('./models/'+clf,'rb') as f:
            loaded_model = pickle.load(f)

        print("The model has been loaded...doing predictions now...")
        predictions = loaded_model.predict(test)

        """Add the predictions as Series to a new pandas dataframe
                                OR
           Depending on the use-case, the entire test data appended with the new files
        """
        prediction_series = list(pd.Series(predictions))

        final_predictions = pd.DataFrame(list(zip(loan_ids, prediction_series)))

        """We can be as creative in sending the responses.
           But we need to send the response codes as well.
        """
        # When not using forms / calling script from command line at the client side use the below responses
        # responses = jsonify(predictions=final_predictions.to_json(orient="records"))
        # responses.status_code = 200
        # return (responses)

        print ("\n \n \n rendering_webpage \n \n")
        
        # this will be sent to render_template
        data = final_predictions.to_html()
        # session variable will act as our global variable that can store value between different requests
        # we use this value in our download view function, enables to download the results
        session['result'] = final_predictions.to_csv()
        
     # send data as well as the form to the template      
    return render_template("TestDataForm.html", data = data, file_form=file_form)

if __name__ == "__main__":
    # 0.0.0.0 means any ip address can send request to this server, 
    # the server will run on localhost:5000 by default
	app.run(host="0.0.0.0", debug=True)
    
