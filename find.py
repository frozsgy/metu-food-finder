import calendar
import datetime
import requests
import json
import re

class TurkishText():

    text = ""
    l = ['ı', 'ğ', 'ü', 'ş', 'i', 'ö', 'ç']
    u = ['I', 'Ğ', 'Ü', 'Ş', 'İ', 'Ö', 'Ç']

    def __init__(self, text):
        self.text = text

    def upper(self):
        res = ""
        for i in self.text:
            if i in self.l:
                res += self.u[self.l.index(i)]
            else :
                res += i.upper()
        return res

    def lower(self):
        res = ""
        for i in self.text:
            if i in self.u:
                res += self.l[self.u.index(i)]
            else :
                res += i.lower()
        return res

    def capitalize(self):
        m = self.text.split()
        res = ""
        for i in m:
            res += TurkishText(i[0]).upper() + TurkishText(i[1:]).lower() + " "
        return res[:-1:]


class Food():

    menu = dict()

    def loadMenu(self):
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        days = calendar.monthrange(year, month)[1]
        for i in range(days):
            iday = datetime.date(year, month, i+1).strftime("%d-%m-%Y")
            url = "https://kafeterya.metu.edu.tr/service.php?tarih=" + iday
            r = requests.get(url)
            page = r.content
            items = json.loads(page)
            if items is not None:
                ogle = items['ogle']
                aksam = items['aksam']
                daily = [[],[]]
                for j in range(5):
                    daily[0].append(ogle[j]['name'])
                    daily[1].append(aksam[j]['name'])
                self.menu[iday] = daily

    def printMenu(self):
        import pprint
        pprint.pprint(self.menu)

    def findFood(self, name):
        trname = TurkishText(name)
        nameu = trname.upper()
        namel = trname.capitalize()
        res = []
        for i in range(len(self.menu)):
            for k in range(2):
                for j in range(4):
                    match = re.search(nameu, list(self.menu.values())[i][k][j])
                    if match:
                        res.append((list(self.menu.keys())[i], k, list(self.menu.values())[i][k][j]))
        if len(res) > 0:
            print("İçinde %s geçen %d öğün bulundu: " % (namel, len(res)))
            for i in res:
                if i[1] == 0:
                    when = "Öğle "
                else :
                    when = "Akşam"
                food = TurkishText(i[2])
                print("%s - %s Yemeği - %s" % (i[0], when, food.capitalize()))
            print("Afiyet olsun!")
            print("-"*20)
        else :
            print("Maalesef bu ay menüde %s yok :/" % (namel))
            print("-"*20)


if __name__ == '__main__':
    print("ODTÜ Yemekhane Menüsü Gezgini'ne Hoşgeldiniz!")
    t = Food()
    print("Menü yükleniyor, lütfen bekleyin...")
    t.loadMenu()
    print("Menü yüklendi.")
    print("-"*20)
    try:
        while True:
            s = input("Menüde aramak istediğiniz yemeğin ismini girin: ")
            t.findFood(s)
    except KeyboardInterrupt:
        print("\n" + "-"*20)
        print("Görüşmek üzere!")
        exit()
