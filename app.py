import flask
import logging
import pickle
import pandas as pd
from datetime import datetime
import random
app = flask.Flask(__name__)

logging.basicConfig(filename = 'FlaskApp.log',level = logging.INFO)
crop_name = ""
#Create subprocess and call the other function to generate images
@app.route('/crop',methods = ['GET'])
def PredictCrop():
    try:
        random.seed(datetime.now())
        #print("inside")
        # print(flask.request.headers)
        #req_data=flask.request.get_json()
        a = {}
        #API call from shivu to get temp and humidity
        temperature = random.randint(15,55)
        humidity = random.randint(15,70)
        ph = float(random.uniform(4.5,7.25))
        rainfall = float(random.uniform(100,130))
        a['temperature']= temperature
        a['humidity'] = humidity
        '''   a['ph'] = float(req_data['pH'])
        a['rainfall'] = req_data['rainfall']'''
        a['ph'] = ph
        a['rainfall'] = rainfall
        new_df = pd.DataFrame(a, columns = ['temperature','humidity','ph','rainfall'],index = [0])
        NB_pkl_filename = 'NBClassifier.pkl'
        NB_pkl = open(NB_pkl_filename, 'rb')
        NB_model = pickle.load(NB_pkl)
        global crop_name
        crop_name = NB_model.predict(new_df)[0]
        #Return crop name
        print(crop_name)
        return crop_name
    except Exception as e:
        return "Caught err "+str(e)

