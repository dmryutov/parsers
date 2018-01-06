-- ----------------------------
-- Table structure for AKCII
-- ----------------------------
DROP TABLE AKCII;
CREATE TABLE AKCII (
ID NUMBER(11) NOT NULL ,
DECLARATION_ID NUMBER(11) NULL ,
VID VARCHAR2(255 BYTE) NULL ,
NOMER VARCHAR2(255 BYTE) NULL ,
CB VARCHAR2(255 BYTE) NULL ,
EKVIVALENT NUMBER(11) NULL ,
EMITENT VARCHAR2(255 BYTE) NULL ,
SUMMA NUMBER(11) NULL ,
FIO_SOBSTVENNIKA VARCHAR2(255 BYTE) NULL ,
PRAVOVOE_OBOSNOVANIE VARCHAR2(255 BYTE) NULL ,
PROISHOZHDENIE_DS VARCHAR2(255 BYTE) NULL 
);
COMMENT ON COLUMN AKCII.VID IS 'Вид ценной бумаги';
COMMENT ON COLUMN AKCII.NOMER IS 'Номер ценной бумаги';
COMMENT ON COLUMN AKCII.CB IS 'Ценная бумага';
COMMENT ON COLUMN AKCII.EKVIVALENT IS 'Денежный эквивалент';
COMMENT ON COLUMN AKCII.EMITENT IS 'Эмитент';
COMMENT ON COLUMN AKCII.SUMMA IS 'Стоимость приобретения';
COMMENT ON COLUMN AKCII.FIO_SOBSTVENNIKA IS 'ФИО собственника';
COMMENT ON COLUMN AKCII.PRAVOVOE_OBOSNOVANIE IS 'Правовое обоснование приобретения ценных бумаг';
COMMENT ON COLUMN AKCII.PROISHOZHDENIE_DS IS 'Происхождение денежных средств';

-- ----------------------------
-- Table structure for BANKOVSKIE_DEPOZITY
-- ----------------------------
DROP TABLE BANKOVSKIE_DEPOZITY;
CREATE TABLE BANKOVSKIE_DEPOZITY (
ID NUMBER(11) NOT NULL ,
DECLARATION_ID NUMBER(11) NULL ,
SUMMA NUMBER(11) NULL ,
VALUTA VARCHAR2(255 BYTE) NULL ,
EKVIVALENT NUMBER(11) NULL ,
FIO_SOBSTVENNIKA VARCHAR2(255 BYTE) NULL ,
V_STRANE VARCHAR2(255 BYTE) NULL ,
VNE_STRANY VARCHAR2(255 BYTE) NULL ,
PROISHOZHDENIE_DS VARCHAR2(255 BYTE) NULL 
);
COMMENT ON COLUMN BANKOVSKIE_DEPOZITY.SUMMA IS 'Сумма денежных средств';
COMMENT ON COLUMN BANKOVSKIE_DEPOZITY.VALUTA IS 'Валюта';
COMMENT ON COLUMN BANKOVSKIE_DEPOZITY.EKVIVALENT IS 'Эквивалент львам';
COMMENT ON COLUMN BANKOVSKIE_DEPOZITY.FIO_SOBSTVENNIKA IS 'ФИО собственника';
COMMENT ON COLUMN BANKOVSKIE_DEPOZITY.V_STRANE IS 'Внутри страны';
COMMENT ON COLUMN BANKOVSKIE_DEPOZITY.VNE_STRANY IS 'Зарубежом';
COMMENT ON COLUMN BANKOVSKIE_DEPOZITY.PROISHOZHDENIE_DS IS 'Происхождение денежных средств';

