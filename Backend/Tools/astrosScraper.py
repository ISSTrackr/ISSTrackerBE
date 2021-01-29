import json
import requests
from Backend.Requests import astrosOnISS
from Backend.Tools.AstrosJsonLoader import process
import os
def getAstroObject(name):
    # get image url
    headers = {
        "apikey": os.environ['apiKey']}

    params = (
        ("q", name),
        ("tbm", "isch"),
    );
    response = requests.get('https://app.zenserp.com/api/v2/search', headers=headers, params=params);
    responseJson = json.loads(response.text)
    links = responseJson['image_results']
    hits = []

    for link in links:
        if str(link).__contains__('Astronaut'):
            hits.append(link['sourceUrl'])

    imageUrl = hits[0]

    #     get nationality
    params = (
        ("q", name + ' nationality'),
    );
    response = requests.get('https://app.zenserp.com/api/v2/search', headers=headers, params=params);
    responseJson = json.loads(response.text)
    nationality = responseJson['answer_box']['answer']

    #     get flag image
    params = (
        ("q", nationality + ' flag'),
        ("tbm", "isch"),
        ("gl", "DE"),
    );
    response = requests.get('https://app.zenserp.com/api/v2/search', headers=headers, params=params);
    responseJson = json.loads(response.text)
    flagUrl = responseJson['image_results'][0]['sourceUrl']
    return {'name': name, 'picture': imageUrl, 'nation': nationality, 'flag': flagUrl}

#
file = open("./astros_pics_flags_nations.json")
data = json.load(file)
file.close()
astrosInDB = data["astros"]
astrosOnISS = astrosOnISS.getAstrosOnISS()
nameList = []

for astroInDB in astrosInDB:
    nameList.append(astroInDB["name"])

newAstroDetected = False

for astro in astrosOnISS:
    if astro not in nameList:
        newAstroDetected = True
        astroObject = getAstroObject(astro)
        data["astros"].append(astroObject)

if newAstroDetected:
    # overwrite json with new data including new astronauts
    file = open("./astros_pics_flags_nations.json", "w")
    file.write(json.dumps(data))
    file.close()
    file = open(r"astros_pics_flags_nations.json")
    data = json.load(file)
    process(data)
