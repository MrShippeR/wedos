# Dynamická DDNS u Wedosu
Skript pro automatickou změnu IP adresy domény. Automaticky se spouští při (re)startu serveru a pak je volán každou hodinu. O nic se nestaráte a nejpozději za hodinu je server opět dostupný. Jak to funguje? 
Skript zjistí svoji ip adresu počítače, na kterém běží. Poté přeloží doménové jméno na IP adresu a obě IP adresy porovná. Pokud se liší, skript *wedos-updatedns.py* změní přes Wedos WAPI (rozhraní) IP adresu, kam má doména směřovat. Pak standartně čekáte až hodinu, než se změny projeví na všech DNS serverech.

## Prerekvizity, které musíme mít připravené v administraci Wedosu.
- nastavenou a uloženou A doménu, kterou chcete skriptem udržovat aktuální [návod Youtube](https://youtu.be/TX9eJdxUDcI), [návod v textové nápovědě s typy DNS adres](https://kb.wedos.com/cs/dns/wedos-dns/wedos-dns-zaznamy-domeny/)
> Nejčastěji vás budou zajímat A domény a CNAME (alias = povedou na stejnou IP adresu). A doména je example.com směřující na konkrétní IP adresu. CNAME můžete nastavit jako subdoménu something.example.com s adresou na example.com. Vřele doporučuji dát alias *.example.com , což přesměruje všechny subdomény na váš server a nemusíte je ručně vyjmenovávat. Případně vás budou zajímat ještě MX záznamy pro emailové adresy. Za zmínku stojí ještě formát AAA, což je to samé co A záznam, jen pro IPv6. Teoreticky by mohl tento skript fungovat pro IPv4 i IPv6, ale neměl jsem možnost IPv6 vyzkoušet.
- nastavené WAPI rozhraní ([návod k WAPI](https://kb.wedos.com/cs/wapi-api-rozhrani/zakladni-informace-wapi-api-rozhrani/wapi-aktivace-a-nastaveni/), rozsahy IP adres českých poskytovatelů: [tomasbenda.cz](https://www.tomasbenda.cz/2016/08/27/rozsah-ipv4-adres-pridelenych-pro-ceskou-republiku/) či [nirsoft.net](https://www.nirsoft.net/countryip/cz.html))



## Uvedení skriptu do provozu (Ubuntu)
1. vytvoření adresáře, přesun do něj a stažení skriptu 
```
$ sudo su
# mkdir /opt/wedos 
# cd /opt/wedos
# wget https://raw.githubusercontent.com/MrShippeR/wedos/main/wedos-updatedns.py
```

2. nastaveníme spustitelnost souboru a vlastníka -> ```user``` v příkladu nahraďte vašim loginem
```
# chmod -R +x /opt/wedos
# chown -R user:user /opt/wedos
```

3. úpravíme skript ```$ nano opt/wedos/wedos-updatedns.py``` - vyplníme řádky, proměnné LOGIN, PASSWORD, DOMAIN, SUBDOMAIN

4. soubor můžeme spustit ručně: ```$ /opt/wedos/wedos-updatedns.py```
> Výstupem skriptu je zpráva, ```IP addresses match``` nebo ```Updated {old IP} to {new IP}```

## Automatické spouštění skriptu
1. otevřeme správce úloh ```$ crontab -e```
2. na konec souboru přidáme tyto dva řádky:
```
@reboot     opt/wedos/wedos-updatedns.py
0 * * * *   opt/wedos/wedos-updatedns.py
```
> což bude spouštět skript při každém (re)startu počítače a pak každou hodinu. Čas si můžete upravit pomocí [konfigurátoru](https://crontab.guru/).

Uložíme a máme hotovo.

Návod je zveřejněný ještě na [podpoře Wedosu](https://help.wedos.cz/navody/domeny/dynamicka-dns-ddns-u-wedosu/). 
