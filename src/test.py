import sys, os
from PyQt5 import Qsci
from PyQt5.QtWidgets import QApplication

class Window(Qsci.QsciScintilla):
    def __init__(self):
        Qsci.QsciScintilla.__init__(self)
        self.lexers = {
            'py': Qsci.QsciLexerPython,
            'html': Qsci.QsciLexerHTML,
            'xml': Qsci.QsciLexerXML,
            'css': Qsci.QsciLexerCSS,
            'js': Qsci.QsciLexerJavaScript,
            'sql': Qsci.QsciLexerSQL,
            'cpp': Qsci.QsciLexerCPP,
            'java': Qsci.QsciLexerJava,
            'cs': Qsci.QsciLexerCSharp,
            'json': Qsci.QsciLexerJSON,
            'perl': Qsci.QsciLexerPerl,
            'rb': Qsci.QsciLexerRuby,
            'lua': Qsci.QsciLexerLua,
            'makefile': Qsci.QsciLexerMakefile,
            'bash': Qsci.QsciLexerBash,
            'properties': Qsci.QsciLexerProperties,
            'pascal': Qsci.QsciLexerPascal,
            'postscript': Qsci.QsciLexerPostScript,
            'yml': Qsci.QsciLexerYAML,
            'fortran': Qsci.QsciLexerFortran,
            'md': Qsci.QsciLexerMarkdown,
        }

        self.initlexers()
        self.setText(open(os.path.abspath(sys.argv[1])).read())
    
    def initlexers(self):
        for lexer in self.lexers:
            if (
                sys.argv[1].split('.')[-1] == lexer
                and self.lexers[lexer] is not None
            ):
                self.setLexer(self.lexers.get(lexer)(self))
                break


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    window.setGeometry(500, 300, 500, 500)
    window.show()
    sys.exit(app.exec_())