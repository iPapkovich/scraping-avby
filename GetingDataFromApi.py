import os
import json

# Укажите путь к вашей папке
folder_path = './JSON_DIR/SOURCE_DIR'

# Проходим по всем файлам в папке
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):  # Проверяем, что файл имеет расширение .json
        file_path = os.path.join(folder_path, filename)
        
        try:
            # Открываем и читаем JSON-файл
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
                # Проверяем, что данные соответствуют ожидаемому формату (список списков)
                if isinstance(data, list) and all(isinstance(item, list) for item in data):
                    print(f"Файл {filename} успешно прочитан:")
                    print(data[1])

                    for i in range(len(data)):
                        print(data[i][1])
                        '''cursor.execute(
                            """
                            INSERT INTO CARS (carid, carbrand, carmodel, cargeneration)
                            VALUES (%s, %s, %s, %s)
                            """,
                            (CARID[i], CARBRAND[i], CARMODEL[i], CARGENERATION[i])
                        )'''

                    

                else:
                    print(f"Файл {filename} не содержит список списков")
                    
        except json.JSONDecodeError:
            print(f"Ошибка при чтении файла {filename}: файл не является валидным JSON")
        except Exception as e:
            print(f"Произошла ошибка при обработке файла {filename}: {str(e)}")

