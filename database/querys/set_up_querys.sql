CREATE TABLE IF NOT EXISTS `sigadica`.`curso` (
    `id_curso` INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `numero_periodos` INTEGER,
    `numero_maximo_periodos` INTEGER,
    `nome` VARCHAR(255) NOT NULL,
    `ano_curriculo` VARCHAR(255),
    `situacao` VARCHAR(255) NOT NULL,
    `data_inclusao` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `data_alteracao`TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `deletado` BOOLEAN DEFAULT FALSE,
    KEY (`nome`)
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
---s20soidk2du298d---
CREATE TABLE IF NOT EXISTS `sigadica`.`disciplina` (
    `id_disciplina` INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `codigo_disciplina` VARCHAR(6) NOT NULL,
    `nome` VARCHAR(255),
    `creditos` INTEGER NOT NULL,
    `carga_teorica` INTEGER,
    `carga_pratica` INTEGER,
    `extensao` INTEGER,
    `descricao` text,
    `data_inclusao` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `data_alteracao`TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `deletado` BOOLEAN DEFAULT FALSE
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
---s20soidk2du298d---
CREATE TABLE IF NOT EXISTS `sigadica`.`cadastro_disciplina_curso` (
    `id_curso` INTEGER NOT NULL,
    `id_disciplina` INTEGER NOT NULL,
    `periodo` INTEGER,
    `categoria_disciplina` VARCHAR(255) DEFAULT 'obrigatoria',
    `deletado` BOOLEAN DEFAULT FALSE,
    `data_inclusao` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `data_alteracao`TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY `curso_disciplina` (`id_curso`,`id_disciplina`),
    FOREIGN KEY (id_curso) REFERENCES `sigadica`.`curso`(id_curso),
    FOREIGN KEY (id_disciplina) REFERENCES `sigadica`.`disciplina`(id_disciplina)
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
---s20soidk2du298d---
CREATE TABLE IF NOT EXISTS `sigadica`.`cadastro_requisito_disciplina` (
    `id_disciplina` INTEGER NOT NULL,
    `id_disciplina_requisito` INTEGER NOT NULL,
    `deletado` BOOLEAN DEFAULT FALSE,
    `data_inclusao` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `data_alteracao`TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY `requisito_disciplina` (`id_disciplina`,`id_disciplina_requisito`),
    FOREIGN KEY (id_disciplina) REFERENCES `sigadica`.`disciplina`(id_disciplina),
    FOREIGN KEY (id_disciplina_requisito) REFERENCES `sigadica`.`disciplina`(id_disciplina)
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
---s20soidk2du298d---
CREATE TABLE IF NOT EXISTS `sigadica`.`usuario` (
    `id_usuario` INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `matricula` VARCHAR(255) NOT NULL,
    `email` VARCHAR(255) NOT NULL,
    `id_curso` INTEGER NOT NULL,
    `data_inclusao` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `data_alteracao`TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `deletado` BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_curso) REFERENCES `sigadica`.`curso`(id_curso)
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
---s20soidk2du298d---
CREATE TABLE IF NOT EXISTS `sigadica`.`avaliacao_disciplina` (
    `id_avaliacao` INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `id_usuario` INTEGER NOT NULL,
    `id_disciplina` INTEGER NOT NULL,
    `nota_monitoria` INTEGER NOT NULL,
    `nota_dificuldade` INTEGER NOT NULL,
    `nota_flexibilidade` INTEGER NOT NULL,
    `nota_didatica` INTEGER NOT NULL,
    `professor` VARCHAR(255) NOT NULL,
    `ano_periodo` VARCHAR(255) NOT NULL,
    `comentario` VARCHAR(255) NOT NULL,
    `data_inclusao` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `data_alteracao`TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `deletado` BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_usuario) REFERENCES `sigadica`.`usuario`(id_usuario)
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
---s20soidk2du298d---
CREATE OR REPLACE VIEW `sigadica`.`disciplinas_curso` AS
SELECT c.id_curso,
	c.nome,
	c.situacao,
	p.deletado as curso_inativo,
	p.periodo,
	p.categoria_disciplina,
	d.codigo_disciplina,
	d.id_disciplina,
	d.carga_pratica,
	d.carga_teorica,
	d.extensao,
	d.descricao,
	d.creditos
FROM sigadica.curso c
	INNER JOIN sigadica.cadastro_disciplina_curso p
		ON p.id_curso = c.id_curso
	INNER JOIN sigadica.disciplina d
		ON p.id_disciplina = d.id_disciplina
WHERE p.deletado = false and d.deletado = false;
---s20soidk2du298d---
CREATE OR REPLACE VIEW `sigadica`.`disciplinas_avaliacao` AS
SELECT c.id_curso,
    d.id_disciplina,
	d.descricao,
	ad.id_avaliacao,
	ad.data_inclusao as data_cadastro,
	ad.nota_monitoria,
    ad.nota_dificuldade,
    ad.nota_flexibilidade,
    ad.nota_didatica,
    ad.professor,
    ad.ano_periodo,
    ad.comentario
FROM sigadica.curso c
	INNER JOIN sigadica.cadastro_disciplina_curso p
		ON p.id_curso = c.id_curso
	INNER JOIN sigadica.disciplina d
		ON p.id_disciplina = d.id_disciplina
    LEFT JOIN sigadica.avaliacao_disciplina ad
		ON ad.id_disciplina = d.id_disciplina
WHERE ad.deletado = false;
---s20soidk2du298d---
CREATE OR REPLACE VIEW `sigadica`.`disciplinas_avaliacao_media_notas` AS
SELECT c.id_curso,
    d.id_disciplina,
	avg(ad.nota_monitoria) as nota_monitoria,
    avg(ad.nota_dificuldade) as nota_dificuldade,
    avg(ad.nota_flexibilidade) as nota_flexibilidade,
    avg(ad.nota_didatica) as nota_didatica
FROM sigadica.curso c
	INNER JOIN sigadica.cadastro_disciplina_curso p
		ON p.id_curso = c.id_curso
	INNER JOIN sigadica.disciplina d
		ON p.id_disciplina = d.id_disciplina
    LEFT JOIN sigadica.avaliacao_disciplina ad
		ON ad.id_disciplina = d.id_disciplina
WHERE ad.deletado = false
GROUP BY c.id_curso,d.id_disciplina;