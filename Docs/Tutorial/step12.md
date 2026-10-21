# Step 12 - Build and Deploy the Application

First verify the application in a persistent local Docker container. Then use the same image and persistent-data layout on the target server. Publishing a new Aiursoft company business additionally follows the company's reviewed Box, identity, employee-permission and business-registration process; this standalone example does not replace it.

## 12.1 Verify the frontend and build the image

From the repository root:

```bash
npm --prefix ./src/MyOrg.MarkToHtml/wwwroot install
npm --prefix ./src/MyOrg.MarkToHtml/wwwroot run build
test -f ./src/MyOrg.MarkToHtml/wwwroot/node_modules/codemirror/lib/codemirror.js
dotnet build ./MyOrg.MarkToHtml.sln
sudo docker build -t myorg/marktohtml:local .
```

The generated Dockerfile has already been renamed by Voyager. Preserve its multi-stage build, frontend pruning, initialization and health check. Building the image requires access to the registries used by that Dockerfile. Review build errors rather than changing application image sources to hide a registry problem.

## 12.2 Start with persistent SQLite and file storage

Create a dedicated data volume. It holds the SQLite database, file storage, application settings and data-protection keys used by the generated image:

```bash
sudo docker volume create marktohtml-data
sudo docker run -d --name marktohtml \
  -p 127.0.0.1:5000:5000 \
  -v marktohtml-data:/data \
  myorg/marktohtml:local
```

Keep the binding on loopback until the initial administrator account and external identity configuration are ready. Visit `http://localhost:5000`, sign in with the development administrator, and change its default password through account management before exposing a local-login deployment. Create and edit a note, upload an image, and verify `/health` returns `Healthy`.

```bash
curl --fail http://localhost:5000/health
sudo docker inspect --format '{{.State.Health.Status}}' marktohtml
sudo docker restart marktohtml
```

After restart, sign in again and confirm the note and uploaded image remain available. Inspect application logs for startup or migration failures; a running container alone is insufficient.

To replace the container with a rebuilt image, stop and remove only the container, then repeat `docker run` with the same volume. Do not remove the data volume:

```bash
sudo docker stop marktohtml
sudo docker rm marktohtml
# Rebuild the image and repeat the docker run command above.
```

Back up the persistent data before changing application versions or database providers. With SQLite, use a consistent SQLite backup or stop the application while copying its data; do not copy only a live database file while ignoring its journal. For MySQL, use a separate database volume and database backup in addition to this application's files and keys. Never point a new provider at an unrelated existing database.

## 12.3 Configure the public entry point and OIDC

Put the container behind the target server's existing HTTPS reverse proxy. Proxy the intended hostname to the application, preserve the normal forwarded headers, and keep the application volume. For a remote server, an SSH tunnel to its loopback port is sufficient for the initial private smoke test. Configure DNS and a valid TLS certificate before enabling an external identity callback.

Register an independent confidential client with your OIDC provider. Use a strict callback such as `https://notes.example.com/signin-oidc`, an appropriate issuer/authority, and the `openid`, `profile` and `email` scopes. Configure the provider to return the username, immutable subject, display name, email and groups expected by the application. Restrict login admission at the identity provider if this is an internal business.

Keep endpoint and feature choices in reviewed deployment configuration. Store the client secret in the server's protected secret configuration, not Git. For a standalone Docker deployment, a mode-0600 private env file can contain `AppSettings__OIDC__ClientId` and `AppSettings__OIDC__ClientSecret`. Replace the example public values below and recreate the container with its existing data volume:

```bash
sudo docker run -d --name marktohtml \
  -p 127.0.0.1:5000:5000 \
  -v marktohtml-data:/data \
  --env-file /etc/marktohtml/oidc.env \
  -e AppSettings__AuthProvider=OIDC \
  -e AppSettings__OIDC__Authority=https://identity.example.com/application/o/notes/ \
  -e AppSettings__OIDC__RolePropertyName=groups \
  -e AppSettings__AllowAnonymousUsage=false \
  myorg/marktohtml:local
```

Stop/remove the previous container first, as in 12.2. Set `AllowAnonymousUsage` according to your intended audience; OIDC login does not by itself make anonymous note conversion private. The template defaults use `preferred_username`, `sub`, `name` and `email` for the other claims; override their OIDC configuration properties if your provider uses different names. No client credential is supplied by this documentation.

Verify a real login, callback and group synchronization. A 302 to the provider proves only that authentication started. Signing into the application does not automatically grant background-job, settings or document-administration permissions.

## 12.4 Assign business permissions

Choose the actual management group, such as `leadership`, and grant only the intended capabilities through the application's role-management pages while an authorized administrator still has access. The group role normally appears after an admitted member first signs in. Confirm the role exists before granting anything. Ordinary users can save and manage their own notes without document-administration permissions.

For an explicitly authorized MySQL administration procedure, the following copies existing Permission claims to an already-created management role. It deliberately stops before COMMIT so you can inspect the role ID and counts. If the role lookup is NULL or the result is wrong, issue ROLLBACK; never delete the existing administrator first.

```sql
START TRANSACTION;
SET @roleId = (SELECT Id FROM AspNetRoles WHERE NormalizedName = 'LEADERSHIP');
SELECT @roleId AS ManagementRoleId;

INSERT INTO AspNetRoleClaims (RoleId, ClaimType, ClaimValue)
SELECT @roleId, 'Permission', c.ClaimValue
FROM (SELECT DISTINCT ClaimValue FROM AspNetRoleClaims WHERE ClaimType = 'Permission') c
WHERE @roleId IS NOT NULL AND NOT EXISTS (
    SELECT 1 FROM AspNetRoleClaims existing
    WHERE existing.RoleId = @roleId
      AND existing.ClaimType = 'Permission'
      AND existing.ClaimValue = c.ClaimValue
);
SELECT COUNT(*) AS GrantedPermissions
FROM AspNetRoleClaims WHERE RoleId = @roleId AND ClaimType = 'Permission';
-- COMMIT only after verifying the intended role and permission set; otherwise ROLLBACK.
```

This is MySQL-specific, not a command for the SQLite example. Prefer the normal management UI; direct database writes require authorization, a backup, and awareness of application caches. Retaining an existing administrator until the replacement role is proven prevents lockout. Already signed-in users must sign out and back in to refresh their permission claims. Do not delete roles or accounts as an automatic part of deploying an app.

## 12.5 Final checks

Verify anonymous behavior matches the chosen setting; ordinary users cannot edit another user's notes or use document-administration actions; the intended management group can perform its assigned actions; upload and recycle-bin flows work; and stored notes/images survive container replacement. Check background jobs and logs, then establish the normal backup and availability checks for the deployment. For company hosting, complete the existing business-registration and employee-trial steps before inviting use.

Continue with the optional [after-class exercises](./step13.md).
