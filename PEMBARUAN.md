# PEMBARUAN — Riwayat Pengembangan FityoraStore

> Ringkasan utama riwayat fase pada branch `ci/security-audit-policy-2026-10-31`.
> Pembaruan rangkuman: 31 Oktober 2026.

## Cakupan dan cara membaca

Dokumen ini menyatukan inti pembaruan yang sebelumnya tersebar di banyak laporan dan log fase. Branch yang diperiksa memiliki dokumen fase 1–61 dan 64; fase 62–63 disebut dalam catatan fase 61/64, tetapi tidak ditemukan sebagai laporan mandiri. Dokumen fase 65–67 tidak ditemukan pada branch ini.

Catatan fase lama berisi banyak output tes berulang. Karena itu, file ini adalah **rangkuman terstruktur**, bukan salinan mentah seluruh log. Riwayat commit Git tetap menyimpan file sumber sebelum konsolidasi. Skrip tes, migration SQL, audit SQL, manifest katalog, konfigurasi, dan source aplikasi bukan changelog dan harus tetap dipertahankan.

## 1. Riwayat perubahan

| Fase | Ringkasan |
|---|---|
| **1–10: Fondasi order dan audit** | Kode pembayaran unik yang dibuat server; alur status pesanan dan audit pembayaran/fulfillment; total checkout dari database; perlindungan state autentikasi dari respons lama; retry dan error state katalog; tes statis/integrasi/regresi serta release gate awal. |
| **11–20: Buyer experience dan checkout** | Penyempurnaan UI/storefront; pencarian dan pengurutan nominal; validasi nomor tujuan/ID pelanggan; pencegahan submit ganda; halaman cek status pesanan dengan validasi kode dan refresh manual. |
| **21–30: Keamanan dan ketahanan rilis** | Hardening RPC dan `search_path`; pemeriksaan grant/role dan keamanan public key; timeout/retry katalog; responsivitas, aksesibilitas, konsistensi desain; CI, preflight, dan pemeriksaan kebersihan rilis. |
| **31–40: Commerce safety, idempotensi, pembayaran manual, katalog** | Isolasi order pelanggan dan checkout aman; request ID/idempotensi untuk mencegah order ganda saat retry; bukti pembayaran di Storage privat dengan akses pemilik/admin; pembayaran dan fulfillment tetap manual; impor katalog/provider code dan harga Roblox yang diberikan pemilik. |
| **41–50: Operasional admin dan stabilitas UI** | Hapus order terbatas untuk admin/Author; maintenance website dan tanggal order; ikon game; pemulihan pengaturan maintenance; perbaikan hak akses/edit harga; penyegaran UI/modal/aksesibilitas dan React Error Boundary. |
| **51–60: Konfigurasi, supplier cost, harga massal** | Keamanan konfigurasi Supabase lokal dan public/publishable key; tabel modal supplier privat; CSV import/export; preview dan konfirmasi perubahan; aturan biaya pembayaran/kode unik; dashboard buyer/admin; penyimpanan paket dan bulk pricing atomik; hardening RLS, indeks, dan RPC admin. |
| **61–64: Baseline produksi dan rekonsiliasi migrasi** | Urutan rollout database; migration ledger produksi yang belum terbentuk; mode maintenance terpisah (fase 62) dan status modal sample/verified (fase 63) sebagaimana dirujuk di catatan fase 61/64; serta rekonsiliasi read-only atas 19 migrasi produksi lama pada fase 64. |

## 2. Aturan bisnis yang sudah terdokumentasi

- **Biaya admin:** QRIS Rp300; DANA/GoPay/OVO/ShopeePay Rp500; SeaBank Rp1.000.
- **Kode unik:** target aturan setelah fase 54 adalah Rp200–Rp999. Total transfer dihitung oleh database: harga paket + biaya metode + kode unik.
- **Harga modal supplier:** nilai kosong berarti belum dikonfigurasi; Rp0 hanya nilai valid jika dimasukkan secara eksplisit. Aksi simpan modal saja tidak boleh mengubah harga jual.
- **Markup harga:** rumus Author yang terdokumentasi adalah `round(supplier_cost * 1.07, 0)` (markup 7% dari modal, bukan margin 7%). Perubahan harga jual memerlukan preview dan konfirmasi eksplisit.
- **Harga massal:** CSV menggunakan ID paket stabil; perubahan dipreview sebelum disimpan; batch database harus atomik dan menyediakan laporan baris gagal/berhasil.
- **Pembayaran dan pemenuhan:** unggah bukti bukan bukti dana diterima. Order hanya boleh ditandai lunas/sukses setelah pembayaran diverifikasi dan top-up benar-benar dipenuhi. Jangan menganggap gateway/provider otomatis tersedia tanpa implementasi dan tes live tersendiri.

## 3. Snapshot produksi terakhir yang tercatat

**Tanggal snapshot: 30 Oktober 2026 (Asia/Jakarta).** Ini adalah audit read-only dalam laporan fase 61/64, bukan verifikasi ulang pada saat dokumen ini dirapikan.

| Item | Hasil saat snapshot |
|---|---:|
| Status Supabase | ACTIVE_HEALTHY |
| Tabel publik | 11; RLS aktif pada seluruh tabel |
| Kategori / brand / paket | 3 / 18 / 309 |
| Paket harga jual Rp0 / di atas Rp0 | 189 / 120 |
| Pesanan | 0 |
| Baris modal supplier / audit harga | 0 / 0 |
| Pengaturan situs | 1 baris; maintenance global tercatat aktif |

