print("=== PAPAN CATUR ===")

for baris in range(8):
    for kolom in range(8):
        if (baris + kolom) % 2 == 0:
            print("⬜", end="")
        else:
            print("⬛", end="")
    print()

from datetime import datetime
import random

print("=========================================")
print("===== PROGRAM AKTIVITAS MALAM AKTIF =====")
print("=========================================")

apresiasi = [
    "Terima kasih sudah semangat menjalani aktivitas seharian, waktunya beristirahat!",
    "Kamu hebat!🤩 akhirnya bisa istirahat juga",
    "Kerja bagus! jangan lupa istirahatkan tubuhmu😋",
    "Setelah hari yang panjang, sekarang waktunya menikmati waktu istirahatmu",
]

print("\n" + random.choice(apresiasi))

tanggal = datetime.now()

if tanggal.day >= 25:
    print("Tanggal tua terdeteksi 😔")
    print("Sepertinya kamu harus mulai berhemat sekarang 💸")

#List kosong untuk aktivitas
daftar_aktivitas = []

print("\nAktivitas yang tersedia:")
print("1. makan malam 🍽️")
print("2. tidur malam 😴")

aktivitas = input("Masukan aktivitas: ").lower()

#Menyimpan aktivitas ke dalam list
daftar_aktivitas.append(aktivitas)

#informasi tambahan aktivitas
keterangan = input("Tambahkan keterangan aktivitas: ")

