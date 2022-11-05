drop database if exists datosrf;
create database if not exists datosrf ;
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
    nombre_archivo varchar(100),
    estado boolean default false,
    foreign key (id_integrante) references integrantes(id_integrante)
);
create table valores(
	id_integrante int,
    valor decimal(10,6),
    foreign key (id_integrante) references integrantes(id_integrante)
    );
insert into integrantes(nombre, a_paterno, a_materno,
alias, fecha_nacimiento, descripcion, domicilio) values("tom", "hanks","ap_1","forest gump","01-05-1950","es un actor","su casita"),
("mujer2", "ap_2","ap_2","prueba2","01-05-1951","es un actor2","su casita2"),("mujer3", "ap_3","ap_3","prueba3","01-05-1953","es un actor3","su casita3"),
("mujer4", "ap_4","ap_4","prueba4","01-05-1954","es un actor4","su casita4"),("mujer5", "ap_5","ap_5","prueba5","01-05-1955","es un actor5","su casita5"),
("mujer6", "ap_6","ap_6","prueba6","01-05-1956","es un actor6","su casita6");

insert into datos_rf(id_integrante, nombre_archivo) values (1, "C:/Users/Orlando/Desktop/git/NuevoProyecto/img/famosos/h1.JPG"),
(1, "C:/Users/Orlando/Desktop/git/NuevoProyecto/img/famosos/h2.JPG"),(1, "C:/Users/Orlando/Desktop/git/NuevoProyecto/img/famosos/h3.JPG"),
(2, "C:/Users/Orlando/Desktop/git/NuevoProyecto/img/famosos/j1.JPG"),(2, "C:/Users/Orlando/Desktop/git/NuevoProyecto/img/famosos/j2.JPG"),
(2, "C:/Users/Orlando/Desktop/git/NuevoProyecto/img/famosos/j3.JPG"),(3, "C:/Users/Orlando/Desktop/git/NuevoProyecto/img/famosos/n1.JPG"),
(3, "C:/Users/Orlando/Desktop/git/NuevoProyecto/img/famosos/n2.JPG"),(3, "C:/Users/Orlando/Desktop/git/NuevoProyecto/img/famosos/n3.JPG"),
(4, "C:/Users/Orlando/Desktop/git/NuevoProyecto/img/famosos/p1.JPG"),(4, "C:/Users/Orlando/Desktop/git/NuevoProyecto/img/famosos/p2.JPG"),
(4, "C:/Users/Orlando/Desktop/git/NuevoProyecto/img/famosos/p3.JPG"),(5, "C:/Users/Orlando/Desktop/git/NuevoProyecto/img/famosos/s1.JPG"),
(5, "C:/Users/Orlando/Desktop/git/NuevoProyecto/img/famosos/s2.JPG"),(5, "C:/Users/Orlando/Desktop/git/NuevoProyecto/img/famosos/s3.JPG"),
(6, "C:/Users/Orlando/Desktop/git/NuevoProyecto/img/famosos/u1.JPG"),(6, "C:/Users/Orlando/Desktop/git/NuevoProyecto/img/famosos/u2.JPG"),
(6, "C:/Users/Orlando/Desktop/git/NuevoProyecto/img/famosos/u3.JPG");