-- ----------------------------
-- Table structure for DEBITORSKAY_ZADOLZHNOST
-- ----------------------------
DROP TABLE DEBITORSKAY_ZADOLZHNOST;
CREATE TABLE DEBITORSKAY_ZADOLZHNOST (
ID NUMBER(11) NOT NULL ,
DECLARATION_ID NUMBER(11) NULL ,
VID_ZADOLZHENNOSTI VARCHAR2(255 BYTE) NULL ,
SUMMA NUMBER(11) NULL ,
VALUTA VARCHAR2(255 BYTE) NULL ,
EKVIVALENT NUMBER(11) NULL ,
FIO_SOBSTVENNIKA VARCHAR2(255 BYTE) NULL ,
PRAVOVOE_OBOSNOVANIE VARCHAR2(255 BYTE) NULL ,
OT_GRAZHDANINA_BOLGARII VARCHAR2(255 BYTE) NULL ,
OT_INOSTRANNOGO_GRAZDANINA VARCHAR2(255 BYTE) NULL 
);
COMMENT ON COLUMN DEBITORSKAY_ZADOLZHNOST.VID_ZADOLZHENNOSTI IS 'Вид дебиторской задолженности';
COMMENT ON COLUMN DEBITORSKAY_ZADOLZHNOST.SUMMA IS 'Сумма денежных средств';
COMMENT ON COLUMN DEBITORSKAY_ZADOLZHNOST.VALUTA IS 'Валюта';
COMMENT ON COLUMN DEBITORSKAY_ZADOLZHNOST.EKVIVALENT IS 'Эквивалент львам';
COMMENT ON COLUMN DEBITORSKAY_ZADOLZHNOST.FIO_SOBSTVENNIKA IS 'ФИО собственника';
COMMENT ON COLUMN DEBITORSKAY_ZADOLZHNOST.PRAVOVOE_OBOSNOVANIE IS 'Правовое обоснование задолженности';
COMMENT ON COLUMN DEBITORSKAY_ZADOLZHNOST.OT_GRAZHDANINA_BOLGARII IS 'От гражданина Болгарии';
COMMENT ON COLUMN DEBITORSKAY_ZADOLZHNOST.OT_INOSTRANNOGO_GRAZDANINA IS 'От иностранного гражданина';

-- ----------------------------
-- Table structure for DECLARATION
-- ----------------------------
DROP TABLE DECLARATION;
CREATE TABLE DECLARATION (
ID NUMBER(11) NOT NULL ,
PERSON_ID NUMBER(11) NULL ,
ENTRY_NUMBER VARCHAR2(10 BYTE) NULL ,
ENTRY_DATE VARCHAR2(30 BYTE) NULL ,
DECLARATION_TYPE VARCHAR2(255 BYTE) NULL ,
YEAR NUMBER(11) NULL ,
DECLARATION_DATE VARCHAR2(30 BYTE) NULL ,
AGREEMENT_DATE VARCHAR2(30 BYTE) NULL ,
CONTROL_HASH VARCHAR2(20 BYTE) NULL 
);

-- ----------------------------
-- Table structure for DOHODY_NE_OT_ZP
-- ----------------------------
DROP TABLE DOHODY_NE_OT_ZP;
CREATE TABLE DOHODY_NE_OT_ZP (
ID NUMBER(11) NOT NULL ,
DECLARATION_ID NUMBER(11) NULL ,
VID VARCHAR2(255 BYTE) NULL ,
DECLARANT NUMBER(11) NULL ,
SUPRUG NUMBER(11) NULL 
);
COMMENT ON COLUMN DOHODY_NE_OT_ZP.VID IS 'Вид дохода';
COMMENT ON COLUMN DOHODY_NE_OT_ZP.DECLARANT IS 'Декларант';
COMMENT ON COLUMN DOHODY_NE_OT_ZP.SUPRUG IS 'Супруг, супруга декларанта';

