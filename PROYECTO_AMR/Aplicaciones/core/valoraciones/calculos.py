# calculos.py

def calcular_promedio_tiro(valores):
    """
    Calcula el promedio de tiro basado en las estadísticas provistas y limita el resultado a un máximo de 100.
    
    Argumento:
    valores: diccionario con las estadísticas necesarias, por ejemplo:
    {
        'GOLES ANOTADOS': valor,
        'TIROS TOTALES': valor,
        'TIROS AL ARCO': valor,
        'PENALES ANOTADOS': valor,
        'PENALES EJECUTADOS': valor
    }

    Retorna:
    float: el promedio calculado para la cualidad Tiro, en una escala de 0 a 100
    """
    goles_anotados = valores.get('GOLES ANOTADOS', 0)
    tiros_totales = valores.get('TIROS TOTALES', 0)
    tiros_al_arco = valores.get('TIROS AL ARCO', 0)
    penales_anotados = valores.get('PENALES ANOTADOS', 0)
    penales_ejecutados = valores.get('PENALES EJECUTADOS', 0)
    
    if tiros_totales == 0 or tiros_al_arco == 0 or penales_ejecutados == 0:
        return 0

    promedio = (( 
        (goles_anotados / tiros_totales) +
        (tiros_al_arco / tiros_totales) +
        ((goles_anotados / tiros_al_arco) * 1.1) +
        (penales_anotados / penales_ejecutados)
    ) / 4 ) * 100
    
    if promedio > 100:
        promedio = 100
    
    return promedio


def calcular_promedio_pase(valores):
    """
    Calcula el promedio de pase basado en las estadísticas provistas y limita el resultado a un máximo de 100.
    
    Argumento:
    valores: diccionario con las estadísticas necesarias, por ejemplo:
    {
        'PASES ACERTADOS': valor,
        'PASES TOTALES': valor,
        'CENTROS ACERTADOS': valor,
        'CENTROS TOTALES': valor
    }

    Retorna:
    float: el promedio calculado para la cualidad Pase, en una escala de 0 a 100
    """
    pases_acertados = valores.get('PASES ACERTADOS', 0)
    pases_totales = valores.get('PASES TOTALES', 0)
    centros_acertados = valores.get('CENTROS ACERTADOS', 0)
    centros_totales = valores.get('CENTROS TOTALES', 0)
    
    if pases_totales == 0 or centros_totales == 0:
        return 0

    promedio = (
        (pases_acertados / pases_totales) +
        (centros_acertados / centros_totales)
    ) / 2 * 100
    
    if promedio > 100:
        promedio = 100
    
    return promedio


def calcular_promedio_velocidad(valores):
    """
    Calcula el promedio de velocidad basado en las estadísticas provistas y limita el resultado a un máximo de 100.
    
    Argumento:
    valores: diccionario con las estadísticas necesarias, por ejemplo:
    {
        'SPRINT': valor,
        'ACELERACION': valor
    }

    Retorna:
    float: el promedio calculado para la cualidad Velocidad, en una escala de 0 a 100
    """
    sprint_kmh = valores.get('SPRINT', 0)
    aceleracion_kmh = valores.get('ACELERACION', 0)
    
    promedio = (
        (sprint_kmh / 42) +
        (aceleracion_kmh / 35.28)
    ) / 2 * 100
    
    if promedio > 100:
        promedio = 100
    
    return promedio


def calcular_promedio_regate(valores):
    """
    Calcula el promedio de regate basado en las estadísticas provistas y limita el resultado a un máximo de 100.
    
    Argumento:
    valores: diccionario con las estadísticas necesarias, por ejemplo:
    {
        'REGATES EXITOSOS': valor,
        'REGATES TOTALES': valor,
        'DUELOS GANADOS': valor,
        'DUELOS TOTALES': valor
    }

    Retorna:
    float: el promedio calculado para la cualidad Regate, en una escala de 0 a 100
    """
    regates_exitosos = valores.get('REGATES EXITOSOS', 0)
    regates_intentos = valores.get('REGATES TOTALES', 0)
    duelos_ganados = valores.get('DUELOS GANADOS', 0)
    duelos_intentos = valores.get('DUELOS TOTALES', 0)
    
    if regates_intentos == 0 or duelos_intentos == 0:
        return 0

    promedio = (
        (regates_exitosos / regates_intentos) +
        (duelos_ganados / duelos_intentos)
    ) / 2 * 100
    
    if promedio > 100:
        promedio = 100
    
    return promedio


def calcular_promedio_defensa(valores):
    """
    Calcula el promedio de defensa basado en las estadísticas provistas y limita el resultado a un máximo de 100.
    
    Argumento:
    valores: diccionario con las estadísticas necesarias, por ejemplo:
    {
        'INTERCEPCIONES EXITOSAS': valor,
        'INTERCEPCIONES INTENTOS': valor,
        'DESPEJES EXITOSOS': valor,
        'DESPEJES INTENTOS': valor
    }

    Retorna:
    float: el promedio calculado para la cualidad Defensa, en una escala de 0 a 100
    """
    intercepciones_exitosas = valores.get('INTERCEPCIONES EXITOSAS', 0)
    intercepciones_intentos = valores.get('INTERCEPCIONES INTENTOS', 0)
    despejes_exitosos = valores.get('DESPEJES EXITOSOS', 0)
    despejes_intentos = valores.get('DESPEJES INTENTOS', 0)
    
    if intercepciones_intentos == 0 or despejes_intentos == 0:
        return 0

    promedio = (
        ((intercepciones_exitosas / intercepciones_intentos) *1.1) +
        (despejes_exitosos / despejes_intentos)
    ) / 2 * 100
    
    if promedio > 100:
        promedio = 100
    
    return promedio


