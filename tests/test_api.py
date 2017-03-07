import unittest
import nightscout
from httmock import all_requests, HTTMock

@all_requests
def sgv_response(url, request):
    return '[{"_id":"58be818183ab6d6632419687","sgv":184,"date":1488879925000,"dateString":"2017-03-07T09:45:25.000Z","trend":3,"direction":"FortyFiveUp","device":"share2","type":"sgv"},{"_id":"58be805583ab6d6632419684","sgv":168,"date":1488879625000,"dateString":"2017-03-07T09:40:25.000Z","trend":3,"direction":"FortyFiveUp","device":"share2","type":"sgv"},{"_id":"58be7f2983ab6d6632419681","sgv":169,"date":1488879325000,"dateString":"2017-03-07T09:35:25.000Z","trend":3,"direction":"FortyFiveUp","device":"share2","type":"sgv"}]'

def treatments_response(url, request):
    return '[{"_id":"58be816483ab6d6632419686","temp":"absolute","enteredBy":"loop://Riley\'s iphone","eventType":"Temp Basal","created_at":"2017-03-07T09:38:35Z","timestamp":"2017-03-07T09:38:35Z","absolute":0.7,"rate":0.7,"duration":30,"carbs":null,"insulin":null},{"_id":"58be803d83ab6d6632419683","temp":"absolute","enteredBy":"loop://Riley\'s iphone","eventType":"Temp Basal","created_at":"2017-03-07T09:33:30Z","timestamp":"2017-03-07T09:33:30Z","absolute":1.675,"rate":1.675,"duration":30,"carbs":null,"insulin":null},{"_id":"58be7f0d83ab6d6632419680","temp":"absolute","enteredBy":"loop://Riley\'s iphone","eventType":"Temp Basal","created_at":"2017-03-07T09:28:30Z","timestamp":"2017-03-07T09:28:30Z","absolute":1.775,"rate":1.775,"duration":30,"carbs":null,"insulin":null}]'

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.api = nightscout.Api('http://testns.example.com')

    def test_get_sgv(self):
        with HTTMock(sgv_response):
            entries = self.api.get_sgvs()

        self.assertEqual(3, len(entries))
        self.assertEqual(184, entries[0].sgv)
        self.assertEqual("FortyFiveUp", entries[0].direction)

    def test_get_treatments(self):
        with HTTMock(treatments_response):
            treatments = self.api.get_treatments()

        self.assertEqual(3, len(treatments))
        self.assertEqual("absolute", treatments[0].temp)
        self.assertEqual("Temp Basal", treatments[0].eventType)

if __name__ == '__main__':
    unittest.main()
