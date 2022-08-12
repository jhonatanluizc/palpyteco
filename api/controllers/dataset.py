import csv
from multiprocessing.spawn import prepare
import random
import urllib.request as request


class Dataset():

    # le um csv por url
    def get_dataset(self, url, spliter):
        response = request.urlopen(url)
        lines = [l.decode('utf-8') for l in response.readlines()]
        dataset = (list(csv.reader(lines)))[1:-1]

        prepare_dataset = []
        for data in dataset:
            prepare_dataset.append(data[2:])
        num_col = int(100/spliter)

        lines = []
        for item in prepare_dataset:
            inicial = 0
            final = num_col
            for x in range(spliter):
                lines.append(item[inicial:final])
                inicial += num_col
                final += num_col

        current_dataset = []
        for item in lines:
            data = []
            for x in range(num_col):
                if x < (num_col-1):
                    valor = item[x].split('/')[0]
                    data.append(int(valor))
                else:
                    classe = item[x].split('/')[2]
                    if(classe == "red"):
                        classe = 1
                    elif(classe == "black"):
                        classe = 2
                    else:
                        classe = 0      
                    data.append(int(classe))
            current_dataset.append(data)

        random.shuffle(current_dataset)

        json = {
                "data": current_dataset,
                "lines": len(current_dataset),
                "columns": len(current_dataset[0])
            }

        return json
    