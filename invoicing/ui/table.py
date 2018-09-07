from ansi_colours import AnsiColours as Colour


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
            print(Table.make_row(row, col_widths, has_key=True))

    @staticmethod
    def make_row(row, col_widths, separator="|", has_key=False):
        string = ""
        for i, column in enumerate(row):
            data = str(column)
            if i is 0 and has_key:
                data = Colour.green(data)
            padding = "".join([" " for _ in range(col_widths[i] - len(str(column)) + 2)])
            string += "  " + data + padding + Colour.light_grey(separator)
        return string

    @staticmethod
    def make_underline(col_widths):
        underline = ""
        for width in col_widths:
            underline += "".join(["-" for _ in range(width + 5)])
        return Colour.light_grey(underline)
