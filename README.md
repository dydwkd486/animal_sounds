# animal_sounds

## 기본 사양

- 파이썬 3.6.0, 3.5.2

- postgresql 11.2

## 설치 방법
### 1. postgresql 설치
- 윈도우 기준
    - postgresql 사이트 : https://www.postgresql.org/
  
    - 11.2버전 설치 바로가기 : https://www.enterprisedb.com/thank-you-downloading-postgresql?anid=1256369

- 우분투 기준
	```
	sudo apt-get update
	sudo apt-get install postgresql
	sudo -u postgres psql
	```

### 2. postgresql 설정 사항
- 윈도우 기준
	```
	psql -U postgres
	postgres 사용자의 암호: 각자 비밀번호 입력 
	postgres=# ALTER USER postgres with encrypted password 'password';
	postgres=# CREATE DATABASE django_test OWNER postgres;
	```

기존 계정(postgres) 비밀번호를 password로 바꿨으며 django_test 데이터베이스를 만들었습니다.

- 우분투 기준
	```
	sudo -u postgres psql
	```
	```
	postgres=# ALTER USER postgres with encrypted password 'password';
	postgres=# CREATE DATABASE django_test OWNER postgres;
	```
	```
	sudo /etc/init.d/postgresql restart
	```
기존 계정(postgres) 비밀번호를 password로 바꿨으며 django_test 데이터베이스를 만들었습니다.

### 3. 깃 설치
	git clone https://github.com/dydwkd486/animal_sounds.git

### 4. requirements 설치
- 윈도우 기준
	```
	pip install -r requirements.txt
	```
- 우분투 기준
	```
	pip3 install -r requirements.txt
	```
   - 오류: The program 'pip3' is currently not installed. To run 'pip3' please ask your administrator to install the  package 'python3-pip'
	```
	sudo apt-get install python3-pip
	```
### 4. DB에 필요 자료 저장.
- 윈도우 기준
	```
	python manage.py migrate
	```
- 우분투 기준
	```
	python3 manage.py migrate
	```
### 5.슈퍼계정 만들기
- 윈도우 기준
	```
	python manage.py createsuperuser
	```
- 우분투 기준
	```
	python3 manage.py createsuperuser
	```
  - 오류 시:UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-2: ordinal not in range(128)
	```
		export PYTHONIOENCODING=utf-8
	```
	입력 후 껏다 켜기.(그래야 적용됨.)

```
사용자 이름 (leave blank to use 'dydwkd486'): admin
이메일 주소: admin@admin.com
Password: 
Password (again): 
비밀번호가 이메일 주소와 너무 유사합니다.
비밀번호가 너무 짧습니다. 최소 8 문자를 포함해야 합니다.
비밀번호가 너무 일상적인 단어입니다.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.
```

## 6.실행
```
python3 manage.py runserver
```

아래와 같이 나오면 잘 실행된것이다.
```
System check identified no issues (0 silenced).
March 05, 2019 - 17:36:26
Django version 2.1.7, using settings 'animal_sounds.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```


## 데이터 베이스 오류 발생시 
자주 실행하다가 데이터 베이스에서 오류가 나면 아래와 같이 하세요

- 윈도우 기준
```
psql -U postgres
postgres 사용자의 암호: 각자 비밀번호 입력
postgres=# DROP DATABASE django_test;
postgres=# CREATE DATABASE django_test OWNER postgres;
```
```
python manage.py createsuperuser
```
```
사용자 이름 (leave blank to use 'dydwkd486'): admin
이메일 주소: admin@admin.com
Password: 
Password (again): 
비밀번호가 이메일 주소와 너무 유사합니다.
비밀번호가 너무 짧습니다. 최소 8 문자를 포함해야 합니다.
비밀번호가 너무 일상적인 단어입니다.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.
```

- 우분투 기준
```
sudo -u postgres psql
postgres=# DROP DATABASE django_test;
postgres=# CREATE DATABASE django_test OWNER postgres;
```
```
python3 manage.py createsuperuser
```
```
사용자 이름 (leave blank to use 'dydwkd486'): admin
이메일 주소: admin@admin.com
Password: 
Password (again): 
비밀번호가 이메일 주소와 너무 유사합니다.
비밀번호가 너무 짧습니다. 최소 8 문자를 포함해야 합니다.
비밀번호가 너무 일상적인 단어입니다.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.
```

## 7.샘플데이터 및 통계 좌표 추가
- 우분투 기준
``` 
sudo -u postgres psql -d django_test -a -f blog_district_201905211131.sql
sudo -u postgres psql -d django_test -a -f dataadd.txt
```
---


## 잊어 먹을까봐 잠시 적어 놓음.
```
sudo -u postgres pg_restore -d django_test test.dump


sudo vi /etc/postgresql/9.5/main/pg_hba.conf
--md5로 변경

nohup python3 manage.py runserver 0.0.0.0:8000 &

sudo lsof -t -i tcp:8000 | xargs kill -9

$ ln -s /etc/nginx/sites-available/ypc /etc/nginx/sites-enable/ypc


sudo ln -s /etc/nginx/sites-available/animal_sounds /etc/nginx/sites-enabled/animal_sounds
sudo ln -s /etc/nginx/sites-available/animal_sounds /etc/nginx/sites-enabled/animal_sounds

sudo -u postgres psql -d django_test -a -f blog_district_201905211131.sql
sudo -u postgres psql -d django_test -a -f dataadd.txt


python3 manage.py runserver 0.0.0.0:8000
껏다 키기


nginx를 이용한 포트 설정
#설치
sudo apt-get install nginx

/etc/nginx
/etc/nginx/nginx.conf

http { ... include /etc/nginx/site-enable/*; ... }


sudo apt-get update
sudo apt-get install software-properties-common
sudo add-apt-repository universe
sudo add-apt-repository ppa:certbot/certbot
sudo apt-get update
sudo apt-get install certbot python-certbot-nginx


sudo certbot --nginx
sudo certbot --nginx certonly
sudo certbot -a dns-plugin -i nginx -d animalsound.cf --server https://acme-v02.api.letsencrypt.org/directory

sudo certbot --nginx -d animalsound.cf

sudo certbot renew --dry-run


ssl_certificate /etc/letsencrypt/live/animalsound.cf/fullchain.pem; # managed by Certbot
ssl_certificate_key /etc/letsencrypt/live/animalsound.cf/privkey.pem; # managed by Certbot
include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot


server {
    listen 80;
    server_name 35.243.84.71;

    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}
server {
        server_name 35.243.84.71;
        listen 443 ssl http2 default_server;
        listen [::]:443 ssl http2 default_server ipv6only=on;

        ssl_certificate /etc/letsencrypt/live/animalsound.cf/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/animalsound.cf/privkey.pem;
        ssl_trusted_certificate /etc/letsencrypt/live/animalsound.cf/fullchain.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}
```
---