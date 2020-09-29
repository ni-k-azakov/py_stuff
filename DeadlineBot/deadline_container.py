class DeadlineContainer:
    def __init__(self):
        self._deadlines = []

    def set_deadline(self, deadline):
        self._deadlines.append(deadline)

    def get_deadlines(self):
        output = ""
        for deadline in self._deadlines:
            output += deadline + '\n'
        return output
