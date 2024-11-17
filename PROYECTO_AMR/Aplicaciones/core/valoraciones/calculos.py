# calculos.py

def calcular_promedio_tiro(valores):
    """
    Calcula el promedio de tiro basado en las estadísticas provistas y limita el resultado a un máximo de 100.
    
    Argumento:
    valores: diccionario con las estadísticas necesarias, por ejemplo:
    {
        'goles_anotados': valor,
        'tiros_totales': valor,
        'tiros_al_arco': valor,
        'penales_anotados': valor,
        'penales_ejecutados': valor
    }

    Retorna:
    float: el promedio calculado para la cualidad Tiro, en una escala de 0 a 100
    """
    # Extraer valores del diccionario, con 0 como valor predeterminado si no están presentes
    goles_anotados = valores.get('goles_anotados', 0)
    tiros_totales = valores.get('tiros_totales', 0)
    tiros_al_arco = valores.get('tiros_al_arco', 0)
    penales_anotados = valores.get('penales_anotados', 0)
    penales_ejecutados = valores.get('penales_ejecutados', 0)
    
    # Evitar divisiones por cero para asegurar que no ocurra un error de cálculo
    if tiros_totales == 0 or tiros_al_arco == 0 or penales_ejecutados == 0:
        return 0

    # Cálculo del promedio basado en la fórmula
    promedio = (( 
        (goles_anotados / tiros_totales) +
        (tiros_al_arco / tiros_totales) +
        ((goles_anotados / tiros_al_arco) * 1.1) +
        (penales_anotados / penales_ejecutados)
    ) / 4 ) * 100
    
    # Limitar el resultado máximo a 100
    if promedio > 100:
        promedio = 100
    
    return promedio


valores_tiro = {
    'goles_anotados': 10,
    'tiros_totales': 10,
    'tiros_al_arco': 10,
    'penales_anotados': 4,
    'penales_ejecutados': 4
}

# Llamada a la función y guardado del resultado
promedio_tiro = calcular_promedio_tiro(valores_tiro)

# Imprimimos el resultado para ver el promedio calculado
print("El promedio de tiro es:", promedio_tiro)


###########################################################################################################################
# calculos.py

def calcular_promedio_pase(valores):
    """
    Calcula el promedio de pase basado en las estadísticas provistas y limita el resultado a un máximo de 100.
    
    Argumento:
    valores: diccionario con las estadísticas necesarias, por ejemplo:
    {
        'pases_acertados': valor,
        'pases_totales': valor,
        'centros_acertados': valor,
        'centros_totales': valor
    }

    Retorna:
    float: el promedio calculado para la cualidad Pase, en una escala de 0 a 100
    """
    # Extraer valores del diccionario, con 0 como valor predeterminado si no están presentes
    pases_acertados = valores.get('pases_acertados', 0)
    pases_totales = valores.get('pases_totales', 0)
    centros_acertados = valores.get('centros_acertados', 0)
    centros_totales = valores.get('centros_totales', 0)
    
    # Evitar divisiones por cero para asegurar que no ocurra un error de cálculo
    if pases_totales == 0 or centros_totales == 0:
        return 0

    # Cálculo del promedio basado en la fórmula
    promedio = (
        (pases_acertados / pases_totales) +
        (centros_acertados / centros_totales)
    ) / 2 * 100
    
    # Limitar el resultado máximo a 100
    if promedio > 100:
        promedio = 100
    
    return promedio

# Diccionario de ejemplo con valores de estadísticas
valores_pase = {
    'pases_acertados': 30,
    'pases_totales': 40,
    'centros_acertados': 15,
    'centros_totales': 20
}

# Llamada a la función y guardado del resultado
promedio_pase = calcular_promedio_pase(valores_pase)

# Imprimimos el resultado para ver el promedio calculado
print("El promedio de pase es:", promedio_pase)


################################################################################################################################

# calculos.py

