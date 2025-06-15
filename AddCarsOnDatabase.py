from psycopg2 import sql
import psycopg2
import os
import json


CARID = ['1', '2', '3']
CARBRAND = ["Алексей", "Мария", "Иван"]
CARMODEL = ["OPEL",'VPOPEL','BMW']
CARGENERATION= ["A","A","CS"]   

print(CARID[0])

DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "123"

# 1. Подключение
conn = psycopg2.connect(
   client_encoding="utf-8",  # Важно!
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
cursor = conn.cursor()

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
                            cursor.execute(
                            """
                            INSERT INTO "STAGING".NEWCARS (carid, carbrand, carmodel, cargeneration)
                            VALUES (%s, %s, %s, %s)
                            
                            """,
                            (data[i][0], data[i][1],data[i][2], data[i][3])
                        )
                    conn.commit()  # Фиксируем изменения
                    
                    

                else:
                    print(f"Файл {filename} не содержит список списков")
                    
        except json.JSONDecodeError:
            print(f"Ошибка при чтении файла {filename}: файл не является валидным JSON")
        except Exception as e:
            print(f"Произошла ошибка при обработке файла {filename}: {str(e)}")

cursor.close()
conn.close()
print("Данные успешно добавлены!")