### Peringatan migrasi produksi

- Pada snapshot itu, schema dan tabel migration ledger Supabase tidak ditemukan dan `list_migrations` mengembalikan daftar kosong. Ini **bukan** bukti bahwa migrasi lama belum pernah diterapkan; sebagian efek migrasi terlihat di schema produksi dan sebagian definisinya telah berubah.
- Backup produksi lengkap yang bisa dipulihkan belum terkonfirmasi. Export schema saja bukan backup penuh; role, data, Auth, Storage, konfigurasi bucket, dan file objek perlu diperhitungkan.
- Jangan jalankan `supabase db push`, `supabase db reset --linked`, atau menandai semua timestamp sebagai applied sebelum backup, baseline, dan rekonsiliasi diselesaikan.
- Jangan mengulang migration seed katalog/brand lama secara massal. File lama dapat menggandakan entri atau menimpa data yang sudah diedit.
- Pertahankan event trigger `ensure_rls`; perbaiki hak eksekusi fungsi yang relevan tanpa menonaktifkan trigger tersebut.

## 4. Prinsip keamanan dan implementasi

1. Browser hanya boleh menerima Supabase URL dan public/publishable anon key. `service_role`, `sb_secret_*`, password database, dan token privat tidak boleh berada di `VITE_*`, source frontend, atau Git.
2. RLS, grant, dan validasi RPC di database adalah batas keamanan utama. Pemeriksaan role di UI bukan pengganti otorisasi database.
3. Fungsi `SECURITY DEFINER` harus mematok `search_path` dan memeriksa otorisasi. Grant `EXECUTE` hanya untuk role yang membutuhkan.
4. Order pelanggan harus terisolasi. Lookup publik untuk cek status hanya boleh mengembalikan data minimum dan tetap perlu peninjauan abuse/rate-limit.
5. Request key/idempotensi hanya boleh dipakai ulang untuk payload checkout yang sama. Respons pemuatan katalog yang sudah usang tidak boleh menimpa pilihan brand terbaru.
6. Perubahan harga, modal supplier, RLS, dan migrasi produksi harus divalidasi serta diaudit. Jangan menyatakan penyimpanan berhasil sebelum respons database dikonfirmasi.

## 5. Cara menjalankan pemeriksaan saat ini

Hasil tes di laporan lama adalah hasil pada waktu masing-masing fase dibuat; bukan bukti bahwa source terbaru sudah lulus. Dari root proyek, setelah dependency terpasang:

```bash
npm ci
npm run check
node --test scripts/*.test.mjs
npm run audit:release
```

- `npm run check`: TypeScript typecheck, ESLint, dan Vite production build.
- `node --test scripts/*.test.mjs`: seluruh tes regresi Node yang tersedia.
- `npm run audit:release`: rangkaian release checks yang didaftarkan di `package.json`.
- Jalankan juga `npm run audit:phaseXX` yang relevan saat mengubah area tertentu.

Tes statis/source-contract tidak membuktikan RLS live, RPC benar-benar terpasang, transfer diterima, WhatsApp bekerja di semua perangkat, atau supplier telah mengirim top-up. Pemeriksaan tersebut memerlukan Preview/live test terkontrol.

## 6. Pekerjaan yang masih perlu dibereskan

- Selesaikan backup dan rekonsiliasi baseline Supabase sebelum migration push otomatis atau DDL produksi.
- Ikuti urutan supplier-cost: Phase 57A → deploy dan uji frontend RPC → baru Phase 57B (table lockdown).
- RPC pricing fase 63 yang status-aware harus diperlakukan sebagai pengganti RPC lama. Jangan menerapkan ulang definisi fungsi lama fase 56/58/60 setelah penggantinya dipasang.
- Jalankan ulang typecheck, lint, build, semua tes, dan release audit dari source/branch yang benar.
- Pada pemeriksaan sesi ini, branch GitHub yang dibaca masih memakai `setPackageError` pada `src/pages/TopupPage.tsx`, sedangkan workspace lokal yang dibahas sudah memakai pola `packageResult`. Sinkronkan source yang benar dan tuntaskan regression test retry serta stale-response sebelum rilis.
- Setelah source checks lulus, deploy ke Vercel Preview; uji alur customer/admin pada perangkat nyata dan gunakan order uji. Verifikasi pembayaran serta fulfillment secara manual sebelum promosi ke production.

## 7. File yang wajib tetap ada

Dokumen fase dapat diringkas, tetapi jangan menghapus file yang diperlukan aplikasi atau audit:

- `src/` — source aplikasi.
- `scripts/` — test regresi dan audit yang dapat dijalankan.
- `supabase/migrations/` — migration aktif; setiap migration harus direkonsiliasi sebelum diterapkan.
- `supabase/archive/` — salinan migration historis.
- `supabase/audits/` dan SQL read-only diagnostics — pemeriksaan schema/keamanan.
- Manifest katalog `.csv`/`.json`, konfigurasi, lockfile, `README.md`, dan `AUDIT_REPORT.md`.

**Kesimpulan:** gunakan `PEMBARUAN.md` sebagai satu pintu baca riwayat fase. Source aplikasi, tes otomatis, SQL migration, manifest katalog, dan audit operasional tetap dipisah karena mempunyai fungsi teknis yang berbeda.