-- ----------------------------
-- Table structure for DOLI_V_OOO
-- ----------------------------
DROP TABLE DOLI_V_OOO;
CREATE TABLE DOLI_V_OOO (
ID NUMBER(11) NOT NULL ,
DECLARATION_ID NUMBER(11) NULL ,
VID VARCHAR2(255 BYTE) NULL ,
DOLEVOE_UCHASTIE VARCHAR2(255 BYTE) NULL ,
ORGANIZACIA VARCHAR2(255 BYTE) NULL ,
MESTO VARCHAR2(255 BYTE) NULL ,
STOIMOST NUMBER(11) NULL ,
FIO_SOBSTVENNIKA VARCHAR2(255 BYTE) NULL ,
PRAVOVOE_OBOSNOVANIE VARCHAR2(255 BYTE) NULL ,
PROISHOZHDENIE_DS VARCHAR2(255 BYTE) NULL ,
TYPE NUMBER(4) NULL 
);
COMMENT ON COLUMN DOLI_V_OOO.VID IS 'Вид имущества';
COMMENT ON COLUMN DOLI_V_OOO.DOLEVOE_UCHASTIE IS 'Размер долевого участия';
COMMENT ON COLUMN DOLI_V_OOO.ORGANIZACIA IS 'Наименование организации';
COMMENT ON COLUMN DOLI_V_OOO.MESTO IS 'Место нахождения / город';
COMMENT ON COLUMN DOLI_V_OOO.STOIMOST IS 'Стоимость долевого участия / продажи';
COMMENT ON COLUMN DOLI_V_OOO.FIO_SOBSTVENNIKA IS 'ФИО собственника / нового собственника';
COMMENT ON COLUMN DOLI_V_OOO.PRAVOVOE_OBOSNOVANIE IS 'Правовое обоснование приобретения / продажи ценных бумаг';
COMMENT ON COLUMN DOLI_V_OOO.PROISHOZHDENIE_DS IS 'Происхождение денежных средств';
COMMENT ON COLUMN DOLI_V_OOO.TYPE IS '0 - 11. Доли в обществах с ограниченной ответственностью или товариществах
1 - 12. Передача доли в обществах с ограниченной ответственностью или товариществах';

-- ----------------------------
-- Table structure for DS_V_POLZU_DECLARANTA
-- ----------------------------
DROP TABLE DS_V_POLZU_DECLARANTA;
CREATE TABLE DS_V_POLZU_DECLARANTA (
ID NUMBER(11) NOT NULL ,
DECLARATION_ID NUMBER(11) NULL ,
VID VARCHAR2(255 BYTE) NULL ,
SUMMA NUMBER(11) NULL ,
VALUTA VARCHAR2(255 BYTE) NULL ,
EKVIVALENT NUMBER(11) NULL ,
OT_DECLARANTA VARCHAR2(255 BYTE) NULL ,
DECLARANTU VARCHAR2(255 BYTE) NULL ,
OT_SUPRUGA VARCHAR2(255 BYTE) NULL ,
SUPRUGU VARCHAR2(255 BYTE) NULL ,
TYPE NUMBER(4) NULL 
);
COMMENT ON COLUMN DS_V_POLZU_DECLARANTA.VID IS 'Вид обеспечения получения денежных средств / расхода';
COMMENT ON COLUMN DS_V_POLZU_DECLARANTA.SUMMA IS 'Размер денежных средств / расхода';
COMMENT ON COLUMN DS_V_POLZU_DECLARANTA.VALUTA IS 'Валюта';
COMMENT ON COLUMN DS_V_POLZU_DECLARANTA.EKVIVALENT IS 'Эквивалент в львах';
COMMENT ON COLUMN DS_V_POLZU_DECLARANTA.OT_DECLARANTA IS 'От декларанта';
COMMENT ON COLUMN DS_V_POLZU_DECLARANTA.DECLARANTU IS 'В пользу декларанта';
COMMENT ON COLUMN DS_V_POLZU_DECLARANTA.OT_SUPRUGA IS 'От супрага, супруги или несовершеннолетних детей';
COMMENT ON COLUMN DS_V_POLZU_DECLARANTA.SUPRUGU IS 'В пользу супрага, супруги или несовершеннолетних детей';
COMMENT ON COLUMN DS_V_POLZU_DECLARANTA.TYPE IS '0 - 14. Полученные денежные средства в пользу / от декларанта его супруга,супруги или несовершеннолетних детей с согласия декларанта (наследство)
1 - 15. Расходы, совершенные в пользу декларанта или самим декларантом, его супругом  или свупругой и несовершеннолетними детьмя с соглашения декларанта, в случае когда они не способны сами оплатить собственными средствами или средствами, которые они занимали в каких-то учреждениях';

