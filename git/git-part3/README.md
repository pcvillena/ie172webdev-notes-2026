# Guide to Git: Part 3

This is a guide to using Git, a version control tool used for collaborative programming. For more information, visit the [Git documentation website](https://git-scm.com/docs).

---

- [Guide to Git: Part 3]
- [Preliminaries](#preliminaries)
- [Undoing a commit]
- [Developing new features using branches]
  - [Branches]
  - [git merge and rebase]
  - [GitHub Pull Requests]
- Other Git Tools
- [SUCCESS]

## Preliminaries

1. Create your account on GitHub.com.
2. Your Git should by accessible to you. Consult your groupmate who setup the Git repository via GitHub.
3. Install git on your PC/Mac. Find the appropriate installer [righthere](https://git-scm.com/downloads).
4. Ensure that your repository is connected to VSCode.

---

> **CAUTION**: The following are advanced uses of git as version control. It is recommended to go over Guide to Git Parts 1 and 2 first, plus some time and practice in using git with your projects and code.

## Undoing a commit

If you accidentally `git commit` a mistake that you want to undo, there are two approaches on how to fix it:

1. Create another commit that fixes the mistake e.g. `git commit -m 'undone the previous commit'`
2. Delete/revert the commit containing the mistake

What you will do will depend on whether you have pushed the erroneous code or not.

---

### If you have already pushed the mistake code in the remote repo

- Use `git revert <commit-hash>` to create a commit that is the exact opposite of a specific commit.
  - A commit hash is a unique identifier composed of numbers and lowercase letters that can be found in either GitHub or VSCode.
  - You also have the option to simply create a normal `git commit -m <summary>` to undo any errors in the code.
  
  **In GitHub:**
  Click the list of commits (the one that says <#> commits)

  ![alt text](image.png)

  From there you can see the list of commits you and others have pushed into the remote repo.

  ![alt text](image-1.png)

  **In VSCode**
  Using the Source Control extension, you can hover over a commit and copy the hash from there.

  ![alt text](image-2.png)

---

### If you have not pushed the code and the mistake only exists locally

- Run `git reset --soft HEAD~1`
  - This command undoes the most recent commit, but keeps all your edited code safe in your workspace.

  ![alt text](image-3.png)

  - To clear all edited code, replace `--soft` with `--hard` to undo any changes to the workspace.
    - Doing this rolls your code back to the last working commit.

---

## Developing new features using branches

### Branches

### git merge and rebase

### GitHub Pull Requests

## Other Git Tools

## SUCCESS

You may now safely develop new features without disrupting your main branch, code away!
