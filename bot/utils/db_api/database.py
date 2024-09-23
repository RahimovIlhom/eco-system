from datetime import datetime

import aiomysql
import pytz
from aiogram.types import Location
from environs import Env

from utils.misc.crypto_encryption import encrypt_data

env = Env()
env.read_env()

tashkent_tz = pytz.timezone('Asia/Tashkent')


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
        sql = ("SELECT employees.tg_id, employees.language, employees.eco_branch_id, employees.fullname, employees.phone, employees.inn, employees.created_at "
               "FROM eco_branch_employees AS employees")
        return await self.execute(sql, fetchall=True)

    async def get_employees_by_branch(self, eco_branch_id) -> tuple:
        sql = ("SELECT employees.tg_id, employees.fullname, employees.phone "
               "FROM eco_branch_employees AS employees "
               "WHERE employees.eco_branch_id = %s")
        return await self.execute(sql, (eco_branch_id,), fetchall=True)

    async def get_employee(self, tg_id) -> dict:
        sql = """
            SELECT 
                employees.tg_id, 
                employees.language, 
                employees.eco_branch_id, 
                employees.fullname, 
                employees.phone, 
                employees.inn, 
                employees.created_at,
                branches.name AS branch_name,
                branches.phone AS branch_phone,
                branches.is_active AS branch_is_active,
                branches.activity_time AS branch_activity_time
            FROM eco_branch_employees AS employees
            LEFT JOIN eco_branches AS branches ON employees.eco_branch_id = branches.id
            WHERE employees.tg_id = %s
        """
        return await self.execute(sql, (tg_id,), fetchone=True)

    async def get_employees_by_eco_branch(self, eco_branch_id) -> tuple:
        sql = ("SELECT employees.tg_id AS chat_id, employees.language AS lang "
               "FROM eco_branch_employees AS employees "
               "WHERE employees.eco_branch_id = %s")
        return await self.execute(sql, (eco_branch_id,), fetchall=True)

    async def add_employee(self, tg_id, eco_branch_id, fullname, phone, language='uz', *args, **kwargs) -> str:
        # Check if the employee already exists
        employee = await self.get_employee(tg_id)

        current_time = datetime.now(tz=tashkent_tz)

        if employee:
            # Directly update the eco_branch_id if the employee exists
            sql = "UPDATE eco_branch_employees SET eco_branch_id = %s, fullname = %s, updated_at = %s WHERE tg_id = %s;"
            await self.execute(sql, (eco_branch_id, fullname, current_time, tg_id))
            return "updated"
        else:
            # Insert a new employee
            sql = ("INSERT INTO eco_branch_employees "
                   "(tg_id, language, eco_branch_id, fullname, phone, created_at, updated_at, inn) "
                   "VALUES "
                   "(%s, %s, %s, %s, %s, %s, %s, %s)")
            await self.execute(sql, (tg_id, language, eco_branch_id, fullname, phone, current_time, current_time, None))
            return "inserted"

    async def remove_employee(self, tg_id) -> None:
        sql = "DELETE FROM eco_branch_employees WHERE tg_id = %s"
        await self.execute(sql, (tg_id,))

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
            eb.chief_name,
            eb.phone,
            eb.address_id,
            eb.location_id,
            eb.start_time,
            eb.end_time,
            eb.working_days,
            eb.information,
            eb.created_at,
            eb.updated_at,
            eb.is_active,
            eb.activity_time,
            l.latitude,
            l.longitude,
            a.address_uz,
            a.address_ru
        FROM eco_branches eb
        JOIN locations l ON eb.location_id = l.id
        JOIN addresses a ON eb.address_id = a.id
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
            updated_at,
            is_active
        FROM eco_branches
        """
        return await self.execute(sql, fetchall=True)

    async def add_branch(self, name_uz, name_ru, location: Location, phone: str, chief_name: str, *args, **kwargs):
        from utils import get_location_details
        await self.add_location(location)  # add new location
        location_id = (await self.get_location_by_coordinates(location))['id']
        address_dict = await get_location_details(location.latitude, location.longitude)
        await self.add_address(**address_dict)  # add new address
        address_id = (await self.get_address_by_datas(**address_dict))['id']
        sql = """
        INSERT INTO eco_branches
        (name, name_uz, name_ru, chief_name, phone, address_id, location_id, start_time, end_time, working_days, 
        information, information_uz, information_ru, created_at, updated_at, is_active, activity_time)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE, %s)
        """
        next_month = datetime.now(tz=tashkent_tz).month + 1
        await self.execute(sql, (name_uz, name_uz, name_ru, chief_name, phone, address_id, location_id, None, None, 'all_days',
                                 'N/A', 'N/A', 'N/A', datetime.now(tz=tashkent_tz), datetime.now(tz=tashkent_tz),
                                 datetime.now(tz=tashkent_tz).replace(month=next_month)))

    async def update_branch(self, branch_id, name_uz, name_ru, location, phone: str, chief_name: str, *args, **kwargs):
        from utils import get_location_details
        # Yangi joylashuvni qo'shish
        await self.add_location(location)
        location_id = (await self.get_location_by_coordinates(location))['id']

        # Yangi manzilni qo'shish
        address_dict = await get_location_details(location.latitude, location.longitude)
        await self.add_address(**address_dict)
        address_id = (await self.get_address_by_datas(**address_dict))['id']

        # Filial ma'lumotlarini yangilash
        sql = """
        UPDATE eco_branches
        SET name = %s, name_uz = %s, name_ru = %s, chief_name = %s, phone = %s, address_id = %s, location_id = %s, 
            start_time = %s, end_time = %s, working_days = %s, information = %s, information_uz = %s, 
            information_ru = %s, updated_at = %s
        WHERE id = %s
        """
        # Ma'lumotlar bazasiga yangilanish uchun kerakli ma'lumotlarni yuborish
        await self.execute(sql, (name_uz, name_uz, name_ru, chief_name, phone, address_id, location_id, None, None,
                                 'all_days', 'N/A', 'N/A', 'N/A', datetime.now(tz=tashkent_tz), branch_id))

    async def deactivate_eco_branch(self, branch_id):
        sql = "UPDATE eco_branches SET is_active = FALSE WHERE id = %s"
        await self.execute(sql, (branch_id,))

    async def activate_eco_branch(self, branch_id):
        sql = "UPDATE eco_branches SET is_active = TRUE, updated_at = %s, activity_time = %s WHERE id = %s"
        next_month = datetime.now(tz=tashkent_tz).month + 1
        await self.execute(sql, (datetime.now(tz=tashkent_tz), datetime.now(tz=tashkent_tz).replace(month=next_month), branch_id,))

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
                          man_made_uz, man_made_ru, postcode_uz, postcode_ru, address_uz, address_ru, *args, **kwargs):
        sql = """
        INSERT INTO addresses
        (country, country_uz, country_ru, state, state_uz, state_ru, city, city_uz, city_ru, 
        county, county_uz, county_ru, residential, residential_uz, residential_ru, neighbourhood, neighbourhood_uz, neighbourhood_ru, 
        road, road_uz, road_ru, house_number, house_number_uz, house_number_ru, amenity, amenity_uz, amenity_ru, 
        shop, shop_uz, shop_ru, man_made, man_made_uz, man_made_ru, postcode, postcode_uz, postcode_ru, address, address_uz, address_ru)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        await self.execute(sql,
                           (country_uz, country_uz, country_ru, state_uz, state_uz, state_ru, city_uz, city_uz, city_ru,
                            county_uz, county_uz, county_ru, residential_uz, residential_uz, residential_ru,
                            neighbourhood_uz, neighbourhood_uz, neighbourhood_ru, road_uz, road_uz, road_ru,
                            house_number_uz, house_number_uz, house_number_ru, amenity_uz,
                            amenity_uz, amenity_ru, shop_uz, shop_uz, shop_ru, man_made_uz, man_made_uz, man_made_ru,
                            postcode_uz, postcode_uz, postcode_ru, address_uz, address_uz, address_ru))

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
        await self.execute(sql, (game_name_uz, game_name_uz, game_name_ru, 'N/A', 'N/A', 'N/A', None, None, 'pending', datetime.now(tz=tashkent_tz), datetime.now(tz=tashkent_tz)))

    async def get_game(self, id):
        sql = """
        SELECT id, name_uz, name_ru, description_uz, description_ru, start_date, end_date, status
        FROM games
        WHERE id = %s
        """
        return await self.execute(sql, (id, ), fetchone=True)

    async def update_game_status(self, id, status):
        if status == 'active':
            sql = """
            UPDATE games SET status = %s, start_date = %s WHERE id = %s
            """
            await self.execute(sql, (status, datetime.now(tz=tashkent_tz).date(), id))
        elif status == 'completed':
            sql = """
            UPDATE games SET status = %s, end_date = %s WHERE id = %s
            """
            await self.execute(sql, (status, datetime.now(tz=tashkent_tz).date(), id))
        else:
            sql = """
            UPDATE games SET status = %s WHERE id = %s
            """
            await self.execute(sql, (status, id))

    async def get_games(self):
        sql = """
        SELECT id, name_uz, name_ru, status
        FROM games
        """
        return await self.execute(sql, fetchall=True)

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
        await self.execute(sql, (game_id, eco_branch_id, code, True, 5, datetime.now(tz=tashkent_tz), datetime.now(tz=tashkent_tz)))

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

    async def add_participant(self, tg_id, language, fullname, phone, payload=None, *args, **kwargs):
        sql = """
        INSERT INTO participants
        (tg_id, language, fullname, phone, suggested_id, created_at, updated_at)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s)
        """
        await self.execute(sql, (tg_id, language, fullname, phone, payload, datetime.now(tz=tashkent_tz), datetime.now(tz=tashkent_tz)))

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
        await self.execute(sql, (participant_id, qrcode_id, location_id, False, datetime.now(tz=tashkent_tz), datetime.now(tz=tashkent_tz)))

    async def update_active_qr_code(self, qrcode_id):
        sql = """
        UPDATE qrcodes SET is_active = FALSE WHERE id = %s
        """
        await self.execute(sql, (qrcode_id,))

    async def add_game_infos(self, title_uz, title_ru, description_uz, description_ru, image_url, *args, **kwargs):
        sql = """
        INSERT INTO game_infos
        (title, title_uz, title_ru, description, description_uz, description_ru, image_url)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s)
        """
        await self.execute(sql, (title_uz, title_uz, title_ru, description_uz, description_uz, description_ru, image_url))

    async def get_game_info(self):
        sql = """
        SELECT id, title_uz, title_ru, description_uz, description_ru, image_url
        FROM game_infos
        ORDER BY id DESC
        """
        return await self.execute(sql, fetchone=True)

    async def add_plastic_card(self, tg_id, card_type, card_number, *args, **kwargs):
        card_number = await encrypt_data(card_number)
        if await self.get_plastic_card(tg_id):
            sql = """
            UPDATE plastic_cards
            SET card_type = %s, card_number = %s, updated_at = %s
            WHERE participant_id = %s
            """
            await self.execute(sql, (card_type, card_number, datetime.now(tz=tashkent_tz), tg_id))
        else:
            sql = """
            INSERT INTO plastic_cards
            (participant_id, card_type, card_number, created_at, updated_at)
            VALUES
            (%s, %s, %s, %s, %s)
            """
            await self.execute(sql, (tg_id, card_type, card_number, datetime.now(tz=tashkent_tz), datetime.now(tz=tashkent_tz)))

    async def get_plastic_card(self, tg_id):
        sql = """
        SELECT card_type, card_number, created_at, updated_at FROM plastic_cards WHERE participant_id = %s
        """
        return await self.execute(sql, (tg_id,), fetchone=True)

    async def remove_plastic_card(self, tg_id):
        sql = """
        DELETE FROM plastic_cards WHERE participant_id = %s
        """
        await self.execute(sql, (tg_id,))
