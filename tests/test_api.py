import unittest
import nightscout
from datetime import datetime
from dateutil.tz import tzutc
from httmock import all_requests, HTTMock
import pytz

@all_requests
def sgv_response(url, request):
    return '[{"_id":"58be818183ab6d6632419687","sgv":184,"date":1488879925000,"dateString":"2017-03-07T09:45:25.000Z","trend":3,"direction":"FortyFiveUp","device":"share2","type":"sgv"},{"_id":"58be805583ab6d6632419684","sgv":168,"date":1488879625000,"dateString":"2017-03-07T09:40:25.000Z","trend":3,"direction":"FortyFiveUp","device":"share2","type":"sgv"},{"_id":"58be7f2983ab6d6632419681","sgv":169,"date":1488879325000,"dateString":"2017-03-07T09:35:25.000Z","trend":3,"direction":"FortyFiveUp","device":"share2","type":"sgv"}]'

def treatments_response(url, request):
    return '[{"_id":"58be816483ab6d6632419686","temp":"absolute","enteredBy":"loop://Riley\'s iphone","eventType":"Temp Basal","created_at":"2017-03-07T09:38:35Z","timestamp":"2017-03-07T09:38:35Z","absolute":0.7,"rate":0.7,"duration":30,"carbs":null,"insulin":null},{"_id":"58be803d83ab6d6632419683","temp":"absolute","enteredBy":"loop://Riley\'s iphone","eventType":"Temp Basal","created_at":"2017-03-07T09:33:30Z","timestamp":"2017-03-07T09:33:30Z","absolute":1.675,"rate":1.675,"duration":30,"carbs":null,"insulin":null},{"_id":"58be7f0d83ab6d6632419680","temp":"absolute","enteredBy":"loop://Riley\'s iphone","eventType":"Temp Basal","created_at":"2017-03-07T09:28:30Z","timestamp":"2017-03-07T09:28:30Z","absolute":1.775,"rate":1.775,"duration":30,"carbs":null,"insulin":null}]'

