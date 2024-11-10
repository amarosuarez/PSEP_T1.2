#coding: latin1
import requests

from app.programadores.programadores import programadoresBP

token = ""


def login():
    global token
    username = input("USERNAME:")
    password = input("PASSWORD:")
    resultado = requests.post("http://localhost:5050/users/login",
                json={"username": username, "password": password},
                headers={"Content-Type": "application/json"})

    res = False

    if resultado:
        token = resultado.json().get("token")
        print(token)
        res = True
    else:
        print("Error")

    return res


def main():
    print('Bienvenido a la API de Programadores y sus webs')

    res = login()
    if (res):

        op = int(input('¿A qué deseas acceder?\n1. Programadores\n2. Webs\n3. Salir\n'))

        while op > 3 or op < 1:
            print('No es una opción válida')
            op = int(input('¿A qué deseas acceder?\n1. Programadores\n2. Webs\n3. Salir\n'))

        if op == 1:
            print('Accediendo a programadores...')
            programadores()
        elif op == 2:
            print('Accediendo a webs...')
            webs()
        elif op == 3:
            print('Hasta pronto!')
    else:
        main()


def programadores():
    api_url = "http://127.0.0.1:5050/programadores"
    print('PROGRAMADORES')
    op = int(input('¿Qué deseas hacer?\n1. Obtener todos los programadores\n2. Obtener un programador\n3. Obtener las webs de un programador\n4. Actualizar un programador\n5. Eliminar un programador\n6. Crear un programador\n7. Volver al menú principal'))

    while op != 7:
        if op == 1:
            response = requests.get(api_url, headers={"Authorization": "Bearer " + token})
            print(response.json())
        elif op == 2:
            print('\n')
            iD = int(input('Cual iD deseas obtener?'))
            response = requests.get(api_url + '/' + str(iD))
            print(response.json())
        elif op == 3:
            print('\n')
            iD = int(input('Cual es el ID del programador del que deseas obtener sus webs?'))
            response = requests.get(api_url + '/' + str(iD) + '/webs')
            print(response.json())
        elif op == 4:
            print('\n')

            opA = int(input('¿Qué deseas hacer?\n1. Actualizar todos los campos\n2. Actualizar solo un campo\n3. Salir'))

            while opA != 3:
                if opA == 1:
                    idMod = int(input('Cual id quieres modificar'))
                    dni = input('Cual es el dni del programador')
                    nombre = input('Cual es el nombre')
                    apellidos = input('Cuales son los apellidos')
                    telefono = int(input('Cual es el telefono'))
                    email = input('Cual es el email')

                    todo = {'Id': idMod, 'DNI': dni, 'Nombre': nombre, 'Apellidos': apellidos, 'Teléfono': telefono,
                            'Email': email}

                    response = requests.put(api_url + '/' +  str(idMod), json=todo, headers={"Authorization": "Bearer " + token})
                    print(response.status_code)
                    print(response.json())
                elif opA == 2:
                    idMod = int(input('Cual id quieres modificar'))

                    modo = int(input(
                        '¿Qué quieres modificar? (1: Dni, 2: Nombre, 3: Apellidos, 4: Telefono,  5: Email, 0: Salir)'))

                    while modo != 0:

                        if modo == 1:
                            dni = input('Cual es el dni del programador: ')
                            todo = {'DNI': dni}
                        elif modo == 2:
                            nombre = input('Cual es el nombre: ')
                            todo = {'Nombre': nombre}
                        elif modo == 3:
                            apellidos = input('Cuales son los apellidos: ')
                            todo = {'Apellidos': apellidos}
                        elif modo == 4:
                            telefono = int(input('Cual es el telefono: '))
                            todo = {'Teléfono': telefono}
                        elif modo == 5:
                            email = input('Cual es el email: ')
                            todo = {'Email': email}
                        else:
                            print('Esa opción no es válida. Por favor, intenta de nuevo.')

                        response = requests.put(api_url + "/" + str(idMod), json=todo)
                        print(response.status_code)
                        print(response.json())

                        print('\n')
                        modo = int(input(
                            '¿Qué quieres modificar? (1: Dni, 2: Nombre, 3: Apellidos, 4: Telefono,  5: Email, 0: Salir)'))

                    print('\n')
                    programadores()

                else:
                    print('No es una opción válida')

                print('\n')
                opA = int(
                    input('¿Qué deseas hacer?\n1. Actualizar todos los campos\n2. Actualizar solo un campo\n3. Salir'))

            print('\n')
            programadores()

        elif op == 5:
            iD = int(input('Cual ID deseas eliminar'))
            response = requests.delete(api_url + '/' + str(iD))
            print(response.status_code)
            print(response.json())

        elif op == 6:
            dni = input('Cual es el dni del programador')
            nombre = input('Cual es el nombre')
            apellidos = input('Cuales son los apellidos')
            telefono = int(input('Cual es el telefono'))
            email = input('Cual es el email')

            todo = {'DNI': dni, 'Nombre': nombre, 'Apellidos': apellidos, 'Teléfono': telefono,
                    'Email': email}
            response = requests.post(api_url, json=todo)
            print(response.status_code)
            print(response.json())
        else:
            print('No es una opción válida')


        print("\n")
        op = int(input(
            '¿Qué deseas hacer?\n1. Obtener todos los programadores\n2. Obtener un programador\n3. Obtener las webs de un programador\n4. Actualizar un programador\n5. Eliminar un programador\n6. Crear un programador\n7. Volver al menú principal'))

    print('\n')
    main()

