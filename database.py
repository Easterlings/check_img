import mysql.connector
from config import DATABASE

class DB:
    def __init__(self, table):
        self.host = DATABASE["host"]
        self.user = DATABASE["user"]
        self.password = DATABASE["password"]
        self.database = DATABASE["database"]
        self.db = None
        self.cursor = None
        self.table = table
    
    def _connectMysql(self):
        self.db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.db.cursor()

    def _closeConnect(self):
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()

    def generate_where(self, data):
        # 检查字典是否为空
        if not data:
            return ""
        # 生成查询语句
        keys = list(data.keys())
        values = list(data.values())
        # 构建 WHERE 子句
        return " WHERE "+" AND ".join([f"{key} = '{value}'" for key, value in zip(keys, values)])
    
    def generate_update_set(self, data):
        # 检查字典是否为空
        if not data:
            return ""
        # 生成查询语句
        keys = list(data.keys())
        values = list(data.values())
        # 构建 WHERE 子句
        return " SET "+" AND ".join([f"{key} = '{value}'" for key, value in zip(keys, values)])

    def get_data_one(self, data):
        try:
            sql = "SELECT * FROM "+self.table+" "+self.generate_where(data)
            # print(sql)
            self._connectMysql()
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            if result is not None:
                return result
        except Exception as e:
            print("An error select data: ", str(e))
        finally:
            self._closeConnect()

    def get_data(self, data):
        try:
            sql = "SELECT * FROM "+self.table+" "+self.generate_where(data)
            # print(sql)
            self._connectMysql()
            self.cursor.execute(sql)

            # 获取结果集
            result = self.cursor.fetchall()
            if result is not None:
                return result
        except Exception as e:
            print("An error select all data: ", str(e))
        finally:
            self._closeConnect()

    def get_data_by_id(self, id):
        sql = "SELECT * FROM {} WHERE id=%s".format(self.table)
        self._connectMysql()
        self.cursor.execute(sql, (id,))
        result = self.cursor.fetchone()
        self._closeConnect()
        if result is not None:
            return result
        print("No data found for the specified product ID.")

    def update_data_one(self, data, where):
        try:
            sql = "UPDATE " + self.table + self.generate_update_set(data) + self.generate_where(where)
            self._connectMysql()
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print("An error occurred while updating data: ", str(e))
        finally:
            self._closeConnect()

    def get_records_starting_with_date(self, date):
        try:
            sql = "SELECT * FROM {} WHERE DATE(created_at) = %s".format(self.table)
            self._connectMysql()
            self.cursor.execute(sql, (date,))
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print("An error occurred while getting records: ", str(e))
        finally:
            self._closeConnect()

    def get_num_starting_with_date(self):
        try:
            sql = "SELECT COUNT(*) FROM {} GROUP BY DATE(created_at)".format(self.table)
            self._connectMysql()
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print("An error occurred while getting records: ", str(e))
        finally:
            self._closeConnect()

    
    def get_date_num_starting_with_date(self):
        try:
            sql = "SELECT DATE_FORMAT(created_at, '%Y-%m-%d'),COUNT(*) FROM {} GROUP BY DATE(created_at)".format(self.table)
            self._connectMysql()
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print("An error occurred while getting records: ", str(e))
        finally:
            self._closeConnect()