def profile_response(url, request):
    return '[{"_id":"58c0e02447d5af0c00e37593","defaultProfile":"Default","store":{"Default":{"dia":"4","carbratio":[{"time":"00:00","value":"20","timeAsSeconds":"0"},{"time":"06:00","value":"10","timeAsSeconds":"21600"},{"time":"11:00","value":"18","timeAsSeconds":"39600"},{"time":"16:00","value":"12","timeAsSeconds":"57600"},{"time":"21:00","value":"18","timeAsSeconds":"75600"}],"carbs_hr":"20","delay":"20","sens":[{"time":"00:00","value":"90","timeAsSeconds":"0"},{"time":"06:00","value":"85","timeAsSeconds":"21600"},{"time":"09:00","value":"95","timeAsSeconds":"32400"}],"timezone":"US/Central","basal":[{"time":"00:00","value":"0.45","timeAsSeconds":"0"},{"time":"02:00","value":"0.3","timeAsSeconds":"7200"},{"time":"04:30","value":"0.45","timeAsSeconds":"16200"},{"time":"07:00","value":"0.6","timeAsSeconds":"25200"},{"time":"10:00","value":"0.4","timeAsSeconds":"36000"},{"time":"12:00","value":"0.4","timeAsSeconds":"43200"},{"time":"15:00","value":"0.4","timeAsSeconds":"54000"},{"time":"17:00","value":"0.4","timeAsSeconds":"61200"},{"time":"20:30","value":"0.4","timeAsSeconds":"73800"}],"target_low":[{"time":"00:00","value":"110","timeAsSeconds":"0"}],"target_high":[{"time":"00:00","value":"130","timeAsSeconds":"0"}],"startDate":"1970-01-01T00:00:00.000Z","units":"mg/dl"},"Test2":{"dia":"4","carbratio":[{"time":"00:00","value":"20","timeAsSeconds":"0"},{"time":"06:00","value":"10","timeAsSeconds":"21600"},{"time":"11:00","value":"18","timeAsSeconds":"39600"},{"time":"16:00","value":"12","timeAsSeconds":"57600"},{"time":"21:00","value":"18","timeAsSeconds":"75600"}],"carbs_hr":"20","delay":"20","sens":[{"time":"00:00","value":"90","timeAsSeconds":"0"},{"time":"06:00","value":"85","timeAsSeconds":"21600"},{"time":"09:00","value":"95","timeAsSeconds":"32400"}],"timezone":"US/Central","basal":[{"time":"00:00","value":"0.45","timeAsSeconds":"0"},{"time":"02:00","value":"0.3","timeAsSeconds":"7200"},{"time":"04:30","value":"0.45","timeAsSeconds":"16200"},{"time":"07:00","value":"0.6","timeAsSeconds":"25200"},{"time":"10:00","value":"0.4","timeAsSeconds":"36000"},{"time":"12:00","value":"0.4","timeAsSeconds":"43200"},{"time":"15:00","value":"0.4","timeAsSeconds":"54000"},{"time":"17:00","value":"0.4","timeAsSeconds":"61200"},{"time":"20:30","value":"0.4","timeAsSeconds":"73800"}],"target_low":[{"time":"00:00","value":"110","timeAsSeconds":"0"}],"target_high":[{"time":"00:00","value":"130","timeAsSeconds":"0"}],"startDate":"1970-01-01T00:00:00.000Z","units":"mg/dl"}},"startDate":"2017-03-24T03:54:00.000Z","mills":"1489035240000","units":"mg/dl","created_at":"2016-10-31T12:58:43.800Z"},{"_id":"58b7777cdfb94b0c00366c7e","defaultProfile":"Default","store":{"Default":{"dia":"4","carbratio":[{"time":"00:00","value":"20","timeAsSeconds":"0"},{"time":"06:00","value":"10","timeAsSeconds":"21600"},{"time":"11:00","value":"18","timeAsSeconds":"39600"},{"time":"16:00","value":"12","timeAsSeconds":"57600"},{"time":"21:00","value":"18","timeAsSeconds":"75600"}],"carbs_hr":"20","delay":"20","sens":[{"time":"00:00","value":"90","timeAsSeconds":"0"},{"time":"06:00","value":"85","timeAsSeconds":"21600"},{"time":"09:00","value":"95","timeAsSeconds":"32400"}],"timezone":"US/Central","basal":[{"time":"00:00","value":"0.45","timeAsSeconds":"0"},{"time":"02:00","value":"0.3","timeAsSeconds":"7200"},{"time":"04:30","value":"0.45","timeAsSeconds":"16200"},{"time":"07:00","value":"0.6","timeAsSeconds":"25200"},{"time":"10:00","value":"0.4","timeAsSeconds":"36000"},{"time":"12:00","value":"0.4","timeAsSeconds":"43200"},{"time":"15:00","value":"0.4","timeAsSeconds":"54000"},{"time":"17:00","value":"0.6","timeAsSeconds":"61200"},{"time":"20:30","value":"0.6","timeAsSeconds":"73800"}],"target_low":[{"time":"00:00","value":"110","timeAsSeconds":"0"}],"target_high":[{"time":"00:00","value":"130","timeAsSeconds":"0"}],"startDate":"1970-01-01T00:00:00.000Z","units":"mg/dl"}},"startDate":"2017-03-02T01:37:00.000Z","mills":"1488418620000","units":"mg/dl","created_at":"2016-10-31T12:58:43.800Z"},{"_id":"5719b2aa5c3e080b000dbfb1","defaultProfile":"Default","store":{"Default":{"dia":"4","carbratio":[{"time":"00:00","value":"18","timeAsSeconds":"0"},{"time":"06:00","value":"10","timeAsSeconds":"21600"},{"time":"11:00","value":"18","timeAsSeconds":"39600"},{"time":"16:00","value":"12","timeAsSeconds":"57600"},{"time":"21:00","value":"18","timeAsSeconds":"75600"}],"carbs_hr":"20","delay":"20","sens":[{"time":"00:00","value":"90","timeAsSeconds":"0"},{"time":"06:00","value":"85","timeAsSeconds":"21600"},{"time":"09:00","value":"95","timeAsSeconds":"32400"}],"timezone":"US/Central","basal":[{"time":"00:00","value":"0.45","timeAsSeconds":"0"},{"time":"02:00","value":"0.3","timeAsSeconds":"7200"},{"time":"04:30","value":"0.45","timeAsSeconds":"16200"},{"time":"07:00","value":"0.6","timeAsSeconds":"25200"},{"time":"10:00","value":"0.4","timeAsSeconds":"36000"},{"time":"12:00","value":"0.4","timeAsSeconds":"43200"},{"time":"15:00","value":"0.4","timeAsSeconds":"54000"},{"time":"17:00","value":"0.6","timeAsSeconds":"61200"},{"time":"20:30","value":"0.6","timeAsSeconds":"73800"}],"target_low":[{"time":"00:00","value":"110","timeAsSeconds":"0"}],"target_high":[{"time":"00:00","value":"130","timeAsSeconds":"0"}],"startDate":"1970-01-01T00:00:00.000Z","units":"mg/dl"}},"startDate":"2016-04-22T05:06:00.000Z","mills":"1461301560000","units":"mg/dl","created_at":"2016-10-31T12:58:43.800Z"}]'