def webs():
    api_url = "http://127.0.0.1:5050/webs"
    print('WEBS')
    op = int(input('¿Qué deseas hacer?\n1. Obtener todas las webs\n2. Obtener una web\n3. Obtener el programador de una web\n4. Actualizar una web\n5. Eliminar una web\n6. Crear una web\n7. Volver al menú principal'))

    while op != 7:
        if op == 1:
            response = requests.get(api_url)
            print(response.json())
        elif op == 2:
            print('\n')
            iD = int(input('Cual iD deseas obtener?'))
            response = requests.get(api_url + '/' + str(iD))
            print(response.json())
        elif op == 3:
            print('\n')
            iD = int(input('Cual es el ID de la web de la cual deseas obtener su programador?'))
            response = requests.get(api_url + '/' + str(iD) + '/programador')
            print(response.json())
        elif op == 4:
            print('\n')

            opA = int(input('¿Qué deseas hacer?\n1. Actualizar todos los campos\n2. Actualizar solo un campo\n3. Salir'))

            while opA != 3:
                if opA == 1:
                    idMod = int(input('Cual id quieres modificar'))
                    titulo = input('Cual es el titulo de la web')
                    tematica = input('Cual es el temática')
                    url = input('Cual es la URL')
                    programador = int(input('Cual es el id del programador'))

                    todo = {'Id': idMod, 'Título': titulo, 'Temática': tematica, 'URL': url,
                            'IdProgramador': programador}

                    response = requests.put(api_url + '/' +  str(idMod), json=todo)
                    print(response.status_code)
                    print(response.json())
                elif opA == 2:
                    idMod = int(input('Cual id quieres modificar'))

                    modo = int(input(
                        '¿Qué quieres modificar? (1: Título, 2: Temática, 3: URL, 4: IdProgramador, 0: Salir)'))

                    while modo != 0:

                        if modo == 1:
                            titulo = input('Cual es el título de la web: ')
                            todo = {'Título': titulo}
                        elif modo == 2:
                            tematica = input('Cual es la temática: ')
                            todo = {'Temática': tematica}
                        elif modo == 3:
                            url = input('Cual es la URL: ')
                            todo = {'URL': url}
                        elif modo == 4:
                            programador = int(input('Cual es el id del programador: '))
                            todo = {'IdProgramador': programador}
                        else:
                            print('Esa opción no es válida. Por favor, intenta de nuevo.')

                        response = requests.put(api_url + "/" + str(idMod), json=todo)
                        print(response.status_code)
                        print(response.json())

                        print('\n')
                        modo = int(input(
                            '¿Qué quieres modificar? (1: Título, 2: Temática, 3: URL, 4: IdProgramador, 0: Salir)'))

                    print('\n')
                    webs()

                else:
                    print('No es una opción válida')

                print('\n')
                opA = int(
                    input('¿Qué deseas hacer?\n1. Actualizar todos los campos\n2. Actualizar solo un campo\n3. Salir'))

            print('\n')
            webs()

        elif op == 5:
            iD = int(input('Cual ID deseas eliminar'))
            response = requests.delete(api_url + '/' + str(iD))
            print(response.status_code)
            print(response.json())

        elif op == 6:
            titulo = input('Cual es el titulo de la web')
            tematica = input('Cual es el temática')
            url = input('Cual es la URL')
            programador = int(input('Cual es el id del programador'))

            todo = {'Título': titulo, 'Temática': tematica, 'URL': url, 'IdProgramador': programador}
            response = requests.post(api_url, json=todo)
            print(response.status_code)
            print(response.json())
        else:
            print('No es una opción válida')


        print("\n")
        op = int(input(
            '¿Qué deseas hacer?\n1. Obtener todas las webs\n2. Obtener una web\n3. Obtener el programador de una web\n4. Actualizar una web\n5. Eliminar una web\n6. Crear una web\n7. Volver al menú principal'))

    print('\n')
    main()

if __name__ == '__main__':
    main()