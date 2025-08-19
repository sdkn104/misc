* http://techacademy.jp/magazine/6235
* http://qiita.com/nnahito/items/565f8755e70c51532459

### Initial (initial remote first, then clone)
1) clone (url should be get on clone button in github page)
```
$ git clone https://github.com/sdkn104/AppEngine.git
$ edit file, add, commit, 
$ git push origine master
```
### Initial (local initial)
1）create local repository
```
$ cd Arduino
$ git init
```
2）add modification info to local repository (add to index)
```
$ git add esp_basic
```
3）register added to local repository (commit) 
```
$ git commit -m "xxx"
```
X) create remote repository by github.com

4）register connection name (alias) of remote repository
     (register https:... to name "origin"
```
$ git remote add origin https://github.com/sdkn104/Arduino.git
```
5)setting to store name/password info in file ~/.git-credentials (linux)
```
git config --global credential.helper store
```
```
git config --global user.name "your name"
git config --global user.email "your mail address"
git config list
```
6）send files in local repository to remote (GitHub) repository
```
$ git push origin master
```

### Update (modification at local)
0) Check diff from remote and merge diffs (see below).
1）Add file modification info to index
```
$ git add xxx
$ git add .   --- add all modified or created(untracked) files
$ git add -u   --- add all modified or deleted files [recommended]
$ git add -A   --- add all modified, created(untracked) or deleted files
```
2）register files (commit)
```
$ git commit -m "just changed"
```
3）send data to GitHub (remote) repository
```
$ git push [--force] origin master  # --force may delete history on remote
```

### Get remote update into local
1) get modification in remote branch into local repository (fetch and merge)
```
$ git checkout master   --- move to master branch
$ git pull origin master   --- remote branch master -> local current branch
                               merge replay changes
or
$ git checkout master   --- move to master branch
$ git fetch origin
$ git merge ...
```

### diff from remote
```
$ git fetch origin ---- download remote copy (not merged)
$ git branch -a   ---- show all local/remote branches
$ git diff remotes/origin/master
```

### others
```
$ git status
$ git log -n 10
$ git log origin/master  --- check remote branch
$ git branch [-r]   --- show branches. -r for remote
$ git diff  ---- working and add(staged)
$ git diff -cached ---- add(staged) and last commit(HEAD)
$ git diff HEAD ---- working copy and last commit(HEAD)
$ git diff fb4fe13 a45e154 ---- diff between commit IDs
$ git clone https://github.com/xxxx/xxx.git localdir
$ git remote -v --- display remote connection (alias) list
$ git rm --cached [-r] dir/file   --- remove from index (make them untracked). keeping working copy.
$ git reset --soft HEAD~1 ---- cancel the last commit, 
$ git reset HEAD [files]  ---- cancel add(staged), keeping last commit(HEAD) and working copy.
$ git checkout [files/dir]  ---- cancel modification of working copy before add (overwrite by HEAD)
$ git ls-files  --- show files
```
