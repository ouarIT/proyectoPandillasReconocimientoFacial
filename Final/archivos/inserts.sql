drop database if exists datosrf;
create database if not exists datosrf;
use datosrf;
create table integrantes(
	id_integrante int auto_increment primary key,
    nombre varchar(50) not null, 
    a_paterno varchar(50) not null,
    a_materno varchar(50) not null,
    alias varchar(50),
    fecha_nacimiento varchar(50),
    descripcion varchar(250),
    domicilio varchar(100)
);
create table datos_rf(
	id  int auto_increment primary key,
    id_integrante int,
    nombre_archivo varchar(300),
    estado boolean default false,
    foreign key (id_integrante) references integrantes(id_integrante)
);
create table valores(
	id_integrante int,
    valor decimal(10,6),
    foreign key (id_integrante) references integrantes(id_integrante)
);

insert into integrantes(nombre, a_paterno, a_materno,
alias, fecha_nacimiento, descripcion, domicilio) values("Orlando", "Aguilar","Rojas","chik","17-06-2000","estudiante","direccion"),
("Marcela", "Zimbrón","Trejo","anazt","17-03-2001","estudiante de ti","su casita2"),("arturo", "alejandro","castro","el alto","16-04-2001","estudiante","casa blanca");

insert into datos_rf(id_integrante, nombre_archivo) values (1, "https://raw.githubusercontent.com/ouarIT/img/main/img01.jpg"),
(1, "https://raw.githubusercontent.com/ouarIT/img/main/img02.jpg"),(1, "https://raw.githubusercontent.com/ouarIT/img/main/img03.jpg"),
(1, "https://raw.githubusercontent.com/ouarIT/img/main/img04.jpg"),(2, "https://raw.githubusercontent.com/ouarIT/img/main/img05.jpg"),
(2, "https://raw.githubusercontent.com/ouarIT/img/main/img06.jpg"),(2, "https://raw.githubusercontent.com/ouarIT/img/main/img07.jpg"),
(2, "https://raw.githubusercontent.com/ouarIT/img/main/img08.jpg"),(3, "https://raw.githubusercontent.com/ouarIT/img/main/img09.jpg"),
(3, "https://raw.githubusercontent.com/ouarIT/img/main/img10.jpg"),(3, "https://raw.githubusercontent.com/ouarIT/img/main/img11.jpg"),
(3, "https://raw.githubusercontent.com/ouarIT/img/main/img12.jpg"),(3, "https://raw.githubusercontent.com/ouarIT/img/main/img13.jpg"),
(3, "https://raw.githubusercontent.com/ouarIT/img/main/img14.jpg"),(3, "https://raw.githubusercontent.com/ouarIT/img/main/img15.jpg");