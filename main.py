from site_parser import SiteParser
import pandas as pd
import xlsxwriter
import datetime


now = datetime.datetime.now()


def run_parsing():
    row = 0
    column = 0

    xlsx = pd.ExcelFile(r"brands.xlsx")
    sheetX = xlsx.parse(0)
    brands = sheetX['brand_domain']

    workbook = xlsxwriter.Workbook('result.xlsx')
    worksheet = workbook.add_worksheet()

    for brand in brands:
        brand_domain = "https://" + brand
        parsing = SiteParser(brand_domain)

        if parsing.get_error_message():
            brand_result = parsing.get_error_message()
        else:
            brand_result = parsing.get_font_famliy_list()

        worksheet.write(row, column, f'{brand}')
        worksheet.write(row, column + 1, f'{brand_result}')

        row += 1
        print(datetime.datetime.now() - now)

    print(datetime.datetime.now() - now)
    workbook.close()


run_parsing()

