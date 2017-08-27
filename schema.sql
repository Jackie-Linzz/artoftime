create table if not exists category (
  cid      char(20) not null  primary key,
  name     char(50) not null,
  ord      int unsigned not null,
  desp    varchar(1000)

);

create table if not exists diet(
  did     char(20)  not null primary key,
  name    char(50) not null,
  price   float(8,2) not null,
  price2  float(8,2),
  ord     int unsigned not null,
  base    float(8,2) not null,
  cid     int unsigned not null ,
  pic     char(100),
  desp    varchar(1000)
);

create table if not exists faculty (
  fid       char(100) not null primary key,
  name      char(50) not null,
  role      char(50) not null,
  password  char(50) not null
);

create table if not exists cookdo (
  th     bigint unsigned not null  primary key auto_increment,
  fid    char(100) not null,
  did    char(20) not null
);

create table if not exists order_history (
  th      bigint unsigned not null  primary key auto_increment,
  uid     bigint unsigned not null,
  did     char(20)  not null,
  num     float(8,2) not null,
  price   float(8,2) not null,
  puid    bigint unsigned not null,
  desk    char(20) not null,
  stamp   double(20,5) not null
);


create table if not exists cook_history (
  th    bigint unsigned not null primary key auto_increment,
  fid   char(50) not null,
  uid   bigint unsigned not null,
  did   char(20)  not null,
  num   float(8,2) not null,
  stamp double(20,5) not null
);

create table if not exists feedback (

  th    bigint unsigned not null primary key auto_increment,
  uid   bigint unsigned not null,
  did   char(20) not null,
  num   float(8,2) not null,
  fb    int not null,
  desp varchar(200),
  stamp double(20,5) not null
);

create table if not exists comment (
  th    bigint unsigned not null primary key auto_increment,
  desk  char(20) not null,
  comm  varchar(1000) not null,
  stamp double(20,5) not null
);

create table if not exists desks (
 desk char(20) not null primary key
);