def calcular_promedio_velocidad(valores):
    """
    Calcula el promedio de velocidad basado en las estadísticas provistas y limita el resultado a un máximo de 100.
    
    Argumento:
    valores: diccionario con las estadísticas necesarias, por ejemplo:
    {
        'sprint_kmh': valor,
        'aceleracion_kmh': valor
    }

    Retorna:
    float: el promedio calculado para la cualidad Velocidad, en una escala de 0 a 100
    """
    # Extraer valores del diccionario, con 0 como valor predeterminado si no están presentes
    sprint_kmh = valores.get('sprint_kmh', 0)
    aceleracion_kmh = valores.get('aceleracion_kmh', 0)
    
    # Cálculo del promedio basado en la fórmula
    promedio = (
        (sprint_kmh / 42) +
        (aceleracion_kmh / 35.28)
    ) / 2 * 100
    
    # Limitar el resultado máximo a 100
    if promedio > 100:
        promedio = 100
    
    return promedio

valores_velocidad = {
    'sprint_kmh': 36,
    'aceleracion_kmh': 30
}

# Llamada a la función y guardado del resultado
promedio_velocidad = calcular_promedio_velocidad(valores_velocidad)

# Imprimimos el resultado para ver el promedio calculado
print("El promedio de velocidad es:", promedio_velocidad)

############################################################################################################################################################

def calcular_promedio_regate(valores):
    """
    Calcula el promedio de regate basado en las estadísticas provistas y limita el resultado a un máximo de 100.
    
    Argumento:
    valores: diccionario con las estadísticas necesarias, por ejemplo:
    {
        'regates_exitosos': valor,
        'regates_intentos': valor,
        'duelos_ganados': valor,
        'duelos_intentos': valor
    }

    Retorna:
    float: el promedio calculado para la cualidad Regate, en una escala de 0 a 100
    """
    # Extraer valores del diccionario, con 0 como valor predeterminado si no están presentes
    regates_exitosos = valores.get('regates_exitosos', 0)
    regates_intentos = valores.get('regates_intentos', 0)
    duelos_ganados = valores.get('duelos_ganados', 0)
    duelos_intentos = valores.get('duelos_intentos', 0)
    
    # Evitar divisiones por cero
    if regates_intentos == 0 or duelos_intentos == 0:
        return 0

    # Cálculo del promedio basado en la fórmula
    promedio = (
        (regates_exitosos / regates_intentos) +
        (duelos_ganados / duelos_intentos)
    ) / 2 * 100
    
    # Limitar el resultado máximo a 100
    if promedio > 100:
        promedio = 100
    
    return promedio
valores_regate = {
    'regates_exitosos': 18,
    'regates_intentos': 20,
    'duelos_ganados': 15,
    'duelos_intentos': 20
}

# Llamada a la función y guardado del resultado
promedio_regate = calcular_promedio_regate(valores_regate)

# Imprimimos el resultado para ver el promedio calculado
print("El promedio de regate es:", promedio_regate)
############################################################################################################################################################

def calcular_promedio_defensa(valores):
    """
    Calcula el promedio de defensa basado en las estadísticas provistas y limita el resultado a un máximo de 100.
    
    Argumento:
    valores: diccionario con las estadísticas necesarias, por ejemplo:
    {
        'intercepciones_exitosas': valor,
        'intercepciones_intentos': valor,
        'despejes_exitosos': valor,
        'despejes_intentos': valor
    }

    Retorna:
    float: el promedio calculado para la cualidad Defensa, en una escala de 0 a 100
    """
    # Extraer valores del diccionario, con 0 como valor predeterminado si no están presentes
    intercepciones_exitosas = valores.get('intercepciones_exitosas', 0)
    intercepciones_intentos = valores.get('intercepciones_intentos', 0)
    despejes_exitosos = valores.get('despejes_exitosos', 0)
    despejes_intentos = valores.get('despejes_intentos', 0)
    
    # Evitar divisiones por cero
    if intercepciones_intentos == 0 or despejes_intentos == 0:
        return 0

    # Cálculo del promedio basado en la fórmula
    promedio = (
        ((intercepciones_exitosas / intercepciones_intentos) *1.1) +
        (despejes_exitosos / despejes_intentos)
    ) / 2 * 100
    
    # Limitar el resultado máximo a 100
    if promedio > 100:
        promedio = 100
    
    return promedio

