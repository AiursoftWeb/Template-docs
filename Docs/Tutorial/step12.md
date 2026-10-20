# Aiursoft Template Tutorial - Step 12 - Deploy the Application to a Real Server

### 

After deploying with OIDC, users logging in for the first time who are not in the system-created role `Administrators` will have no permissions. We need to assign some permissions to users so they can use the system properly.

Suppose in the target organization, we want all employees to be the highest-level administrators of this system, and employees come from the OIDC `employees` role. We need to grant all permissions of the `employees` role to the `employees` role itself.

In this case, you can use the following SQL statement to accomplish this task:

```sql
-- 步骤 1: 查询名为 'employees' 的角色的 ID，并将其存储在一个变量中
SET @roleId = (SELECT Id FROM AspNetRoles WHERE Name = 'employees');

-- 步骤 2: 为 'employees' 角色插入所有可能的权限
-- 这段代码会从 AspNetRoleClaims 表中复制所有不重复的 ClaimType 和 ClaimValue 组合
-- 并使用 WHERE NOT EXISTS 子句来确保不会重复添加已经存在的权限
INSERT INTO AspNetRoleClaims (RoleId, ClaimType, ClaimValue)
SELECT
    @roleId,
    c.ClaimType,
    c.ClaimValue
FROM
    (SELECT DISTINCT ClaimType, ClaimValue FROM AspNetRoleClaims) AS c
WHERE NOT EXISTS (
    SELECT 1
    FROM AspNetRoleClaims
    WHERE RoleId = @roleId
      AND ClaimType = c.ClaimType
      AND ClaimValue = c.ClaimValue
);
```

After executing the SQL statement above, the `employees` role will have all permissions. This way, all logged-in employees can use all features of the system.

!!! note "Users who are already logged in"

    If a user has already logged in once, they need to log in again to receive the new permissions.

You might also need to delete the `Administrators` role. Of course, before deleting it, we need to first revoke all its permissions. You can use the following SQL statement to accomplish this task:

```sql
-- 步骤 1: 查询名为 'Administrators' 的角色的 ID，并将其存储在一个变量中
SET @adminRoleId = (SELECT Id FROM AspNetRoles WHERE Name = 'Administrators');

-- 步骤 2: 删除 'Administrators' 角色的所有权限
DELETE FROM AspNetRoleClaims
WHERE RoleId = @adminRoleId;
-- 步骤 3: 删除 'Administrators' 角色本身
DELETE FROM AspNetRoles
WHERE Id = @adminRoleId;
```

After executing the above SQL statement, the `Administrators` role has been removed.

With this, we have completed the task of assigning permissions to the OIDC users, and the specific groups within our organization can now securely begin managing and using this system.
