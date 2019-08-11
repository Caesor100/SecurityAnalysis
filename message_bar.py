class MessageBar:
    """Class for displaying a message in the information panel."""
    def __init__(self, bar=None):
        self.bar = bar
        self.dividing_line = '='*40 + '\n'
        self.signal_true = 'command was successful'

    def send_message(self, text):
        """Display information on the dashboard."""
        formatted_text = self.dividing_line + str(text) + '\n' + self.dividing_line + self.bar.toPlainText()
        self.bar.setText(formatted_text)

    def send_block_message(self, *args, ticker=None):
        """Display block information on the dashboard."""
        formatted_text = self.dividing_line
        if ticker:
            formatted_text += 'Company reporting assessment ' + ticker + ':' + '\n\n'
        for text in args:
            formatted_text += '* ' + str(text) + '\n'
        formatted_text += self.dividing_line + self.bar.toPlainText()
        self.bar.setText(formatted_text)

    def clear(self):
        """Clear the dashboard."""
        self.bar.setText('')
