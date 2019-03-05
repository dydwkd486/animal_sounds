# animal_sounds

## 기본 사양

- 파이썬 3.6.0, 3.5.2

- postgresql 11.2

## 설치 방법
1. postgresql 설치
 - 윈도우 기준
  
 postgresql 사이트 : https://www.postgresql.org/
  
 11.2버전 설치 바로가기 : https://www.enterprisedb.com/thank-you-downloading-postgresql?anid=1256369

 - 우분투 기준
 
 sudo apt-get update

 sudo apt-get install postgresql

 sudo -u postgres psql


2. postgresql 설정 사항
- 윈도우 기준

psql -U postgres

postgres 사용자의 암호: 각자 비밀번호 입력 

postgres=# ALTER USER postgres with encrypted password 'password';

 기존 계정(postgres) 비밀번호를 password로 바꿨습니다.

postgres=# CREATE DATABASE django_test OWNER postgres;

- 우분투 기준
sudo -u postgres psql

postgres=# ALTER USER postgres with encrypted password 'password';

postgres=# CREATE DATABASE django_test OWNER postgres;

sudo /etc/init.d/postgresql restart

3. 깃 설치
 git clone https://github.com/dydwkd486/animal_sounds.git

4. requirements 설치
-윈도우 기준

pip install -r requirements.txt

-우분투 기준
pip3 install -r requirements.txt

 -오류: The program 'pip3' is currently not installed. To run 'pip3' please ask your administrator to install the 
package 'python3-pip'

  --sudo apt-get install python3-pip

4. DB에 필요 자료 저장.

python3 manage.py migrate

5.슈퍼계정 만들기
python3 manage.py createsuperuser

 --오류 시:UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-2: ordinal not in range(128)

  export PYTHONIOENCODING=utf-8

사용자 이름 (leave blank to use 'dydwkd486'): admin

이메일 주소: admin@admin.com

Password: 

Password (again): 

비밀번호가 이메일 주소와 너무 유사합니다.

비밀번호가 너무 짧습니다. 최소 8 문자를 포함해야 합니다.

비밀번호가 너무 일상적인 단어입니다.

Bypass password validation and create user anyway? [y/N]: y

Superuser created successfully.

## 실행

python3 manage.py runserver

	System check identified no issues (0 silenced).
	March 05, 2019 - 17:36:26
	Django version 2.1.7, using settings 'animal_sounds.settings'
	Starting development server at http://127.0.0.1:8000/
	Quit the server with CONTROL-C.
