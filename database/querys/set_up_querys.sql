CREATE TABLE IF NOT EXISTS `sigadica`.`curso` (
    `id_curso` INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `numero_periodos` INTEGER,
    `numero_maximo_periodos` INTEGER,
    `nome` VARCHAR(255) NOT NULL,
    `ano_curriculo` VARCHAR(255),
    `situacao` VARCHAR(255) NOT NULL,
    `data_inclusao` timestamp default current_timestamp,
    `data_alteracao`timestamp default current_timestamp,
    KEY (`nome`)
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
---s20soidk2du298d---
CREATE TABLE IF NOT EXISTS `sigadica`.`periodo` (
    `id_curso` INTEGER NOT NULL,
    `codigo_disciplina` VARCHAR(6) NOT NULL,
    `periodo` INTEGER,
    `ativo` boolean default true,
    `data_inclusao` timestamp default current_timestamp,
    `data_alteracao`timestamp default current_timestamp,
    KEY (`codigo_disciplina`),
    KEY (`id_curso`),
    UNIQUE KEY `curso_disciplina` (`id_curso`,`codigo_disciplina`)
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
---s20soidk2du298d---
CREATE TABLE IF NOT EXISTS `sigadica`.`disciplina` (
    `codigo_disciplina` VARCHAR(6) NOT NULL PRIMARY KEY,
    `creditos` INTEGER NOT NULL,
    `carga_teorica` INTEGER,
    `carga_pratica` INTEGER,
    `extensao` INTEGER,
    `descricao` text,
    `data_inclusao` timestamp default current_timestamp,
    `data_alteracao`timestamp default current_timestamp
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
---s20soidk2du298d---
CREATE TABLE IF NOT EXISTS `sigadica`.`requisito` (
    `codigo_disciplina` VARCHAR(6) NOT NULL,
    `codigo_disciplina_requisito` VARCHAR(6) NOT NULL,
    `data_inclusao` timestamp default current_timestamp,
    `data_alteracao`timestamp default current_timestamp,
    UNIQUE KEY `requisito_disciplina` (`codigo_disciplina`,`codigo_disciplina_requisito`)
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
---s20soidk2du298d---
CREATE OR REPLACE VIEW `sigadica`.`disciplinas_curso` AS
SELECT c.id_curso,
	c.nome,
	c.situacao,
	p.periodo,
	p.ativo,
	d.codigo_disciplina,
	d.carga_pratica ,
	d.carga_teorica ,
	d.extensao,
	d.descricao,
	d.creditos
FROM sigadica.curso c
	INNER JOIN sigadica.periodo p
		ON p.id_curso = c.id_curso
	INNER JOIN sigadica.disciplina d
		ON p.codigo_disciplina = d.codigo_disciplina;