-- ----------------------------
-- Table structure for KREDITORSKAY_ZADOLZHNOST
-- ----------------------------
DROP TABLE KREDITORSKAY_ZADOLZHNOST;
CREATE TABLE KREDITORSKAY_ZADOLZHNOST (
ID NUMBER(11) NOT NULL ,
DECLARATION_ID NUMBER(11) NULL ,
VID_ZADOLZHENNOSTI VARCHAR2(255 BYTE) NULL ,
SUMMA NUMBER(11) NULL ,
VALUTA VARCHAR2(255 BYTE) NULL ,
EKVIVALENT NUMBER(11) NULL ,
FIO_SOBSTVENNIKA VARCHAR2(255 BYTE) NULL ,
PRAVOVOE_OBOSNOVANIE VARCHAR2(255 BYTE) NULL ,
NAIMENOVANIE_BANKA VARCHAR2(255 BYTE) NULL ,
DRUGOI_KREDITOR VARCHAR2(255 BYTE) NULL 
);
COMMENT ON COLUMN KREDITORSKAY_ZADOLZHNOST.VID_ZADOLZHENNOSTI IS 'Вид дебиторской задолженности';
COMMENT ON COLUMN KREDITORSKAY_ZADOLZHNOST.SUMMA IS 'Сумма денежных средств';
COMMENT ON COLUMN KREDITORSKAY_ZADOLZHNOST.VALUTA IS 'Валюта';
COMMENT ON COLUMN KREDITORSKAY_ZADOLZHNOST.EKVIVALENT IS 'Эквивалент львам';
COMMENT ON COLUMN KREDITORSKAY_ZADOLZHNOST.FIO_SOBSTVENNIKA IS 'ФИО собственника';
COMMENT ON COLUMN KREDITORSKAY_ZADOLZHNOST.PRAVOVOE_OBOSNOVANIE IS 'Правовое обоснование задолженности';
COMMENT ON COLUMN KREDITORSKAY_ZADOLZHNOST.NAIMENOVANIE_BANKA IS 'Наименование банка';
COMMENT ON COLUMN KREDITORSKAY_ZADOLZHNOST.DRUGOI_KREDITOR IS 'Физическое или юридическое лицо - кредитор';

-- ----------------------------
-- Table structure for NALICHNIE_DS
-- ----------------------------
DROP TABLE NALICHNIE_DS;
CREATE TABLE NALICHNIE_DS (
ID NUMBER(11) NOT NULL ,
DECLARATION_ID NUMBER(11) NULL ,
SUMMA NUMBER(11) NULL ,
VALUTA VARCHAR2(255 BYTE) NULL ,
EKVIVALENT NUMBER(11) NULL ,
FIO_SOBSTVENNIKA VARCHAR2(255 BYTE) NULL ,
PROISHOZHDENIE_DS VARCHAR2(255 BYTE) NULL 
);
COMMENT ON COLUMN NALICHNIE_DS.SUMMA IS 'Сумма денежных средств';
COMMENT ON COLUMN NALICHNIE_DS.VALUTA IS 'Валюта';
COMMENT ON COLUMN NALICHNIE_DS.EKVIVALENT IS 'Эквивалент львам';
COMMENT ON COLUMN NALICHNIE_DS.FIO_SOBSTVENNIKA IS 'ФИО собственника';
COMMENT ON COLUMN NALICHNIE_DS.PROISHOZHDENIE_DS IS 'Происхождение денежных средств';

