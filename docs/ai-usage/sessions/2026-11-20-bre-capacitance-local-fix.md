# BRE-Kapazitätsfix: Vorbereitung und Freigabe zur Veröffentlichung

## Ursprüngliche lokale Vorbereitung

Der folgende Abschnitt dokumentiert den zunächst auf lokale Änderungen
beschränkten Auftrag. Die spätere Freigabe steht im nächsten Abschnitt.

- 20.11.2026, Codex; genaue Modellkennung nicht ermittelt.
- Nutzerauftrag: BRE-Reparatur in beiden lokalen Ordnern, Commit und Push
  zunächst ausschließlich im MZA-Repository. Dieses DIBS-Repository bleibt
  ausdrücklich uncommitted und ungepusht.
- Sauberer Ausgang master `c6d69e4f39bfb8e8c3af6cddefb232aaeea30eed`;
  Status, Branch und Origin geprüft. Lokaler Branch `fix/bre-capacitance-translation`.
- Fehlenden Code→Klasse-Aufruf ergänzt, vollständige Übersetzung vor dem
  CSV-Export geprüft und int64-Ausgabe festgelegt. Öffentlichen pandas.errors-
  Warnklassenimport verwendet. Keine Gebäude-/Profilparameter geändert.
- Identische Kapazitätsreparatur wie im MZA-Pendant; dieses DIBS-Skript war
  bereits echtes Python und benötigte keine HTML-Wiederherstellung.
- Sieben Tests am wirklichen Kapazitätsblock/Export erfolgreich mit Python
  3.11.18, pandas 2.2.1 und NumPy 1.26.4; beobachtete Laufzeit 0,115 s.
  Alle 19 Codevarianten, ungültige/fehlende Werte, numerische Codes, CSV-
  Rücklesen und künftiges pandas-Replace-Verhalten geprüft. Syntax gültig.
- README, lokale Reparaturdokumentation, Testcode und Prüfungszusammenfassung
  ergänzt. Kein vollständiger privater Rohdatenlauf oder Gebäudesimulationslauf.
- Bekannte pandas-FutureWarning; kein Abhängigkeitsupgrade und keine Änderung
  installierter PyPI-Pakete. MZA-Integration ist ein separater Schritt.
- Menschliche Prüfung offen. Kein Commit, kein Push, keine Historyänderung
  dieses Repositories. Nach Nutzerprüfung des MZA-Pendants weiterentscheiden.

## Anschließender Nutzerauftrag vom 20.11.2026

- Commit und Push jetzt auch für DIBS autorisiert, zunächst auf einem
  Reparaturbranch. README ausdrücklich nicht ändern oder mit veröffentlichen.
- Bereits vorbereiteter Branch `fix/bre-capacitance-translation` verwendet;
  Ausgangs-HEAD weiterhin `c6d69e4f39bfb8e8c3af6cddefb232aaeea30eed`.
  Status/Branch/Origin geprüft und origin/master aktualisiert, unverändert.
- Ausschließlich die zuvor von Codex ergänzte README-Passage zurückgenommen.
  README ist gegenüber HEAD unverändert und wird nicht vorgemerkt.
- Separate frühere Reparaturbeschreibung entfernt; die fachliche Erklärung
  kommt in Commit und Pull-Request-Beschreibung. AI-Traceability und bestehende
  maschinenlesbare/Test-Nachweise bleiben als Prüfungsdokumentation erhalten.
- Keine Änderung am bereits getesteten Code oder Testskript. SHA-256 beider
  Dateien gegen docs/validation/environment.json bestätigt: sieben erfolgreiche
  Regressionstests gelten für genau diese Fassung. Kein erneuter Rohdatenlauf.
- Pull Request gegen master zur Prüfung vorgesehen, kein Merge in diesem
  Auftrag. Die ursprüngliche README wird auch im Branchvergleich ausgeschlossen.
- Finaler Commit/Push und PR-Link erst nach erfolgreicher Ausführung berichten.
  Commitzuordnung über Verlauf dieser Sessiondatei und AI-Usage-Session-Footer.

## Tatsächlich veröffentlicht

- Codecommit `97a3486930d12e5a5a5a0676e0b258f6d972526d` erstellt und auf
  `origin/fix/bre-capacitance-translation` gepusht.
- Draft-PR https://github.com/IWUGERMANY/DIBS---Dynamic-ISO-Building-Simulator/pull/13
  gegen master erstellt. Fehler, Beispiel, Änderung, Prüfung, Grenzen und
  Rücknahme stehen in der PR-Beschreibung. Kein Merge ausgeführt.
- README gegenüber origin/master unverändert; zusätzlich Remote-PR-Dateiliste
  geprüft: README und separate Reparaturübersicht sind nicht Bestandteil des PR.
- Sechs vorgemerkte Dateien, Whitespace-Prüfung bestanden, ausgewählte bekannte
  Secret-Präfixe ohne Treffer. Code-/Testhashes entsprechen den sieben erfolgreich
  ausgeführten Regressionstests. Arbeitsordner nach Code-Push sauber.
- Dieser Publikationsnachtrag ändert weder Code noch Tests oder README.

## Nutzerfreigabe zum Merge

- Nutzer beauftragt anschließend den Merge des Reparaturbranches in den
  Hauptbranch. Das GitHub-Repository verwendet `master` als Standardbranch;
  es wird kein zusätzlicher `main` angelegt oder ein Branch umbenannt.
- PR #13 geprüft: offen, Draft, konfliktfrei und mergefähig; keine gemeldeten
  CI-Checks. Quell-/Testhashes stimmen weiterhin mit sieben bestandenen Tests überein.
- README zwischen Basis und Reparaturbranch unverändert. Merge mit Mergecommit
  und fachlicher Beschreibung vorgesehen, ohne Löschen des Reparaturbranches.
- Nutzerfreigabe zum Merge ist keine Behauptung einer unabhängigen fachlichen
  Codeprüfung. Ergebnis/Commit des Merges erst nach Ausführung berichten.
