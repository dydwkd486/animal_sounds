# animal_sounds

기본 사양
파이썬 3.6.0
postgresql 11.2

설치
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

- 우분투 기준
sudo -u postgres psql

postgres=# ALTER USER postgres with encrypted password 'password';

sudo /etc/init.d/postgresql restart

3. 깃 설치
 git clone https://github.com/dydwkd486/animal_sounds.git

