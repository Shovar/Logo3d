# Logo3D-(LP-FIB)

Logo3D es un lenguaje de programación que moderniza el LOGO clásico adoptando una nueva y elegante sintaxis y situando a la popular tortuga en un entorno 3D.

## Contenido

Este fichero contiene:
	-logo3d.g -> La gramática del lenguaje Logo3D
	-logo3d.py -> El intérprete del lenguaje Logo3D
	-turtle3d.py -> API de la tortuga para hacer representaciones en 3D
	-visitor.py -> Visitor de la gramática encargado de evaluarla
	-requirements.txt -> Contiene las librerías necesarias

## Uso
1. Abrir un terminal en esta carpeta.

2. Tener antlr instalado

Descargar de la web  https://www.antlr.org/download.html 

Comprobar:
```bash
java -jar antlr-4.9-complete.jar
```
3. Tener configurado antlr
Ejemplo en Windows:

-Añadir  antlr-4.9-complete.jar al classpath
```bash
	SET CLASSPATH=.;PATH\TO\antlr-4.9-complete.jar;%CLASSPATH%
```
-Crear alias para el ANTLR TOOL y el testRig
```bash
	doskey antlr4=java org.antlr.v4.Tool $*		
	doskey grun=java org.antlr.v4.gui.TestRig $*
```

Ejemplo en Unix:

-Añadir  antlr-4.9-complete.jar al classpath
```bash
	$ export CLASSPATH=".:/PATH/TO/antlr-4.9-complete.jar:$CLASSPATH"
```
-Crear alias para el ANTLR TOOL y el testRig
```bash
	$ alias antlr4='java -Xmx500M -cp "/PATH/TO/antlr-4.9-complete.jar:$CLASSPATH" org.antlr.v4.Tool'
	$ alias grun='java -Xmx500M -cp "/PATH/TO/antlr-4.9-complete.jar:$CLASSPATH" org.antlr.v4.gui.TestRig'
```

4. Instalar las librerías de requirements.txt
Windows:
```bash
py -m pip install -r requirements.txt
```
Unix/macOS:
```bash
python -m pip install -r requirements.txt
```
5. Generar archivos de la gramática 
```bash
antlr4 -Dlanguage=Python3 -no-listener -visitor logo3d.g
```
6. Ejecutar el programa
```bash
python3 logo3d.py file.l3d [main_func] [args]
```
IMPORTANTE: 
- Si el programa a ejecutar no contiene un procedimiento llamado 'main' es necesario incluir el nombre del procedimiento principal en la línea de ejecución.

- Si el procedimiento principal del programa a ejecutar contiene argumentos, es necesario incluir su nombre y los argumentos en la misma linea de bash.

- Si durante la ejecución el programa necesita leer alguna entrada, las irá pidiendo una a una y por orden de llamada sacando por consola el símbolo '?'. Tratará como error el poner todas las entradas en una misma línea.

## Autor
Shovar
