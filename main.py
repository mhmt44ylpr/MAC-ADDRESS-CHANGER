import time
import subprocess
from random import randint
from colorama import Fore, init
from pyfiglet import Figlet
import re
from optparse import OptionParser
from rich.console import Console
from tabulate import tabulate
import threading

# Colorama'yı başlatıyoruz, terminalde renkli çıktılar için
init(autoreset=True)
console = Console()

# MAC adresi değiştirme işlevselliğini kapsayan sınıf
class MacChanger():
    # Desteklenen ağ arayüzlerinin listesi
    # Bu listede geçerli olan ağ kartlarını belirtmelisiniz (örneğin eth0, wlan0 vb.)
    network_interfaces = [
        "eth0", "eth1", "enp0s3", "eno1",  # Ethernet arayüzleri
        "wlan0", "wlan1", "wlp2s0", "wlp3s0"  # Kablosuz ağ arayüzleri
    ]

    def __init__(self):
        # Başlangıçta kullanılacak olan MAC adresi ve diğer parametreler
        self.macaddress = 'ff:ff:ff:ff:ff:ff'  # Varsayılan olarak 'ff:ff:ff:ff:ff:ff' değeri
        self.interface = ''  # Kullanıcı tarafından belirlenen ağ arayüzü
        self.auto = ''  # 'auto' modu seçilip seçilmediği
        self.history = list()  # MAC adresi değişim geçmişini saklayacak liste
        self.get_user_input()  # Kullanıcıdan gerekli girişleri almak için fonksiyon çağrısı

    def get_user_input(self):
        """
        Komut satırından alınan parametrelerle kullanıcıdan ağ arayüzü ve MAC adresi alıyoruz.
        Burada, '-i' ile interface, '-m' ile MAC adresi, '-a' ile otomatik değiştirme durumu belirtilir.
        """
        parse = OptionParser()
        parse.add_option('-i', '--interface', dest='interface',
                         help='Ağ arayüzünü giriniz (örn: eth0, wlan0, vb.)')
        parse.add_option('-m', '--mac', dest='macaddress',
                         help='Yeni MAC adresini giriniz (örn: 00:12:1a:2b:22:11)')
        parse.add_option('-a', '--auto', dest='auto',
                         help='Otomatik MAC adresi değişimi için -a/--auto auto olarak belirtiniz')

        # Komut satırından alınan parametreleri işleme
        (option, _) = parse.parse_args()

        # Eğer interface belirtmezse, hata mesajı verilir ve program sonlandırılır.
        if not option.interface:
            console.log('[red]Lütfen bir interface bağlantısı girip programı baştan çalıştırınız[/red]')
            exit()

        # Girilen interface listede geçerli değilse, hata mesajı verilir ve program sonlandırılır.
        if option.interface not in self.network_interfaces:
            console.log('[red]Lütfen geçerli bir interface bağlantısı giriniz..[/red]')
            exit()

        # MAC adresi geçerli formatta mı kontrol edilir
        def is_valid_mac(mac_address):
            pattern = re.compile(r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$")
            return bool(pattern.match(mac_address))

        # Kullanıcı MAC adresi girdiyse, geçerliliğini kontrol ederiz.
        if option.macaddress:
            if is_valid_mac(option.macaddress):
                self.macaddress = option.macaddress  # Geçerli ise MAC adresini kullanırız
            else:
                console.log('[red]Geçersiz MAC adresi formatı! ff:ff:ff:ff:ff:ff gibi olmalı.[/red]')
                exit()

        # Kullanıcının seçtiği interface ve auto modunu kaydediyoruz
        self.interface = option.interface
        self.auto = option.auto

    def change_to_mac(self):
        """
        MAC adresini değiştiren ve otomatik modda her 10 saniyede bir MAC adresini değiştiren fonksiyon.
        Eğer '-a auto' seçeneği belirtilirse, program her 10 saniyede bir otomatik olarak MAC adresini değiştirir.
        """
        # Rastgele bir MAC adresi oluşturma fonksiyonu
        def random_mac():
            mac = [0x02, randint(0x00, 0x7f)] + [randint(0x00, 0xff) for _ in range(4)]
            return ':'.join(f'{octet:02x}' for octet in mac)

        # MAC adresini değiştirme işlemi için ifconfig komutları
        def change():
            subprocess.call(['ifconfig', self.interface, 'down'])  # Interface'i kapat
            subprocess.call(['ifconfig', self.interface, 'hw', 'ether', self.macaddress])  # MAC adresini değiştir
            subprocess.call(['ifconfig', self.interface, 'up'])  # Interface'i tekrar başlat

        if self.auto == 'auto':
            # Otomatik mod aktifse, her 10 saniyede bir MAC adresini değiştirir
            console.log('[yellow]Otomatik mod başladı. [bold red]ENTER[/bold red] tuşuna basarak çıkabilirsiniz.[/yellow]')

            # Programın durmasını sağlayacak bir 'stop_flag' kontrolü
            stop_flag = {'value': False}

            def wait_for_input():
                # Kullanıcıdan input bekler, 'ENTER' tuşuna basıldığında program durur
                input()
                stop_flag['value'] = True

            # Kullanıcıdan input beklemek için farklı bir thread başlatıyoruz
            threading.Thread(target=wait_for_input, daemon=True).start()

            # Sürekli olarak MAC adresini değiştiriyoruz, kullanıcı 'ENTER' tuşuna basarsa duracak
            while not stop_flag['value']:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                self.macaddress = random_mac()  # Rastgele MAC adresi oluştur
                change()  # MAC adresini değiştir
                self.history.append([timestamp, self.interface, self.macaddress])  # Geçmişe kaydet

                # Değişim başarılıysa çıktı veririz
                if self.macaddress == self.mac_control():
                    print(Fore.BLUE + f'[{timestamp}], MAC: {self.macaddress}, interface: {self.interface} olarak değiştirildi')

                for _ in range(60):  # 10 dakika boyunca MAC adresi değişimini kontrol et
                    time.sleep(10)
                    if stop_flag['value']:  # Kullanıcı 'ENTER' tuşuna basarsa döngüden çıkılır
                        break

            # Program sonlandığında, günlük bilgisi yazdırılır
            console.log('[bold red]Program durduruldu. Günlük yazdırılıyor...[/bold red]')
            self.get_history()

        else:
            # Eğer otomatik mod değilse, sadece bir kez MAC adresini değiştirir
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            if self.macaddress == 'ff:ff:ff:ff:ff:ff':  # Varsayılan MAC adresiyse, rastgele bir MAC adresi oluşturur
                self.macaddress = random_mac()
            change()  # MAC adresini değiştir
            self.history.append([timestamp, self.interface, self.macaddress])  # Değişim geçmişine kaydet

            # Değişim başarılıysa çıktı veririz
            if self.macaddress == self.mac_control():
                print(Fore.BLUE + f'[{timestamp}], MAC: {self.macaddress}, interface: {self.interface} olarak değiştirildi')

    def get_history(self):
        """
        MAC adresi değişim geçmişini ekrana yazdırır.
        Geçmiş varsa, tablo halinde gösterilir.
        """
        if self.history:
            print(Fore.BLUE + '*'*10 + 5*' ' + 'Mac Değişim Günlüğü' + '*'*10 + 5*' ')
            print(tabulate(self.history, headers=["#", "Zaman", "MAC Adresi"], tablefmt="fancy_grid"))
        else:
            print(Fore.RED + 'Herhangi bir günlük geçmişi bulunamadı.')

    def mac_control(self):
        """
        Ağ arayüzünün geçerli MAC adresini kontrol eder.
        """
        new_mac_add = subprocess.check_output(['ifconfig', self.interface]).decode()
        mac_address = re.search(r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', new_mac_add).group(0)
        return mac_address


if __name__ == '__main__':
    # Figlet ile başlık yazdırıyoruz
    figlet = Figlet(font='slant')
    print(Fore.CYAN + figlet.renderText('MAC CHANGER'))

    # MacChanger sınıfını başlatıyoruz
    change_to_mac = MacChanger()
    change_to_mac.change_to_mac()  # MAC adresini değiştirme işlemini başlatıyoruz
