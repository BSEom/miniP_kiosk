CREATE USER kiosk IDENTIFIED BY 12345;

GRANT CONNECT, RESOURCE TO kiosk;

GRANT CREATE SESSION, CREATE TABLE, CREATE VIEW, DROP ANY TABLE TO kiosk;

GRANT ALTER ON menu TO kiosk;

GRANT DROP ANY TABLE TO kiosk;


COMMIT;



