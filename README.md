<div align="center">

# ⚜️ Warhammer 40,000: Rogue Trader — Traduzione Italiana ⚜️

**La traduzione amatoriale completa in italiano di _Warhammer 40,000: Rogue Trader_ di Owlcat Games.**

*Ogni dialogo, ogni voce del Codex, ogni descrizione di abilità e oggetto: tutta la Distesa di Koronus, finalmente in italiano.*

[![Licenza: CC BY-NC 4.0](https://img.shields.io/badge/Licenza-CC%20BY--NC%204.0-lightgrey.svg)](LICENSE)
![Stringhe tradotte](https://img.shields.io/badge/stringhe%20tradotte-77.538-success)
![Parole](https://img.shields.io/badge/parole-~1.8%20milioni-blue)
![Stato](https://img.shields.io/badge/stato-completa-brightgreen)
![Lingua](https://img.shields.io/badge/lingua-italiano-009246)

</div>

---

> *«Il Mandato di Commercio è nelle vostre mani, Lord Capitano. Che l'Imperatore guidi la vostra rotta tra le stelle.»*

## 📜 Cos'è

_Warhammer 40,000: Rogue Trader_ non ha una localizzazione ufficiale in italiano. Questo progetto la colma: **77.538 stringhe** del file di localizzazione del gioco tradotte in italiano, per circa **1,8 milioni di parole**. Interfaccia, dialoghi, narrazione, Codex, abilità, talenti, oggetti, missioni e diari di bordo.

## ✨ Caratteristiche

- **Completa**: tutte le stringhe con testo del gioco sono tradotte, comprese le espansioni presenti nel file di localizzazione.
- **Terminologia ufficiale Games Workshop**: Ecclesiarchia, Inquisitore, Navigatore, Astropate, Tecnoprete… Le forme già "latine" restano invariate (Imperium, Administratum, Adeptus Mechanicus, Astartes, Sororitas).
- **Glossario condiviso e coerente**: lo stesso termine ha la stessa resa in tutto il gioco ([`work/GLOSSARIO.md`](work/GLOSSARIO.md)).
- **Concordanza di genere curata**:
  - il Rogue Trader è declinato al maschile o al femminile in base al personaggio che crei, tramite i tag `{mf|…|…}` del gioco;
  - un registro di **961 personaggi** fissa il genere di ciascuno, ricavato dalle prove del testo originale ([`work/GENERI.md`](work/GENERI.md)).
- **Tono fedele all'originale**:
  - il fanatismo dell'Ecclesiarchia, la freddezza del Mechanicus, il gergo del Commercio Freddo;
  - il "voi" deferente rivolto al Lord Capitano;
  - nessun calco letterale.
- **Nomi propri preservati**: personaggi, abilità, talenti e oggetti unici mantengono il nome originale; gli oggetti comuni hanno nomi italiani.
- **Markup intatto**: link all'enciclopedia `{g|…}`, segnaposto `{name}`, tag di formattazione e variabili del gioco sono preservati e validati automaticamente.

## 🚀 Installazione

Il gioco non prevede l'italiano tra le lingue selezionabili. La traduzione si installa quindi **al posto di una lingua esistente**, ad esempio lo spagnolo.

1. Scarica [`itIT.json`](itIT.json) da questo repository.
2. Rinominalo in **`esES.json`**.
3. Apri la cartella di installazione del gioco e vai in:
   ```
   WH40KRT_Data/StreamingAssets/Localization/
   ```
   *(Steam: tasto destro sul gioco → Gestisci → Sfoglia i file locali)*
4. Fai una **copia di backup** dell'`esES.json` originale, poi sostituiscilo con il file rinominato.
5. Avvia il gioco e, nelle impostazioni, scegli **Español** come lingua.

> ⚠️ Gli aggiornamenti del gioco o una verifica dei file possono ripristinare il file originale: in tal caso ripeti la procedura.

## 🛠️ Struttura del progetto

| Percorso | Contenuto |
|---|---|
| `itIT.json` | La traduzione finale, pronta all'uso |
| `work/out/` | La traduzione suddivisa in 224 blocchi di lavoro |
| `work/GLOSSARIO.md` | Glossario dei termini adottati |
| `work/GENERI.md` | Registro dei generi dei personaggi |
| `work/FIXUP.md` | Correzioni di coerenza applicate dopo la traduzione |
| `work/doubts/`, `work/gender/` | Scelte di traduzione discusse e registro delle correzioni |
| `tools/tradtool.py` | Pipeline: suddivisione, validazione del markup, ricomposizione |

Il testo originale inglese del gioco **non è incluso**: appartiene a Owlcat Games. Per rigenerare i file di lavoro, copia `enGB.json` dalla cartella `Localization` del gioco nella radice del progetto, poi lancia:

```bash
python3 tools/tradtool.py prepare   # rigenera work/units.json e work/chunks/
python3 tools/tradtool.py check     # valida i blocchi tradotti rispetto all'originale
python3 tools/tradtool.py merge     # ricompone itIT.json
```

## 🤖 AI disclosure

Questa traduzione è stata realizzata **con l'intelligenza artificiale**, usando i modelli **Claude di Anthropic** guidati da un sistema di **prompt engineering proprietario di grado enterprise**. L'architettura è multi-agente:

- **orchestratori Claude Opus**:
  - pianificano il lavoro, mantengono glossario e registro dei generi;
  - distribuiscono i blocchi;
  - verificano i risultati e risolvono le incoerenze tra un blocco e l'altro.
- **worker Claude Sonnet**: in pool paralleli, traducono e revisionano i singoli blocchi seguendo le istruzioni e il glossario condiviso.

Il processo:

1. glossario della terminologia ufficiale Games Workshop;
2. un lotto pilota rivisto per fissare stile e registro;
3. traduzione in parallelo dei 224 blocchi, con il glossario come unica fonte di verità;
4. validazione automatica di ogni tag e segnaposto del gioco;
5. verifica della concordanza di genere blocco per blocco, più ricontrolli mirati sui personaggi che condividono lo stesso titolo.

Il lavoro è stato diretto e rivisto da un essere umano, ma resta una traduzione generata da un'IA: errori e imprecisioni sono possibili, e le segnalazioni sono benvenute!

## 🤝 Contribuire

Hai trovato un errore di traduzione, una frase innaturale o un genere sbagliato? Apri una [issue](https://github.com/Bloodis94/Warhammer40K-RogueTrader-Italian-translation/issues) indicando:

- il testo che vedi nel gioco (o uno screenshot);
- dove compare (dialogo, missione, Codex…);
- la correzione che proponi.

Le pull request sono benvenute: modifica il blocco giusto in `work/out/`, verifica con `tradtool.py check` e rigenera `itIT.json` con `merge`.

## ⚖️ Licenza

La traduzione è distribuita con licenza **[Creative Commons BY-NC 4.0](LICENSE)**:

- ✅ **puoi** usarla, condividerla e modificarla liberamente, anche in mod e progetti amatoriali, **citando l'autore** con un link a questo repository;
- ❌ **non puoi** usarla per **scopi commerciali** senza un accordo scritto esplicito con l'autore.

## 📢 Disclaimer

Progetto amatoriale e non ufficiale, **non affiliato né approvato** da Owlcat Games o Games Workshop. _Warhammer 40,000: Rogue Trader_ è un marchio di Owlcat Games. Warhammer 40,000, il logo Warhammer 40,000, l'aquila bicipite e tutti i nomi, marchi e loghi associati sono proprietà di Games Workshop Limited. La licenza di questo repository copre esclusivamente il lavoro di traduzione.

---

<div align="center">

*Per l'Imperatore e per la Dinastia von Valancius.* ⚜️

</div>

---

### 🏷️ Tag

`warhammer-40k` · `warhammer-40000` · `rogue-trader` · `warhammer-40k-rogue-trader` · `wh40k-rogue-trader` · `owlcat-games` · `traduzione-italiana` · `italian-translation` · `localizzazione-italiana` · `italian-localization` · `patch-italiano` · `italian-patch` · `mod-italiano` · `fan-translation` · `traduzione-amatoriale` · `ai-translation` · `traduzione-ai` · `claude` · `llm` · `rpg` · `crpg` · `gioco-di-ruolo` · `videogiochi` · `koronus-expanse` · `distesa-di-koronus` · `imperium` · `adeptus-mechanicus` · `game-localization` · `localization` · `l10n` · `i18n` · `italiano` · `italian` · `pc-game`

**Parole chiave:** traduzione italiana Rogue Trader, Rogue Trader in italiano, patch ITA Warhammer 40K Rogue Trader, Rogue Trader sub ita, mod traduzione italiana Owlcat, Warhammer 40000 Rogue Trader italiano, come mettere l'italiano in Rogue Trader.