valores_defensa = {
    'intercepciones_exitosas': 15,
    'intercepciones_intentos': 20,
    'despejes_exitosos': 10,
    'despejes_intentos': 12
}

# Llamada a la función y guardado del resultado
promedio_defensa = calcular_promedio_defensa(valores_defensa)

# Imprimimos el resultado para ver el promedio calculado
print("El promedio de defensa es:", promedio_defensa)

############################################################################################################################################################
def calcular_promedio_fisico(valores):
    """
    Calcula el promedio físico basado en las estadísticas provistas y limita el resultado a un máximo de 100.
    
    Argumento:
    valores: diccionario con las estadísticas necesarias, por ejemplo:
    {
        'salto_evaluado': valor,
        'distancia_recorrida': valor,
        'sprints_realizados': valor,
        'fuerza_explosiva_evaluada': valor,
        'fuerza_isometrica_evaluada': valor,
        'resistencia_evaluada': valor
    }

    Retorna:
    float: el promedio calculado para la cualidad Física, en una escala de 0 a 100
    """
    # Extraer valores del diccionario, con 0 como valor predeterminado si no están presentes
    salto_evaluado = valores.get('salto_evaluado', 0)
    distancia_recorrida = valores.get('distancia_recorrida', 0)
    sprints_realizados = valores.get('sprints_realizados', 0)
    fuerza_explosiva_evaluada = valores.get('fuerza_explosiva_evaluada', 0)
    fuerza_isometrica_evaluada = valores.get('fuerza_isometrica_evaluada', 0)
    resistencia_evaluada = valores.get('resistencia_evaluada', 0)
    
    # Cálculo del promedio basado en la fórmula
    promedio = (
        (salto_evaluado / 100) +
        (distancia_recorrida / 1000) +
        (sprints_realizados / 15) +
        (fuerza_explosiva_evaluada / 200) +
        (fuerza_isometrica_evaluada / 180) +
        (resistencia_evaluada / 25)
    ) / 6 * 100
    
    # Limitar el resultado máximo a 100
    if promedio > 100:
        promedio = 100
    
    return promedio

valores_fisico = {
    'salto_evaluado': 90,
    'distancia_recorrida': 800,
    'sprints_realizados': 12,
    'fuerza_explosiva_evaluada': 180,
    'fuerza_isometrica_evaluada': 150,
    'resistencia_evaluada': 20
}

# Llamada a la función y guardado del resultado
promedio_fisico = calcular_promedio_fisico(valores_fisico)

# Imprimimos el resultado para ver el promedio calculado
print("El promedio físico es:", promedio_fisico)

############################################################################################################################################################

def calcular_promedio_reflejos(valores):
    """
    Calcula el promedio de reflejos basado en las estadísticas provistas y limita el resultado a un máximo de 100.
    
    Argumento:
    valores: diccionario con las estadísticas necesarias, por ejemplo:
    {
        'penales_atajados': valor,
        'penales_recibidos': valor,
        '1v1_ganados': valor,
        '1v1_intentos': valor,
        'atajadas_criticas': valor,
        'tiros_bloqueados': valor
    }

    Retorna:
    float: el promedio calculado para reflejos, en una escala de 0 a 100
    """
    # Extraer valores del diccionario
    penales_atajados = valores.get('penales_atajados', 0)
    penales_recibidos = valores.get('penales_recibidos', 0)
    one_v_one_ganados = valores.get('1v1_ganados', 0)
    one_v_one_intentos = valores.get('1v1_intentos', 0)
    atajadas_criticas = valores.get('atajadas_criticas', 0)
    tiros_bloqueados = valores.get('tiros_bloqueados', 0)

    # Evitar divisiones por cero
    if penales_recibidos == 0 or one_v_one_intentos == 0 or tiros_bloqueados == 0:
        return 0

    # Calcular el promedio de reflejos
    promedio = (
        (penales_atajados / penales_recibidos * 1.5) +
        (one_v_one_ganados / one_v_one_intentos) +
        (atajadas_criticas / tiros_bloqueados)
    ) / 3 * 100 * 1.1
    
    return min(promedio, 100)  # Limitar a 100


