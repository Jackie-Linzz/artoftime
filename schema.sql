create table if not exists category (
cid      char(20) not null  primary key,
name     char(50) not null,
ord      int unsigned not null,
desp     varchar(1000)

);

create table if not exists diet(
did     char(20)  not null primary key,
name    char(50) not null,
price   float(8,2) not null,
price2  float(8,2),
ord     int unsigned not null,
base    float(8,2) not null,
cid     char(20) not null,
who     char(10) not null,
pic     char(100),
desp    varchar(1000)
);

create table if not exists id (
name   char(20) not null primary key,
num    bigint unsigned not null
);

create table if not exists password (
fid       char(100) not null primary key,
passwd    char(50) not null
);

create table if not exists faculty (
fid       char(100) not null primary key,
name      char(50) not null,
role      char(50) not null
);

create table if not exists cook_do (
  th     bigint unsigned not null  primary key auto_increment,
  fid    char(100) not null,
  did    char(20) not null
);

create table if not exists order_history (
  uid     bigint unsigned not null primary key,
  did     char(20)  not null,
  num     float(8,2) not null,
  price   float(8,2) not null,
  desk    char(20) not null,
  pid     bigint unsigned not null,
  stamp   double(20,6) not null
);


create table if not exists cook_history (
  th    bigint unsigned not null primary key auto_increment,
  fid   char(50) not null,
  uid   bigint unsigned not null,
  stamp double(20,6) not null
);
create table if not exists cash_history (
  th    bigint unsigned not null primary key auto_increment,
  fid   char(100) not null,
  uid   bigint unsigned not null,
  pid   bigint unsigned not null,
  status  char(10) not null,
  stamp double(20,6) not null
);

create table if not exists feedback (
  th    bigint unsigned not null primary key auto_increment,
  uid   bigint unsigned not null,
  fb    int not null,
  stamp double(20,6) not null
);

create table if not exists comment (
  th    bigint unsigned not null primary key auto_increment,
  desk  char(20) not null,
  comment  varchar(1000) not null,
  stamp double(20,6) not null
);

create table if not exists desks (
 desk char(20) not null primary key
);

create table if not exists mask (
  did  char(20) not null primary key
);