if aktivitas == "makan malam":
    print("\n == Selamat datang di program makan malam 🍽️ ==")
    print("Ingin makan malam apa hari ini?")

    print("\nMenu yang tersedia:")
    print("- ikan goreng 🐟")
    print("- ayam goreng 🍗")
    print("- telur sambal goreng 🍳")
    print("- mie instan 🍜")
    
    menu = input("\nMasukan menu makan malam: ").lower()

    if menu == "ikan goreng":
        print("\n🐟 Menu dipilih: Ikan Goreng")
        print("Bahan tersedia, silahkan masak ikan goreng.")
        print("Chef mode activated 🧑‍🍳")
        print("Ikan sedang digoreng...")

        minum = input("\nApakah kamu ingin minum hari ini? (ya/tidak): ").lower()

        if minum == "ya":
            print("\nPilihan minuman:")
            print("- es teh 🧋")
            print("- air putih 💧")
            print("- jus 🍹")

            minuman = input("pilih minuman: ").lower()

            if minuman == "es teh":
                manis = input (
                    "Mau tingkat kemanisan berapa? (less sugar/normal/extra sugar): "
                ).lower()
                if manis == "less sugar":
                    print("Es teh less sugar sedang dibuat 🧋")

                elif manis == "normal":
                    print("Es teh manis normal sedang dibuat 🧋✨")

                elif manis == "extra sugar":
                    jawaban = input(
                        "Kamu yakin mau extra sugar? Bakalan kemanisan loh.. (ya/tidak): "
                    ).lower()
                    if jawaban == "ya":
                        print("Baiklah, sepertinya kamu sedang butuh banyak gula hari ini")
                        print("Es teh extra sugar sedang dibuat🧋✨✨")

                print("Ikan goreng dan Es teh sudah siap dihidangkan!")
                print("Selamat menikmati! 😋✨")

            elif minuman == "air putih":
                print("Air putih, pilihan yang sangat bagus!")

                print("Ikan goreng dan Air putih sudah siap dihidangkan!")
                print("Selamat menikmati! 😋✨")

            elif minuman == "jus":
                print("Jus dengan buah segar, pilihan yang sangat bagus!")
                print("Jus yang segar sedang dibuat 🍹")

                print("Ikan goreng dan Jus sudah siap dihidangkan!")
                print("Selamat menikmati! 😋✨")

        rating = int(input("Berikan rating untuk menu ini (1-10): "))

        if rating <= 5:
            print("Yahh, semoga next time makanannya lebih enak 😢")
            
        elif rating <= 8:
            print("Yeayy, kamu cukup menikmati makan malam ini 😊")

        else:
            print("WOW! Kamu sangat menyukai menu ini 🤩")

    elif menu == "ayam goreng":
        print("\n🍗 Menu dipilih: Ayam Goreng")

        jawaban = input(
            "Sepertinya kamu harus menangkap ayamnya terlebih dahulu 🐓\nMau tangkap ayam dulu? (ya/tidak): "
        ).lower()

        if jawaban == "ya":
            print("Kamu berhasil menangkap ayam! 🐓🏃💨")
            print("Bahan tersedia, silahkan masak ayam goreng.")
        
        else:
            print("Yahh.. ayamnya kabur 🥹")
            print("Haha aku hanya bercanda, bahan tersedia kok 😋🍗")

        print("Chef mode activated 🧑‍🍳")
        print("Ayam sedang digoreng...")

        minum = input("\nApakah kamu ingin minum hari ini? (ya/tidak): ").lower()

        if minum == "ya":
            print("\nPilihan minuman:")
            print("- es teh 🧋")
            print("- air putih 💧")
            print("- jus 🍹")

            minuman = input("pilih minuman: ").lower()

            if minuman == "es teh":
                manis = input (
                    "Mau tingkat kemanisan berapa? (less sugar/normal/extra sugar): "
                ).lower()
                if manis == "less sugar":
                    print("Es teh less sugar sedang dibuat 🧋")

                elif manis == "normal":
                    print("Es teh manis normal sedang dibuat 🧋✨")

                elif manis == "extra sugar":
                    jawaban = input(
                        "Kamu yakin mau extra sugar? Bakalan kemanisan loh.. (ya/tidak): "
                    ).lower()
                    if jawaban == "ya":
                        print("Baiklah, sepertinya kamu sedang butuh banyak gula hari ini")
                        print("Es teh extra sugar sedang dibuat🧋✨✨")

                print("Ayam goreng dan Es teh sudah siap dihidangkan!")
                print("Selamat menikmati! 😋✨")

            elif minuman == "air putih":
                print("Air putih, pilihan yang sangat bagus!")

                print("Ayam Goreng dan Air putih sudah siap dihidangkan!")
                print("Selamat menikmati! 😋✨")

            elif minuman == "jus":
                print("Jus dengan buah segar, pilihan yang sangat bagus!")
                print("Jus yang segar sedang dibuat 🍹")

                print("Ayam Goreng dan Jus sudah siap dihidangkan!")
                print("Selamat menikmati! 😋✨")

        rating = int(input("Berikan rating untuk menu ini (1-10): "))

        if rating <= 5:
            print("Yahh, semoga next time makanannya lebih enak 😢")
            
        elif rating <= 8:
            print("Yeayy, kamu cukup menikmati makan malam ini 😊")

        else:
            print("WOW! Kamu sangat menyukai menu ini 🤩")

    elif menu == "telur sambal goreng":
        print("\n🍳 Menu dipilih: Telur Sambal Goreng")

        jawaban = input(
            "Kamu yakin kuat makan pedes? 🌶️🔥 (ya/tidak): "
        ).lower()

        if jawaban == "ya":
            print ("Wahh pemberani juga, Keren!😎")
            print("Bahan tersedia, silahkan masak telur sambal goreng.")

        else:
            print("Baiklah, kita masak telur goreng biasa 🍳")
            print ("Bahan tersedia, silahkan masak telur goreng biasa.")

        minum = input("\nApakah kamu ingin minum hari ini? (ya/tidak): ").lower()

        if minum == "ya":
            print("\nPilihan minuman:")
            print("- es teh 🧋")
            print("- air putih 💧")
            print("- jus 🍹")

            minuman = input("pilih minuman: ").lower()

            if minuman == "es teh":
                manis = input (
                    "Mau tingkat kemanisan berapa? (less sugar/normal/extra sugar): "
                ).lower()
                if manis == "less sugar":
                    print("Es teh less sugar sedang dibuat 🧋")

                elif manis == "normal":
                    print("Es teh manis normal sedang dibuat 🧋✨")

                elif manis == "extra sugar":
                    jawaban = input(
                        "Kamu yakin mau extra sugar? Bakalan kemanisan loh.. (ya/tidak): "
                    ).lower()
                    if jawaban == "ya":
                        print("Baiklah, sepertinya kamu sedang butuh banyak gula hari ini")
                        print("Es teh extra sugar sedang dibuat🧋✨✨")

                print("Telur goreng dan Es teh sudah siap dihidangkan!")
                print("Selamat menikmati! 😋✨")

            elif minuman == "air putih":
                print("Air putih, pilihan yang sangat bagus!")

                print("Telur goreng dan Air putih sudah siap dihidangkan!")
                print("Selamat menikmati! 😋✨")

            elif minuman == "jus":
                print("Jus dengan buah segar, pilihan yang sangat bagus!")
                print("Jus yang segar sedang dibuat 🍹")

                print("Telur goreng dan Jus sudah siap dihidangkan!")
                print("Selamat menikmati! 😋✨")

        rating = int(input("Berikan rating untuk menu ini (1-10): "))

        if rating <= 5:
            print("Yahh, semoga next time makanannya lebih enak 😢")
            
        elif rating <= 8:
            print("Yeayy, kamu cukup menikmati makan malam ini 😊")

        else:
            print("WOW! Kamu sangat menyukai menu ini 🤩")

    elif menu == "mie instan":
        print("\n🍜 Menu dipilih: Mie Instan")
        print("Menu anak kost terdeteksi 😂🤭")

        jenis = input(
            "Mau makan mie goreng atau mie kuah? (goreng/kuah): "
        ).lower()

        if jenis == "goreng":
            print("Mie goreng dipilih 🍜🔥")

        else:
            print("Mie kuah dipilih 🫕✨")

        print("\nPilihan topping:")
        print("- telur 🍳")
        print("- sosis 🌭")
        print("- bakso 🥩")
        print("- keju 🧀")

        topping = input("Pilih topping: ").lower()

        if topping == "telur":
            print("Topping telur berhasil ditambahkan 🍳")

        elif topping == "sosis":
            print("Topping sosis berhasil ditambahkan 🌭")

        elif topping == "bakso":
            print("Topping bakso berhasil ditambahkan 🥩")

        elif topping == "keju":
            print("Topping keju berhasil ditambahkan 🧀")
        
        else:
            print("Topping tidak tersedia 😢")

        while True:
            tambahan = input(
                "\nMau tambah topping lagi? (ya/tidak): "    
            ).lower()
            
            if tambahan == "ya":
                topping2 = input(
                    "Pilih topping tambahan (telur/sosis/bakso/keju): "
                )
                print("Topping tambahan", topping2, "Berhasil ditambahkan 😋")

            elif tambahan == "tidak":
                print("Baiklah, topping sudah cukup 😋🤩✨")
                break
            else:
                print("Topping tidak tersedia 😢")

        print("Bahan tersedia, silahkan masak mie instan.")
        print("Chef mode activated 🧑‍🍳")
        print("Mie sedang dimasak...")

        minum = input("\nApakah kamu ingin minum hari ini? (ya/tidak): ").lower()

        if minum == "ya":
            print("\nPilihan minuman:")
            print("- es teh 🧋")
            print("- air putih 💧")
            print("- jus 🍹")

            minuman = input("pilih minuman: ").lower()

            if minuman == "es teh":
                manis = input (
                    "Mau tingkat kemanisan berapa? (less sugar/normal/extra sugar): "
                ).lower()
                if manis == "less sugar":
                    print("Es teh less sugar sedang dibuat 🧋")

                elif manis == "normal":
                    print("Es teh manis normal sedang dibuat 🧋✨")

                elif manis == "extra sugar":
                    jawaban = input(
                        "Kamu yakin mau extra sugar? Bakalan kemanisan loh.. (ya/tidak): "
                    ).lower()
                    if jawaban == "ya":
                        print("Baiklah, sepertinya kamu sedang butuh banyak gula hari ini")
                        print("Es teh extra sugar sedang dibuat🧋✨✨")

                print("Mie instan dan Es teh sudah siap dihidangkan!")
                print("Selamat menikmati! 😋✨")

            elif minuman == "air putih":
                print("Air putih, pilihan yang sangat bagus!")

                print("Mie instan dan Air putih sudah siap dihidangkan!")
                print("Selamat menikmati! 😋✨")

            elif minuman == "jus":
                print("Jus dengan buah segar, pilihan yang sangat bagus!")
                print("Jus yang segar sedang dibuat 🍹")

                print("Mie instan dan Jus sudah siap dihidangkan!")
                print("Selamat menikmati! 😋✨")

        rating = int(input("Berikan rating untuk menu ini (1-10): "))

        if rating <= 5:
            print("Yahh, semoga next time makanannya lebih enak 😢")
            
        elif rating <= 8:
            print("Yeayy, kamu cukup menikmati makan malam ini 😊")

        else:
            print("WOW! Kamu sangat menyukai menu ini 🤩")

    else:
        print("\n❌ Menu tidak tersedia.")
        print("Silahkan membeli bahan terlebih dahulu 🛒")

