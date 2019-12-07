from requests_html import HTMLSession
import simplejson as json
import re


class Carrier:
    url1 = 'https://www.cd.cz/spojeni-a-jizdenka/'
    url2 = 'https://www.cd.cz/spojeni-a-jizdenka/spojeni-tam/'

    def __init__(self):
        pass

    def get_journeys(self, source, destination, departure_date):
        post_data = {
            "ttCombination": 25,
            "formType": 1,
            "isReturnOnly": False,
            "stations[from][listID]": 100003,
            "stations[from][name]": source,
            "stations[from][errorName]": "From",
            "stations[to][listID]": 1,
            "stations[to][name]": destination,
            "stations[to][errorName]": "To",
            "stations[isViaChange]": False,
            "services[bike]": False,
            "services[children]": False,
            "services[wheelChair]": False,
            "services[refreshment]": False,
            "services[carTrain]": False,
            "services[silentComp]": False,
            "services[ladiesComp]": False,
            "services[powerSupply]": False,
            "services[wiFi]": False,
            "services[inSenior]": False,
            "services[serviceClass]": "Class2",
            "dateTime[isReturn]": False,
            "dateTime[date]": departure_date.replace('-', '.'),
            "dateTime[time]": "00:00",
            "dateTime[isDeparture]": True,
            "dateTime[dateReturn]": "8.12.2018",
            "dateTime[timeReturn]": "11:40",
            "dateTime[isDepartureReturn]": True,
            "params[onlyDirectConnections]": False,
            "params[onlyConnWithoutRes]": False,
            "params[useBed]": "NoLimit",
            "params[deltaPMax]": -1,
            "params[maxChanges]": 4,
            "params[minChangeTime]": -1,
            "params[maxChangeTime]": 240,
            "params[onlyCD]": False,
            "params[onlyCDPartners]": True,
            "params[historyTrain]": False,
            "params[psgOwnTicket]": False,
            "params[addServiceReservation]": False,
            "params[addServiceDog]": False,
            "params[addServiceBike]": False,
            "params[addServiceSMS]": False,
            "passengers[passengers][0][id]": 1,
            "passengers[passengers][0][typeID]": 5,
            "passengers[passengers][0][count]": 1,
            "passengers[passengers][0][age]": -1,
            "passengers[passengers][0][ageState]": 0,
            "passengers[passengers][0][cardIDs]": "",
            "passengers[passengers][0][isFavourite]": False,
            "passengers[passengers][0][isDefault]": False,
            "passengers[passengers][0][isSelected]": True,
            "passengers[passengers][0][nickname]": "",
            "passengers[passengers][0][phone]": "",
            "passengers[passengers][0][cardTypeID]": 0,
            "passengers[passengers][0][fullname]": "",
            "passengers[passengers][0][cardNumber]": "",
            "passengers[passengers][0][birthdate]": "",
            "passengers[passengers][0][avatar]": "",
            "passengers[passengers][0][image]": ""
        }
        session = HTMLSession()
        guid_request = session.post(self.url1, data=post_data)
        json_obj = json.loads(guid_request.text)

        guid = json_obj['guid']
        self.url2 = f'{self.url2}{guid}'
        connections_request = session.get(self.url2)
        json_trains = json.loads(re.findall(r"var model = (.*)", connections_request.text)[0][:-2])

        trains = []
        for item in json_trains['list']:
            train = item['trains'][0]
            train_data = {
                'departure_datetime': '{} {}'.format(train['depDate'], train['depTime']),
                'arrival_datetime': '{} {}'.format(train['arrDate'], train['arrTime']),
                'source': train['from'],
                'destinations': train['to'],
                'distance': train['distance'],
                'price': item['price']['price']
            }
            trains.append(train_data)

        return trains
