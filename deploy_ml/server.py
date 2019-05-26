"""Filename: server.py
"""

import os
import pandas as pd
from sklearn.externals import joblib
from flask import Flask, jsonify, request, render_template
import dill as pickle

app = Flask(__name__)


# @app.route('/')
# def index():
    # return render_template('index.html', name='Samit')

@app.route('/', methods=['post', 'get'])
def apicall():
    """API Call

    Pandas dataframe (sent as a payload) from API Call
    """
    data = ""
    if request.method == 'POST' :
        test_json = request.get_json()
        test = pd.read_json(test_json, orient='records')

        # To resolve the issue of TypeError: Cannot compare types 'ndarray(dtype=int64)' and 'str'
        # test['Dependents'] = [str(x) for x in list(test['Dependents'])]

        #Getting the Loan_IDs separated out
        loan_ids = test['Loan_ID']
 
        clf = 'model_v1.pk'

        if test.empty:
            return(bad_request())
        else:
            #Load the saved model
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
        # responses = jsonify(predictions=final_predictions.to_json(orient="records"))
        # responses.status_code = 200
      
        # return (responses)
        print ("\n \n \n rendering_webpage \n \n")
        data = final_predictions.to_html()
        # return render_template("api_call.html", name="Samit", data=final_predictions.to_html())
        
   
    # return render_template("predict_get.html")
    return render_template("api_call.html", data = data)

if __name__ == "__main__":
	app.run(host="127.0.0.1", debug=True)
