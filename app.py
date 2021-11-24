from flask import Flask, request, jsonify, render_template

import util

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/predict', methods=['GET', 'POST'])
def predict_visibility():
    util.load_saved_artifacts()
    if request.method == 'POST':
        temp = float(request.form['temperature'])
        hum = float(request.form['humidity'])
        hum = hum / 100
        ws = float(request.form['wind_speed'])
        wb = float(request.form['wind_bearing'])
        pressure = float(request.form['pressure'])
        month = int(request.form['month'])
        weather = request.form['weather']

        prediction = util.get_predicted_visibility(temp, hum, ws, wb, pressure, month, weather)

        emoji = "😇" if prediction > 8 else "😕"

        return render_template("prediction.html", prediction_text=f"Visible Distance is {prediction} KM  {emoji}")
    else:
        months = list(range(1, 13))
        return render_template("prediction.html", weather_options=util.get_weathers(), months=months)


if __name__ == "__main__":
    app.run(debug=True)
    # print(util.__data_columns)   # just to make sure if everything running fine
