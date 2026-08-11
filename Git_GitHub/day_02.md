# 2026.08.11 과제

## 1. Git 기본 흐름

Git 작업의 가장 기본적인 순서

```bash
git status
git add 파일명
git commit -m "커밋 메시지"
git push origin main
```

흐름으로 보면:

```text
파일 생성/수정
    ↓
git add
    ↓
Staging Area
    ↓
git commit
    ↓
로컬 Git 저장소
    ↓
git push
    ↓
GitHub
```

---

## 2. 파일 생성과 `git add`의 차이

### 파일 생성

```bash
touch hello.py
```

`touch`는 실제 파일을 만든다. / (옆에 파일 생성 직접 눌러도 됨) 

### Git에 커밋할 준비

```bash
git add hello.py
```

`git add`는 파일을 만드는 명령어가 아니다!! 

> `git add` = 변경된 파일을 커밋할 목록에 올리는 것 ⭐️

따라서 존재하지 않는 파일을 add하면:

```text
fatal: pathspec 'hello.py' did not match any files
```

오류가 발생한다. (경험담임... 하하)

---

## 3. `git status`

현재 Git 상태를 확인한다.

```bash
git status
```

주요 상태:

```text
Untracked files
```

→ 새로 생겼지만 아직 Git이 관리하지 않는 파일

```text
Changes not staged for commit
```

→ 수정/삭제됐지만 아직 `git add` 하지 않은 파일

```text
Changes to be committed
```

→ `git add`가 완료되어 커밋을 기다리는 파일

---

## 4. `git add -A`

```bash
git add -A
```

현재 프로젝트 전체의 변경사항을 한 번에 Staging Area에 올린다.

포함되는 것:

- 새 파일
- 수정된 파일
- 삭제된 파일
- 이동된 파일

예:

```text
renamed: git/hello.py -> hello.py
deleted: .DS_Store
new file: .gitignore
```

> 주의: 필요 없는 파일까지 포함할 수 있으므로 `git status`를 먼저 확인하는 것이 좋다.

---

# 5. Commit

현재 Staging Area에 있는 변경사항을 Git 기록으로 저장한다.

```bash
git commit -m "Create hello.py"
```

예:

```text
[main 1ec5827] Create ai.py
```

`1ec5827`은 해당 커밋의 고유 ID 일부이다.

### Commit은 저장 지점이라고 생각하면 쉽다.

```text
작업
 ↓
Commit A
 ↓
작업
 ↓
Commit B
 ↓
작업
 ↓
Commit C
```

---

# 6. Branch

브랜치는 같은 프로젝트에서 별도의 작업 흐름을 만드는 기능이다.

### 브랜치 생성

```bash
git branch left
```

### 브랜치 이동

```bash
git switch left
```

### 현재 브랜치 확인

```bash
git branch
```

예:

```text
  left
* main
  right
```

`*`가 현재 브랜치이다.

---

## 브랜치는 파일 복사본이 아니다

예를 들어:

```text
main
 ├── hello.py
 └── world.py
```

에서 `left`, `right` 브랜치를 만들었다고 해서 파일이 실제로 3개씩 복사되는 것은 아니다.

Git이 각 브랜치별로 **어떤 버전의 프로젝트를 사용하고 있는지 기록**하는 것이다.

---

# 7. 브랜치 실습

## left 브랜치

```bash
git switch left
touch left.py
git add left.py
git commit -m "add left.py"
```

## right 브랜치

```bash
git switch right
touch right.py
git add right.py
git commit -m "add right.py"
```

결과:

```text
          left.py
         /
main ───●
         \
          right.py
```

---

# 8. `touch`로 만든 파일이 `| 0`으로 나오는 이유

```bash
touch left.py
```

만 실행하면 파일은 있지만 내용은 비어 있다.

그래서 merge할 때:

```text
left.py | 0
1 file changed, 0 insertions(+), 0 deletions(-)
```

처럼 표시된다.

파일에 실제 내용을 넣으면:

```python
print("left")
```

Git에서는:

```text
left.py | 1 +
1 insertion(+)
```

처럼 표시된다.

---

# 9. Merge

다른 브랜치의 변경사항을 현재 브랜치에 합친다.

예를 들어 `left`를 `main`에 합치려면:

```bash
git switch main
git merge left
```

> merge는 여러 파일을 한 파일로 합치는 것이 아니라  
> **두 브랜치에서 발생한 변경사항을 하나의 프로젝트에 합치는 것**이다.

---

