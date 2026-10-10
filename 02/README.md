# Praktikum Minggu 02 - Komunikasi Antar Proses pada Sistem Terdistribusi

**Mata Kuliah:** Praktikum Sistem Terdistribusi dan Terdesentralisasi
**Topik:** Komunikasi Antar Proses pada Sistem Terdistribusi

---

# 📚 Tujuan Praktikum

1. ...
2. ....
3. .....

---

# 📚 Dasar Teori

---

# ⏩ PEMBAHASAN PRAKTIKUM

## PRAKTIK 1 - PROSES PADA SATU NODE

### 1. Tampilkan berbagai proses yang ada pada Laptop-Windows

<img src="images/01_Tampilan_Proses.png" width="700">

#### Pembahasan

---

### 2. Jalankan salah satu aplikasi kemudian perlihatkan proses yang dimunculkan oleh aplikasi

Sebagai contoh menjalankan Notepad untuk percobaan:

<img src="images/02_Jalankan_Notepad.png" width="700">

Kemudian untuk melihat proses yang dimunculkan aplikasi tersebut dapat dilihat pada task manager, yaitu sebagai berikut :

<img src="images/04_Proses_Notepad.png" width="700">

<img src="images/03_Detail_Proses.png" width="700">

#### Pembahasan

---

### 3. Merestart dan Mematikan proses yang dimunculkan oleh aplikasi

1. Untuk mematikan proses dapat dilakukan melalui Task Manager:

<img src="images/05_Mematikan_Proses_Via_TaskManager.png" width="700">

2. Kemudian dapat dilakukan juga melalu CMD:

Untuk melihat daftar proses yang sedang berjalan di Windows gunakan perintah:

```
tasklist
```

Untuk mencari proses dari aplikasi gunakan perintah:

```
tasklist | findstr /i "Nama_Aplikasi"
```

Contoh :

```
tasklist | findstr /i notepad
```

<img src="images/06_Mematikan_Proses_Via_CMD.png" width="700">

Untuk mematikan proses dapat menggunakan perintah

```
taskkill /IM nama_proses.exe /F
```

Contoh :

```
taskkill /IM notepad.exe /F
```

<img src="images/07_Mematikan_Proses_Via_CMD.png" width="700">

Untuk memastikan proses berhenti. Gunakan Perintah:

```
tasklist | findstr /i "Nama_Aplikasi"
```

Contoh :

<img src="images/08_Memastikan_Proses_Berhenti.png" width="700">

#### Pembahasan

---

2. Merestart Proses

Untuk merestart proses dapat dilakukan dengan perintah

```
start "" notepad
```

<img src="images/09_Merestart_Proses.png" width="700">

<img src="images/10_Merestart_Proses.png" width="700">

#### Pembahasan

---

## PRAKTIK 2 - KOMUNIKASI ANTAR PROSES pada SISTEM TERDISTRIBUSI

### 1. Buat Workspace-01

<img src="images/11_Buat_Workspace.png" width="700">

#### Pembahasan

---

# 📝 Kesimpulan

---

## 🗒️ Referensi
