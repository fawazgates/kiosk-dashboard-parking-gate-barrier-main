# kiosk dashboard parking gate barrier



## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://gitlab.com/bisa_ai/msib/kiosk-group/kiosk-dashboard-parking-gate-barrier.git
git branch -M main
git push -uf origin main
```
## Install 
- Untuk menjalankan program web dashboard ini diperlukan install ``` requirements.txt ``` yang berisi beberapa package yang perlu diinstall 
- Sangat disarangkan menggunakan virtual environment pythonn (venv)

## Penjelasan Fitur Web Dashboard 
Berikut adalah fitur fitur yang ada web dashboard ini 
### Login 
Default admin web 
username : admin 
Password : admin 
### Fitur Dashboard 
Dashboard digunakan untuk menampilkan history kendaraan yang masuk dan keluar melewati smart barrier gate ini, Data didapat dari seseorang menscan rfid lewat rfid scanner yang terdapat pada box control smart barrier gate lalu dari box control tersebut terdapat raspberry pi yang digunakan untuk mengirim data ke database dan ditampilkan lewat dashboard ini untuk program raspberry i terdapat pada branch ``` hardware   ```
### Fitur Database 
Digunakan untuk menampilkan database yang berisi daftar daftar orang yang telah terdaftar pada sistem database ini 
### Fitur Register RFID 
Digunakan untuk mendaftarkan RFID Baru pada pengguna atau penduduk member rfid baru ke database sehingga dapat ditampilkan pada fitur database
### Fitur Register Admin 
Digunakan untuk mendaftarkan admin untuk masuk ke sistem web ini 
