# BITTE UNBEDINGT DURCHLESEN

# Vorlage zur Erstellung einer Diplomarbeit in LaTeX an der HTL Dornbirn
Sie basiert auf der Vorlage für Diplomarbeiten und Dissertationen der TU Wien und enthält unterschiedliche nützliche Packages, die für eine Diplomarbeit nützlich sind.

## Kurz zu LaTeX
LaTeX ist ein Textsatzsystem, das speziell für das Setzen wissenschaftlicher und technischer Dokumente entwickelt wurde. Im Gegensatz zu WYSIWYG (What You See Is What You Get)-Editoren wie Word, zeigt LaTeX den fertigen Text nicht direkt an. Stattdessen wird der Quellcode kompiliert, um das fertige Dokument zu erzeugen. Der Text wird in Textdateien mit der Endung .tex geschrieben und muss dann kompiliert werden, um das endgültige Dokument, meist im PDF-Format, zu erzeugen.

### Wichtige Konzepte
- LaTeX-Dokumente können sehr umfangreich und komplex werden, daher ist es oft sinnvoll, das Dokument in mehrere Dateien aufzuteilen. Es gibt dann ein Hauptdokument, das die die Hauptstruktur und grundlegende Inhalte enthält. Kapitel oder Abschnitte können dann in separate Dateien geschrieben und in das Hauptdokument eingebunden werden. Auch die Bibliographie wird oft in einer separaten Datei geführt. Das Deckblatt wird in dieser Vorlage in der .sty-Datei definiert.
- LaTeX-Befehle beginnen mit einem Backslash (\). Beispiele sind \documentclass, \usepackage, \begin, \end, \section, \title, etc.
- Umgebungen werden mit \begin{} und \end{} definiert und umschließen Blöcke von Text oder anderen Inhalten, z.B. \begin{document}...\end{document}, \begin{equation}...\end{equation}.
- Pakete: Erweiterungen, die zusätzliche Funktionen bieten. Sie werden mit \usepackage{} bzw. \RequirePackage{} (in der .sty-Datei) eingebunden.

### Die inkludierten Packages
Da die Vorlage sehr viele Packages beinhält, werden hier nur kurz die beschrieben, die bei der Nutzung am öftesten aufkommen. Manche Packages sind optional. Wenn man sie also nicht benutzen will, sollte man ihr \RequirePackage{} aus der .sty-Datei löschen.
- Minted: Dieses Package dient dazu schöne Codeblöcke einzubinden. Alternativ können Plugins für z.B. VS Code bentzt werden, die dann als Bilder eingebunden werden. Zur Nutzung dieses Packages ist es wichtig, dass "Pygments" funktioniert, was man mit "pygmentize -V" in der Konsole testen kann. Falles man irgendwelche Fehler bezüglich "pygmentize" und PATH-Variable bekommt, lässt sich das Problem am einfachsten durch die Neuinstallation von Python beheben, wobei unbedingt die automatische Erstellung der PATH-Variable angehakt werden muss!
- Acronyms: Dieses Package ist sehr einfach und wird verwendet, um Akronyme bzw. Abkürzungsverzeichnisse zu erstellen. Die Nutzung von diesem Package in Kombination mit Glossaries ist riskant, da man NIE dieselben Bezeichungen für Acronyms und Glossaries Akronyme und Glossarbegriffe verwenden darf!
- Glossaries: Das Paket wird benötigt, wenn man ein Glossar erstellen will. Es kann aber auch Abkürzungsverzeichnisse bzw. Akronyme erstellen und somit das Acronyms Package ersetzen. Zur Nutzung dieses Packages wird aber Perl benötigt, was auf Linux Systemen meist vorinstalliert ist. Auf Windows muss man [Strawberry Perl](https://strawberryperl.com/) herunterladen. Außerdem muss das Glossar immer separat noch compiled werden, was man in Overleaf automatisch geschieht und in TeXstudio auch konfiguriert werden kann (siehe https://www.dickimaw-books.com/latex/buildglossaries/#texstudio)

Alle Packages haben immer bestimmte Befehle, um bestimmte Funktionen auszuführen. Da es aber so viele sind, ist es am einfachsten, wenn man sich einfach die Vorlage etwas anschaut und selbst herumprobiert.

## Die Aufsetzung
### LaTeX Distribution und Editor
Zur Bearbeitung des Dokuments würde ich eine dieser zwei folgenden Methoden empfehlen:
- Lokal auf dem eigenen PC mit der LaTeX Distribution [MikTex](https://miktex.org/download), da diese sehr leichtgewichtig ist und [TeXstudio](https://www.texstudio.org/) als Editor. Dabei können aber auch andere Distributionen wie TeX Live sowie andere Editoren verwendet werden.
- Im Browser über [Overleaf](https://www.overleaf.com): Dies ist die "einfachste" Methode, allerdings ist für eine GitHub Verbindung ein Abo notwendig ist, das sich aber für die wenigen Monate auszahlt.

### Das Dokument
1. Dieses Git Repository auf ein eigenes Repo clonen.
2. Im Editor (z.B. TeXstudio) das Hauptdokument (WI_DA_LaTeX_Template.tex) öffnen und in TeXstudio mit rechtsklick auf das Dokument als explizites Root-Dokument setzen. So kann man, egal in welchem Dokument man sich befindet, immer einfach compilen ohne zuerst auf das richtige Dokument gehen zu müssen.

![grafik](https://github.com/user-attachments/assets/058be2d6-2eba-43f5-b627-717aca496da4)

3. Wenn man nun alle Schritte zum Aufsetzen des Dokuments und der einzelnen Packages erledigt hat, sollte man das Dokument kompilieren können und eine PDF daraus bekommen.
