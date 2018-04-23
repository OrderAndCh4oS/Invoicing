
class Style:
    @staticmethod
    def create_title(title):
        return "\n" + title + "\n" + Style.create_underline(title)

    @staticmethod
    def create_underline(title):
        return "".join(['-' for _ in range(len(title))])