# Todo: These methods can be used as a basis for creating a JSON response
class Table:
    @staticmethod
    def create_table(rows, headers):
        col_widths = [len(header) for header in headers]
        for row in rows:
            for i, column in enumerate(row):
                if len(str(column)) > col_widths[i]:
                    col_widths[i] = len(str(column))

        print(Table.make_row(headers, col_widths))
        print(Table.make_underline(col_widths))
        for row in rows:
            print(Table.make_row(row, col_widths))

    @staticmethod
    def make_row(row, col_widths, separator = "|"):
        string = ""
        for i, column in enumerate(row):
            padding = "".join([" " for _ in range(col_widths[i] - len(str(column)) + 2)])
            string += "  " + str(column) + padding + separator
        return string

    @staticmethod
    def make_underline(col_widths):
        underline = ""
        for width in col_widths:
            underline += "".join(["-" for _ in range(width + 5)])
        return underline
