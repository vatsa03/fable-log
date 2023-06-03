import falcon
import os
import shutil
import pymysql
import json
import time

max_retries = 3
retry_delay = 5

connected = False
retries = 0

while not connected and retries < max_retries:
    try:
        connection = pymysql.connect(
            host='database',
            user='kush',
            port=3306,
            db="fable",
            charset='utf8mb4',
            password='weak_password'
        )
        connected = True
    except pymysql.err.OperationalError:
        retries += 1
        print(f"Connection failed. Retrying ({retries}/{max_retries})...")
        time.sleep(retry_delay)

if not connected:
    print("Failed to establish a connection to the database.")

class FableLog:
    def on_post(self, req, resp):
        data = req.media
        size_bytes = os.path.getsize("log.txt")

        size_mb = size_bytes / (1024)

        if (size_mb < 5):
            if os.stat("log.txt").st_size > 0:
                with open('log.txt', 'r') as file:
                    log_data = json.load(file)
                    log_data.append(data)

                with open('log.txt', 'w') as file:
                    json.dump(log_data, file)
            else:
                with open('log.txt', 'w') as file:
                    json.dump([data], file)
        else:
            if os.path.exists("log_buffer.txt"):
                os.remove("log_buffer.txt")
            shutil.copyfile("log.txt", "log_buffer.txt")
            with open('log.txt', 'w') as file:
                json.dump([data], file)
            
            with open("log_buffer.txt", "r") as file:
                data_items = json.load(file)
                for data in data_items:
                    try:
                        cursor = connection.cursor()
                        query = "INSERT INTO fablelog (event_name, user_id, unix_ts) VALUES (%s, %s, %s)"
                        values = (data['event_name'], data['user_id'], data['unix_ts'])

                        cursor.execute(query, values)

                        connection.commit()

                        print("Data inserted successfully.")
                    finally:
                        cursor.close()
                    
        resp.status = falcon.HTTP_200
        resp.text = "data received"


app = falcon.API()
app.add_route('/log', FableLog())

if __name__ == '__main__':
    from wsgiref import simple_server
    host = '0.0.0.0'
    port = 8081
    httpd = simple_server.make_server(host, port, app)
    httpd.serve_forever()
