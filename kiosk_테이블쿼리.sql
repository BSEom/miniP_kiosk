DROP TABLE "Menu";

CREATE TABLE Menu (
	menu_id		number				NOT NULL,
	menu_name	varchar2(100)		NOT NULL,
	exp			varchar2(200)		NOT NULL,
	menu_price	number				NOT NULL,
	category	varchar2(100)		NULL,
	image		varchar2(200)		NULL
);

DROP TABLE "order";

CREATE TABLE order_table (
	order_id	number		NOT NULL,
	order_price	number		NOT NULL,
	order_date	date		NOT NULL
);

DROP TABLE "OrderInfo";

CREATE TABLE OrderInfo (
			orderinfo_id	number		NOT NULL,
			order_id	number		NOT NULL,
			menu_id	number		NOT NULL,
			price	number		NOT NULL,
			count	number		NOT NULL);

ALTER TABLE Menu ADD CONSTRAINT PK_MENU PRIMARY KEY (menu_id);

ALTER TABLE order_table ADD CONSTRAINT PK_ORDER PRIMARY KEY (order_id);

ALTER TABLE OrderInfo ADD CONSTRAINT PK_ORDERINFO PRIMARY KEY (orderinfo_id);

ALTER TABLE OrderInfo ADD CONSTRAINT FK_order_TO_OrderInfo_1 FOREIGN KEY (order_id)
REFERENCES order_table (order_id);

ALTER TABLE OrderInfo ADD CONSTRAINT FK_Menu_TO_OrderInfo_1 FOREIGN KEY (menu_id)
REFERENCES Menu (menu_id);

COMMIT;
