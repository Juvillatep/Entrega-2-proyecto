import pandas as pd

Data = pd.read_excel('FI mecatrónica.xlsx', sheet_name='Hoja1')  # Exporta el archivo .xlsx y lo define como dataframe


def Seleccion_carrera(
        Programa):  # Segun la carrera del estudiante nos seleccionara solo sus materias y malla curricular
    Carrera = Data[Data['CARRERA'] == Programa]
    return Carrera


def Materias_nivelatorias(Nivelatoria1, Nivelatoria2,
                          Ingles):  # Si el estudiante debe cumplir con materias de nivelacion o no, este las marcara como aprobada o no

    if 'NO' == Nivelatoria1:
        Data.at[0, 'APROBADA'] = 1

    if 'NO' == Nivelatoria2:
        Data.at[1, 'APROBADA'] = 1

    if 'NO' == Ingles:
        Data.at[(2, 3, 4, 5), 'APROBADA'] = 1

    return Data


def Materias_aprobadas(Materias,Programa):  # marcara las materias que ha aprobado hasta el momento

    for Materia in Materias:
        Aprobada = Seleccion_carrera(Programa)[Materia == Seleccion_carrera(Programa)['NOMBRE DE LA ASIGNATURA']]
        Fila = Aprobada.index
        Data.at[Fila[0], 'APROBADA'] = int(1)
    Carrera = Seleccion_carrera(Programa)
    return Carrera


def Semestres_proximos(Semestre,Materias,Programa):  # se encarga de seleccionar exclusivamente las materias de los semestres mas proximos

    Asignaturas = Materias_aprobadas(Materias,Programa)[(Semestre + 1) == Materias_aprobadas(Materias,Programa)['SEMESTRE']]
    Asignaturas = Asignaturas[0 == Asignaturas['APROBADA']]
    return Asignaturas


def Materias_reprobadas(Semestre,Materias,Programa):  # Las materias que no aprobo durante el semestre las devolvera como opciones a insribir en el siguiente semestre

    Reprobadas = Materias_aprobadas(Materias,Programa)[Semestre == Materias_aprobadas(Materias,Programa)['SEMESTRE']]
    Reprobadas = Reprobadas[0 == Reprobadas['APROBADA']]
    return Reprobadas


def Calcular_creditos(Creditos,Semestre,Materias,Programa):  # compara los creditos de las materias reprobadas y del proximo semestre con los creditos que el estudiante desea
    Fila1 = Materias_reprobadas(Semestre,Materias,Programa)
    Fila1 = Fila1.index
    Fila2 = Semestres_proximos(Semestre,Materias,Programa)
    Fila2 = Fila2.index
    Total = 0
    for X in Fila1:
        Necesarios = Materias_reprobadas(Semestre,Materias,Programa).at[X, 'CRÉDITOS']
        Data.at[X, 'INSCRIBIR'] = 'Si'
        Total = Total + Necesarios
    for Y in Fila2:
        Recomendadas = Semestres_proximos(Semestre,Materias,Programa).at[Y, 'CRÉDITOS']
        Total = Total + Recomendadas
        if Creditos > Total:
            Data.at[Y, 'INSCRIBIR'] = 'Si'
            continue
        else:
            break
    return Materias_reprobadas(Semestre,Materias,Programa)


def Inscribir_materias():
    Inscribir = Data[Data['INSCRIBIR'] == 'Si']
    return Inscribir


def main():
    Programa = input('Carrera a la que pertenece')
    Nivelatoria1 = input('¿Debe nivelar Matemáticas Básicas?')
    Nivelatoria2 = input('¿Debe nivelar Lecto-escritura?')
    Ingles = input('¿Debe nivelar Inglés?')
    Semestre = int(input('Semestre que curso'))
    Creditos = int(input('Creditos que desea inscribir'))
    Materias = []
    Materia = input('Materia aprobada')
    while '' != Materia:
        Materias.append(Materia)
        Materia = input('Materia aprobada')

    Seleccion_carrera(Programa)
    Materias_nivelatorias(Nivelatoria1, Nivelatoria2, Ingles)
    Materias_aprobadas(Materias,Programa)
    Semestres_proximos(Semestre,Materias,Programa)
    Materias_reprobadas(Semestre,Materias,Programa)
    Calcular_creditos(Creditos,Semestre,Materias,Programa)
    return print(Inscribir_materias())

main()