# 10. Fast-forward Merge

다른 브랜치만 앞으로 진행되어 있다면 Git이 단순히 main 위치를 앞으로 이동시킨다.

```bash
git merge left
```

결과:

```text
Updating ...
Fast-forward
```

구조:

```text
main
  ↓

● ─── ● left

      ↓ merge

● ─── ●
      main
      left
```

별도의 Merge Commit이 만들어지지 않는다.

---

# 11. Merge Commit

두 브랜치가 각각 다른 작업을 했다면 합칠 때 새로운 Merge Commit이 만들어질 수 있다.

예:

```text
        left
       /
──────●
       \
        right
```

`left`를 먼저 main에 합치고 `right`까지 합치면:

```text
        left
       /    \
──────●      ● main
       \    /
        right
```

터미널에서는:

```text
Merge made by the 'ort' strategy.
```

처럼 나타난다.

---

# 12. Merge Conflict

두 브랜치가 같은 파일의 같은 부분을 서로 다르게 수정하면 Git이 자동으로 결정하지 못한다.

예:

```text
a 브랜치
hello.py
print("a")
```

```text
b 브랜치
hello.py
print("b")
```

Merge:

```bash
git merge b
```

충돌 발생:

```text
CONFLICT (add/add): Merge conflict in hello.py
Automatic merge failed
```

### 해결 순서

1. 충돌난 파일을 직접 수정
2. 원하는 코드만 남긴다.
3. 해결된 파일을 add

```bash
git add hello.py
```

4. commit

```bash
git commit -m "merge conflict in hello.py"
```

### Merge를 취소하고 싶다면

```bash
git merge --abort
```

---

# 13. Git 로그 확인

커밋 기록을 확인한다.

```bash
git log
```

브랜치 흐름까지 보기:

```bash
git log --all --graph
```

더 간단하게 보기:

```bash
git log --oneline --graph --decorate --all
```

예:

```text
*   main
|\
| * b
* | a
|/
*
```

`|`, `/`, `\`를 통해 브랜치가 갈라지고 합쳐진 과정을 확인할 수 있다.

### 긴 log 화면에서 나오기

```text
q
```

---

# 14. 브랜치 삭제

```bash
git branch -D left
```

여러 개 동시에 삭제:

```bash
git branch -D left right
```

---

# 15. GitHub 원격 저장소 연결

현재 연결 확인:

```bash
git remote -v
```

예:

```text
origin  https://github.com/.../oz_ai.git (fetch)
origin  https://github.com/.../oz_ai.git (push)
```

---

## 처음 연결할 때

```bash
git remote add origin 저장소주소
```

이미 `origin`이 존재하면:

```text
error: remote origin already exists.
```

이 경우 새로 추가하지 않고 주소를 변경한다.

```bash
git remote set-url origin 새로운주소
```

---

# 16. Push

로컬 Git의 커밋을 GitHub로 올린다.

```bash
git push origin main
```

```text
origin = GitHub 저장소
main   = 올릴 브랜치
```

---

# 17. Push가 거절되는 경우

GitHub에서 README 등을 직접 수정하면:

```text
내 컴퓨터 main
GitHub main
```

두 곳의 기록이 달라질 수 있다.

그 상태에서:

```bash
git push origin main
```

하면:

```text
! [rejected] main -> main (fetch first)
```

오류가 날 수 있다.

이때 GitHub 변경사항을 먼저 가져온다.

```bash
git pull --rebase origin main
```

그다음 다시:

```bash
git push origin main
```

---

# 18. Pull

GitHub의 최신 변경사항을 내 컴퓨터로 가져온다.

```bash
git pull origin main
```

예:

```text
GitHub에서 README 수정
        ↓
git pull origin main
        ↓
내 컴퓨터 README도 최신 상태
```

---

# 19. `pull --rebase`

```bash
git pull --rebase origin main
```

GitHub의 최신 커밋을 먼저 가져온 뒤, 그 위에 내 로컬 커밋을 다시 올린다.

```text
GitHub 최신 기록
      ↓
