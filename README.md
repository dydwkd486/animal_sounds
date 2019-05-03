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

sudo -u postgres pg_restore -d django_test test.dump

sudo vi /etc/postgresql/9.5/main/pg_hba.conf
--md5로 변경


## 추가 적으로 해야할 사항
* 2019.03.06
- 회원가입
   - ~~회원가입시 성공 알림 필요.~~
   - ~~스테프 권한 안되는 문제 해결 할것.~~

- 동물 디테일
   - ~~수정 누르고 수정후 오류문제 해결할것.~~
   - ~~수정, 삭제 당사자만 보이게 하기.~~	

- 메인화면
   - ~~표도 연결시키기~~
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
   - ~~UI 정렬 조금 해야 함~~
   - ~~지도에 검색기능~~ 
   - ~~'새로운정보 작성' => 업로드~~
   - ~~'File' -> image file 명시~~
   - ~~'content' => 쓰고 싶은 글자 써도 되는거 맞낭~~
   - ~~저장하기 버튼 => 짱 크게~~

- 목록
   - ~~페이지 만들고 들어갈수있게 하기~~

- ~~사용법 정리 정리~~
***

* 2019.03.11
- 회원가입
   - ~~전문가 및 전문가인 경우 설명에 대해 설명 적기~~
   - 틀린 경우 나오게 하기

- 메인화면
   - ~~시작화면은 메인으로 먼저 들어갈수있게 하기~~
   - ~~맵 옆으로 줄이고 오른쪽에 필터 만들기~~
   - ~~맵확인 누를시 관련해서 필터도 다 적용시키기~~
   - ~~업로드 바 일반인들이 알기 쉽게 변경하기~~
   - ~~좌표에 없는 애들은 맵에 안보이게 수정~~


- 새로운 정보 작성
   - ~~전문가 및 일반인 나누기~~
   - ~~title 부분 개체명으로 바꾸기~~
   - ~~대분류 간단하게 하기~~

- 목록
   - ~~페이지 만들고 들어갈수있게 하기~~

- 웹앱 이용가능하게 기능 늘리기
- 필터 부분에 신경 많이 쓰기
- 소리에 초점이 많이 잡히는 것을 원하는 듯
- 디자인은 일반인이 이용한다는 생각으로 준비
- 연구소에 있던 자료 집어넣기
- 8도 작업

디비 문제 도움말 추가 하기
 - 나중을 위한 디비 백업 방법과 디비, 파일 저장 방법 알기
***

* 2019.03.20
- 로그인
   - (디자인)화면: 벌집 형식으로 변경할것

- 메인화면
   - ~~(디자인)구분과 지역 정렬하기(3개씩 정렬해서 깔끔하게 해도 될듯)~~
   - ~~(디자인) 기간 부분이 색이 없어서 정렬이 안되어있는 느낌이라고 하셨음.~~
   - ~~(기술) 동물 정보들이 지도 안에 보일수있게 작업하기~~
   - (디자인) UI는 최대한 통일감있게 작업하기
   - (기술) 검색결과 없을시 좀더 있어보이게 하기
   - (디자인) 메뉴바를 조금더 세련되게 하기
   - ~~(기술) 메뉴바를 업로드, 검색,목록으로 바꿀것~~

- 디테일 페이지
   - ~~(기술) 이미지 사이즈 늘어지는 문제 해결할 것(비율로 유지하면 될것)~~
   - (기술) 이미지 없는 경우는 어떻게 처리 할것인지?
   - (기술) 소리 클립핑하고 그부분을 사운드로 집어 넣기
   - (기술) 세부정보 집어 넣기
   - (디자인) 디테일 페이지 전체적인 UI는 한 화면에서 다 볼수있게 하고 스크롤을 내리면 생태정보가 보일수있게 하기
   - ~~(기술) 업로드 날짜도 추가하기~~

- 새로운 정보 작성
   - (디자인) 음성파일이 더 중요하니 업로드를 위로 배치 하기
   - (기술,디자인) 이름을 한글로 통일하기 (나아아아아아아중에 영어버전도 만들것)
   - (디자인) add,regist 부분에 사용법?
   - (디자인) 로테이션 정보와 아닌것들이 포함 되어있으니 나눠놓기

- 목록
   - (기술) 조금 더 세세하게 작성하기 

- 서버 부분
   - 스토리지 문제, 무료로 사용하니 유료일때 가격알아보기

***
참고 사이트 http://ko.dbpedia.org/page/, http://lod.nature.go.kr/page/Lutra_lutra

***

***
* 2019.04.03

- 로그인
   - 로그인 화면 가운데에 있었으면 어떨까라는 의견이 나왔음.
   - 뒤 이미지 용량 줄여서 빠르게 나오게 하기(늦게 나온다고 지적하셨음.)
   - 로그인 형식도 정직하게 만들기 (ex. 로그인: 비밀번호:)
   - 데코레이션에 화이팅 해봐라~ 라고 하셨습니다.
- 디테일
   - 음성 자른 데이터가 보일수있게 할수있을까? - 내의견

- 메인 화면
   - ~~메인화면을 3분할하여 1.맵, 2.목록, 3.필터 형식으로 변경~~
   - ~~북한-> 이북으로 변경 요청이 있었음.~~
   - 메뉴바 부분 데코레이션을 원하셨지만 업체끼고 그러면 만들어주것지~ 라고 하심.
   - ~~메인화면에 있는 목록에서 사진부분이 눌림문제, 설명 부분이 너무 작음, "이름:" 없애도 될듯.~~
   - 남는 구간없이 깔끔하게 수정할 것.

- 회원가입
   - 회원가입 부분을 좀 더 정직하게 이용할수 있게 변경 (ex. 아이디: 비밀번호:)
   - 중복확인 기능
   - 로고 누르면 로그인 화면으로 넘어 갈수있게 추가 하기

- 서버 부분
   - 나중에 발표하는 경우가 생길때 추가 하는것생각할것.
   - 타 연구실과 회의시 이야기하고 추가하면 될듯.

- 데이터 추가하기
   - 데이터 잘라서 집어 넣으면 될듯.!
***

