
# MAC Changer Tool

Bu Python tabanlı araç, bilgisayarınızdaki ağ arayüzünün (Ethernet ya da Kablosuz) MAC adresini değiştirmek için kullanılabilir. Aracın kullanımını adım adım takip edebilir ve farklı senaryolara göre çalıştırabilirsiniz.

![image](https://github.com/user-attachments/assets/ca07ca67-ac7b-4bf3-b1a8-345022a24d37)

## Gerekli Kütüphaneler

Projeyi çalıştırmak için gereken kütüphaneleri yüklemek için terminalde şu komutu çalıştırabilirsiniz:

```bash
pip install -r requirements.txt
```

`requirements.txt` dosyanızın içeriği şu şekilde olmalıdır:

```
colorama
pyfiglet
rich
tabulate
```

Bu kütüphaneler, çıktıların renkli ve kullanıcı dostu görünmesini sağlar, ayrıca MAC adresi değiştirme işlemini gerçekleştirir.

## Kullanım

### 1. **MAC Adresi Değiştirme - Bir Seferlik Değişim**

**Bir defa MAC adresi değiştirmek için** şu komutları kullanabilirsiniz:

#### Komut:
```bash
sudo python main.py -i eth0
```

#### Alternatif Komut:
```bash
sudo python main.py --interface eth0
```

Burada, `eth0` yerine kullanmak istediğiniz ağ arayüzünü girebilirsiniz (örn: `wlan0`, `enp0s3` gibi).

**Açıklama:**
- Bu komut, belirttiğiniz ağ arayüzü (`eth0`, `wlan0` gibi) üzerinden bir MAC adresi değişikliği yapar.
- Değişiklik yalnızca bir kez gerçekleşir.

### 2. **Otomatik MAC Adresi Değiştirme**

Eğer **MAC adresinin otomatik olarak değiştirilmesini** isterseniz, şu komutu kullanabilirsiniz:

#### Komut:
```bash
sudo python main.py -i eth0 -a auto
```

**Açıklama:**
- Bu komut, belirttiğiniz arayüzde MAC adresini sürekli olarak değiştirir. Her 10 saniyede bir yeni bir MAC adresi atanır.
- `auto` modunda, her yeni MAC adresi değişikliği yapıldığında bir log kaydı tutularak işlem tarihleri ve MAC adresleri kaydedilir.
- Bu modda çıkmak için `ENTER` tuşuna basmanız yeterlidir.

### 3. **Özel MAC Adresi Belirleme**

Eğer **özelleştirilmiş bir MAC adresi** kullanmak isterseniz, şu komutu kullanabilirsiniz:

#### Komut:
```bash
sudo python main.py -i eth0 -m 00:11:22:33:44:55
```

**Açıklama:**
- Bu komut ile, kendi belirlediğiniz `00:11:22:33:44:55` gibi bir MAC adresi kullanılabilir. Buradaki `-m` seçeneği ile MAC adresini değiştirebilirsiniz.

### Çıkmak İçin:
Otomatik modda çalışırken, **ENTER** tuşuna basarak programdan çıkabilirsiniz.

---

## Kod Açıklamaları

### **Başlangıçta Kullanılan Arayüzler:**
Bu araç, ağ arayüzlerini (ethernet veya kablosuz) değiştirmek için kullanılır. Program, `eth0`, `wlan0`, `enp0s3`, `eno1` gibi yaygın ağ arayüzlerini destekler. Uygulama, bu arayüzlerin dışında bir arayüz belirtilirse hata verir.

### **MAC Adresi Değiştirme İşlemi:**
Program, seçilen ağ arayüzüne bir MAC adresi atamak için `ifconfig` komutunu kullanır. Değişim işlemi yapılmadan önce ağ arayüzü kapatılır, MAC adresi değiştirilir ve sonrasında arayüz tekrar başlatılır.

### **Otomatik Mod:**
`auto` modu, MAC adresini her 10 saniyede bir otomatik olarak değiştirmeyi sağlar. Bu özellik, bilgisayarın ağ arayüzü üzerinde sürekli rastgele değişiklikler yapar. Kullanıcı `ENTER` tuşuna basarak programı durdurabilir.

### **Geçmiş Kaydı:**
MAC adresi her değiştiğinde, değişim zaman damgası, arayüz adı ve yeni MAC adresi kaydedilir. Geçmiş verileri kullanıcıya tabular formatta gösterilir.

---

## Örnek Çıktılar

1. **Bir kez MAC Adresi Değiştirme:**
```bash
$ sudo python main.py -i eth0
[2025-05-12 06:10:30], MAC: 02:19:25:2e:7f:a1, interface: eth0 olarak değiştirildi
```

2. **Otomatik Modda Çalışma:**
```bash
$ sudo python main.py -i eth0 -a auto
Otomatik mod başladı. Çıkmak için q tuşuna basın.
[2025-05-12 06:10:30], MAC: 02:19:25:2e:7f:a1, interface: eth0 olarak değiştirildi
[2025-05-12 06:10:40], MAC: 02:19:25:3f:7f:a2, interface: eth0 olarak değiştirildi
...
```

---

## İlgili Kütüphaneler

Bu araç, aşağıdaki Python kütüphanelerini kullanmaktadır:

- **colorama**: Konsolda renkli yazı yazmak için.
- **pyfiglet**: ASCII sanatı ile başlık yazdırmak için.
- **rich**: Zengin metin biçimlendirme ve ekran çıktısı için.
- **tabulate**: Verileri tablo formatında ekrana yazdırmak için.

---

## Yardım ve Destek

Herhangi bir sorunla karşılaşırsanız, lütfen [GitHub Issues](https://github.com/your-repo/issues) kısmından geri bildirimde bulunun.

---

### Notlar:
- **sudo** kullanmanız gerekecektir çünkü ağ arayüzüne erişim sağlamak ve MAC adresini değiştirmek için yönetici izinlerine ihtiyaç vardır.
- **Python 3.x** sürümü gereklidir.

---

### 4. GitHub'da Projeyi Yüklemek

Projenizi GitHub'a yükledikten sonra, yukarıdaki içeriği `README.md` dosyanıza ekleyebilirsiniz. Bu şekilde, kullanıcılar projenizi daha rahat kullanabilir ve tüm komutlar, parametreler hakkında bilgi sahibi olabilirler.

GitHub’a yükleme işlemini gerçekleştirmek için:

1. **Projenizi GitHub'a Yükleyin:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repository-url>
   git push -u origin master
   ```

---