-- ----------------------------
-- Table structure for NEDVIZHIMOE_IMUSCHESTVO
-- ----------------------------
DROP TABLE NEDVIZHIMOE_IMUSCHESTVO;
CREATE TABLE NEDVIZHIMOE_IMUSCHESTVO (
ID NUMBER(11) NOT NULL ,
DECLARATION_ID NUMBER(11) NULL ,
VID_SOBSTVENNOSTI VARCHAR2(255 BYTE) NULL ,
MESTO VARCHAR2(255 BYTE) NULL ,
ADMINISTRATIVNYI_CENTER VARCHAR2(255 BYTE) NULL ,
PLOSCHAD NUMBER(11) NULL ,
PLOSHAD_STROENIA VARCHAR2(255 BYTE) NULL ,
GOD_PRIOBRETENIA NUMBER(11) NULL ,
FIO_SOBSTVENNIKA VARCHAR2(255 BYTE) NULL ,
DOLYA_SOBSTVENNOSTI VARCHAR2(255 BYTE) NULL ,
STOIMOST NUMBER(11) NULL ,
PRAVO_NA_PRIOBRETENIE VARCHAR2(255 BYTE) NULL ,
PROISHOZHDENIE_DS VARCHAR2(255 BYTE) NULL ,
TYPE NUMBER(4) NULL 
);
COMMENT ON COLUMN NEDVIZHIMOE_IMUSCHESTVO.VID_SOBSTVENNOSTI IS 'Вид собственности';
COMMENT ON COLUMN NEDVIZHIMOE_IMUSCHESTVO.MESTO IS 'Местонахождение';
COMMENT ON COLUMN NEDVIZHIMOE_IMUSCHESTVO.ADMINISTRATIVNYI_CENTER IS 'Община (административный центр)';
COMMENT ON COLUMN NEDVIZHIMOE_IMUSCHESTVO.PLOSCHAD IS 'Площадь кв.м.';
COMMENT ON COLUMN NEDVIZHIMOE_IMUSCHESTVO.PLOSHAD_STROENIA IS 'Площадь строения кв.м.';
COMMENT ON COLUMN NEDVIZHIMOE_IMUSCHESTVO.GOD_PRIOBRETENIA IS 'Год приобретения';
COMMENT ON COLUMN NEDVIZHIMOE_IMUSCHESTVO.FIO_SOBSTVENNIKA IS 'ФИО собственника';
COMMENT ON COLUMN NEDVIZHIMOE_IMUSCHESTVO.DOLYA_SOBSTVENNOSTI IS 'Доля собственности';
COMMENT ON COLUMN NEDVIZHIMOE_IMUSCHESTVO.STOIMOST IS 'Стоимость (львы)';
COMMENT ON COLUMN NEDVIZHIMOE_IMUSCHESTVO.PRAVO_NA_PRIOBRETENIE IS 'Право на приобретение';
COMMENT ON COLUMN NEDVIZHIMOE_IMUSCHESTVO.PROISHOZHDENIE_DS IS 'Происхождение денежных средств';
COMMENT ON COLUMN NEDVIZHIMOE_IMUSCHESTVO.TYPE IS '0 - 1.Право собственности и ограниченное право собственности
1 - 1.1.Сельскохозяйственные земли и леса
2 - 2.Информация о передаче имущества за предыдущий год';

-- ----------------------------
-- Table structure for PERSON
-- ----------------------------
DROP TABLE PERSON;
CREATE TABLE PERSON (
ID NUMBER(11) NOT NULL ,
NAME VARCHAR2(150 BYTE) NULL ,
WORK VARCHAR2(255 BYTE) NULL ,
POSITION VARCHAR2(255 BYTE) NULL ,
WORK_CODE NUMBER(11) NULL ,
EGN VARCHAR2(255 BYTE) NULL ,
PASSPORT_NUMBER VARCHAR2(50 BYTE) NULL ,
PASSPORT_DATA VARCHAR2(50 BYTE) NULL ,
ADDRESS VARCHAR2(255 BYTE) NULL 
);

-- ----------------------------
-- Table structure for TRANSPORT
-- ----------------------------
DROP TABLE TRANSPORT;
CREATE TABLE TRANSPORT (
ID NUMBER(11) NOT NULL ,
DECLARATION_ID NUMBER(11) NULL ,
VID VARCHAR2(255 BYTE) NULL ,
MARKA VARCHAR2(255 BYTE) NULL ,
STOIMOST NUMBER(11) NULL ,
GOD_PRIOBRETENIA VARCHAR2(255 BYTE) NULL ,
FIO_SOBSTVENNIKA VARCHAR2(255 BYTE) NULL ,
DOLYA_SOBSTVENNOSTI VARCHAR2(255 BYTE) NULL ,
PRAVO_NA_PRIOBRETENIE VARCHAR2(255 BYTE) NULL ,
PROISHOZHDENIE_DS VARCHAR2(255 BYTE) NULL ,
TYPE NUMBER(4) NULL 
);
COMMENT ON COLUMN TRANSPORT.VID IS 'Вид транспорта';
COMMENT ON COLUMN TRANSPORT.MARKA IS 'Марка транспорта';
COMMENT ON COLUMN TRANSPORT.STOIMOST IS 'Стоимость  приобретения';
COMMENT ON COLUMN TRANSPORT.GOD_PRIOBRETENIA IS 'Год приобретения';
COMMENT ON COLUMN TRANSPORT.FIO_SOBSTVENNIKA IS 'ФИО собственника';
COMMENT ON COLUMN TRANSPORT.DOLYA_SOBSTVENNOSTI IS 'Доля собственности';
COMMENT ON COLUMN TRANSPORT.PRAVO_NA_PRIOBRETENIE IS 'Право на приобретение';
COMMENT ON COLUMN TRANSPORT.PROISHOZHDENIE_DS IS 'Происхождение денежных средств';
COMMENT ON COLUMN TRANSPORT.TYPE IS '0 - 3. Сухопутные транспортные средства
1 - 3.1. Воздушные транспортные средства
2 - 4. Водные транспортные средства
3 - 5. Информация о передаче имущества за предыдущий год';

