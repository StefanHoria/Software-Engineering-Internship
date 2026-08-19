# Notițe Git — Ziua 1–2 și Ziua 12

Notițele luate în timpul modulului de Git din practică, plus comenzile de Git LFS
învățate mai târziu, când push-ul a început să pice din cauza modelelor `.tflite`.

---

## 1. Configurare

```bash
git --version                                   # versiunea de git folosită
git config --global user.name "Stefan Horia"    # identitatea autorului
git config --global user.email stefanhoria36@gmail.com
git config --global core.editor "code --wait"   # VS Code ca editor principal
git config --global core.autocrlf true          # end-of-line pentru Windows
git config --global -e                          # deschide fișierul de configurare
git config --help                               # lista completă de comenzi
```

## 2. Crearea snapshot-urilor

```bash
git init                        # inițializare repository nou
git add file1.txt file2.txt     # staging files
git status                      # starea fișierelor din repository
git status -s                   # forma scurtă a statusului
```

### Commit

```bash
git commit -m "Initial Commit"  # commit cu mesaj scurt
git commit                      # deschide editorul pentru un mesaj mai lung
git commit -a                   # commit la toate fișierele modificate
```

### Ștergere și redenumire

```bash
rm file2.txt        # șterge fișierul; trebuie apoi dat git add pentru a înregistra ștergerea
git rm file2.txt    # șterge fișierul și îl scoate din index într-un singur pas

mv file1.txt main.js        # redenumire/mutare; necesită git add pentru ambele nume
git mv main.js file1.js     # face redenumirea direct în index
```

## 3. Ignorarea fișierelor

```bash
echo logs/ > .gitignore     # creează .gitignore cu o primă regulă
code .gitignore             # editare manuală
git add .gitignore          # .gitignore trebuie el însuși versionat

git rm --cached -r bin/     # scoate din index un folder deja urmărit
```

> După `git rm --cached` fișierul poate fi modificat local fără să mai apară în working tree.
> Șabloane gata făcute: <https://github.com/github/gitignore>.

## 4. Diferențe (staged / unstaged)

```bash
git diff              # schimbări nestaged
git diff --staged     # schimbări aflate în staging area

git config --global diff.tool vscode
git config --global difftool.vscode.cmd "code --wait --diff $LOCAL $REMOTE"
git difftool --staged # deschide VS Code pentru vizualizare
```

## 5. Istoric

```bash
git log                        # istoricul commit-urilor
git log --oneline              # istoric compact
git log --oneline --reverse    # în ordine cronologică
git show HEAD~1                # detaliile unui commit anume
```

## 6. Anularea modificărilor

```bash
git restore --staged file1.js            # scoate fișierul din staging
git clean -fd                            # șterge modificările locale netrackuite
git restore --source=HEAD~1 file1.js     # readuce fișierul la o versiune anterioară
```

## 7. Git LFS — fișiere mari

Problema întâlnită: GitHub refuză push-ul pentru fișiere peste 100 MB, iar modelele
`.tflite` / `.task` și clipul `.mov` depășeau limita. Soluția a fost Git LFS.

```bash
git lfs install
git lfs track "*.tflite" "*.task" "*.mov" "*.zip"
git add .gitattributes
git lfs migrate import --include="*.tflite,*.task,*.mov"   # rescrie istoricul deja existent
git lfs ls-files                                           # verificare
git push
```

Regulile efective sunt în [`.gitattributes`](../.gitattributes) din rădăcina repository-ului.
