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
        sql = "SELECT tg_id, language, eco_branch_id, fullname, phone, inn, created_at FROM eco_branch_employees"
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

    async def employee_set_language(self, tg_id, language: str) -> None:
        sql = "UPDATE eco_branch_employees SET language = %s WHERE tg_id = %s"
        await self.execute(sql, (language, tg_id))

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

    async def get_eco_branch(self, branch_id):
        sql = """
        SELECT
            eb.id,
            eb.name_uz,
            eb.name_ru,
            eb.address_id,
            eb.location_id,
            eb.start_time,
            eb.end_time,
            eb.working_days,
            eb.information,
            eb.created_at,
            eb.updated_at,
            l.latitude,
            l.longitude
        FROM eco_branches eb
        JOIN locations l ON eb.location_id = l.id
        WHERE eb.id = %s
        """
        return await self.execute(sql, (branch_id,), fetchone=True)

    async def get_branches(self):
        sql = """
        SELECT 
            id,
            name_uz,
            name_ru,
            address_id,
            location_id,
            start_time,
            end_time,
            working_days,
            information,
            created_at,
            updated_at
        FROM eco_branches
        """
        return await self.execute(sql, fetchall=True)

    async def add_branch(self, name_uz, name_ru, location: Location, *args, **kwargs):
        from utils import get_location_details
        await self.add_location(location)  # add new location
        location_id = (await self.get_location_by_coordinates(location))['id']
        address_dict = await get_location_details(location.latitude, location.longitude)
        await self.add_address(**address_dict)  # add new address
        address_id = (await self.get_address_by_datas(**address_dict))['id']
        sql = """
        INSERT INTO eco_branches
        (name, name_uz, name_ru, address_id, location_id, start_time, end_time, working_days, 
        information, information_uz, information_ru, created_at, updated_at)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        await self.execute(sql, (name_uz, name_uz, name_ru, address_id, location_id, None, None, 'all_days',
                                 'N/A', 'N/A', 'N/A', datetime.now(), datetime.now()))

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

    async def add_address(self, country_uz, country_ru, state_uz, state_ru, city_uz, city_ru, county_uz, county_ru,
                          residential_uz, residential_ru, neighbourhood_uz, neighbourhood_ru, road_uz, road_ru,
                          house_number_uz, house_number_ru, amenity_uz, amenity_ru, shop_uz, shop_ru,
                          man_made_uz, man_made_ru, postcode_uz, postcode_ru):
        sql = """
        INSERT INTO addresses
        (country, country_uz, country_ru, state, state_uz, state_ru, city, city_uz, city_ru, 
        county, county_uz, county_ru, residential, residential_uz, residential_ru, neighbourhood, neighbourhood_uz, neighbourhood_ru, 
        road, road_uz, road_ru, house_number, house_number_uz, house_number_ru, amenity, amenity_uz, amenity_ru, 
        shop, shop_uz, shop_ru, man_made, man_made_uz, man_made_ru, postcode, postcode_uz, postcode_ru)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        await self.execute(sql,
                           (country_uz, country_uz, country_ru, state_uz, state_uz, state_ru, city_uz, city_uz, city_ru,
                            county_uz, county_uz, county_ru, residential_uz, residential_uz, residential_ru,
                            neighbourhood_uz, neighbourhood_uz, neighbourhood_ru, road_uz, road_uz, road_ru,
                            house_number_uz, house_number_uz, house_number_ru, amenity_uz,
                            amenity_uz, amenity_ru, shop_uz, shop_uz, shop_ru, man_made_uz, man_made_uz, man_made_ru,
                            postcode_uz, postcode_uz, postcode_ru))

    async def get_address_by_datas(self, country_uz, state_uz, city_uz, county_uz, residential_uz, neighbourhood_uz,
                                   road_uz, house_number_uz, amenity_uz, shop_uz, man_made_uz, postcode_uz, *args, **kwargs):
        sql = """
        SELECT id, country, state, city, county, residential, neighbourhood, road, house_number, amenity, shop, man_made, postcode
        FROM addresses
        WHERE country = %s AND state = %s AND city = %s AND county = %s AND residential = %s AND neighbourhood = %s
        AND road = %s AND house_number = %s AND amenity = %s AND shop = %s AND man_made = %s AND postcode = %s
        """
        return await self.execute(sql, (
            country_uz, state_uz, city_uz, county_uz, residential_uz, neighbourhood_uz, road_uz, house_number_uz,
            amenity_uz, shop_uz, man_made_uz, postcode_uz), fetchone=True)

    async def add_game(self, game_name_uz, game_name_ru, *args, **kwargs):
        sql = """
        INSERT INTO games
        (name, name_uz, name_ru, description, description_uz, description_ru, start_date, end_date, status, created_at, updated_at)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        await self.execute(sql, (game_name_uz, game_name_uz, game_name_ru, 'N/A', 'N/A', 'N/A', None, None, 'pending', datetime.now(), datetime.now()))

    async def get_active_games(self):
        sql = """
        SELECT id, name_uz, name_ru, description, start_date, end_date, status, created_at, updated_at
        FROM games
        WHERE status = 'active'
        """
        return await self.execute(sql, fetchall=True)

    async def add_qr_code(self, game_id, eco_branch_id, code):
        sql = """
        INSERT INTO qrcodes
        (game_id, eco_branch_id, code, is_active, activity_time, created_at, updated_at)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s)
        """
        await self.execute(sql, (game_id, eco_branch_id, code, True, 5, datetime.now(), datetime.now()))

    async def check_qr_code(self, code):
        sql = """
        SELECT id, game_id, eco_branch_id, code, is_active, activity_time, created_at, updated_at
        FROM qrcodes
        WHERE code = %s
        """
        return await self.execute(sql, (code,), fetchone=True)

    async def get_participant(self, tg_id):
        sql = """
        SELECT tg_id, language, fullname, phone, created_at, updated_at
        FROM participants
        WHERE tg_id = %s
        """
        return await self.execute(sql, (tg_id,), fetchone=True)

    async def add_participant(self, tg_id, language, fullname, phone, *args, **kwargs):
        sql = """
        INSERT INTO participants
        (tg_id, language, fullname, phone, created_at, updated_at)
        VALUES
        (%s, %s, %s, %s, %s, %s)
        """
        await self.execute(sql, (tg_id, language, fullname, phone, datetime.now(), datetime.now()))

    async def participant_set_language(self, tg_id, language: str) -> None:
        sql = "UPDATE participants SET language = %s WHERE tg_id = %s"
        await self.execute(sql, (language, tg_id))

    async def participant_set_fullname(self, tg_id, fullname: str) -> None:
        sql = "UPDATE participants SET fullname = %s WHERE tg_id = %s"
        await self.execute(sql, (fullname, tg_id))

    async def get_participant_points(self, tg_id):
        sql = """
        SELECT COUNT(*) AS number FROM participants WHERE suggested_id = %s
        """
        return await self.execute(sql, (tg_id,), fetchone=True)

    async def get_participant_qr_codes(self, tg_id):
        sql = """
        SELECT 
            q.id, 
            q.participant_id, 
            q.qrcode_id, 
            q.location_id, 
            q.winner, 
            q.created_at, 
            q.updated_at, 
            p.fullname,
            v.code  -- QR kod qiymatini qo'shish
        FROM registered_qrcodes q
        JOIN participants p ON q.participant_id = p.tg_id
        JOIN qrcodes v ON q.qrcode_id = v.id  -- QR kod qiymatlarini olish
        WHERE q.participant_id = %s
        """
        return await self.execute(sql, (tg_id,), fetchall=True)

    async def get_registered_qr_code(self, qrcode_id):
        sql = """
        SELECT 
            q.id, 
            q.participant_id, 
            q.qrcode_id, 
            q.location_id, 
            q.winner, 
            q.created_at, 
            q.updated_at, 
            p.fullname 
        FROM registered_qrcodes q
        JOIN participants p ON q.participant_id = p.tg_id
        WHERE q.qrcode_id = %s
        """
        return await self.execute(sql, (qrcode_id,), fetchone=True)

    async def add_registered_qrcode(self, participant_id, qrcode_id, location_id):
        sql = """
        INSERT INTO registered_qrcodes
        (participant_id, qrcode_id, location_id, winner, created_at, updated_at)
        VALUES
        (%s, %s, %s, %s, %s, %s)
        """
        await self.execute(sql, (participant_id, qrcode_id, location_id, False, datetime.now(), datetime.now()))

    async def update_active_qr_code(self, qrcode_id):
        sql = """
        UPDATE qrcodes SET is_active = FALSE WHERE id = %s
        """
        await self.execute(sql, (qrcode_id,))

    async def get_game_info(self):
        sql = """
        SELECT id, title_uz, title_ru, description_uz, description_ru, image_url
        FROM game_infos
        ORDER BY id DESC
        """
        return await self.execute(sql, fetchone=True)