def devicestatus_response(url, request):
    return '[{"_id":"6026cdc76f861d31a","device":"50F","openaps":{"suggested":{"temp":"absolute","bg":88,"tick":"+1","eventualBG":85,"insulinReq":0,"deliverAt":"2021-02-12T18:49:42.849Z","sensitivityRatio":1,"predBGs":{"IOB":[88,88,88,87,86,84,82,80,77],"ZT":[88,78,69,60,51,43,39,39,39,39],"COB":[88,89,89,90,91,91,92,93,94,95,96,96]},"COB":29.567142857142855,"IOB":3.726,"reason":"COB: 29.567142857142855, Dev: 66, BGI: -10, ISF: 35, CR: 7.5, Target: 108, minPredBG 49, minGuardBG 85, IOBpredBG 39, COBpredBG 85; Eventual BG 85 < 90, setting 60m zero temp. ","duration":60,"rate":0,"timestamp":"2021-02-12T18:49:42Z"},"iob":{"iob":3.726,"basaliob":0,"activity":0.0568,"time":"2021-02-12T18:49:42Z"}},"uploaderBattery":25,"created_at":"2021-02-12T18:49:42Z","NSCLIENT_ID":"1613155782893"}]'

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.api = nightscout.Api('http://testns.example.com')

    def test_get_sgv(self):
        with HTTMock(sgv_response):
            entries = self.api.get_sgvs()

        self.assertEqual(3, len(entries))
        self.assertEqual(184, entries[0].sgv)
        self.assertEqual("FortyFiveUp", entries[0].direction)
        self.assertEqual(datetime(2017, 3, 7, 9, 45, 25, tzinfo=tzutc()), entries[0].date)

    def test_get_treatments(self):
        with HTTMock(treatments_response):
            treatments = self.api.get_treatments()

        self.assertEqual(3, len(treatments))
        self.assertEqual("absolute", treatments[0].temp)
        self.assertEqual("Temp Basal", treatments[0].eventType)
        timestamp = datetime(2017, 3, 7, 9, 38, 35, tzinfo=tzutc())
        self.assertEqual(timestamp, treatments[0].timestamp)
        self.assertEqual(timestamp, treatments[0].created_at)

    def test_get_profile(self):
        with HTTMock(profile_response):
            profile_definition_set = self.api.get_profiles()

        profile_definition = profile_definition_set.get_profile_definition_active_at(datetime(2017, 3, 5, 0, 0, tzinfo=tzutc()))
        self.assertEqual(datetime(2017, 3, 2, 1, 37, tzinfo=tzutc()), profile_definition.startDate)

        profile = profile_definition.get_default_profile()
        self.assertEqual(pytz.timezone('US/Central'), profile.timezone)
        self.assertEqual(4, profile.dia)

        five_thirty_pm = datetime(2017, 3, 24, 17, 30)
        five_thirty_pm = profile.timezone.localize(five_thirty_pm)
        self.assertEqual(0.6, profile.basal.value_at_date(five_thirty_pm))

    def test_get_cob_iob(self):
        with HTTMock(devicestatus_response):
            cob, iobpred, iob = self.api.get_cob_iob()
        print(cob)
        print(iobpred)
        print(iob)

if __name__ == '__main__':
    unittest.main()