def calcular_promedio_fisico(valores):
    """
    Calcula el promedio físico basado en las estadísticas provistas y limita el resultado a un máximo de 100.
    
    Argumento:
    valores: diccionario con las estadísticas necesarias, por ejemplo:
    {
        'SALTO EVALUADO': valor,
        'DISTANCIA RECORRIDA': valor,
        'SPRINTS REALIZADOS': valor,
        'FUERZA EXPLOSIVA EVALUADA': valor,
        'FUERZA ISOMETRICA EVALUADA': valor,
        'FUERZA RESISTENCIA EVALUADA': valor
    }

    Retorna:
    float: el promedio calculado para la cualidad Física, en una escala de 0 a 100
    """
    salto_evaluado = valores.get('SALTO EVALUADO', 0)
    distancia_recorrida = valores.get('DISTANCIA RECORRIDA', 0)
    sprints_realizados = valores.get('SPRINTS REALIZADOS', 0)
    fuerza_explosiva_evaluada = valores.get('FUERZA EXPLOSIVA EVALUADA', 0)
    fuerza_isometrica_evaluada = valores.get('FUERZA ISOMETRICA EVALUADA', 0)
    resistencia_evaluada = valores.get('FUERZA RESISTENCIA EVALUADA', 0)
    
    promedio = (
        (salto_evaluado / 100) +
        (distancia_recorrida / 1000) +
        (sprints_realizados / 15) +
        (fuerza_explosiva_evaluada / 200) +
        (fuerza_isometrica_evaluada / 180) +
        (resistencia_evaluada / 25)
    ) / 6 * 100
    
    if promedio > 100:
        promedio = 100
    
    return promedio


def calcular_promedio_reflejos(valores):
    """
    Calcula el promedio de reflejos basado en las estadísticas provistas y limita el resultado a un máximo de 100.
    
    Argumento:
    valores: diccionario con las estadísticas necesarias, por ejemplo:
    {
        'PENALES ATAJADOS': valor,
        'PENALES RECIBIDOS': valor,
        '1V1 GANADOS': valor,
        '1V1 TOTALES': valor,
        'ATAJADAS CRITICAS REFLEJOS': valor,
        'TIROS BLOQUEADOS REFLEJOS': valor
    }

    Retorna:
    float: el promedio calculado para reflejos, en una escala de 0 a 100
    """
    penales_atajados = valores.get('PENALES ATAJADOS', 0)
    penales_recibidos = valores.get('PENALES RECIBIDOS', 0)
    one_v_one_ganados = valores.get('1V1 GANADOS', 0)
    one_v_one_totales = valores.get('1V1 TOTALES', 0)
    atajadas_criticas_reflejos = valores.get('ATAJADAS CRITICAS REFLEJOS', 0)
    tiros_bloqueados_reflejos = valores.get('TIROS BLOQUEADOS REFLEJOS', 0)

    if penales_recibidos == 0 or one_v_one_totales == 0 or tiros_bloqueados_reflejos == 0:
        return 0

    promedio = (
        (penales_atajados / penales_recibidos * 1.5) +
        (one_v_one_ganados / one_v_one_totales) +
        (atajadas_criticas_reflejos / tiros_bloqueados_reflejos)
    ) / 3 * 100 * 1.1
    
    return min(promedio, 100)  # Limitar a 100


def calcular_promedio_manejo(valores):
    """
    Calcula el promedio de manejo basado en las estadísticas provistas y limita el resultado a un máximo de 100.
    
    Argumento:
    valores: diccionario con las estadísticas necesarias, por ejemplo:
    {
        'TIROS BLOQUEADOS MANEJO': valor,
        'TIROS AL ARCO': valor,
        'DESPEJES EXITOSOS': valor,
        'DESPEJES TOTALES': valor,
        'ATRAPES SIN REBOTE': valor,
        'BALONES ATRAPADOS': valor
    }

    Retorna:
    float: el promedio calculado para manejo, en una escala de 0 a 100
    """
    tiros_bloqueados_manejo = valores.get('TIROS BLOQUEADOS MANEJO', 0)
    tiros_al_arco = valores.get('TIROS AL ARCO', 0)
    despejes_exitosos = valores.get('DESPEJES EXITOSOS', 0)
    despejes_totales = valores.get('DESPEJES TOTALES', 0)
    atrapes_sin_rebote = valores.get('ATRAPES SIN REBOTE', 0)
    balones_atrapados = valores.get('BALONES ATRAPADOS', 0)

    if tiros_al_arco == 0 or despejes_totales == 0 or balones_atrapados == 0:
        return 0

    promedio = (
        (tiros_bloqueados_manejo / tiros_al_arco) +
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
        'SAQUES LARGOS EXITOSOS': valor,
        'SAQUES LARGOS INTENTOS': valor,
        'SAQUES CORTOS EXITOSOS': valor,
        'SAQUES CORTOS INTENTOS': valor
    }

    Retorna:
    float: el promedio calculado para saque de arco, en una escala de 0 a 100
    """
    saques_largos_exitosos = valores.get('SAQUES LARGOS EXITOSOS', 0)
    saques_largos_intentos = valores.get('SAQUES LARGOS INTENTOS', 0)
    saques_cortos_exitosos = valores.get('SAQUES CORTOS EXITOSOS', 0)
    saques_cortos_intentos = valores.get('SAQUES CORTOS INTENTOS', 0)

    if saques_largos_intentos == 0 or saques_cortos_intentos == 0:
        return 0

    promedio = (
        (saques_largos_exitosos / saques_largos_intentos) +
        (saques_cortos_exitosos / saques_cortos_intentos)
    ) / 2 * 100
    
    return min(promedio, 100)  # Limitar a 100
