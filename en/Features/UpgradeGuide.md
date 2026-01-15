# Upgrade Template

## Step 1 Prepare Before Upgrade

* Ensure the current repository is up to date by running `git pull`.
* Ensure the build passes and all unit tests pass.
* Ensure `./lint.sh` passes.
* Ensure there are no uncommitted changes on the current branch.
* Backup the current codebase in case anything goes wrong.
* Ensure you have installed the latest version of the Voyager tool.

Next, perform some pre-upgrade preparations. First, open Jetbrains Rider, and ensure all C# classes are in separate files (i.e., each class is defined in its own file), with no multiple class definitions in a single file. If there are any, split them into individual files.

## Step 2 Execute Upgrade

Run the following script:

```bash
#!/bin/bash

# ==========================================
# Aiursoft Template Upgrade Script (Final v2)
# ==========================================

# 遇到错误立即停止
set -e

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ================= 配置区 =================
TEMP_BRANCH_NAME="template-upgrade-layer"
TEMPLATE_NAME="web-app-all-in-one" 
# =========================================

# 1. 环境检查
SLN_FILE=$(find . -maxdepth 1 -name "*.sln" | head -n 1)

if [ -z "$SLN_FILE" ]; then
    echo -e "${RED}Error: No .sln file found in current directory.${NC}"
    exit 1
fi

PROJECT_NAME=$(basename "$SLN_FILE" .sln)
CURRENT_BRANCH=$(git branch --show-current)
CURRENT_DIR=$(pwd)

echo -e "${GREEN}Project:${NC} $PROJECT_NAME"
echo -e "${GREEN}Current Branch:${NC} $CURRENT_BRANCH"

# 检查是否有未提交的更改
if [ -n "$(git status --porcelain)" ]; then 
    echo -e "${RED}Error: You have uncommitted changes.${NC}"
    echo "Please commit or stash your changes before running the merge."
    exit 1
fi

echo -e "${BLUE}=== Step 1: Preparing Orphan Branch ===${NC}"

if git show-ref --verify --quiet "refs/heads/$TEMP_BRANCH_NAME"; then
    git branch -D "$TEMP_BRANCH_NAME"
fi

git checkout --orphan "$TEMP_BRANCH_NAME"
git rm -rf . > /dev/null 2>&1
git clean -fdx > /dev/null 2>&1

echo -e "${BLUE}=== Step 2: Generating Fresh Template in Temp Dir ===${NC}"
GEN_DIR=$(mktemp -d)
pushd "$GEN_DIR" > /dev/null

echo "Generating template '$TEMPLATE_NAME'..."
voyager new -t "$TEMPLATE_NAME" -n "$PROJECT_NAME"

popd > /dev/null

echo -e "${BLUE}=== Step 3: Moving Template Files Back ===${NC}"

if [ -d "$GEN_DIR/.git" ]; then
    rm -rf "$GEN_DIR/.git"
fi

cp -r "$GEN_DIR/." "$CURRENT_DIR/"
rm -rf "$GEN_DIR"

echo -e "${BLUE}=== Step 4: Cleaning Template Noise ===${NC}"

# 4.1 删除模版自带的 Migrations
find . -type d -name "Migrations" -exec rm -rf {} +
echo -e "${YELLOW}Removed template migrations.${NC}"

# 4.2 删除 bin/obj
find . -type d -name "bin" -exec rm -rf {} +
find . -type d -name "obj" -exec rm -rf {} +

# [新增] 4.3 彻底删除模版里的所有 .resx 文件
# 这样合并时，模版侧没有任何资源文件，Git 会完全保留你当前的资源文件，
# 且不会引入任何新的资源文件。
find . -type f -name "*.resx" -exec rm -f {} +
find . -type f -name "*.csproj" -exec rm -f {} +
find . -type f -name "*.png" -exec rm -f {} +
find . -type f -name "*.svg" -exec rm -f {} +
echo -e "${YELLOW}Removed all template .resx files (Keeping yours strictly).${NC}"

echo -e "${BLUE}=== Step 5: Committing Template State ===${NC}"
git add .
git commit -m "chore: generated latest template code for $PROJECT_NAME" --quiet

echo -e "${BLUE}=== Step 6: Merging into $CURRENT_BRANCH ===${NC}"
git checkout "$CURRENT_BRANCH"

# 允许不相关的历史合并
set +e
git merge "$TEMP_BRANCH_NAME" --allow-unrelated-histories --no-commit
MERGE_EXIT_CODE=$?
set -e

# 清理临时分支
git branch -D "$TEMP_BRANCH_NAME" > /dev/null

echo -e "------------------------------------------------"
if [ $MERGE_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}Success! Auto-merged without conflicts.${NC}"
    echo "Check the changes and run 'git commit'."
else
    echo -e "${YELLOW}Merge Conflict Detected! (Expected behavior)${NC}"
    echo -e "This is good. It means git preserved your custom logic while trying to bring in updates."
    echo -e "1. Open your IDE."
    echo -e "2. Look for files with ${RED}red conflict markers${NC}."
    echo -e "3. Note: All .resx files conflicts are gone (we ignored template resx)."
    echo -e "4. Resolve conflicts (Startup.cs, .csproj, etc)."
    echo -e "5. Run 'git add .' and 'git commit'."
fi
```

## Step 3 Resolve Merge Conflicts

You are expected to encounter a large number of conflicts that need to be resolved manually, especially files like `Startup.cs` and `.csproj`. Please follow these steps:

* Open your IDE (recommended: Visual Studio or Jetbrains Rider).
* Locate all files marked as conflicts (usually indicated with red markers).
* Resolve conflicts file by file, ensuring you preserve your own business logic while incorporating improvements from the template.
* Note: All conflicts in `.resx` files have been ignored, as we have removed all resource files from the template, ensuring your resource files will not be overwritten.
* After resolving all conflicts, run `git add .` followed by `git commit` to complete the merge.

## Step 4 Verify Upgrade Results

* Compile the project to ensure there are no compilation errors.

Next, you will likely need to recreate Migrations for the new project. Open the terminal, navigate to the `Sqlite` and `MySQL` project directories, and create new initial migration files according to the README in each directory.

Then continue:

* Run all unit tests to ensure no tests fail.
* Run `./lint.sh` to ensure code style checks pass.
* Manually test key functionalities to ensure everything runs correctly.
* Finally, commit your changes to the version control system.

Congratulations! You have successfully upgraded the project to the latest template version! Happy coding! 🚀