-- ----------------------------
-- Sequence structure for ID_SEQ
-- ----------------------------
DROP SEQUENCE ID_SEQ;
CREATE SEQUENCE ID_SEQ
 INCREMENT BY 1
 MINVALUE 1
 MAXVALUE 9999999999999999999999999999
 START WITH 278181
 CACHE 20;

-- ----------------------------
-- Indexes structure for table AKCII
-- ----------------------------

-- ----------------------------
-- Primary Key structure for table AKCII
-- ----------------------------
ALTER TABLE AKCII ADD PRIMARY KEY (ID);

-- ----------------------------
-- Indexes structure for table BANKOVSKIE_DEPOZITY
-- ----------------------------

-- ----------------------------
-- Primary Key structure for table BANKOVSKIE_DEPOZITY
-- ----------------------------
ALTER TABLE BANKOVSKIE_DEPOZITY ADD PRIMARY KEY (ID);

-- ----------------------------
-- Indexes structure for table DEBITORSKAY_ZADOLZHNOST
-- ----------------------------

-- ----------------------------
-- Primary Key structure for table DEBITORSKAY_ZADOLZHNOST
-- ----------------------------
ALTER TABLE DEBITORSKAY_ZADOLZHNOST ADD PRIMARY KEY (ID);

-- ----------------------------
-- Indexes structure for table DECLARATION
-- ----------------------------

-- ----------------------------
-- Primary Key structure for table DECLARATION
-- ----------------------------
ALTER TABLE DECLARATION ADD PRIMARY KEY (ID);

-- ----------------------------
-- Indexes structure for table DOHODY_NE_OT_ZP
-- ----------------------------

-- ----------------------------
-- Primary Key structure for table DOHODY_NE_OT_ZP
-- ----------------------------
ALTER TABLE DOHODY_NE_OT_ZP ADD PRIMARY KEY (ID);

-- ----------------------------
-- Indexes structure for table DOLI_V_OOO
-- ----------------------------

-- ----------------------------
-- Primary Key structure for table DOLI_V_OOO
-- ----------------------------
ALTER TABLE DOLI_V_OOO ADD PRIMARY KEY (ID);

-- ----------------------------
-- Indexes structure for table DS_V_POLZU_DECLARANTA
-- ----------------------------

-- ----------------------------
-- Primary Key structure for table DS_V_POLZU_DECLARANTA
-- ----------------------------
ALTER TABLE DS_V_POLZU_DECLARANTA ADD PRIMARY KEY (ID);

-- ----------------------------
-- Indexes structure for table KREDITORSKAY_ZADOLZHNOST
-- ----------------------------

-- ----------------------------
-- Primary Key structure for table KREDITORSKAY_ZADOLZHNOST
-- ----------------------------
ALTER TABLE KREDITORSKAY_ZADOLZHNOST ADD PRIMARY KEY (ID);

-- ----------------------------
-- Indexes structure for table NALICHNIE_DS
-- ----------------------------

-- ----------------------------
-- Primary Key structure for table NALICHNIE_DS
-- ----------------------------
ALTER TABLE NALICHNIE_DS ADD PRIMARY KEY (ID);

