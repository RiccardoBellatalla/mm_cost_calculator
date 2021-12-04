#remember that when you add something in the .html format you MUST add the variable = request.form['etc'] in the @app.route

import os, json
from flask import Flask, render_template, request, json #, current_app as ap
app = Flask(__name__)

# static/data/test_data.json
#filename = os.path.join(app.static_folder, 'data', 'dispatch_fees.json')
#with open(filename) as dispatch_fees:
#    data = json.load(dispatch_fees)

# read file
#with open("test.json") as jsonFile:
#    jsonObject = json.load(jsonFile)
#    jsonFile.close()

with open('./static/data/dispatch_fees.json', 'r') as dispatch_fees:
    dispatch_fees = dispatch_fees.read()

with open('./static/data/packaging_type.json', 'r') as packaging_type:
    packaging_txt = packaging_type.read()


# validators
validators_log_limits = {
    'fr' : {
        'max_weight' : 150,
        'max_size' : 160,
    },
    'es' : {
        'max_weight' : 500,
        'max_size' : 180,
    }
}

# test
fr = 'ciao'
@app.route('/test')
def t():
#    print(app.static_folder)
#    print(filename)
    #print(packaging)
    #print(type(packaging))
    #u = json.loads(packaging)
    #print(type(u))
    return fr
# test

@app.route('/')
def main():
    return render_template("app.html")

@app.route("/calculate", methods=['POST'])
def calculate():
    platform_id = 'es'
    num1 = float(request.form['num1'])
    num2 = float(request.form['num2'])
    num3 = float(request.form['num3'])
    weight = float(request.form['weight'])

    if int(num1) >= validators_log_limits[platform_id]['max_size'] : size1_check = 'too large'
    else : size1_check = ''

    if int(num2) >= validators_log_limits[platform_id]['max_size'] : size2_check = 'too large'
    else : size2_check = ''

    if int(num3) >= validators_log_limits[platform_id]['max_size'] : size3_check = 'too large'
    else : size3_check = ''

    if int(weight) >= validators_log_limits[platform_id]['max_weight'] : weight_check = 'too heavy'
    else : weight_check = ''

    longest = max(num1, num2, num3)
    shortest = min(num1, num2, num3)
    medium = (num1 + num2 + num3) - longest - shortest

    packaging = json.loads(packaging_txt)

    if (
        longest < packaging[platform_id]['Standard Parcel']['longest']
        and medium < packaging[platform_id]['Standard Parcel']['medium']
        and shortest < packaging[platform_id]['Standard Parcel']['shortest']
        and (weight + 0.1) < packaging[platform_id]['Standard Parcel']['weight']) :
        parcel_type = 'Standard Parcel'
        if weight <= 1.0 : weight += 0.05
        else : weight += 0.1
    elif (
        longest < packaging[platform_id]['Large Parcel Dimensions']['longest']
        and medium < packaging[platform_id]['Large Parcel Dimensions']['medium']
        and shortest < packaging[platform_id]['Large Parcel Dimensions']['shortest']
        and (weight + 0.25) < packaging[platform_id]['Large Parcel Dimensions']['weight']) :
        parcel_type = 'Large Parcel Dimensions'
        weight += 0.25
    elif (
        longest < packaging[platform_id]['Extra Large Parcel Dimensions']['longest']
        and medium < packaging[platform_id]['Extra Large Parcel Dimensions']['medium']
        and shortest < packaging[platform_id]['Extra Large Parcel Dimensions']['shortest']
        and (weight + 0.25) < packaging[platform_id]['Extra Large Parcel Dimensions']['weight']) :
        parcel_type = 'Extra Large Parcel Dimensions'
        weight += 0.25
    elif (
        longest < packaging[platform_id]['Oversize Parcel Dimensions']['longest']
        and medium < packaging[platform_id]['Oversize Parcel Dimensions']['medium']
        and shortest < packaging[platform_id]['Oversize Parcel Dimensions']['shortest']
        and weight < packaging[platform_id]['Oversize Parcel Dimensions']['weight']) :
        parcel_type = 'Oversize Parcel Dimensions'
        weight += 0.25
    else : parcel_type = ""

    dfees = json.loads(dispatch_fees)
    print(dfees[platform_id]) #to debug
    print(parcel_type)
    print(dfees[platform_id][parcel_type])

    for key, value in dfees[platform_id][parcel_type].items() :
        if float(key) > weight :
            cost_to_dispatch = value
            break

    result = num1 + num2 + num3 + weight
    return render_template('app.html',
                            cost_to_dispatch=cost_to_dispatch,
                            longest=longest,
                            medium=medium,
                            shortest=shortest,
                            weight=weight,
                            result=round(result,3),
                            parcel_type=parcel_type,
                            size1_alert=size1_check,
                            size2_alert=size2_check,
                            size3_alert=size3_check,
                            weight_alert=weight_check)
