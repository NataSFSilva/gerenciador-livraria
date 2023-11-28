CREATE DATABASE streaming;

USE streaming;

CREATE TABLE filme (
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

INSERT INTO filmes (titulo, genero, direcao, lancamento) VALUES
    ("Um Corpo que cai", "Suspense", "Hitchcock", "1958-07-21"),
    ("Psicose", "Suspense, terror", "Hitchcock", "1961-11-01"),
    ("Tempos Modernos", "Comédia, romance", "Charlie Chaplin", "1936-02-25");