-- ----------------------------
-- Indexes structure for table NEDVIZHIMOE_IMUSCHESTVO
-- ----------------------------

-- ----------------------------
-- Primary Key structure for table NEDVIZHIMOE_IMUSCHESTVO
-- ----------------------------
ALTER TABLE NEDVIZHIMOE_IMUSCHESTVO ADD PRIMARY KEY (ID);

-- ----------------------------
-- Indexes structure for table PERSON
-- ----------------------------

-- ----------------------------
-- Primary Key structure for table PERSON
-- ----------------------------
ALTER TABLE PERSON ADD PRIMARY KEY (ID);

-- ----------------------------
-- Indexes structure for table TRANSPORT
-- ----------------------------

-- ----------------------------
-- Primary Key structure for table TRANSPORT
-- ----------------------------
ALTER TABLE TRANSPORT ADD PRIMARY KEY (ID);

-- ----------------------------
-- Foreign Key structure for table AKCII
-- ----------------------------
ALTER TABLE AKCII ADD FOREIGN KEY (DECLARATION_ID) REFERENCES DECLARATION (ID) ON DELETE CASCADE;

-- ----------------------------
-- Foreign Key structure for table BANKOVSKIE_DEPOZITY
-- ----------------------------
ALTER TABLE BANKOVSKIE_DEPOZITY ADD FOREIGN KEY (DECLARATION_ID) REFERENCES DECLARATION (ID) ON DELETE CASCADE;

-- ----------------------------
-- Foreign Key structure for table DEBITORSKAY_ZADOLZHNOST
-- ----------------------------
ALTER TABLE DEBITORSKAY_ZADOLZHNOST ADD FOREIGN KEY (DECLARATION_ID) REFERENCES DECLARATION (ID) ON DELETE CASCADE;

-- ----------------------------
-- Foreign Key structure for table DECLARATION
-- ----------------------------
ALTER TABLE DECLARATION ADD FOREIGN KEY (PERSON_ID) REFERENCES PERSON (ID) ON DELETE CASCADE;

-- ----------------------------
-- Foreign Key structure for table DOHODY_NE_OT_ZP
-- ----------------------------
ALTER TABLE DOHODY_NE_OT_ZP ADD FOREIGN KEY (DECLARATION_ID) REFERENCES DECLARATION (ID) ON DELETE CASCADE;

-- ----------------------------
-- Foreign Key structure for table DOLI_V_OOO
-- ----------------------------
ALTER TABLE DOLI_V_OOO ADD FOREIGN KEY (DECLARATION_ID) REFERENCES DECLARATION (ID) ON DELETE CASCADE;

-- ----------------------------
-- Foreign Key structure for table DS_V_POLZU_DECLARANTA
-- ----------------------------
ALTER TABLE DS_V_POLZU_DECLARANTA ADD FOREIGN KEY (DECLARATION_ID) REFERENCES DECLARATION (ID) ON DELETE CASCADE;

-- ----------------------------
-- Foreign Key structure for table KREDITORSKAY_ZADOLZHNOST
-- ----------------------------
ALTER TABLE KREDITORSKAY_ZADOLZHNOST ADD FOREIGN KEY (DECLARATION_ID) REFERENCES DECLARATION (ID) ON DELETE CASCADE;

-- ----------------------------
-- Foreign Key structure for table NALICHNIE_DS
-- ----------------------------
ALTER TABLE NALICHNIE_DS ADD FOREIGN KEY (DECLARATION_ID) REFERENCES DECLARATION (ID) ON DELETE CASCADE;

-- ----------------------------
-- Foreign Key structure for table NEDVIZHIMOE_IMUSCHESTVO
-- ----------------------------
ALTER TABLE NEDVIZHIMOE_IMUSCHESTVO ADD FOREIGN KEY (DECLARATION_ID) REFERENCES DECLARATION (ID) ON DELETE CASCADE;

-- ----------------------------
-- Foreign Key structure for table TRANSPORT
-- ----------------------------
ALTER TABLE TRANSPORT ADD FOREIGN KEY (DECLARATION_ID) REFERENCES DECLARATION (ID) ON DELETE CASCADE;
