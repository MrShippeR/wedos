# Dynamická DDNS u Wedosu
Skript pro automatickou změnu IP adresy vaší domény. Stačí tento skript nechat spouštět plánovačem úloh/crontab a zajistíte si tím vždy aktuální IP adresu vaší domény, když vám poskytovatel nenabízí statickou IP.

Návod psaný pro Linux - Ubuntu a jeho deriváty:
1) stáhněte soubor wedos-updatedns.py a umístěte jej do nové složky /opt/wedos/wedos-updatedns.py
2) nastavte vlastníka na svůj účet: $ sudo chown -R user:user /opt/wedos/
3) rozšiřte oprávnění, aby byl soubor spustitelný: $ sudo chmod +x /opt/wedos/wedos-updatedns.py
4) soubor můžeme vyzkoušet - spustit ručně: $ ./opt/wedos/wedos-updatedns.py

5) automatické spouštění skriptu: $ sudo crontab -e a přidáme řádky
5a) pro spuštění skriptu po restartu zařízení: @reboot   /opt/wedos/wedos-updatedns.py
5b) a každou hodinu: 0 * * * * var/www/ddns/wedos-updatedns.py
6) uložíme a máme hotovo

Návod je zveřejněný ještě na podpoře Wedosu.
https://help.wedos.cz/otazka/dynamicka-dns-ddns-u-wedosu/36428/
