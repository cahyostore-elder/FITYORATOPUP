<!-- FITYORASTORE README | Premium dark / neon edition -->

<div align="center">
  <img
    src="https://capsule-render.vercel.app/api?type=waving&color=0:080B1A,45:10294A,100:00D4FF&height=205&section=header&text=FITYORASTORE&fontSize=52&fontColor=FFFFFF&animation=twinkling&fontAlignY=36&desc=Gaming%20Top-Up%20%7C%20Digital%20Commerce&descAlignY=57&descSize=16"
    alt="FityoraStore animated neon header"
    width="100%"
  />
  <img
    src="https://www.image2url.com/r2/default/images/1792516845807-06420514-e480-4470-a4e3-c437d537cb7d.jpeg"
    alt="FityoraStore anime banner"
    width="100%"
  />
</div>

<div align="center">
  <img
    src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=20&duration=2800&pause=900&color=00D9FF&center=true&vCenter=true&width=820&lines=Top+up+lebih+praktis%2C+harga+lebih+jelas.;Built+with+React+%2B+TypeScript+%2B+Vite.;Supabase+%7C+Security+%7C+Reliable+Order+Flow."
    alt="Animated FityoraStore typing tagline"
  />

  <p>
    <img src="https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=101010" alt="React 18" />
    <img src="https://img.shields.io/badge/TypeScript-5-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript 5" />
    <img src="https://img.shields.io/badge/Vite-7-646CFF?style=for-the-badge&logo=vite&logoColor=white" alt="Vite 7" />
    <img src="https://img.shields.io/badge/Supabase-Backend-3FCF8E?style=for-the-badge&logo=supabase&logoColor=white" alt="Supabase" />
    <img src="https://img.shields.io/badge/Vercel-Deploy-000000?style=for-the-badge&logo=vercel&logoColor=white" alt="Vercel" />
  </p>

  **Gaming Top-Up · Digital Commerce · Secure by Design**

  [Repository](https://github.com/cahyostore-elder/FITYORATOPUP)
  · [Dokumentasi terpadu](./PEMBARUAN.md)
  · [Issues](https://github.com/cahyostore-elder/FITYORATOPUP/issues)
</div>

---

> [!IMPORTANT]
> **STATUS PRODUKSI: BELUM BOLEH DIANGGAP SIAP UNTUK TRANSAKSI PELANGGAN.**
> Repository ini masih memerlukan rekonsiliasi migration history dengan schema Supabase live. Jangan membuka checkout produksi, menjalankan `supabase db push`, `supabase db reset --linked`, atau mengeksekusi SQL arsip sebelum backup, baseline, dan forward migration ditinjau serta diuji.

## ✦ Tentang FityoraStore

FityoraStore adalah platform katalog dan pemesanan top-up game/digital. Source utama website berada langsung di root repository dan menggunakan React, TypeScript, Vite, serta Supabase.

Fokus pengembangannya adalah pengalaman pembeli yang nyaman, kontrol admin yang jelas, harga transparan, dan alur pesanan yang aman. Validasi order, perhitungan total, hak akses, serta perubahan data sensitif wajib ditegakkan di database—bukan hanya mengandalkan tampilan frontend.

## ◈ Fitur utama

| Area | Kemampuan |
|---|---|
| Storefront | Katalog game, brand dan paket; pencarian nominal; tampilan responsif; loading, retry, dan empty state. |
| Akun pembeli | Autentikasi, profil, dashboard pelanggan, serta riwayat pesanan sesuai hak akses. |
| Checkout | Validasi tujuan, ringkasan biaya, pencegahan submit berulang, dan integrasi order melalui database. |
| Status pesanan | Pengecekan status menggunakan kode order. |
| Dashboard admin | Pengelolaan katalog, konten, pesanan, maintenance, dan harga sesuai role. |
| Harga supplier | Harga modal dipisahkan dari harga jual; perubahan modal tidak boleh diam-diam mengubah harga jual. |
| Bulk pricing | Alur preview, validasi, konfirmasi, serta impor/ekspor data sesuai implementasi dan migration aktif. |
| Quality & security | Regression tests, release audits, validasi environment, RLS, dan pemeriksaan RPC. |

> Pembayaran dan pemenuhan top-up tetap perlu diverifikasi sesuai alur operasional yang benar-benar aktif. Bukti pembayaran yang diunggah tidak otomatis membuktikan dana telah diterima.

## ⌁ Teknologi

- **Frontend:** React 18, TypeScript, Vite 7.
- **UI:** Tailwind CSS dan Lucide Icons.
- **Backend platform:** Supabase — PostgreSQL, Auth, RLS, RPC, dan Storage.
- **Deployment target:** Vercel.
- **Quality checks:** TypeScript, ESLint, Vite production build, dan Node.js test runner.

## 🚀 Menjalankan project

Pastikan terminal berada di folder root yang berisi `package.json`.

### 1. Clone repository

```bash
git clone https://github.com/cahyostore-elder/FITYORATOPUP.git
cd FITYORATOPUP
```

### 2. Install dependency

```bash
npm ci
```

### 3. Siapkan environment lokal

Salin `.env.example` menjadi `.env.local`, lalu isi konfigurasi Supabase milik project yang benar:

```env
VITE_SUPABASE_URL=https://YOUR_PROJECT_REF.supabase.co
VITE_SUPABASE_PUBLISHABLE_KEY=YOUR_PUBLIC_PUBLISHABLE_KEY
```

Jangan commit `.env.local`. Jangan pernah memasukkan `service_role`, `sb_secret_*`, password database, atau token privat ke variabel `VITE_*` karena nilainya dapat masuk ke bundle browser.

### 4. Jalankan development server

```bash
npm run dev
```

Vite akan menampilkan alamat lokal untuk dibuka di browser.

## 🧪 Pemeriksaan kualitas

Jalankan dari root repository:

```bash
# TypeScript + ESLint + production build
npm run check

# Seluruh regression tests
node --test scripts/*.test.mjs

# Rangkaian release audit
npm run audit:release
```

Audit fase tertentu tetap tersedia melalui script `audit:phase*` di `package.json`, contohnya:

```bash
npm run audit:phase57
npm run audit:phase61
npm run audit:phase64
```

Tes statis/source-contract tidak membuktikan bahwa migration sudah diterapkan ke Supabase live, pembayaran telah diterima, atau supplier telah memenuhi pesanan. Verifikasi live dan smoke test tetap diperlukan.

## 🛡️ Keamanan dan aturan harga

### Supabase dan akses data

- RLS dan otorisasi di database/RPC adalah batas keamanan utama.
- Pemeriksaan role di frontend hanya untuk UX, bukan pengganti otorisasi server/database.
- Fungsi `SECURITY DEFINER` harus memiliki `search_path` yang dipatok dan pemeriksaan otorisasi yang benar.
- Berikan hak `EXECUTE` hanya kepada role yang memerlukannya.
- Jangan pernah mengekspos service-role atau secret key di source, Git, maupun bundle frontend.

### Harga modal dan harga jual

- Harga modal supplier disimpan terpisah dari harga jual.
- Modal kosong berarti belum dikonfigurasi, bukan otomatis Rp0.
- Menyimpan atau memperbarui harga modal saja tidak boleh mengubah harga jual.
- Perubahan harga jual harus melalui preview dan konfirmasi eksplisit oleh role yang berwenang.
- Setiap perubahan sensitif perlu divalidasi dan dicatat sesuai mekanisme audit aplikasi.

## ⚠️ Status migrasi Supabase

Migration historis yang belum direkonsiliasi disimpan di area arsip. File SQL arsip adalah **bahan pemeriksaan historis**, bukan instruksi untuk dieksekusi ulang.

Sebelum perubahan pada database produksi:

1. Pastikan project ref Supabase sesuai dengan environment Vercel.
2. Buat backup dan verifikasi bahwa backup dapat dipulihkan.
3. Periksa schema live, RLS, grants, fungsi RPC, trigger, indeks, dan migration ledger.
4. Susun baseline serta forward-only migration yang sudah direview.
5. Uji di staging/local dan lakukan smoke test sebelum menyentuh traffic pelanggan.

**Jangan** menjalankan seluruh SQL arsip sekaligus. Perubahan migration ledger bukan pengganti pemeriksaan efek SQL pada database.

## ▲ Deploy ke Vercel

Gunakan pengaturan berikut:

| Pengaturan | Nilai |
|---|---|
| Root Directory | `./` |
| Framework Preset | Vite |
| Install Command | `npm ci` |
| Build Command | `npm run build` |
| Output Directory | `dist` |

Tambahkan environment variables berikut pada Preview dan Production:

- `VITE_SUPABASE_URL`
- `VITE_SUPABASE_PUBLISHABLE_KEY`

Deploy ke **Preview terlebih dahulu**. Uji login, katalog, pemilihan paket, checkout dengan order uji, status pesanan, hak akses admin, perubahan harga, dan tampilan mobile. Promosikan ke Production hanya setelah pemeriksaan source, database, dan alur transaksi lolos.

## 🗂️ Struktur repository

```text
FITYORATOPUP/
├── .github/                 # Workflow GitHub
├── public/                  # Asset publik
├── scripts/                 # Regression tests dan audit
├── src/                     # Source React/TypeScript
├── supabase/
│   ├── migrations/          # Forward migrations aktif
│   ├── archive/             # Arsip historis — jangan replay
│   └── audits/              # Pemeriksaan database
├── .env.example             # Template environment tanpa secret
├── package.json             # Dependency dan perintah npm
├── vite.config.ts           # Konfigurasi Vite
├── vercel.json              # Konfigurasi deployment
├── PEMBARUAN.md             # Dokumentasi proyek terpadu
└── README.md                # Halaman utama repository
```

## 📚 Dokumentasi proyek

Dokumentasi teknis, catatan fase, panduan, dan laporan audit dikumpulkan di **[PEMBARUAN.md](./PEMBARUAN.md)**. File tersebut menjadi rujukan dokumentasi proyek; README ini dipertahankan sebagai halaman pengantar utama.

## 🤝 Kontribusi dan perubahan

1. Pastikan bekerja pada branch yang benar dan tidak menimpa perubahan lokal lain.
2. Jalankan regression tests dan `npm run check` sebelum commit.
3. Untuk perubahan SQL, sertakan prasyarat, alasan, strategi forward/rollback, dan tes akses role.
4. Jangan sertakan file environment lokal, secret, kredensial, atau data pelanggan.
5. Perbarui dokumentasi ketika alur rilis atau aturan operasional berubah.

---

<div align="center">
  <img
    src="https://capsule-render.vercel.app/api?type=waving&color=0:00D4FF,50:10294A,100:080B1A&height=115&section=footer&animation=twinkling"
    alt="FityoraStore neon footer"
    width="100%"
  />

  **⚡ FITYORASTORE**

  <sub>Top up lebih praktis · Harga lebih jelas · Kelola lebih aman</sub>

  <br />

  <sub>Built with React · TypeScript · Vite · Supabase</sub>
</div>
