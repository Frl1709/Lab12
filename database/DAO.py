from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():

    @staticmethod
    def getAllCountry():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT Country
                    FROM go_retailers"""
        cursor.execute(query, )
        for row in cursor:
            result.append(row['Country'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT Date
                   FROM go_sales.go_daily_sales"""
        cursor.execute(query, )
        for row in cursor:
            if row['Date'].year not in result:
                result.append(row['Date'].year)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getRetailer(country):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select *
            from go_retailers
            where Country = %s"""
        cursor.execute(query, (country,))
        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getConnection(country, anno):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select rc1, rc2, pn1 pn, COUNT(distinct(pn1)) as weight
        from (select gr1.Retailer_code rc1, gds1.Product_number pn1
                from go_retailers gr1, go_daily_sales gds1
                where gr1.Retailer_code = gds1.Retailer_code and EXTRACT(year from gds1.`Date`) = %s and gr1.Country = %s) t1,
            (select gr2.Retailer_code rc2, gds2.Product_number pn2
                from go_retailers gr2, go_daily_sales gds2
                where gr2.Retailer_code = gds2.Retailer_code and EXTRACT(year from gds2.`Date`) = %s and gr2.Country = %s) t2
        where rc1 < rc2 and pn1 = pn2
        GROUP BY t1.rc1, t2.rc2"""
        cursor.execute(query, (anno, country,anno, country,))
        for row in cursor:
            result.append((row['rc1'],
                           row['rc2'],
                           row['pn'],
                           row['weight']))

        cursor.close()
        conn.close()
        return result