내 로컬 작업
```

커밋 기록을 비교적 깔끔하게 유지할 수 있다.

단, 커밋하지 않은 변경사항이 있으면:

```text
cannot pull with rebase:
You have unstaged changes.
```

오류가 발생할 수 있다.

이때 먼저:

```bash
git status
```

로 확인하고 변경사항을 commit하거나 stash해야 한다.

---

# 20. `.gitignore`

Git에 올리지 않을 파일을 지정한다.

예:

```gitignore
.env
.DS_Store
```

### `.env`

API Key, 비밀번호 등 중요한 값을 저장할 수 있기 때문에 GitHub에 올리지 않는 것이 중요하다.

### `.DS_Store`

macOS가 Finder 설정을 저장하기 위해 자동 생성하는 파일이다.

프로젝트에는 필요하지 않으므로 보통 Git에서 제외한다.

---

# 21. 이미 Git이 추적 중인 파일은 `.gitignore`만으로 안 사라진다

이미 `.env`가 Git에 올라간 상태라면:

```gitignore
.env
```

를 작성해도 자동으로 제거되지 않는다.

Git 추적을 끊어야 한다.

```bash
git rm --cached .env
```

`.DS_Store`도 동일하다.

```bash
git rm --cached .DS_Store
```

그다음:

```bash
git add .gitignore
git commit -m "chore: ignore env and DS_Store"
git push origin main
```

`--cached`를 사용하면 **내 컴퓨터의 실제 파일은 유지하고 Git에서만 제거**한다.

---

# 22. 파일 이동

예를 들어:

```text
git/hello.py
```

를

```text
hello.py
```

로 이동하면 Git은 처음에는:

```text
deleted: git/hello.py
untracked: hello.py
```

처럼 볼 수도 있다.

```bash
git add -A
```

후에는:

```text
renamed: git/hello.py -> hello.py
```

처럼 이동으로 인식할 수 있다.

---

# 23. 내가 자주 틀린 오류

### `git statis`

❌ 잘못된 명령어

```bash
git statis
```

✅ 올바른 명령어

```bash
git status
```

---

### `add hello.py`

❌

```bash
add hello.py
```

`add`는 터미널 자체 명령어가 아니다.

✅

```bash
git add hello.py
```

---

### 존재하지 않는 파일 add

```bash
git add left.py
```

파일이 없으면:

```text
pathspec 'left.py' did not match any files
```

먼저 파일 생성:

```bash
touch left.py
```

---

### origin 중복 생성

```bash
git remote add origin ...
```

이미 origin이 있다면:

```text
remote origin already exists.
```

주소 변경:

```bash
git remote set-url origin 새로운주소
```

---

# 24. Git 핵심 명령어 한눈에 보기

| 명령어 | 의미 |
|---|---|
| `git status` | 현재 상태 확인 |
| `touch 파일명` | 파일 생성 |
| `git add 파일명` | 파일을 커밋 준비 상태로 이동 |
| `git add -A` | 전체 변경사항 커밋 준비 |
| `git commit -m "메시지"` | 변경사항 기록 |
| `git branch` | 브랜치 확인 |
| `git branch 이름` | 브랜치 생성 |
| `git switch 이름` | 브랜치 이동 |
| `git merge 이름` | 다른 브랜치 병합 |
| `git branch -D 이름` | 브랜치 삭제 |
| `git log --oneline --graph --all` | 브랜치/커밋 흐름 확인 |
| `git remote -v` | GitHub 연결 주소 확인 |
| `git push origin main` | GitHub로 업로드 |
| `git pull origin main` | GitHub 변경사항 가져오기 |
| `git pull --rebase origin main` | GitHub 최신 기록 위에 내 커밋 재배치 |
| `git rm --cached 파일명` | 실제 파일은 남기고 Git 추적만 제거 |

---

# 25. 가장 중요한 흐름

## 일반 작업

```bash
git status
git add 파일명
git commit -m "메시지"
git push origin main
```

## 브랜치 작업

```bash
git branch feature
git switch feature

# 파일 작업

git add .
git commit -m "작업 내용"

git switch main
git merge feature
```

## GitHub가 내 로컬보다 최신일 때

```bash
git pull --rebase origin main
git push origin main
```

---

# 핵심 정리

> **Git은 파일의 변경 이력을 관리하는 도구이고, GitHub는 Git 저장소를 온라인에 보관하고 공유하는 서비스이다.**

> **`git add`는 파일 생성이 아니라 커밋 준비, `git commit`은 기록 저장, `git push`는 GitHub 업로드이다.**

> **Branch는 독립적인 작업 흐름을 만들고, Merge는 각 브랜치의 변경사항을 합친다.**

> **같은 부분을 다르게 수정하면 Merge Conflict가 발생하며 직접 수정 후 `git add → git commit`으로 해결한다.**

> **`.env`, `.DS_Store` 같은 파일은 `.gitignore`를 이용해 Git에 올라가지 않도록 관리한다.**