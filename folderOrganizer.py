import os
import shutil

def getUserDownloadPath():
    user = os.getlogin()
    downloadPath = f"C:\\Users\\{user}\\Downloads\\"
    return downloadPath

def createDirectory(path, extensions): 
    try: 
        for i in range(len(extensions)): 
            if not os.path.isdir(path + extensions[i][0]):
                os.mkdir(path + extensions[i][0])
        if os.mkdir(path + 'Otros') == False: 
            os.mkdir(path + 'Otros')
    except FileExistsError as e: 
        print('Ha ocurrido una excepción: ' + str(e))
    except OSError as e: 
        print('Se ha producido un error.')
        print(str(e))
        raise

def moveFiles(extList, file, ext, path):
    if ext in extList: 
        shutil.move(path + file, path + extList[0])

def order(path, fileList, extensions):
    for file in fileList:
        for i in range(len(extensions)):
            fileName, ext = os.path.splitext(file)
            moveFiles(extensions[i - 1], file, ext, path)
        if os.path.isfile(path + file): 
            if ext != '': 
                shutil.move(path + file, path + 'Otros')

def main():
    extensions = (('Documentos', '.docx', '.txt', '.doc', '.pdf', '.pptx', '.ppt', '.tex', '.xls', '.xlsx', '.csv'), 
                        ('Fotos', '.png', '.jpg', '.jpeg', '.gif', '.ico', '.bmp', '.svg'), 
                        ('Audio', '.mp3', '.wav', '.wma', '.ogg', '.flac'),
                        ('Video', '.mov', '.mp4', '.avi', '.mkv', '.wmv'),
                        ('Ejecutable', '.exe', '.msi'), 
                        ('Comprimidos', '.rar', '.zip', '.7z', '.rar5'))
    print('\t ● ORGANIZADOR DE DESCARGAS ● ')
    while True: 
        print('''A continuación seleccione una opción: 
            1) Crear carpetas. 
            2) Mover archivos.
            3) Información.
            4) Salir.''')
        num = int(input(' >> '))
        if num == 1:
            path = getUserDownloadPath()
            createDirectory(path, extensions)
            print('Las carpetas han sido creadas correctamente')
        elif num == 2:
            path = getUserDownloadPath()
            fileList = os.listdir(path)
            order(path, fileList, extensions)
            print('Archivos movidos correctamente')
        elif num == 3:
            print('\t* Organizador de Descargas *')
            print('''\tPrograma escrito con Python 3.10.1
            \n
            Separa archivos por: 
            a) Documentos: .docx; .txt; .doc; .pdf; .pptx; .ppt; .tex; .xls; .xlsx; .csv
            b) Fotos: .png; .jpg/.jpeg; .gif; .ico; .bmp; .svg
            c) Audio: .mp3; .wav; .wma; .ogg; .flac
            d) Video: .mov; .mp4; .avi; .mkv; .wmv
            e) Ejecutable: .exe; .msi
            f) Comprimidos: .rar; .zip; .7z; .rar5
            g) Otros: Extensiones no reconocidas. 
            \nNOTA: Las carpetas tendran los nombres especificados anteriormente.\n''')
        elif num == 4: 
            break
        else: 
            print('ERROR: Ha introducido un número invalido\nPor favor, intentelo de nuevo.')


if __name__ == '__main__':
    main()