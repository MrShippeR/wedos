# Dynamická DDNS u Wedosu
Skript pro automatickou změnu IP adresy domény. Automaticky se spouští při (re)startu serveru a pak je volán každou hodinu. O nic se nestaráte a nejpozději za hodinu je server opět dostupný. Jak to funguje? 
Skript zjistí svoji ip adresu počítače, na kterém běží. Poté přeloží doménové jméno na IP adresu a obě IP adresy porovná. Pokud se liší, skript *wedos-updatedns.py* změní přes Wedos WAPI (rozhraní) IP adresu, kam má doména směřovat. Pak standartně čekáte až hodinu, než se změny projeví na všech DNS serverech.

## Rekvizity, které musíme mít připravené v administraci Wedosu.
- nastavenou A doménu
- nastavené heslo k WAPI
https://kb.wedos.com/cs/wapi-api-rozhrani/zakladni-informace-wapi-api-rozhrani/wapi-aktivace-a-nastaveni/


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

3. úpravíme skript ```$ nano wedos-updatedns.py``` - vyplníme 3 řádky, proměnné LOGIN, PASSWORD, DOMAIN 

- nastavte vlastníka na svůj účet: $ sudo chown -R user:user /opt/wedos/
- rozšiřte oprávnění, aby byl soubor spustitelný: $ sudo chmod +x /opt/wedos/wedos-updatedns.py
4. soubor můžeme vyzkoušet - spustit ručně: $ ./opt/wedos/wedos-updatedns.py

5. automatické spouštění skriptu: $ sudo crontab -e a přidáme řádky
5. pro spuštění skriptu po restartu zařízení: @reboot   /opt/wedos/wedos-updatedns.py
5. a každou hodinu: 0 * * * * var/www/ddns/wedos-updatedns.py
6. uložíme a máme hotovo

Návod je zveřejněný ještě na podpoře Wedosu.
https://help.wedos.cz/otazka/dynamicka-dns-ddns-u-wedosu/36428/
