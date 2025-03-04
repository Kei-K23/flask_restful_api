from db import create_connection

class ItemModel:
    def __init__(self, _id, name ,price, owner_id):
        self.id = _id
        self.name = name
        self.price = price
        self.owner_id = owner_id
    
    @classmethod
    def find_by_username(cls, name):
        conn = create_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        conn.close()
        if row:
            return cls(*row)
    
    @classmethod
    def find_by_id(cls, id):
        conn = create_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM items WHERE id=?"
        result = cursor.execute(query, (id,))
        row = result.fetchone()
        conn.close()
        if row:
            return cls(*row)

    @classmethod
    def find_all(cls, name):
        conn = create_connection()
        cursor = conn.cursor()
        
        if name:
            query = "SELECT * FROM items WHERE name LIKE ?"
            # Include the '%' wildcard in the parameter value
            result = cursor.execute(query, (f"%{name}%",))
        else:
            query = "SELECT * FROM items"
            result = cursor.execute(query)
        
        rows = result.fetchall()
        conn.close()
        return [cls(*row) for row in rows]

    @classmethod
    def update(cls, name, price, id, user_id):
        conn = create_connection()
        cursor = conn.cursor()
        query = "UPDATE items SET name = ?, price = ? WHERE id = ? AND owner_id = ?"
        cursor.execute(query, (name, price, id, user_id,))
        conn.commit()
        conn.close()
        
    @classmethod
    def delete(cls, id, user_id):
        conn = create_connection()
        cursor = conn.cursor()
        query = "DELETE FROM items WHERE id = ? AND owner_id = ?"
        cursor.execute(query, (id, user_id,))
        conn.commit()
        conn.close()
    
    def save_to_db(self):
        conn = create_connection()
        cursor = conn.cursor()
        query = "INSERT INTO items (name, price, owner_id) VALUES (?, ?, ?)"
        cursor.execute(query, (self.name, self.price, self.owner_id,))
        conn.commit()
        conn.close()
