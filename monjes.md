# Monjes y canibales 
**El problema consiste en: estamos en una isla y tenemos 3 monjes junto con 3 canibales y un bote lo que tenemos que hacer es pasar a todos al otro lado de la lista.**

## Reglas

	- No pueden haber mas canibales que monjes en un lado.
	- Cualquiera de los dos puede remar y regresar con el bote.
	- No puede ir el bote vacio.

## Solucion
Para poder representar a los monjes utilizaremos la letra "M" y para  los canibales utilizaremos la letra "C".

 |Lado Izquiero| Bote de ida|  Se queda |Bote de regreso    |Isla|
 |:-----------:| :---------:| :-------: |:-------------:| :-:    |
 |CCC MMM      | 	CC		| 	  C     | 		C 		| C      |
 |CC MMM	   |    CC      |     C		| 		C		| CC     |
 |C MMM 	   |    MM      |     M     |       MC      | MC     |
 |CC MM        |    MM      |    MM     |       C       | MMM    |
 |CCC          |    CC      |    C      |       C       | C MMM  |
 |CC           |    CC      |    CC     |               | CCC MMM|

 El problema se ha completado

 > Autor: Jose Osvaldo