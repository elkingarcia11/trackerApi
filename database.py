import psycopg2
from psycopg2.extras import RealDictCursor
from config import settings

conn = psycopg2.connect(host=settings.DATABASE_HOSTNAME, database=settings.DATABASE_NAME, user=settings.DATABASE_USERNAME, password=settings.DATABASE_PASSWORD, cursor_factory=RealDictCursor)
cursor = conn.cursor()