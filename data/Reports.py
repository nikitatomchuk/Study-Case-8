from data.Report import Report


class Reports:

    def __init__(self):
        self.__reports = {}

    def add(self, report: Report):
        self.__reports.update({report.get_report_date(): report})

    def get_all_reports(self):
        return self.__reports.values()

    def print_all_reports(self):
        for report in self.__reports:
            print(report)