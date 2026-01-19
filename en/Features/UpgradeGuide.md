# Upgrade Template

## Step 1 Prepare Before Upgrade

* Make sure the current repository is up to date by running `git pull`.
* Make sure the build passes and all unit tests pass.
* Make sure `./lint.sh` passes.
* Make sure there are no uncommitted changes on the current branch.
* Backup the current codebase in case anything goes wrong.
* Make sure you have installed the latest version of the Voyager tool.

Next, perform some pre-upgrade preparations. First, open Jetbrains Rider and ensure all C# classes are in separate files (i.e., each class is defined in its own file), not multiple classes defined in the same file. If any are found, split them into individual files.

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

# 4.3 删除 所有几乎所有项目都已经被重命名或删除的文件
find . -type f -name "HomeController.cs" -exec rm -f {} +
find . -type f -name "DashboardController.cs" -exec rm -f {} +
find . -type f -name "ViewModelArgsInjector.cs" -exec rm -f {} +
find . -type f -name "README.md" -exec rm -f {} +

# [新增] 4.3 彻底删除模版里的所有 .resx 文件
# 这样合并时，模版侧没有任何资源文件，Git 会完全保留你当前的资源文件，
# 且不会引入任何新的资源文件。
find . -type f -name "*.resx" -exec rm -f {} +
find . -type f -name "*.csproj" -exec rm -f {} +
find . -type f -name "*.png" -exec rm -f {} +
find . -type f -name "*.svg" -exec rm -f {} +
find . -type f -name "package-lock.json" -exec rm -f {} +
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

Expect a large number of conflicts that need to be resolved manually, especially files like `Startup.cs` and `.csproj`. Follow these steps:

* Open your IDE (recommended: Visual Studio or JetBrains Rider).
* Locate all files marked as conflicting (usually indicated by red markers).
* Resolve conflicts file by file, ensuring you preserve your own business logic while incorporating improvements from the template.
* Note: All conflicts in `.resx` files have been ignored, as we removed all resource files from the template to ensure your resource files are not overwritten.
* After resolving all conflicts, run `git add .` followed by `git commit` to complete the merge.

If you're using tools like Antigravity or Cursor, you can do the following:

* Open Antigravity or Cursor.
* Navigate to the conflicting files.
* Use the following prompt:

```markdown
**Role & Objective:**
You are acting as a senior software architect. You are tasked with resolving merge conflicts for a project originally generated via the **Aiursoft Template**.

**Context:**

* **Origin:** This project was scaffolded using the Aiursoft Template long ago.
* **Evolution:** Since then, extensive custom business logic has been developed, causing the codebase to diverge significantly from the original template.
* **Current Goal:** We are upgrading the project to the latest version of the template to leverage new features and improvements.
* **The Conflict:** The template provides core infrastructure (file upload, image compression, multi-DB support, auth, permissions, background tasks, etc.). However, simply overwriting the current project with the new template is impossible as it would destroy our proprietary business logic. We have regenerated the project using the new template and attempted a merge, resulting in numerous conflicts.

**Conflict Resolution Guidelines:**

**1. Infrastructure vs. Business Logic**

* **Template Infrastructure (High Priority):** If a conflict involves an infrastructure-level improvement provided by the new template, **prioritize the template's code**.
* *Note:* Be mindful that the template might alter UI elements (e.g., Homepage, Dashboard) that the project may not utilize or has customized.


* **Custom Infrastructure (Top Priority):** If the current project includes infrastructure changes made specifically to serve unique business needs (e.g., extra build steps, specific middleware configurations, additional User Management APIs), **prioritize the current project's code**.

**2. Stability & Safety (Critical)**

* **Highest Priority:** The absolute priority is to avoid breaking the project.
* **Unknown Logic:** If you encounter logic you do not fully understand, prioritize retaining the code that ensures the project remains operational.
* **Do Not Delete:** Do not blindly delete or discard code that clearly affects functionality.

**3. Handling Business Logic**

* **Unique Assets:** Pages, copy/text, tests, unique permissions, and database entities that are specific to the current project must be preserved. Do not treat these as "template files to be overwritten/deleted."
* **Additive Changes:** If both the current project and the new template attempt to add items to the same system (e.g., the permissions list), **retain ALL items**. Ensure that both the template's new logic and the project's existing logic can coexist and function.

**4. Class Merging Strategy**

* **Identical Content:** If a class exists in both and the content is identical, default to the **template's version**.
* **Divergent Content:** If the content differs, perform a **manual merge**. You must retain the current project's business logic while absorbing the template's technical improvements.

**Definition of Done:**

1. The project must compile successfully.
2. All unit tests must pass.
3. The `./lint.sh` script must run without errors.
4. Key functionalities must be manually verified to ensure everything runs normally.
```

## Step 4 Verify Upgrade Results

* Build the project to ensure there are no compilation errors.

Next, you will likely need to recreate Migrations for the new project. Open the terminal, navigate to the `Sqlite` and `MySQL` project directories, and create new initial migration files respectively according to the README files in each directory.

Then continue:

* Run all unit tests to ensure no tests fail.
* Run `./lint.sh` to ensure code style checks pass.
* Manually test key features to ensure everything runs properly.
* Finally, commit your changes to the version control system.

That's it! You have successfully upgraded the project to the latest template version! Happy coding! 🚀
