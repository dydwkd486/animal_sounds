# animal_sounds

�⺻ ���
���̽� 3.6.0
postgresql 11.2

��ġ
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

- ����� ����
sudo -u postgres psql

postgres=# ALTER USER postgres with encrypted password 'password';

sudo /etc/init.d/postgresql restart

3. �� ��ġ
 git clone https://github.com/dydwkd486/animal_sounds.git