@app.route('/fertilizer',methods = ['POST'])
def FertRecommend():
    req_data=flask.request.get_json()
    ns = req_data['N']
    ps = req_data['P']
    ks = req_data['K']
    pHs = req_data['pH']
    global crop_name
    crop = crop_name
    #Get NPK values from data set as nr,pr,kr,phr
    try:
        df = pd.read_csv('fert_data.csv')
        values = df[df['crop'] == crop_name]
        nr = values['N'][0]
        pr = values['P'][0]
        kr = values ['K'][0]
    except:
        nr = 80
        pr = 40
        kr = 40
        pHr = 5.5
    
    n = nr - ns
    p = pr - ps
    k = kr - ks
    pH = pHr - pHs
    string = ""
    if pH > 0 :
        string+="""\n\n The ph value of your soil is low.\n\n Please consider the following suggestions.\n\n
    • Use organic materials.
    • Consider applying sulphur. Another way to increase your soil’s acidity gradually is by adding sulphur. The effectiveness of sulphur depends on a number of factors, including moisture, temperature, and bacteria. Because these factors can be unpredictable, the ability of sulphur to lower a soil’s pH can take several months.
    • Think about adding aluminium sulphate. This compound instantly makes the soil more acidic due to a chemical reaction involving aluminium. Because of this, many amateur and small-scale gardeners prefer aluminium sulphate to organic compounds or plain sulphur. 
    • Rinse your plants after application. If the sulphur or aluminium sulphate gets on the leaves of your plants, you will need to rinse it off with a hose. Failure to rinse them off can result in burns to the leaves and damage to your plants. Watering your plants will also help the compounds set.\n\n\n"""
    elif pH < 0:
        string+="""\n\n\nThe ph value of your soil is high and might not be good for your crop. Please consider the following suggestions.\n\n\n
    • Pick a liming material. If you have tested your soil and found that it is too acidic, you can raise the pH by adding a base. The most common materials used to increase the pH of soil are compounds made from powdered limestone, or lime, which you can find at most home and garden store.
    • Think about using wood ashes. The ash of burned trees is also quite basic and can add micronutrients like calcium, potassium, phosphate, and boron. Wood ash is not as effective as lime. However, it can dramatically increase a soil’s pH over time. 
    • Apply the liming source. In order to get the best results, you will want to till the liming material into the soil about two to three months before planting (usually in the fall or winter) so that there is plenty of time for the pH to change. The lime should be tilled into the soil’s the root zone or the top 7 inches (18 cm) of soil.
    • Water the soil regularly. Lime will have little effect on dry soils, so you will need to apply water regularly. Water activates the lime and helps it seep into the soil. Use a garden hose or sprinkler to apply water.\n\n\n
"""
    else:
        string+="\n\n\npH value is in optimum condition. Incase you add fertilizers, please make sure you don't change the acidity of the soil.\n\n\n"
    
    if n > 0 :
        string+="""\n\n\nThe N value of your soil is low. Please consider the following suggestions.\n\n\n
    • Add sawdust or fine woodchips to your soil – the carbon in the sawdust/woodchips love nitrogen and will help absorb and soak up and excess nitrogen.
    • Plant heavy nitrogen feeding plants – tomatoes, corn, broccoli, cabbage and spinach are examples of plants that thrive off nitrogen and will suck the nitrogen dry.
    • Water – soaking your soil with water will help leach the nitrogen deeper into your soil, effectively leaving less for your plants to use.
    • Sugar – In limited studies, it was shown that adding sugar to your soil can help potentially reduce the amount of nitrogen is your soil. Sugar is partially composed of carbon, an element which attracts and soaks up the nitrogen in the soil. This is similar concept to adding sawdust/woodchips which are high in carbon content.
    • Do nothing – It may seem counter-intuitive, but if you already have plants that are producing lots of foliage, it may be best to let them continue to absorb all the nitrogen to amend the soil for your next crops.\n\n\n"""
    elif n < 0:
        string+="""\n\n\n The N value of soil is high and might give rise to weeds. Please consider the following suggestions.
    1. Manure – adding manure is one of the simplest ways to amend your soil with nitrogen. Be careful as there are various types of manures with varying degrees of nitrogen.
    2. Coffee grinds – use your morning addiction to feed your gardening habit! Coffee grinds are considered a green compost material which is rich in nitrogen. Once the grounds break down, your soil will be fed with delicious, delicious nitrogen. An added benefit to including coffee grounds to your soil is while it will compost, it will also help provide increased drainage to your soil.
    3. Plant nitrogen fixing plants – planting vegetables that are in Fabaceae family like peas, beans and soybeans have the ability to increase nitrogen in your soil
    4. Plant ‘green manure’ crops"""
    else:
        string+='N value is in optimum condition. Incase you add fertilizers, please add 0-P-K'
    
    if p < 0 :
        string+="""\n\n\n The P value of your crop is high. \n\n\n• Avoid adding manure – manure contains many key nutrients for your soil but typically including high levels of phosphorous. Limiting the addition of manure will help reduce phosphorus being added.
    • Use only phosphorus-free fertilizer – if you can limit the amount of phosphorous added to your soil, you can let the plants use the existing phosphorus while still providing other key nutrients such as Nitrogen and Potassium. Find a fertilizer with numbers such as 10-0-10, where the zero represents no phosphorous.
    • Water your soil – soaking your soil liberally will aid in driving phosphorous out of the soil. This is recommended as a last ditch effort."""
    elif p > 0:
            string+="""\n\n\n The P value of your crop is low. Please consider the following options.\n\n\n
    1. Bone meal – a fast acting source that is made from ground animal bones which is rich in phosphorous.
    2. Rock phosphate – a slower acting source where the soil needs to convert the rock phosphate into phosphorous that the plants can use.
    3. Phosphorus Fertilizers – applying a fertilizer with a high phosphorous content in the NPK ratio (example: 10-20-10, 20 being phosphorous percentage)
    4. Organic compost – adding quality organic compost to your soil will help increase phosphoos content
    5. Manure – as with compost, manure can be an excellent source of phosphorous for your plants
    6. Clay soil – introducing clay particles into your soil can help retain & fix phosphorus deficiencies.
    7. Ensure proper soil pH – having a pH in the 6.0 to 7.0 range has been scientifically proven to have the optimal phosphorus uptake in plants"""
    else:
        string+='P value is in optimum condition. Incase you add fertilizers, please add N-0-K'            
    
    if k > 0 :
        string+="""
    • Loosen the soil deeply with a shovel, and water thoroughly to dissolve water-soluble potassium. Allow the soil to fully dry, and repeat digging and watering the soil two or three more times.
    • Sift through the soil, and remove as many rocks as possible, using a soil sifter. Minerals occurring in rocks such as mica and feldspar slowly release potassium into the soil slowly through weathering.
    • Stop applying potassium-rich commercial fertilizer. Apply only commercial fertilizer that has a '0' in the final number field. Commercial fertilizers use a three number system for measuring levels of nitrogen, phosphorous and potassium. The last number stands for potassium. Another option is to stop using commercial fertilizers all together and to begin using only organic matter to enrich the soil.
    • Mix crushed eggshells, crushed seashells, wood ash or soft rock phosphate to the soil to add calcium. Mix in up to 10 percent of organic compost to help amend and balance the soil.
"""
    elif k < 0 :
        string+="""
    • Mix in muricate of potash or sulphate of potash
    • Try kelp meal or seaweed
    • Try Sul-Po-Mag
"""
    else:
        string+='K value is in optimum condition. Incase you add fertilizers, please add N-P-0'
    
    return string   


@app.route('/',methods=['GET'])
def hello():
    return "Process is up and runnning."


app.run(port = 5555, host='0.0.0.0')
