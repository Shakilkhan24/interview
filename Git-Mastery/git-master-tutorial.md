# Git Master Tutorial - Complete End-to-End Guide
## From Medium to DevOps Expert: Comprehensive Git Mastery

---

## Table of Contents

### Part I: Medium Level Commands (Grouped by Functionality)
1. [Repository Setup & Configuration](#1-repository-setup--configuration)
2. [Basic Operations (Add, Commit, Status)](#2-basic-operations-add-commit-status)
3. [Branching Operations](#3-branching-operations)
4. [Merging Operations](#4-merging-operations)
5. [Stashing Operations](#5-stashing-operations)
6. [Remote Operations](#6-remote-operations)
7. [History & Inspection](#7-history--inspection)
8. [Undoing Changes](#8-undoing-changes)
9. [Tagging Operations](#9-tagging-operations)
10. [File Operations](#10-file-operations)

### Part II: Advanced DevOps Level
11. [Advanced Branching Strategies](#11-advanced-branching-strategies)
12. [Git Hooks & Automation](#12-git-hooks--automation)
13. [CI/CD Integration](#13-cicd-integration)
14. [Git Workflows](#14-git-workflows)
15. [Submodules & Subtrees](#15-submodules--subtrees)
16. [Advanced Rebase & Interactive Rebase](#16-advanced-rebase--interactive-rebase)
17. [Git Internals & Plumbing Commands](#17-git-internals--plumbing-commands)
18. [Performance Optimization](#18-performance-optimization)
19. [Security & Best Practices](#19-security--best-practices)
20. [Troubleshooting Complex Scenarios](#20-troubleshooting-complex-scenarios)

---

## Part I: Medium Level Commands (Grouped by Functionality)

### 1. Repository Setup & Configuration

#### 1.1 Initializing Repositories

```bash
# Initialize a new Git repository in current directory
git init

# Initialize with a specific branch name (default: main/master)
git init -b main

# Initialize a bare repository (for server/shared repos)
git init --bare my-repo.git

# Clone an existing repository
git clone <repository-url>

# Clone with specific branch
git clone -b <branch-name> <repository-url>

# Clone with depth (shallow clone - saves space)
git clone --depth 1 <repository-url>

# Clone and rename directory
git clone <repository-url> <new-directory-name>
```

#### 1.2 Configuration Commands

```bash
# Set global user name and email
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Set repository-specific configuration
git config user.name "Your Name"
git config user.email "your.email@example.com"

# View all configuration
git config --list

# View global configuration
git config --global --list

# View local repository configuration
git config --local --list

# Set default branch name
git config --global init.defaultBranch main

# Set default editor
git config --global core.editor "code --wait"  # VS Code
git config --global core.editor "vim"          # Vim
git config --global core.editor "nano"         # Nano

# Set default merge tool
git config --global merge.tool vimdiff

# Set aliases (shortcuts)
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual '!gitk'

# View specific config value
git config user.name
git config user.email

# Unset configuration
git config --global --unset user.name
```

#### 1.3 Repository Information

```bash
# Show repository remote URL
git remote -v

# Show Git version
git --version

# Show repository root directory
git rev-parse --show-toplevel

# Check if current directory is a Git repository
git rev-parse --git-dir
```

---

### 2. Basic Operations (Add, Commit, Status)

#### 2.1 Status & File Tracking

```bash
# Check status of working directory
git status

# Short status format
git status -s
git status --short

# Show status with ignored files
git status --ignored

# Check what files are tracked/untracked
git ls-files                    # Tracked files
git ls-files --others           # Untracked files
git ls-files --others --exclude-standard  # Untracked (excluding .gitignore)
```

#### 2.2 Adding Files to Staging

```bash
# Add specific file to staging
git add <filename>

# Add all files in current directory
git add .

# Add all files recursively
git add -A
git add --all

# Add files interactively (choose what to add)
git add -i
git add --interactive

# Add files with patch mode (select parts of files)
git add -p
git add --patch

# Add files matching pattern
git add *.js
git add src/

# Add files and show what was added
git add -v
git add --verbose

# Add files but don't stage them (dry run)
git add -n
git add --dry-run
```

#### 2.3 Committing Changes

```bash
# Commit staged changes with message
git commit -m "Your commit message"

# Commit with detailed message (opens editor)
git commit

# Commit all changes (skip staging)
git commit -a
git commit --all

# Commit with message and skip staging
git commit -am "Your commit message"

# Amend last commit (change message or add files)
git commit --amend

# Amend last commit with new message
git commit --amend -m "New commit message"

# Amend last commit and keep same message
git commit --amend --no-edit

# Commit with sign-off
git commit -s
git commit --signoff

# Create empty commit (useful for triggering CI/CD)
git commit --allow-empty -m "Trigger build"
```

#### 2.4 Viewing Changes

```bash
# Show changes in working directory
git diff

# Show staged changes
git diff --staged
git diff --cached

# Show changes between commits
git diff <commit1> <commit2>

# Show changes in specific file
git diff <filename>

# Show word-level diff (instead of line-level)
git diff --word-diff

# Show summary of changes
git diff --stat

# Show changes with context lines
git diff -U5  # 5 lines of context
```

---

### 3. Branching Operations

#### 3.1 Creating & Listing Branches

```bash
# List all local branches
git branch

# List all branches (local and remote)
git branch -a

# List only remote branches
git branch -r

# Create new branch
git branch <branch-name>

# Create and switch to new branch
git checkout -b <branch-name>
git switch -c <branch-name>  # Newer command

# Create branch from specific commit
git branch <branch-name> <commit-hash>

# Create branch from remote branch
git branch <branch-name> origin/<branch-name>

# List branches with last commit info
git branch -v

# List branches merged into current branch
git branch --merged

# List branches not merged into current branch
git branch --no-merged

# Show current branch name
git branch --show-current
```

#### 3.2 Switching Between Branches

```bash
# Switch to existing branch
git checkout <branch-name>
git switch <branch-name>  # Newer command (recommended)

# Switch to previous branch
git checkout -
git switch -

# Create and switch in one command
git checkout -b <branch-name>
git switch -c <branch-name>

# Switch and create tracking branch
git checkout -b <branch-name> origin/<branch-name>
git switch -c <branch-name> origin/<branch-name>
```

#### 3.3 Renaming & Deleting Branches

```bash
# Rename current branch
git branch -m <new-name>

# Rename specific branch
git branch -m <old-name> <new-name>

# Delete local branch
git branch -d <branch-name>

# Force delete local branch (even if not merged)
git branch -D <branch-name>

# Delete remote branch
git push origin --delete <branch-name>
git push origin :<branch-name>  # Alternative syntax

# Delete tracking branches that no longer exist on remote
git fetch --prune
git fetch -p
```

#### 3.4 Branch Tracking

```bash
# Set upstream branch for current branch
git branch --set-upstream-to=origin/<branch-name>

# Set upstream when pushing
git push -u origin <branch-name>
git push --set-upstream origin <branch-name>

# View tracking information
git branch -vv

# Remove upstream tracking
git branch --unset-upstream
```

---

### 4. Merging Operations

#### 4.1 Basic Merging

```bash
# Merge branch into current branch
git merge <branch-name>

# Merge with commit message
git merge <branch-name> -m "Merge message"

# Merge without creating merge commit (fast-forward)
git merge --ff <branch-name>

# Merge and always create merge commit
git merge --no-ff <branch-name>

# Merge without committing (staged for commit)
git merge --no-commit <branch-name>

# Abort merge in progress
git merge --abort
```

#### 4.2 Merge Strategies

```bash
# Use specific merge strategy
git merge -s ours <branch-name>      # Keep our version
git merge -s theirs <branch-name>   # Keep their version
git merge -s recursive <branch-name> # Default recursive strategy

# Merge with strategy options
git merge -X ours <branch-name>      # Resolve conflicts favoring ours
git merge -X theirs <branch-name>    # Resolve conflicts favoring theirs
git merge -X ignore-space-change <branch-name>
git merge -X ignore-all-space <branch-name>
```

#### 4.3 Squash Merging

```bash
# Squash merge (combines all commits into one)
git merge --squash <branch-name>

# After squash merge, you need to commit
git commit -m "Squashed merge message"
```

#### 4.4 Handling Merge Conflicts

```bash
# View conflicted files
git status

# Use our version for conflicted file
git checkout --ours <filename>

# Use their version for conflicted file
git checkout --theirs <filename>

# Use merge tool to resolve conflicts
git mergetool

# Mark conflict as resolved
git add <resolved-file>

# Continue merge after resolving conflicts
git commit
```

---

### 5. Stashing Operations

#### 5.1 Basic Stashing

```bash
# Stash current changes
git stash

# Stash with message
git stash save "Work in progress"

# Stash including untracked files
git stash -u
git stash --include-untracked

# Stash including ignored files
git stash -a
git stash --all

# Stash specific files
git stash push <file1> <file2>

# Stash keeping changes in working directory
git stash --keep-index
```

#### 5.2 Viewing & Managing Stashes

```bash
# List all stashes
git stash list

# Show stash contents
git stash show

# Show detailed stash contents
git stash show -p
git stash show stash@{0}

# Show specific stash
git stash show stash@{1}
```

#### 5.3 Applying & Popping Stashes

```bash
# Apply most recent stash (keeps stash)
git stash apply

# Apply specific stash
git stash apply stash@{1}

# Pop most recent stash (removes stash)
git stash pop

# Pop specific stash
git stash pop stash@{1}
```

#### 5.4 Deleting Stashes

```bash
# Delete most recent stash
git stash drop

# Delete specific stash
git stash drop stash@{1}

# Delete all stashes
git stash clear
```

#### 5.5 Creating Branches from Stashes

```bash
# Create branch from stash
git stash branch <branch-name>

# Create branch from specific stash
git stash branch <branch-name> stash@{1}
```

---

### 6. Remote Operations

#### 6.1 Viewing & Managing Remotes

```bash
# List all remotes
git remote

# List remotes with URLs
git remote -v

# Show remote URL
git remote get-url origin

# Add remote repository
git remote add <name> <url>

# Rename remote
git remote rename <old-name> <new-name>

# Remove remote
git remote remove <name>
git remote rm <name>

# Show remote details
git remote show origin

# Update remote URL
git remote set-url origin <new-url>
```

#### 6.2 Fetching from Remote

```bash
# Fetch from default remote (origin)
git fetch

# Fetch from specific remote
git fetch origin

# Fetch specific branch
git fetch origin <branch-name>

# Fetch all remotes
git fetch --all

# Fetch and prune deleted remote branches
git fetch --prune
git fetch -p

# Fetch with tags
git fetch --tags

# Fetch specific tag
git fetch origin tag <tag-name>
```

#### 6.3 Pulling from Remote

```bash
# Pull from remote (fetch + merge)
git pull

# Pull from specific remote and branch
git pull origin <branch-name>

# Pull with rebase instead of merge
git pull --rebase

# Pull and only allow fast-forward
git pull --ff-only

# Pull without committing (just fetch)
git pull --no-commit
```

#### 6.4 Pushing to Remote

```bash
# Push to default remote (origin)
git push

# Push to specific remote and branch
git push origin <branch-name>

# Push and set upstream
git push -u origin <branch-name>
git push --set-upstream origin <branch-name>

# Push all branches
git push --all

# Push all tags
git push --tags

# Push specific tag
git push origin <tag-name>

# Force push (dangerous - overwrites remote)
git push --force
git push -f

# Force push with lease (safer - fails if remote changed)
git push --force-with-lease

# Push to multiple remotes
git push origin <branch-name> && git push backup <branch-name>

# Delete remote branch via push
git push origin --delete <branch-name>
```

---

### 7. History & Inspection

#### 7.1 Viewing Commit History

```bash
# Show commit history
git log

# One-line log format
git log --oneline

# Graph view with branches
git log --graph --oneline --all

# Show last N commits
git log -n 5
git log -5

# Show commits with file changes
git log --stat

# Show full diff in commits
git log -p

# Show commits for specific file
git log <filename>

# Show commits by author
git log --author="John Doe"

# Show commits in date range
git log --since="2024-01-01" --until="2024-12-31"

# Show commits with search in messages
git log --grep="bug fix"

# Show commits with specific text in code
git log -S "function_name"

# Show commits in reverse order
git log --reverse

# Show commits with decoration (branches, tags)
git log --decorate

# Show commits with file paths
git log --name-only
git log --name-status
```

#### 7.2 Viewing Specific Commits

```bash
# Show specific commit
git show <commit-hash>

# Show commit with stat
git show --stat <commit-hash>

# Show commit with full diff
git show -p <commit-hash>

# Show commit message only
git show -s <commit-hash>

# Show file at specific commit
git show <commit-hash>:<filename>
```

#### 7.3 Comparing Commits & Files

```bash
# Compare working directory with HEAD
git diff HEAD

# Compare two commits
git diff <commit1> <commit2>

# Compare branches
git diff <branch1> <branch2>

# Compare file across commits
git diff <commit1> <commit2> -- <filename>

# Show what changed between commits
git diff --stat <commit1> <commit2>

# Compare with common ancestor
git diff <commit1>...<commit2>
```

#### 7.4 Finding Commits

```bash
# Find commit by message
git log --grep="search term"

# Find commit that introduced bug
git bisect start
git bisect bad
git bisect good <commit-hash>
git bisect reset

# Find when file was deleted
git log --diff-filter=D --summary

# Find commits touching specific line
git log -L <start>,<end>:<filename>
git log -L :<function-name>:<filename>
```

---

### 8. Undoing Changes

#### 8.1 Unstaging Files

```bash
# Unstage file (keep changes in working directory)
git reset HEAD <filename>
git restore --staged <filename>  # Newer command

# Unstage all files
git reset HEAD
git restore --staged .
```

#### 8.2 Discarding Working Directory Changes

```bash
# Discard changes in working directory
git checkout -- <filename>
git restore <filename>  # Newer command

# Discard all changes in working directory
git checkout -- .
git restore .  # Newer command

# Discard changes and remove untracked files
git clean -fd
```

#### 8.3 Resetting Commits

```bash
# Soft reset (keeps changes staged)
git reset --soft HEAD~1

# Mixed reset (keeps changes unstaged) - default
git reset --mixed HEAD~1
git reset HEAD~1

# Hard reset (discards all changes) - DANGEROUS
git reset --hard HEAD~1

# Reset to specific commit
git reset --hard <commit-hash>

# Reset branch to match remote
git reset --hard origin/<branch-name>
```

#### 8.4 Reverting Commits

```bash
# Revert last commit (creates new commit)
git revert HEAD

# Revert specific commit
git revert <commit-hash>

# Revert without committing
git revert --no-commit <commit-hash>

# Revert multiple commits
git revert <commit1> <commit2>
```

#### 8.5 Cleaning Untracked Files

```bash
# Show what would be removed
git clean -n
git clean --dry-run

# Remove untracked files
git clean -f

# Remove untracked files and directories
git clean -fd

# Remove ignored files too
git clean -fX

# Remove all untracked and ignored files
git clean -fx
```

---

### 9. Tagging Operations

#### 9.1 Creating Tags

```bash
# Create lightweight tag
git tag <tag-name>

# Create annotated tag (recommended)
git tag -a <tag-name> -m "Tag message"

# Create tag at specific commit
git tag -a <tag-name> <commit-hash> -m "Tag message"

# Create signed tag
git tag -s <tag-name> -m "Tag message"
```

#### 9.2 Viewing Tags

```bash
# List all tags
git tag

# List tags matching pattern
git tag -l "v1.*"

# Show tag details
git show <tag-name>

# List tags with messages
git tag -n
```

#### 9.3 Pushing Tags

```bash
# Push specific tag
git push origin <tag-name>

# Push all tags
git push --tags
git push origin --tags

# Push annotated tags only
git push --follow-tags
```

#### 9.4 Deleting Tags

```bash
# Delete local tag
git tag -d <tag-name>

# Delete remote tag
git push origin --delete <tag-name>
git push origin :refs/tags/<tag-name>
```

#### 9.5 Checking Out Tags

```bash
# Checkout tag (creates detached HEAD)
git checkout <tag-name>

# Create branch from tag
git checkout -b <branch-name> <tag-name>
```

---

### 10. File Operations

#### 10.1 Moving & Renaming Files

```bash
# Move/rename file (Git detects automatically)
git mv <old-name> <new-name>

# Move file to different directory
git mv <file> <directory>/

# Force move (overwrite existing)
git mv -f <old-name> <new-name>
```

#### 10.2 Removing Files

```bash
# Remove file from Git and filesystem
git rm <filename>

# Remove file from Git only (keep in filesystem)
git rm --cached <filename>

# Remove directory recursively
git rm -r <directory>

# Force remove
git rm -f <filename>
```

#### 10.3 Ignoring Files

```bash
# Create .gitignore file
touch .gitignore

# Ignore specific file
echo "filename" >> .gitignore

# Ignore directory
echo "directory/" >> .gitignore

# Ignore pattern
echo "*.log" >> .gitignore

# Check if file is ignored
git check-ignore -v <filename>
```

#### 10.4 Viewing File Information

```bash
# Show file in specific commit
git show <commit-hash>:<filename>

# Show file in specific branch
git show <branch-name>:<filename>

# Find when file was added
git log --diff-filter=A -- <filename>

# Find when file was deleted
git log --diff-filter=D -- <filename>

# Show file history with renames
git log --follow -- <filename>

# Show blame (who changed each line)
git blame <filename>

# Show blame with more context
git blame -L 10,20 <filename>
```

---

## Part II: Advanced DevOps Level

### 11. Advanced Branching Strategies

#### 11.1 GitFlow Workflow

```bash
# Main branches
main/master          # Production-ready code
develop             # Integration branch

# Supporting branches
feature/<name>      # New features
release/<version>   # Release preparation
hotfix/<name>       # Critical production fixes

# Example GitFlow commands
git checkout -b develop
git checkout -b feature/user-authentication develop
git checkout -b release/1.2.0 develop
git checkout -b hotfix/critical-bug main
```

#### 11.2 GitHub Flow

```bash
# Simple workflow: main branch + feature branches
git checkout -b feature/new-feature
# ... make changes ...
git push -u origin feature/new-feature
# Create Pull Request
# After merge, delete branch
git branch -d feature/new-feature
git push origin --delete feature/new-feature
```

#### 11.3 GitLab Flow

```bash
# Environment branches
main                # Production
staging            # Staging environment
pre-production     # Pre-production testing

# Feature branches merge to main
# Main merges to staging
# Staging merges to pre-production
# Pre-production merges to main (production)
```

#### 11.4 Branch Protection Rules

```bash
# Check branch protection (via API or UI)
# Typically configured in repository settings

# Bypass protection (if you have permissions)
git push --no-verify origin <branch-name>
```

#### 11.5 Branch Naming Conventions

```bash
# Feature branches
feature/JIRA-123-add-login
feature/user-authentication

# Bug fixes
bugfix/JIRA-456-fix-crash
fix/memory-leak

# Hotfixes
hotfix/critical-security-patch
hotfix/production-issue

# Releases
release/v1.2.0
release/2024-Q1

# Chores
chore/update-dependencies
chore/refactor-code
```

---

### 12. Git Hooks & Automation

#### 12.1 Understanding Git Hooks

Git hooks are scripts that run automatically at certain points in Git workflow.

**Client-side hooks:**
- `pre-commit` - Before commit
- `prepare-commit-msg` - Before commit message editor
- `commit-msg` - Validate commit message
- `post-commit` - After commit
- `pre-rebase` - Before rebase
- `post-rewrite` - After commit rewriting
- `pre-push` - Before push

**Server-side hooks:**
- `pre-receive` - Before receiving push
- `update` - Before updating ref
- `post-receive` - After receiving push

#### 12.2 Creating Hooks

```bash
# Hooks are in .git/hooks/ directory
ls .git/hooks/

# Create pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Run tests before commit
npm test
if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi
EOF

chmod +x .git/hooks/pre-commit

# Create commit-msg hook (validate commit message)
cat > .git/hooks/commit-msg << 'EOF'
#!/bin/bash
commit_msg=$(cat $1)
if ! echo "$commit_msg" | grep -qE "^(feat|fix|docs|style|refactor|test|chore):"; then
    echo "Commit message must start with: feat, fix, docs, style, refactor, test, or chore"
    exit 1
fi
EOF

chmod +x .git/hooks/commit-msg

# Create pre-push hook
cat > .git/hooks/pre-push << 'EOF'
#!/bin/bash
# Prevent pushing to main branch
protected_branch='main'
current_branch=$(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')

if [ $protected_branch = $current_branch ]; then
    read -p "You're about to push to main. Are you sure? (yes/no) " -n 3 -r
    echo
    if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
        exit 1
    fi
fi
EOF

chmod +x .git/hooks/pre-push
```

#### 12.3 Using Husky (Node.js Projects)

```bash
# Install Husky
npm install --save-dev husky

# Initialize Husky
npx husky install

# Create pre-commit hook
npx husky add .husky/pre-commit "npm test"

# Create commit-msg hook
npx husky add .husky/commit-msg 'npx --no -- commitlint --edit "$1"'
```

#### 12.4 Using pre-commit (Python Projects)

```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
EOF

# Install hooks
pre-commit install

# Run on all files
pre-commit run --all-files
```

#### 12.5 Custom Hook Examples

```bash
# Pre-commit: Run linter
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Run ESLint
npm run lint
if [ $? -ne 0 ]; then
    exit 1
fi
EOF

# Pre-commit: Check for secrets
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Check for AWS keys, passwords, etc.
if git diff --cached | grep -E "(AKIA[0-9A-Z]{16}|password|secret)"; then
    echo "Potential secrets detected. Commit aborted."
    exit 1
fi
EOF

# Post-commit: Send notification
cat > .git/hooks/post-commit << 'EOF'
#!/bin/bash
# Send Slack notification
COMMIT_MSG=$(git log -1 --pretty=%B)
AUTHOR=$(git log -1 --pretty=%an)
curl -X POST -H 'Content-type: application/json' \
  --data "{\"text\":\"New commit by $AUTHOR: $COMMIT_MSG\"}" \
  $SLACK_WEBHOOK_URL
EOF
```

---

### 13. CI/CD Integration

#### 13.1 GitLab CI/CD

```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - deploy

build:
  stage: build
  script:
    - docker build -t myapp:$CI_COMMIT_SHA .
    - docker push myapp:$CI_COMMIT_SHA
  only:
    - main
    - develop

test:
  stage: test
  script:
    - npm test
    - npm run lint
  except:
    - main

deploy:
  stage: deploy
  script:
    - kubectl set image deployment/myapp myapp=myapp:$CI_COMMIT_SHA
  only:
    - main
```

#### 13.2 GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: npm test
      - name: Run linter
        run: npm run lint
```

#### 13.3 Jenkins Integration

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build') {
            steps {
                sh 'docker build -t myapp:$GIT_COMMIT .'
            }
        }
        
        stage('Test') {
            steps {
                sh 'npm test'
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh 'kubectl apply -f k8s/'
            }
        }
    }
}
```

#### 13.4 Git Tags for Releases

```bash
# Create release tag
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin v1.2.0

# In CI/CD, trigger deployment on tag push
# GitHub Actions example:
# on:
#   push:
#     tags:
#       - 'v*'
```

#### 13.5 Semantic Versioning with Git

```bash
# Get version from latest tag
VERSION=$(git describe --tags --abbrev=0)
NEXT_VERSION=$(echo $VERSION | awk -F. '{print $1"."$2"."($3+1)}')

# Create version tag
git tag -a $NEXT_VERSION -m "Release $NEXT_VERSION"
git push origin $NEXT_VERSION
```

---

### 14. Git Workflows

#### 14.1 Centralized Workflow

```bash
# Simple workflow - everyone pushes to main
git clone <repo>
git checkout -b feature
# ... make changes ...
git commit -am "Add feature"
git push origin feature
# Merge via Pull Request
```

#### 14.2 Feature Branch Workflow

```bash
# Each feature in separate branch
git checkout -b feature/user-login
# ... develop feature ...
git push -u origin feature/user-login
# Create Pull Request
# After merge, cleanup
git checkout main
git pull
git branch -d feature/user-login
```

#### 14.3 Forking Workflow

```bash
# Fork repository on GitHub/GitLab
# Clone your fork
git clone https://github.com/your-username/repo.git
cd repo

# Add upstream repository
git remote add upstream https://github.com/original-owner/repo.git

# Create feature branch
git checkout -b feature/new-feature

# Make changes and push
git push origin feature/new-feature

# Keep fork updated
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

#### 14.4 GitFlow Workflow (Detailed)

```bash
# Initialize GitFlow
git flow init

# Start feature
git flow feature start user-authentication

# Finish feature (merges to develop)
git flow feature finish user-authentication

# Start release
git flow release start 1.2.0

# Finish release (creates tag, merges to main and develop)
git flow release finish 1.2.0

# Start hotfix
git flow hotfix start critical-bug

# Finish hotfix (merges to main and develop)
git flow hotfix finish critical-bug
```

---

### 15. Submodules & Subtrees

#### 15.1 Git Submodules

```bash
# Add submodule
git submodule add https://github.com/user/repo.git path/to/submodule

# Clone repository with submodules
git clone --recursive <repo-url>
# Or after clone
git submodule update --init --recursive

# Update submodules
git submodule update --remote

# Update all submodules
git submodule update --remote --recursive

# Remove submodule
git submodule deinit -f path/to/submodule
git rm -f path/to/submodule
rm -rf .git/modules/path/to/submodule

# Commit submodule changes
cd path/to/submodule
git commit -am "Update submodule"
cd ../..
git add path/to/submodule
git commit -m "Update submodule reference"
```

#### 15.2 Git Subtrees

```bash
# Add subtree
git subtree add --prefix=lib/external-repo \
  https://github.com/user/repo.git main --squash

# Pull changes from subtree
git subtree pull --prefix=lib/external-repo \
  https://github.com/user/repo.git main --squash

# Push changes to subtree
git subtree push --prefix=lib/external-repo \
  https://github.com/user/repo.git main
```

#### 15.3 Submodules vs Subtrees

**Submodules:**
- Separate repository
- Requires submodule commands
- Better for independent projects
- More complex to manage

**Subtrees:**
- Code merged into main repo
- Simpler workflow
- Better for tightly coupled code
- Larger repository size

---

### 16. Advanced Rebase & Interactive Rebase

#### 16.1 Interactive Rebase

```bash
# Rebase last N commits interactively
git rebase -i HEAD~3

# Rebase from specific commit
git rebase -i <commit-hash>

# Rebase onto different branch
git rebase -i <base-branch>

# Interactive rebase commands:
# pick    - Use commit as-is
# reword  - Change commit message
# edit    - Stop to amend commit
# squash  - Combine with previous commit
# fixup   - Like squash, but discard message
# drop    - Remove commit
# exec    - Run command
```

#### 16.2 Rebase Examples

```bash
# Rebase current branch onto main
git rebase main

# Rebase with autosquash (automatically squash fixup commits)
git rebase -i --autosquash HEAD~5

# Rebase and update author
git rebase -i HEAD~3
# Change 'pick' to 'edit' for commits to modify
git commit --amend --author="New Author <email@example.com>"
git rebase --continue

# Rebase and sign commits
git rebase --signoff HEAD~3
```

#### 16.3 Rebase vs Merge

**Rebase:**
- Linear history
- Cleaner commit history
- Rewrites commit history
- Don't rebase shared/public branches

**Merge:**
- Preserves history
- Shows branch structure
- Safe for shared branches
- Can create complex history

#### 16.4 Rebase Best Practices

```bash
# Always rebase feature branches before merging
git checkout feature-branch
git fetch origin
git rebase origin/main
git push --force-with-lease

# Rebase local commits before pushing
git rebase -i HEAD~5

# Abort rebase if something goes wrong
git rebase --abort

# Continue rebase after resolving conflicts
git add <resolved-files>
git rebase --continue

# Skip commit during rebase
git rebase --skip
```

---

### 17. Git Internals & Plumbing Commands

#### 17.1 Understanding Git Objects

```bash
# Git stores data as objects:
# - Blobs (file contents)
# - Trees (directory structure)
# - Commits (snapshots)
# - Tags (pointers to commits)

# View object type
git cat-file -t <object-hash>

# View object content
git cat-file -p <object-hash>

# View object size
git cat-file -s <object-hash>
```

#### 17.2 Plumbing Commands

```bash
# Low-level commands (plumbing)
git hash-object <file>           # Create blob object
git cat-file -p <hash>           # View object
git ls-tree <tree-hash>          # List tree contents
git write-tree                   # Create tree from index
git commit-tree <tree> -p <parent> -m "message"  # Create commit
git update-ref refs/heads/main <commit-hash>  # Update branch pointer

# View refs
git show-ref
cat .git/HEAD
cat .git/refs/heads/main
```

#### 17.3 Reflog

```bash
# View reflog (history of HEAD movements)
git reflog

# View reflog for specific branch
git reflog show <branch-name>

# Recover lost commits using reflog
git reflog
git checkout <commit-hash-from-reflog>

# Create branch from reflog entry
git branch recovery-branch HEAD@{2}

# Expire old reflog entries
git reflog expire --expire=90.days.ago
```

#### 17.4 Packfiles & Garbage Collection

```bash
# Run garbage collection
git gc

# Aggressive garbage collection
git gc --aggressive

# Prune unreachable objects
git prune

# Verify repository integrity
git fsck

# Check repository size
du -sh .git
```

#### 17.5 Index (Staging Area)

```bash
# View index contents
git ls-files --stage

# Update index directly
git update-index --add <file>
git update-index --remove <file>

# Clear index
git read-tree --empty
```

---

### 18. Performance Optimization

#### 18.1 Large Repository Optimization

```bash
# Shallow clone (only recent history)
git clone --depth 1 <repo-url>

# Partial clone (exclude large files)
git clone --filter=blob:none <repo-url>

# Clone single branch
git clone --single-branch --branch main <repo-url>

# Increase Git buffer size
git config --global http.postBuffer 524288000

# Use Git LFS for large files
git lfs install
git lfs track "*.psd"
git lfs track "*.zip"
```

#### 18.2 Git LFS (Large File Storage)

```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.psd"
git lfs track "*.zip"
git lfs track "*.mp4"

# View tracked files
git lfs ls-files

# Migrate existing files to LFS
git lfs migrate import --include="*.psd" --everything
```

#### 18.3 Sparse Checkout

```bash
# Enable sparse checkout
git config core.sparseCheckout true

# Specify directories to checkout
echo "src/main/*" > .git/info/sparse-checkout
echo "docs/*" >> .git/info/sparse-checkout

# Apply sparse checkout
git read-tree -mu HEAD
```

#### 18.4 Performance Tuning

```bash
# Enable filesystem cache
git config --global core.preloadindex true

# Enable multi-threaded operations
git config --global core.fscache true
git config --global core.multiPackIndex true

# Optimize pack files
git config --global pack.threads 0  # Use all CPU cores

# Increase compression level
git config --global pack.compression 9

# Enable delta compression
git config --global pack.deltaCacheSize 2g
git config --global pack.deltaCacheLimit 1g
```

#### 18.5 Repository Maintenance

```bash
# Repack repository
git repack -a -d --depth=250 --window=250

# Prune and optimize
git prune
git gc --aggressive

# Verify and fix repository
git fsck --full
git gc --prune=now
```

---

### 19. Security & Best Practices

#### 19.1 Commit Signing

```bash
# Generate GPG key
gpg --full-generate-key

# List GPG keys
gpg --list-secret-keys --keyid-format LONG

# Configure Git to use GPG
git config --global user.signingkey <key-id>

# Sign commits
git commit -S -m "Signed commit"

# Always sign commits
git config --global commit.gpgsign true

# Verify signed commits
git log --show-signature
```

#### 19.2 SSH Keys for Git

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add SSH key to agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Test SSH connection
ssh -T git@github.com
```

#### 19.3 Credential Management

```bash
# Use credential helper
git config --global credential.helper store
git config --global credential.helper cache

# Use credential helper with timeout
git config --global credential.helper 'cache --timeout=3600'

# Use SSH instead of HTTPS
git remote set-url origin git@github.com:user/repo.git
```

#### 19.4 Security Best Practices

```bash
# Don't commit secrets
# Use .gitignore for sensitive files
echo ".env" >> .gitignore
echo "*.key" >> .gitignore
echo "secrets/" >> .gitignore

# Use git-secrets (AWS)
git secrets --install
git secrets --register-aws

# Scan for secrets before commit
git secrets --scan

# Use environment variables or secret managers
# AWS Secrets Manager, HashiCorp Vault, etc.
```

#### 19.5 Access Control

```bash
# Use branch protection rules (GitHub/GitLab UI)
# Require pull request reviews
# Require status checks
# Require signed commits
# Restrict who can push to main

# Use Git hooks for additional validation
# Pre-receive hooks on server
# Pre-push hooks on client
```

#### 19.6 Audit & Compliance

```bash
# View commit history with authors
git log --pretty=format:"%h - %an, %ar : %s"

# Export commit log
git log --all --pretty=format:"%H|%an|%ae|%ad|%s" > commits.csv

# Find commits by author
git log --author="John Doe"

# Find commits in date range
git log --since="2024-01-01" --until="2024-12-31"

# View file change history
git log --follow -- <file>
```

---

### 20. Troubleshooting Complex Scenarios

#### 20.1 Recovering Lost Commits

```bash
# Find lost commits using reflog
git reflog

# Recover from reflog
git checkout -b recovery-branch <commit-hash-from-reflog>

# Recover from dangling commits
git fsck --lost-found
git show <dangling-commit-hash>
```

#### 20.2 Resolving Merge Conflicts

```bash
# Abort merge
git merge --abort

# Use merge tool
git mergetool

# Resolve using ours/theirs
git checkout --ours <file>
git checkout --theirs <file>

# Manual conflict resolution
# Edit conflicted files
# Mark as resolved
git add <resolved-file>
git commit
```

#### 20.3 Fixing Corrupted Repository

```bash
# Check repository integrity
git fsck --full

# Recover from backup
cp -r .git .git.backup
# Restore from backup if needed

# Re-clone if severely corrupted
git clone <remote-url> <new-directory>
# Copy working files
cp -r <old-directory>/* <new-directory>/
```

#### 20.4 Large File Issues

```bash
# Remove large file from history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch <large-file>" \
  --prune-empty --tag-name-filter cat -- --all

# Use BFG Repo-Cleaner (faster alternative)
bfg --delete-files <large-file>
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

#### 20.5 Detached HEAD State

```bash
# You're in detached HEAD state
git checkout <commit-hash>  # Creates detached HEAD

# Create branch from detached HEAD
git checkout -b new-branch

# Or return to branch
git checkout main
```

#### 20.6 Undoing Pushed Commits

```bash
# If you haven't pushed yet
git reset --hard HEAD~1

# If already pushed (use with caution)
git revert HEAD  # Creates new commit undoing changes
# OR
git reset --hard HEAD~1
git push --force-with-lease  # Only if you're sure
```

#### 20.7 Split Repository

```bash
# Extract subdirectory to new repository
git filter-branch --prune-empty --subdirectory-filter <directory> main

# Or use git subtree
git subtree push --prefix=<directory> <new-remote> main
```

#### 20.8 Combine Multiple Repositories

```bash
# Add remote
git remote add other-repo <url>
git fetch other-repo

# Merge other repository
git merge --allow-unrelated-histories other-repo/main

# Or use subtree
git subtree add --prefix=<directory> <remote> main --squash
```

#### 20.9 Clean Up History

```bash
# Remove sensitive data from history
git filter-branch --force --env-filter '
if [ "$GIT_COMMITTER_EMAIL" = "old@email.com" ]
then
    export GIT_COMMITTER_EMAIL="new@email.com"
    export GIT_AUTHOR_EMAIL="new@email.com"
fi
' --tag-name-filter cat -- --branches --tags

# Remove empty commits
git filter-branch --prune-empty HEAD
```

#### 20.10 Debugging Git Issues

```bash
# Enable verbose output
GIT_TRACE=1 git <command>
GIT_TRACE2=1 git <command>

# Debug HTTP operations
GIT_CURL_VERBOSE=1 git <command>
GIT_TRACE_PACKET=1 git <command>

# Check Git configuration
git config --list --show-origin

# Verify remote URL
git remote -v

# Test connection
git ls-remote origin
```

---

## Quick Reference Cheat Sheet

### Most Common Commands

```bash
# Daily workflow
git status
git add .
git commit -m "message"
git push
git pull

# Branching
git checkout -b feature/new-feature
git branch
git checkout main
git merge feature/new-feature

# Undoing
git reset HEAD <file>
git checkout -- <file>
git revert HEAD

# History
git log --oneline --graph --all
git show <commit>
git diff
```

### DevOps-Specific Commands

```bash
# CI/CD
git tag -a v1.2.0 -m "Release"
git push --tags

# Hooks
chmod +x .git/hooks/pre-commit

# Submodules
git submodule update --init --recursive

# Performance
git clone --depth 1 <repo>
git gc --aggressive

# Security
git commit -S -m "Signed"
git log --show-signature
```

---

## Best Practices Summary

1. **Commit Often**: Small, logical commits
2. **Write Good Messages**: Clear, descriptive commit messages
3. **Use Branches**: Feature branches for all changes
4. **Review Before Merge**: Use Pull Requests
5. **Keep Main Clean**: Only merge tested, reviewed code
6. **Use Tags**: Tag releases and important milestones
7. **Sign Commits**: Use GPG signing for security
8. **Don't Force Push**: Use `--force-with-lease` if needed
9. **Use Hooks**: Automate checks and validations
10. **Regular Maintenance**: Run `git gc` periodically

---

## Conclusion

This comprehensive Git tutorial covers everything from medium-level commands to advanced DevOps practices. Master these concepts and commands to become proficient in Git for both development and DevOps workflows.

**Key Takeaways:**
- Group related commands together for better understanding
- Practice with real projects to reinforce learning
- Use Git hooks and automation for DevOps workflows
- Follow best practices for security and collaboration
- Understand Git internals for advanced troubleshooting

Happy Git-ing! 🚀

