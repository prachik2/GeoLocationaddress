import pandas as pd
import requests
from django.shortcuts import render
from django.views.generic import TemplateView

# enter your api key here
api_key = '<YOUR API KEY>'
url = 'https://maps.googleapis.com/maps/api/geocode/json?'

latitute = pd.Series([])
longitute = pd.Series([])
lat_list = []
lng_list = []


class AddressView(TemplateView):
    template_name = 'base.html'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            if request.FILES.get('import_file') is None:
                return render(request, 'base.html', {'error_message': 'No file found'})

            else:
                address_file = request.FILES.get("import_file").name
                if not address_file.endswith('.csv'):
                    error_msg = 'File has not valid extension to upload (.csv extension required.)'
                    return render(request, 'base.html', {'error_message': error_msg})

                df = pd.read_csv(address_file, header=0)
                for idx, row in df.iterrows():
                    print(idx, row)
                    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address={}".format(row['Address'])
                    geocode_url = geocode_url + "&key={}".format(api_key)
                    results = requests.get(geocode_url)
                    results = results.json()

                    if results['results']:
                        if results['results'][0]["geometry"]['location']["lat"]:
                            latitute[idx] = results['results'][0]["geometry"]['location']["lat"]

                        if results['results'][0]["geometry"]['location']["lng"]:
                            longitute[idx] = results['results'][0]["geometry"]['location']["lng"]

                    else:
                        latitute[idx] = 0
                        longitute[idx] = 0

                df.insert(2, "Latitute", latitute)
                df.insert(3, "Longitute", longitute)
                df2 = df.to_csv(address_file, index=0)
        return render(request, 'base.html', {})

    # def post(self, request, *args, **kwargs):
    #     if request.is_ajax():
    #         data = request.POST
    #         ip = request.META.get("HTTP_HOST")
    #
    #         url = "http://" + ip + "/api/buyer-consg-create/"
    #
    #         try:
    #             data1 = requests.post(url, data)
    #         except:
    #             return HttpResponse(data, content_type="application/json")
    #         print(data1, "@@@@@@@@@@@@@@@")
    #         data2 = json.loads(data1.content)
    #         data3 = json.dumps(data2)
    #         return HttpResponse(data3, content_type="application/json")