elif aktivitas == "tidur malam":
    print("\n=== MODE TIDUR === 😴")

    from datetime import datetime
    import time
    import winsound

    jam = datetime.now()

    print("Waktu sekarang:", jam.strftime("%H:%M"))

    jam = datetime.now()

    print("Waktu sekarang:", jam.strftime("%H:%M"))

    if jam.hour >= 22:
        print("Sudah malam, waktunya tidur 🌙🛌")
        print("Selamat tidur dan mimpi indah 🤓✨")

    else:
        print("Belum waktunya tidur malam.")
        print("Tapi jangan tidur terlalu larut yaa!")

    jawaban = input(
        "Apakah kamu sudah benar-benar siap tidur atau masih mau scrolling dulu? 📱 (tidur/scrolling): "
    ).lower()

    if jawaban == "scrolling":
        print("Oke, hanya 5 menit ya!")
        print("Tapi biasanya scrolling jadi 2 jam nih, haha")

    else:
        print("WOW! Pilihan yang bagus, tubuhmu butuh istirahat")

    suasana = input(
        "\nMau tidur sambil dengar musik atau mau langsung tidur? 🎵 (musik/langsung): "
    ).lower()

    if suasana == "musik":
        print("Playlist pengantar tidur diaktifkan 🎶🌙")
        print("Musik diputar")

    else:
        print("Mode tidur cepat diaktifkan 😴")

    alarm = input (
        "\nMau pasang alarm untuk besok? ⏰ (ya/tidak): "
    ).lower()

    if alarm == "ya":
        waktu_alarm = input(
            "Set alarm jam berapa? (contoh 05:00): "
        )
        print("Alarm berhasil dipasang jam", waktu_alarm, "⏰")
        print("Alarm sedang menunggu waktu yang sesuai...")
            
        while True:
            sekarang = datetime.now().strftime("%H:%M")
            
            if sekarang == waktu_alarm:
                print("\n⏰ ALARM BERBUNYI!! ⏰")
                print("AYO BANGUN! CEPAT! NANTI TELAT")

                winsound.Beep(1000, 1000)

                break
            time.sleep(30) 
            
    else:
        print("OKEE, kamu sudah siap untuk bangun lebih siang")
        print("Selamat tidur dan mimpi indah 😴🌙✨")

else:
    print("\nAktivitas belum tersedia.")
    print("Silahkan pilih aktivitas yang ada di daftar 😊")

print("\n=========================================")
print("===== PROGRAM AKTIVITAS YANG TERSIMPAN =====")
print("=========================================")

for nomor, item in enumerate(daftar_aktivitas, start=1):
    print(f"{nomor}. {item}")
    
print("\nKeterangan aktivitas:")
print(keterangan)