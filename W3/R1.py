
import urllib.request as request
import json


def main():
    src = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions.json"
    with request.urlopen(src) as response:
        data = json.load(response)

    clist = data["result"]["results"]
    with open("data1.txt", "w", encoding="utf-8") as file:
        for location in clist:
            file.write(location["stitle"]+","+location["longitude"]+","+location["latitude"]+",")
            jpg = location["file"].split('http')
            file.write("http"+jpg[1]+"\n")


if __name__ == '__main__':
    main()