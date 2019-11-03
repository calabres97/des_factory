# Simulación de sucesos discretos.
Para que un sistema funcione necesita que haya 10 máquinas operativas. Para evitar el fallo del mismo se disponen de 4 máquinas adicionales en reserva que reemplazarán a aquellas que se vayan estropeando.   

Siguiendo la teoría de fiabilidad de sistemas, suponemos que las máquinas se encuentran en la etapa de desgaste dentro de la curva de bañera usada típicamente en las funciones de fiabilidad, por lo que la distribución del tiempo que tardan en estropearse las máquinas es una normal. El fichero fallos.txt incluye datos históricos sobre los tiempos de fallos de las máquinas que permite estimar los parámetros de dicha distribución.   

Las máquinas estropeadas son enviadas al taller de reparación en la que tres operarios trabajan individualmente y de forma paralela en la reparación. El tiempo de reparación se distribuye exponencialmente pero, debido a la experiencia que van acumulando los operarios, la tasa va aumentando con el tiempo linealmente entre 0.55 máquinas/hora (inicialmente) y 1.65 máquinas/hora (al final de la simulación).   

Debido al alto coste de la puesta en marcha de las máquinas, aunque haya menos de 10 máquinas operativas y, por lo tanto, el sistema no funcione, no se parará el funcionamiento de dichas máquinas.   

Una vez reparada una máquina pasa a la reserva y, por lo tanto, queda disponible para su uso en caso de que sea necesario.
