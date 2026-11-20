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
