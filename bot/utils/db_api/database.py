from datetime import datetime

import aiomysql
from aiogram.types import Location
from environs import Env

env = Env()
env.read_env()


class Database:

    def __init__(self):
        self.pool = None

    async def create(self):
        if not self.pool:
            self.pool = await aiomysql.create_pool(
                host=env.str('MYSQL_DB_HOST'),
                port=env.int('MYSQL_DB_PORT'),
                user=env.str('MYSQL_DB_USER'),
                password=env.str('MYSQL_DB_PASSWORD'),
                db=env.str('MYSQL_DB_NAME'),
                autocommit=True,
                charset='utf8mb4',
            )

    async def close(self):
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            self.pool = None

    async def execute(self, query: str, args: tuple = (), fetchone: bool = False, fetchall: bool = False):
        async with self.pool.acquire() as connection:
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, args)
                if fetchone:
                    result = await cursor.fetchone()
                    return dict(result) if result else None
                if fetchall:
                    result = await cursor.fetchall()
                    return tuple(dict(row) for row in result) if result else ()

    async def get_employees(self) -> tuple:
        sql = "SELECT tg_id, language, eco_branch, fullname, phone, inn, created_at FROM eco_branch_employees"
        return await self.execute(sql, fetchall=True)

    async def get_employee(self, tg_id) -> dict:
        sql = ("SELECT tg_id, language, eco_branch_id, fullname, phone, inn, created_at "
               "FROM eco_branch_employees WHERE tg_id = %s")
        return await self.execute(sql, (tg_id,), fetchone=True)

    async def add_employee(self, tg_id, eco_branch_id, fullname, phone, *args, **kwargs) -> None:
        sql = ("INSERT INTO eco_branch_employees "
               "(tg_id, language, eco_branch_id, fullname, phone, created_at, updated_at, inn) "
               "VALUES "
               "(%s, %s, %s, %s, %s, %s, %s, %s)")
        await self.execute(sql, (tg_id, 'uz', eco_branch_id, fullname, phone,
                                 datetime.now(), datetime.now(), None))

    async def admin_get_language(self, tg_id) -> dict:
        sql = "SELECT language FROM admins WHERE tg_id = %s"
        return await self.execute(sql, (tg_id,), fetchone=True)

    async def admin_set_language(self, tg_id, language: str) -> None:
        if not await self.admin_get_language(tg_id):
            sql = "INSERT INTO admins (tg_id, language) VALUES (%s, %s)"
            await self.execute(sql, (tg_id, language))
        else:
            sql = "UPDATE admins SET language = %s WHERE tg_id = %s"
            await self.execute(sql, (language, tg_id))

    async def get_branches(self):
        sql = """
        SELECT 
            id,
            name,
            start_time,
            end_time,
            working_days,
            information,
            created_at,
            updated_at
        FROM eco_branches
        """
        return await self.execute(sql, fetchall=True)

    async def add_branch(self, name, location: Location, *args, **kwargs):
        from utils import get_location_details
        await self.add_location(location)  # add new location
        location_id = (await self.get_location_by_coordinates(location))['id']
        address_dict = await get_location_details(location.latitude, location.longitude)
        await self.add_address(**address_dict)  # add new address
        address_id = (await self.get_address_by_datas(**address_dict))['id']
        sql = """
        INSERT INTO eco_branches
        (name, address_id, location_id, start_time, end_time, working_days, information, created_at, updated_at)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        await self.execute(sql, (name, address_id, location_id, None, None, 'all_days', None, datetime.now(), datetime.now()))

    async def add_location(self, location: Location):
        sql = """
        INSERT INTO locations
        (latitude, longitude)
        VALUES
        (%s, %s)
        """
        await self.execute(sql, (location.latitude, location.longitude))

    async def get_location_by_coordinates(self, location: Location):
        sql = """
        SELECT id, latitude, longitude FROM locations
        WHERE latitude = %s AND longitude = %s
        """
        return await self.execute(sql, (location.latitude, location.longitude), fetchone=True)

    async def add_address(self, country, state, city, county, residential, neighbourhood, road, house_number, amenity, shop, man_made, postcode):
        sql = """
        INSERT INTO addresses
        (country, state, city, county, residential, neighbourhood, road, house_number, amenity, shop, man_made, postcode)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        await self.execute(sql, (country, state, city, county, residential, neighbourhood, road, house_number, amenity, shop, man_made, postcode))

    async def get_address_by_datas(self, country, state, city, county, residential, neighbourhood, road, house_number, amenity, shop, man_made, postcode):
        sql = """
        SELECT id, country, state, city, county, residential, neighbourhood, road, house_number, amenity, shop, man_made, postcode
        FROM addresses
        WHERE country = %s AND state = %s AND city = %s AND county = %s AND residential = %s AND neighbourhood = %s
        AND road = %s AND house_number = %s AND amenity = %s AND shop = %s AND man_made = %s AND postcode = %s
        """
        return await self.execute(sql, (country, state, city, county, residential, neighbourhood, road, house_number, amenity, shop, man_made, postcode), fetchone=True)






























