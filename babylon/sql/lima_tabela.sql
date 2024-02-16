DELETE FROM babylon_glossario_termo_arquivos;
DELETE FROM babylon_glossario_termo;
DELETE FROM babylon_glossario;
DELETE FROM babylon_glossario_autor where id_autor > 1;
DELETE FROM babylon_glossario_idioma where id_idioma > 1;
UPDATE sqlite_sequence SET seq = 0 WHERE NAME IN ('babylon_glossario_termo', 'babylon_glossario', 'babylon_glossario_termo_arquivos');
UPDATE sqlite_sequence SET seq = 1 WHERE NAME IN ('babylon_glossario_autor', 'babylon_glossario_idioma');
VACUUM;