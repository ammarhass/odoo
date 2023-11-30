from odoo import models



class StudentreportXlsx(models.AbstractModel):
    _name = 'report.iti.report_student_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, students):
        print("students", students)
        row = 0
        col = 0
        # sheet = workbook.add_worksheet('student ID card')
        # bold = workbook.add_format({'bold': True})
        # sheet.set_column('A:B', 15)
        for obj in students:
            sheet = workbook.add_worksheet('student ID card')
            bold = workbook.add_format({'bold': True})
            sheet.set_column('A:B', 15)
            # report_name = obj.name
            # One sheet by partner
            sheet.write(row, col, 'Name', bold)
            sheet.write(row, col+1, obj.name, bold)
            sheet.write(row+1, col, 'Email', bold)
            sheet.write(row+1, col+1, obj.email)
            sheet.write(row+2, col, 'Track', bold)
            sheet.write(row+2, col+1, obj.track_id.name , bold)


class EmployeesreportXlsx(models.AbstractModel):
    _name = 'report.iti.report_employees_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, employees):
        print("Employees ", employees)
        bold = workbook.add_format({'bold': True})
        sheet = workbook.add_worksheet('Employees Info'
        row = 0
        col = 0
        sheet.write(row, col, 'Name', bold)
        sheet.write(row, col + 1, 'Email', bold)
        sheet.write(row, col + 2, 'Phone', bold)
        sheet.write(row, col + 3, 'Job Position', bold)

        # print(employees.employees_ids)
        for obj in employees.employees_ids:
            # print(obj)
            row += 1
            sheet.set_column('A:A', 20)
            sheet.set_column('B:B', 35)
            sheet.set_column('C:D', 25)
            sheet.write(row, col, obj.name, bold)
            sheet.write(row, col+1, obj.work_email, bold)
            sheet.write(row, col+2, obj.work_phone, bold)
            sheet.write(row, col+3, obj.job_id.name, bold)