CREATE DATABASE streaming IF NOT EXISTS;

USE streaming;

CREATE TABLE filme IF NOT EXISTS (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    titulo VARCHAR(100),
    direcao VARCHAR(100),
    genero VARCHAR(100),
    lancamento DATE
);

SET character_set_client = utf8;
SET character_set_connection = utf8;
SET character_set_results = utf8;
SET collation_connection = utf8_general_ci;