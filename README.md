# Vorlage zur Erstellung einer Diplomarbeit in LaTeX für die HTL Dornbirn.
Sie basiert auf der Vorlage für Diplomarbeiten und Dissertationen der TU Wien und enthält unterschiedliche nützliche Packages, die für eine Diplomarbeit nützlich sind.

## Kurz zu LaTeX
LaTeX ist ein Textsatzsystem, das speziell für das Setzen wissenschaftlicher und technischer Dokumente entwickelt wurde. Im Gegensatz zu WYSIWYG (What You See Is What You Get)-Editoren wie Word, zeigt LaTeX den fertigen Text nicht direkt an. Stattdessen wird der Quellcode kompiliert, um das fertige Dokument zu erzeugen. Der Text wird in Textdateien mit der Endung .tex geschrieben und muss dann kompiliert werden, um das endgültige Dokument, meist im PDF-Format, zu erzeugen.

### Wichtige Konzepte
- LaTeX-Dokumente können sehr umfangreich und komplex werden, daher ist es oft sinnvoll, das Dokument in mehrere Dateien aufzuteilen. Es gibt dann ein Hauptdokument, das die die Hauptstruktur und grundlegende Inhalte enthält. Kapitel oder Abschnitte können dann in separate Dateien geschrieben und in das Hauptdokument eingebunden werden. Auch die Bibliographie wird oft in einer separaten Datei geführt.
- LaTeX-Befehle beginnen mit einem Backslash (\). Beispiele sind \documentclass, \usepackage, \begin, \end, \section, \title, etc.
- Umgebungen werden mit \begin{} und \end{} definiert und umschließen Blöcke von Text oder anderen Inhalten, z.B. \begin{document}...\end{document}, \begin{equation}...\end{equation}.
- Pakete: Erweiterungen, die zusätzliche Funktionen bieten. Sie werden mit \usepackage{} bzw. \RequirePackage{} (in der .sty-Datei) eingebunden.

### Die inkludierten Packages


## Die Aufsetzung
### LaTeX Distribution und Editor
Zur Bearbeitung des Dokuments würde ich eine dieser zwei folgenden Methoden empfehlen:
- Lokal auf dem eigenen PC mit der LaTeX Distribution MikTex (https://miktex.org/download), da diese sehr leichtgewichtig ist und TeXstudio (https://www.texstudio.org/) als Editor. Dabei können aber auch andere Distributionen wie TeX Live sowie andere Editoren verwendet werden.
- Im Browser über Overleaf (https://www.overleaf.com): Dies ist die "einfachste" Methode, allerdings ist für eine GitHub Verbindung ein Abo notwendig ist, das sich aber für die wenigen Monate auszahlt.

### Das Dokument
1. Dieses Git Repository auf ein eigenes Repo clonen.
2. Im Editor (z.B. TeXstudio) das Hauptdokument (WI_DA_LaTeX_Template.tex) öffnen und in TeXstudio mit rechtsklick auf das Dokument als explizites Root-Dokument setzen. So kann man, egal in welchem Dokument man sich befindet, immer einfach compilen ohne zuerst auf das richtige Dokument gehen zu müssen.
![grafik](https://github.com/user-attachments/assets/058be2d6-2eba-43f5-b627-717aca496da4)
3. Die Grundschritte sind nun erledigt. Allerdings nutzt die Vorlage mehrere Packages, die noch extra Schritte benötigen, um compiliert zu werden:
