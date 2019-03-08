﻿# animal_sounds

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

## 실행
```
python3 manage.py runserver
```

```
System check identified no issues (0 silenced).
March 05, 2019 - 17:36:26
Django version 2.1.7, using settings 'animal_sounds.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

## 추가 적으로 해야할 사항
* 2019.03.06
- 회원가입
   - ~~회원가입시 성공 알림 필요.~~
   - ~~스테프 권한 안되는 문제 해결 할것.~~

- 동물 디테일
   - ~~수정 누르고 수정후 오류문제 해결할것.~~
   - ~~수정, 삭제 당사자만 보이게 하기.~~	

- 메인화면
   - 표도 연결시키기
   - ~~이미지 안나올때 대체할 것~~
   - ~~검색 결과 없을시: 화면에 검색 결과 발견되지 않았습니다 추가~~
   - ~~새 위치 저장: 업로드로 변경, 위치는 ANIMAL SOUND, Home,지도, 목록의 최상단이 적합~~
   - 새로 올라온 업로드 리스트를 보여주는 것 같으니 해당 창에 대한 설명 배너 추가
   - 통계창도 마찬가지로 배너 추가
   - ~~지도 검색기능~~
   - ~~지도 검색기능+개체명 검색~~

- 새로운 정보 작성
   - 전문가용, 일반 사용자용 나누기
   - ~~오디오 태깅 추가~~
   - ~~달력폼~~
   - UI 정렬 조금 해야 함
   - ~~지도에 검색기능~~ 
   - ~~'새로운정보 작성' => 업로드~~
   - ~~'File' -> image file 명시~~
   - ~~'content' => 쓰고 싶은 글자 써도 되는거 맞낭~~
   - ~~저장하기 버튼 => 짱 크게~~

- 목록
   - 페이지 만들고 들어갈수있게 하기

- ~~사용법 정리 정리~~
***

