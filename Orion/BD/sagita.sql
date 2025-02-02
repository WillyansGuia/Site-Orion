create table sagita_usuario(
    id_usuario int primary key auto_increment,
    nome_usuario varchar(80) not null,
    ds_email varchar(80) not null,
    ds_senha varchar(8) not null,
    ds_status boolean not null,
    ds_endereco varchar(80) not null,
    no_cep char(9) not null
)
default charset utf8mb4;

insert into sagita_usuario
values(default, 'Willyans Estevam da Guia', 'willyansguia.original@gmail.com', 'willsagi', 1, 'Travessa Mariana, 121', '35900-172');

insert into sagita_usuario
values(default, 'Douglas Nascimento', 'douglasral@gmail.com', 'kof22dgh', 0, 'Rua Santa Helena, 201', '55643-000');

insert into sagita_usuario
values(default, 'Vinicius Lobato', 'lobatovini@gmail.com', 'lobato25', 0, 'Rua Ouro Preto, 121', '35900-161');

select * from sagita_usuario;

