import csv
import urllib.request as request


class Dataset():

    # le um csv por url
    def get_dataset(self, url):
        response = request.urlopen(url)
        lines = [l.decode('utf-8') for l in response.readlines()]
        dataset = list(csv.reader(lines))
        return dataset