# animal_sounds

## �⺻ ���

- ���̽� 3.6.0, 3.5.2

- postgresql 11.2

## ��ġ ���
1. postgresql ��ġ
 - ������ ����
  
 postgresql ����Ʈ : https://www.postgresql.org/
  
 11.2���� ��ġ �ٷΰ��� : https://www.enterprisedb.com/thank-you-downloading-postgresql?anid=1256369

 - ����� ����
 
 sudo apt-get update

 sudo apt-get install postgresql

 sudo -u postgres psql


2. postgresql ���� ����
- ������ ����

psql -U postgres

postgres ������� ��ȣ: ���� ��й�ȣ �Է� 

postgres=# ALTER USER postgres with encrypted password 'password';

 ���� ����(postgres) ��й�ȣ�� password�� �ٲ���ϴ�.

postgres=# CREATE DATABASE django_test OWNER postgres;

- ����� ����
sudo -u postgres psql

postgres=# ALTER USER postgres with encrypted password 'password';

postgres=# CREATE DATABASE django_test OWNER postgres;

sudo /etc/init.d/postgresql restart

3. �� ��ġ
 git clone https://github.com/dydwkd486/animal_sounds.git

4. requirements ��ġ
-������ ����

pip install -r requirements.txt

-����� ����
pip3 install -r requirements.txt

 -����: The program 'pip3' is currently not installed. To run 'pip3' please ask your administrator to install the 
package 'python3-pip'

  --sudo apt-get install python3-pip

4. DB�� �ʿ� �ڷ� ����.

python3 manage.py migrate

5.���۰��� �����
python3 manage.py createsuperuser

 --���� ��:UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-2: ordinal not in range(128)

  export PYTHONIOENCODING=utf-8

����� �̸� (leave blank to use 'dydwkd486'): admin

�̸��� �ּ�: admin@admin.com

Password: 

Password (again): 

��й�ȣ�� �̸��� �ּҿ� �ʹ� �����մϴ�.

��й�ȣ�� �ʹ� ª���ϴ�. �ּ� 8 ���ڸ� �����ؾ� �մϴ�.

��й�ȣ�� �ʹ� �ϻ����� �ܾ��Դϴ�.

Bypass password validation and create user anyway? [y/N]: y

Superuser created successfully.

## ����

python3 manage.py runserver

	System check identified no issues (0 silenced).
	March 05, 2019 - 17:36:26
	Django version 2.1.7, using settings 'animal_sounds.settings'
	Starting development server at http://127.0.0.1:8000/
	Quit the server with CONTROL-C.
