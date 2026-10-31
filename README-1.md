<div align="center">
  <img src="https://www.image2url.com/r2/default/images/1792516845807-06420514-e480-4470-a4e3-c437d537cb7d.jpeg" alt="FityoraStore — anime banner" width="100%" />
</div>

<div align="center">

# ⚡ FITYORASTORE
### Gaming Top-Up · Digital Commerce · Secure by Design

**Top up lebih praktis. Harga lebih transparan. Pengelolaan lebih terkontrol.**

<p>
  <img src="https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React 18" />
  <img src="https://img.shields.io/badge/TypeScript-5-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/Vite-7-646CFF?style=for-the-badge&logo=vite&logoColor=white" alt="Vite 7" />
  <img src="https://img.shields.io/badge/Supabase-Backend-3FCF8E?style=for-the-badge&logo=supabase&logoColor=white" alt="Supabase" />
  <img src="https://img.shields.io/badge/Vercel-Deployment-000000?style=for-the-badge&logo=vercel&logoColor=white" alt="Vercel" />
</p>

[Repository](https://github.com/cahyostore-elder/FITYORATOPUP) · [Dokumentasi lengkap & riwayat perubahan](./PEMBARUAN.md)

</div>

---

> [!IMPORTANT]
> **STATUS RILIS: BELUM TERBUKA UNTUK TRANSAKSI PRODUKSI.** Repository ini adalah source project yang sedang melalui rekonsiliasi database dan pemeriksaan rilis. Migration history Supabase produksi belum memiliki baseline yang tervalidasi, sementara schema live sudah memuat sebagian perubahan historis. Jangan membuka checkout pelanggan, menjalankan `supabase db push`, `supabase db reset --linked`, atau mengeksekusi migration arsip sebelum backup, baseline, dan forward migration ditinjau serta diuji.

## ✦ Tentang FityoraStore

FityoraStore adalah platform katalog dan pemesanan top-up game/digital yang dibangun dengan **React, TypeScript, Vite, dan Supabase**. Source utama aplikasi berada langsung di root repository ini.

Proyek ini dirancang dengan fokus pada pengalaman pembeli, kontrol admin, transparansi harga, dan keamanan proses order. Aturan penting seperti validasi pesanan, perhitungan total, hak akses, dan perubahan data sensitif harus ditegakkan di database—bukan hanya mengandalkan tampilan frontend.

## ◈ Fitur utama

| Area | Kemampuan |
|---|---|
| **Storefront** | Katalog kategori dan brand, pencarian nominal, sortir harga, tampilan responsif, serta status pemuatan dan retry. |
| **Akun pembeli** | Autentikasi, profil, dashboard pelanggan, dan riwayat pesanan sesuai hak akses akun. |
| **Checkout** | Validasi tujuan, ringkasan biaya, pencegahan submit berulang, dan kontrak order dengan database. |
| **Status pesanan** | Pencarian status dengan kode order dan informasi status yang lebih jelas. |
| **Dashboard admin** | Pengelolaan katalog/konten, pesanan, maintenance, serta pengaturan harga sesuai role. |
| **Supplier cost** | Pemisahan harga modal dari harga jual, pencatatan audit, serta alur simpan yang dibatasi untuk admin/Author. |
| **Bulk pricing** | Preview perubahan, impor/ekspor CSV, validasi data, konfirmasi, dan pemrosesan batch atomik sesuai migrasi yang aktif. |
| **Quality & security** | Regression test, release audit, validasi konfigurasi publik, RLS, dan pemeriksaan RPC. |

> **Catatan operasional:** pembayaran dan pemenuhan top-up tetap memerlukan verifikasi manual kecuali integrasi payment gateway/provider benar-benar dikonfigurasi dan diuji terpisah. Bukti pembayaran yang diunggah bukan bukti bahwa dana telah diterima.

## ⌁ Teknologi

- **Frontend:** React 18, TypeScript, Vite 7.
- **UI & styling:** Tailwind CSS dan Lucide Icons.
- **Backend platform:** Supabase (PostgreSQL, Auth, RLS, RPC, Storage).
- **Deployment target:** Vercel.
- **Automated checks:** Node.js built-in test runner, TypeScript compiler, ESLint, dan Vite production build.

## 🚀 Menjalankan project secara lokal

Gunakan Codespaces atau lingkungan lokal dengan **Node.js 20.19+ atau 22.12+**.

### 1. Clone repository

```bash
git clone https://github.com/cahyostore-elder/FITYORATOPUP.git
cd FITYORATOPUP
```

Pastikan terminal berada di root project—folder yang berisi `package.json`.

### 2. Install dependency

```bash
npm ci
```

### 3. Siapkan environment

Salin `.env.example` menjadi `.env.local`, lalu isi nilai milik project Supabase yang benar:

```env
VITE_SUPABASE_URL=https://YOUR_PROJECT_REF.supabase.co
VITE_SUPABASE_PUBLISHABLE_KEY=YOUR_PUBLIC_PUBLISHABLE_KEY
```

Jangan commit `.env.local`. Jangan pernah menaruh `service_role`, `sb_secret_*`, password database, atau token privat ke variabel `VITE_*` karena variabel frontend dapat masuk ke bundle browser.

### 4. Jalankan development server

```bash
npm run dev
```

Vite akan menampilkan alamat lokal yang dapat dibuka di browser.

## 🧪 Pemeriksaan kualitas

Jalankan pemeriksaan dari root repository:

```bash
# TypeScript typecheck + ESLint + Vite production build
npm run check

# Seluruh regression test berbasis Node.js
node --test scripts/*.test.mjs

# Rangkaian release audit
npm run audit:release
```

Perintah tambahan tersedia melalui script `audit:phase*` di `package.json`, misalnya `npm run audit:phase64` untuk rekonsiliasi produksi.

**Penting:** tes statis/source-contract tidak membuktikan bahwa migration telah diterapkan ke Supabase live, RLS benar di project produksi, transfer telah diterima, WhatsApp berfungsi di semua perangkat, atau supplier telah memenuhi pesanan. Semua itu memerlukan pengujian terkontrol pada lingkungan Preview/live.

## 🛡️ Keamanan dan aturan harga

### Supabase & akses data

- RLS dan otorisasi RPC/database adalah batas keamanan utama.
- Pemeriksaan role di frontend hanya untuk UX, bukan pengganti pemeriksaan role di server/database.
- Fungsi `SECURITY DEFINER` harus memiliki `search_path` yang dipatok dan pemeriksaan otorisasi yang benar.
- Berikan `EXECUTE` hanya kepada role yang memang memerlukan.
- Jangan pernah mengekspos service-role/secret key di source, Git, atau bundle frontend.

### Harga modal dan harga jual

- Harga modal supplier disimpan terpisah dari harga jual.
- Modal kosong berarti **belum dikonfigurasi**, bukan otomatis Rp0.
- Menyimpan modal saja tidak boleh mengubah harga jual.
- Perubahan harga jual harus melalui preview dan konfirmasi eksplisit oleh role yang berwenang.
- Aturan markup 7% yang terdokumentasi adalah `round(supplier_cost * 1.07, 0)`—markup atas modal, bukan gross margin 7%.

### Biaya pembayaran

Aturan biaya yang terdokumentasi di rangkaian fase:

| Metode | Biaya admin |
|---|---:|
| QRIS | Rp300 |
| DANA / GoPay / OVO / ShopeePay | Rp500 |
| SeaBank | Rp1.000 |

Kode unik pembayaran yang dituju setelah Phase 54 adalah Rp200–Rp999. **Database harus menjadi sumber kebenaran** untuk biaya dan total akhir. Cocokkan aturan ini dengan fungsi database yang benar-benar aktif sebelum menerima order.

## ⚠️ Status database & migrasi produksi

Repository baru ini menyimpan 30 migration historis di:

```text
supabase/archive/migrations-pre-baseline-20261030/
```

Folder aktif `supabase/migrations/` sengaja dikosongkan sampai baseline produksi dan migration lanjutan direkonsiliasi. File dalam folder arsip merupakan **bukti historis**, bukan daftar perintah SQL yang boleh dijalankan ulang.

Sebelum perubahan database produksi:

1. Pastikan project ref Supabase sesuai dengan Environment Variables Vercel.
2. Buat dan verifikasi backup yang benar-benar dapat dipulihkan, termasuk komponen data/Auth/Storage yang relevan.
3. Tinjau schema live, kebijakan RLS, grant, fungsi RPC, indeks, trigger, dan status migration.
4. Susun baseline serta forward-only migration yang sudah direview.
5. Uji pada staging/local dan lakukan smoke test sebelum menyentuh traffic pelanggan.

**Jangan** menjalankan seluruh SQL arsip sekaligus. Jangan menggunakan `migration repair --status applied` sebagai pengganti pemeriksaan efek SQL—perintah tersebut hanya mengubah migration ledger.

Detail panduan operasional, riwayat fase, audit, keamanan, dan rekonsiliasi migrasi tersedia di [`PEMBARUAN.md`](./PEMBARUAN.md).

## ▲ Deploy ke Vercel

Gunakan konfigurasi berikut:

| Pengaturan | Nilai |
|---|---|
| Root Directory | `./` |
| Framework Preset | Vite |
| Install Command | `npm ci` |
| Build Command | `npm run build` |
| Output Directory | `dist` |

Tambahkan environment variables pada Vercel Preview dan Production:

- `VITE_SUPABASE_URL`
- `VITE_SUPABASE_PUBLISHABLE_KEY`

Deploy ke **Preview terlebih dahulu**. Uji login, katalog, pemilihan nominal, checkout dengan order uji, cek status, hak akses admin, perubahan harga, dan layout mobile. Promosikan ke Production hanya setelah pemeriksaan source, database, dan alur transaksi lolos.

## 🗂️ Struktur repository

```text
FITYORATOPUP/
├── src/                         # Source React/TypeScript
├── public/                      # Asset publik
├── scripts/                     # Regression test dan audit
├── supabase/
│   ├── migrations/              # Forward migrations aktif (menunggu baseline)
│   ├── archive/                 # Migration historis — jangan dieksekusi ulang
│   └── audits/                  # SQL pemeriksaan/read-only
├── .env.example                 # Template environment tanpa secret
├── package.json                 # Script dan dependency
├── vite.config.ts               # Konfigurasi Vite dan guard key
├── vercel.json                  # SPA rewrite untuk Vercel
└── README.md                    # Dokumentasi proyek
```

## 📚 Dokumentasi

- [`PEMBARUAN.md`](./PEMBARUAN.md) — seluruh dokumentasi teknis, riwayat fase, laporan audit, dan catatan operasional.
- [`package.json`](./package.json) — daftar perintah dev, check, dan audit.
- [`supabase/archive/`](./supabase/archive/) — arsip migrasi historis untuk referensi; bukan instruksi eksekusi.

## 🤝 Kontribusi dan perubahan

Sebelum mengirim perubahan:

1. Kerjakan dari branch yang benar dan pastikan tidak menimpa pekerjaan lokal lain.
2. Jalankan tes yang relevan serta `npm run check`.
3. Untuk perubahan SQL, sertakan alasan, prasyarat, rollback/forward plan, dan tes akses role.
4. Jangan sertakan `.env.local`, secret, kredensial, atau data pelanggan.
5. Perbarui dokumentasi bila alur rilis atau aturan operasional berubah.

---

<div align="center">

### ⚡ FITYORASTORE
**Top up dengan lebih praktis. Kelola dengan lebih aman.**

<sub>Built with React · TypeScript · Vite · Supabase</sub>

</div>
