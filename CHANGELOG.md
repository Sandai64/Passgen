# Changes

## [Non publié]

## [1.2] (29/10/2018)
### Added
- the verbosity option now adds to the file : 
	- the charlist used
	- the file name
	- the buffer size used
	- the version of Passgen used

### Fixes
- Fixed a crash whith the folder size calculation

### additional notes
- the `passgenlib.py` file has been removed from the source folder, as it is no longer used

## [1.1] (1/10/2018)
- Programme traduit en Français
- Appel du `Garbage Collector` à chaque fichier généré
- Le Buffer du générateur est maintenant de 100 MB
- Maintenant une charlist peut être importée directement depuis un fichier
- Toute dépendance à passgenlib a été supprimée

## [1.0] (29/07/2018)
- Le buffer est limité à 8 Ko
- Ajout des outils de compilation (source)
