import aiomysql

DATABASE_CONFIG = {
    'host': '192.168.0.17',   
    'port': 3306,
    'user': 'gym_root',      
    'password': 'Teletrabajo88',
    'db': 'gymsport'
}

pool = None  

# Función para inicializar el pool de conexiones
async def init_db_pool():
    global pool
    pool = await aiomysql.create_pool(
        host=DATABASE_CONFIG['host'],
        port=DATABASE_CONFIG['port'],
        user=DATABASE_CONFIG['user'],
        password=DATABASE_CONFIG['password'],
        db=DATABASE_CONFIG['db'],
        minsize=1,  
        maxsize=10  
    )

# Función para obtener la conexión a la base de datos desde el pool
async def get_db():
    global pool
    conn = await pool.acquire()  # Obtiene una conexión del pool
    try:
        yield conn  # Devuelve la conexión
    finally:
        await pool.release(conn)  # Libera la conexión al pool

# Función para cerrar el pool de conexiones
async def close_db_pool():
    global pool
    pool.close()
    await pool.wait_closed()