def calcular_promedio_manejo(valores):
    """
    Calcula el promedio de manejo basado en las estadísticas provistas y limita el resultado a un máximo de 100.
    
    Argumento:
    valores: diccionario con las estadísticas necesarias, por ejemplo:
    {
        'tiros_bloqueados': valor,
        'tiros_al_arco': valor,
        'despejes_exitosos': valor,
        'despejes_totales': valor,
        'atrapes_sin_rebote': valor,
        'balones_atrapados': valor
    }

    Retorna:
    float: el promedio calculado para manejo, en una escala de 0 a 100
    """
    # Extraer valores del diccionario
    tiros_bloqueados = valores.get('tiros_bloqueados', 0)
    tiros_al_arco = valores.get('tiros_al_arco', 0)
    despejes_exitosos = valores.get('despejes_exitosos', 0)
    despejes_totales = valores.get('despejes_totales', 0)
    atrapes_sin_rebote = valores.get('atrapes_sin_rebote', 0)
    balones_atrapados = valores.get('balones_atrapados', 0)

    # Evitar divisiones por cero
    if tiros_al_arco == 0 or despejes_totales == 0 or balones_atrapados == 0:
        return 0

    # Calcular el promedio de manejo
    promedio = (
        (tiros_bloqueados / tiros_al_arco) +
        (despejes_exitosos / despejes_totales) +
        (atrapes_sin_rebote / balones_atrapados)
    ) / 3 * 100 * 1.1
    
    return min(promedio, 100)  # Limitar a 100


def calcular_promedio_saque(valores):
    """
    Calcula el promedio de saque de arco basado en las estadísticas provistas y limita el resultado a un máximo de 100.
    
    Argumento:
    valores: diccionario con las estadísticas necesarias, por ejemplo:
    {
        'saques_largos_exitosos': valor,
        'saques_largos_totales': valor,
        'saques_cortos_exitosos': valor,
        'saques_cortos_totales': valor
    }

    Retorna:
    float: el promedio calculado para saque de arco, en una escala de 0 a 100
    """
    # Extraer valores del diccionario
    saques_largos_exitosos = valores.get('saques_largos_exitosos', 0)
    saques_largos_totales = valores.get('saques_largos_totales', 0)
    saques_cortos_exitosos = valores.get('saques_cortos_exitosos', 0)
    saques_cortos_totales = valores.get('saques_cortos_totales', 0)

    # Evitar divisiones por cero
    if saques_largos_totales == 0 or saques_cortos_totales == 0:
        return 0

    # Calcular el promedio de saque de arco
    promedio = (
        (saques_largos_exitosos / saques_largos_totales) +
        (saques_cortos_exitosos / saques_cortos_totales)
    ) / 2 * 100
    
    return min(promedio, 100)  # Limitar a 100

valores_reflejos = {
    'penales_atajados': 3,
    'penales_recibidos': 5,
    '1v1_ganados': 7,
    '1v1_intentos': 10,
    'atajadas_criticas': 4,
    'tiros_bloqueados': 6
}
valores_manejo = {
    'tiros_bloqueados': 10,
    'tiros_al_arco': 15,
    'despejes_exitosos': 8,
    'despejes_totales': 10,
    'atrapes_sin_rebote': 6,
    'balones_atrapados': 8
}
valores_saque = {
    'saques_largos_exitosos': 5,
    'saques_largos_totales': 8,
    'saques_cortos_exitosos': 4,
    'saques_cortos_totales': 6
}

# Llamada a las funciones y resultado
promedio_reflejos = calcular_promedio_reflejos(valores_reflejos)
promedio_manejo = calcular_promedio_manejo(valores_manejo)
promedio_saque = calcular_promedio_saque(valores_saque)

# Imprimimos los resultados
print("Promedio Reflejos:", promedio_reflejos)
print("Promedio Manejo:", promedio_manejo)
print("Promedio Saque:", promedio_saque)