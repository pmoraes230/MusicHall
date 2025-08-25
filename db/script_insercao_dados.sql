INSERT INTO Perfil(Nome_Perfil) VALUES
("Administrador"), ("Vendedor"), ("Validador");

SELECT * FROM Perfil; 

INSERT INTO Usuario(Nome_Usuario, Email_Usuario, CPF_Usuario, Senha_Usuario, Perfil_ID) VALUES
("Patrick Nascimento", "patrick54682366@edu.pa.senac.br", "070.854.742-70", "$2a$12$/h8TSAowe65BxKe2oogSyOXcq0oU275p3trOV6GSTT5ygGRB/L0QS", 1),
("Francisco Moraes", "francisco@email.com", "854.879.852-78", "$2a$12$xdKaGN7EhYWJV.yw86SoTeK9ihG6MMdXoc8AZGa9qgv81.Limlbde", 1),
("Claudio Raposo", "claudioraposo@email.com", "400.028.922-00", "$2a$12$OTjHaR27nI8/bDNMN7k48uuyAYMglCveRDc72nZ6o0x6cfCj8pZXq", 2),
("Felipe Monteiro", "felipemonteiro@email.com", "546.851.874-90", "$2a$12$JeeIC8qcSo5U/ysKgLSilOQqKIPPbjuVvv98uUQ0bnYmrrK9Z52GS", 2),
("Maria do Carmo", "mcarmo@email.com", "123.852.456-10", "$2a$12$6kHL0Ef7r65Ony9ja/FTduRA8KCPV7L4Cv6u7rapkK9LSiUzqUR7S", 3);

Select * from Usuario;

INSERT INTO Evento(Nome_Evento, LimitePessoas_Evento, Data_Evento, Horario_Evento, Descricao_Evento, Usuario_ID_Usuario) VALUES
("O grande show", 5000, "2025-09-20", "21:30:00", "O grande show com a cantora Liza no senac Music Hall", 1);

SELECT * FROM Evento;

INSERT INTO Setor(Nome_Setor, LImite_Setor, Preco_Setor, Evento_ID_Evento) VALUES
("Público Geral", 4500, "0.00", 1), ("Convidados Vips", 50, "85.00", 1), ("Imprensa Credenciada", 450, "0.00", 1);

SELECT * FROM Setor;

INSERT INTO Cliente(Nome_Cliente, CPF_Cliente, Email_Cliente) VALUES
("Maria de Fátima", "542.695.852-50", "mariafatima@email.com"),
("Pamela Nascimento", "854.921.764-00", "pamnascimento@email.com"),
("Raimundo Nascimento", "204.320.970-35", "raimundoNas@email.com"),
("Diego Anjos", "336.554.871.00", "diegoanjos@email.com"),
("Patricia Moraes", "182.157.666-80", "patmoraes@email.com");

SELECT * FROM Cliente;

INSERT INTO Ingresso(Cliente_ID, Evento_ID, Setor_ID, ID_Ingresso, Data_Emissao_Ingresso) VALUES
(3,1,2, "GDGFH234", "2025-08-25 08:50:00"),
(3,1,3, "GDGFH582", "2025-08-20 21:00:00"),
(1,1,1, "GDGFH580", "2025-08-15 15:30:00"),
(1,1,3, "GDGFH570", "2025-08-15 19:55:00"),
(2,1,1, "GDGFH503", "2025-08-07 05:55:00");

SELECT * FROM Ingresso;