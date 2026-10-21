# Step 12 - Run Your App in Docker

**Our goal:** package the app, start a private local container, and prove that its notes survive replacement.

We will do the local checks first.
A public server and external sign-in are a separate, optional part at the end.

Stop the development server with **Ctrl+C**.
Docker will use the same port, so do not leave both running.

```bash
cd ~/Source/MyOrg.MarkToHtml
```

This returns to the repository root, where Dockerfile lives.

## 12.1 Check the three base-image addresses

Open the generated Dockerfile in your editor.
Voyager may have replaced the infrastructure registry name with your organization name.
Our project is MyOrg.MarkToHtml, but these existing infrastructure images still belong to Aiursoft.

Find the **three existing FROM lines**.
Make their image addresses match these lines:

```dockerfile
FROM --platform=$BUILDPLATFORM hub.aiursoft.com/node:24-alpine AS npm-env
FROM --platform=$BUILDPLATFORM hub.aiursoft.com/aiursoft/internalimages/dotnet AS build-env
FROM hub.aiursoft.com/aiursoft/internalimages/dotnetonlyruntime
```

The first stage prepares browser libraries.
The second compiles the .NET application.
The third runs the published result.

These lines are not a whole Dockerfile to paste over the original.
Keep the commands between them.
Keep CSPROJ_PATH and PROJ_NAME pointing at **MyOrg.MarkToHtml**.

If you see `hub.myOrg.com/myOrg/...`, correct those image addresses before building.
An `invalid reference format` error here is not a C# error.

## 12.2 Check the application before packaging

```bash
npm --prefix ./src/MyOrg.MarkToHtml/wwwroot install
```

This installs frontend dependencies in the named folder without changing the terminal's current folder.
`--prefix` tells npm where to find package.json.

```bash
npm --prefix ./src/MyOrg.MarkToHtml/wwwroot run build
```

This runs the same frontend build used in the image.
**Expected:** successful completion.

```bash
ls ./src/MyOrg.MarkToHtml/wwwroot/node_modules/codemirror/lib/codemirror.js
```

This checks that CodeMirror survived pruning.
**Expected:** the file's path. If it is missing, revisit the keep object in Step 2.

```bash
dotnet build ./MyOrg.MarkToHtml.sln
```

This compiles the application. **Expected:** no build errors.

```bash
Storage__Path="$PWD/.tutorial-test-data" dotnet test ./MyOrg.MarkToHtml.sln
```

This runs the template's existing tests with their own file-storage folder.
The variable assignment applies only to this command; it avoids mixing test files with the notes and pictures you created by hand.
**Expected:** all discovered tests pass.
Do not continue with a failing test; read its failure message first.

## 12.3 Build the image

```bash
sudo docker build -t myorg/marktohtml:local .
```

`build` reads Dockerfile.
`-t` gives the result a name and tag. The final dot selects the current folder as build context.
`sudo` lets this Linux setup talk to the Docker service.

**Expected:** the build finishes and creates `myorg/marktohtml:local`.
The first build downloads dependencies and can take several minutes.

A registry authentication error means the base images are not accessible with your current account.
Use your authorized registry access; do not silently replace the template's build/runtime images.

## Checkpoint 12A - The image exists

```bash
sudo docker image ls myorg/marktohtml
```

This lists the image we just built.
**Expected:** a row with repository `myorg/marktohtml` and tag `local`.

An image is the packaged application. A container is a running instance of it.
Next we will create that instance.

## 12.4 Create a persistent data volume

```bash
sudo docker volume create marktohtml-data
```

This creates a Docker-managed folder for our data.
**Expected:** `marktohtml-data`.

The template image uses `/data` for its SQLite database, uploads, settings, and protection keys.
We will attach the same volume whenever we replace the container.

```bash
sudo docker run -d --name marktohtml \
  -p 127.0.0.1:5000:5000 \
  -v marktohtml-data:/data \
  myorg/marktohtml:local
```

Copy this whole block as **one command**.
A backslash joins the next line; do not put spaces after it.

- `-d` starts the container in the background.
- `--name marktohtml` gives it a name we can use in later commands.
- `-p 127.0.0.1:5000:5000` connects local port 5000 to container port 5000.
- `127.0.0.1` keeps this experiment reachable only from this machine.
- `-v marktohtml-data:/data` attaches our persistent volume to the image's data folder.
- The final line chooses the image we built.

**Expected:** Docker prints a container ID.
The app may need a few seconds to start and apply migrations.

Open `http://localhost:5000` in the browser.
This is a **fresh database** in the volume; it does not automatically contain the notes from development.
Sign in with the initial administrator account.

Open **Personal / Change Password** and change the development password.
Do this while the app is still private.

## Checkpoint 12B - Health and real data both work

Create a note containing `My Docker note`.
Upload a picture, paste its Markdown into that note, and save again.
Reopen the note and confirm the picture loads.

Now check the health endpoint:

```bash
curl --fail http://localhost:5000/health
```

This asks the application whether it is healthy.
`--fail` makes an HTTP error fail the command.
**Expected:** `Healthy`.

```bash
sudo docker inspect --format '{{.State.Health.Status}}' marktohtml
```

This reads Docker's periodic health-check result.
**Expected:** eventually `healthy`. `starting` means the first checks are still in progress.

If the page or health check fails, look at this container's logs:

```bash
sudo docker logs --tail 50 marktohtml
```

This prints its latest 50 log lines.
Look for startup, migration, or database-connection errors.
A container being listed as running does not prove the app works.

## Checkpoint 12C - A restart keeps your note

```bash
sudo docker restart marktohtml
```

This stops and starts the same container.
Wait for the app to become healthy again.

Sign in with your **changed** password.
Open My Documents, then the Docker note.
**Expected:** both the note and its picture are still available.

## Checkpoint 12D - A replacement keeps your note too

Let's replace the container while keeping its data volume.

```bash
sudo docker stop marktohtml
```

This stops only our application container.

```bash
sudo docker rm marktohtml
```

This removes that container. It does **not** remove the named volume.
Do not run `docker volume rm marktohtml-data` if you want to keep the notes.

Run the same `docker run` command from 12.4 again, with the same volume name.
Wait for health, sign in, and reopen the note.

**Expected:** the changed password, note, and picture all survive.
That is our local deployment checkpoint. Well done.

When trying a new application image later, back up the data first.

For SQLite, use a consistent SQLite backup or stop the app while copying its database and journal files.

For MySQL, back up that database separately as well as the app's uploaded files and keys.

## 12.5 Optional - Plan the public server and external sign-in

You can stop at the local Docker checkpoint if you do not have a server or identity-provider access yet.
Do not copy placeholder hostnames into a real deployment.

Before continuing, you need:

- A server and hostname you are authorized to use.
- DNS, a valid HTTPS certificate, and the server's normal reverse proxy.
- Access to register an OIDC client and configure its allowed users/groups.
- The intended management group and an account authorized to grant its permissions.

For Aiursoft company hosting, follow the reviewed Box and business-onboarding process.
A standalone `docker run` command does not register a company business or finish employee access setup.

### Prepare the identity-provider client

Register a confidential client for this application.
Use a strict callback such as `https://notes.example.com/signin-oidc`.
Replace that hostname with your actual approved hostname.

Request `openid`, `profile`, and `email` scopes.
Configure the provider to return the username, immutable subject, display name, email, and groups.
Restrict who may sign in at the provider if this is an internal app.

### Prepare permissions before switching login providers

Use the role editor from Step 6 to create or select the actual management group, for example `leadership`.

Grant only its intended capabilities while you still have authorized management access.

Do not remove the working administrator first.

Ordinary users can manage their own notes without document-administration permissions.
External login admission and application permission grants are separate decisions.

### Keep only the secret in the private file

On the server, use an editor to create `/etc/marktohtml/oidc.env` outside the repository.
Its content is one line, with your actual client secret:

```text
AppSettings__OIDC__ClientSecret=replace-with-your-real-client-secret
```

Protect this file so only the account administering deployment can read it.
For this root-administered Docker example, use owner root and mode 0600.
Do not commit it, print it, or paste it into this tutorial.

Declare the public client ID, authority, group claim, and feature choices in reviewed deployment configuration.
They are not secrets.

### Recreate the container with the intended configuration

Stop/remove the previous container as in 12D.
Keep the same persistent volume.
After replacing **every** example public value, the equivalent standalone command is:

```bash
sudo docker run -d --name marktohtml \
  -p 127.0.0.1:5000:5000 \
  -v marktohtml-data:/data \
  --env-file /etc/marktohtml/oidc.env \
  -e AppSettings__AuthProvider=OIDC \
  -e AppSettings__OIDC__ClientId=notes-client \
  -e AppSettings__OIDC__Authority=https://identity.example.com/application/o/notes/ \
  -e AppSettings__OIDC__RolePropertyName=groups \
  -e AppSettings__AllowAnonymousUsage=false \
  myorg/marktohtml:local
```

The first three options are the same container name, private port, and volume from the local example.
`--env-file` reads the private client secret.

Each `-e` sets one application setting:

- AuthProvider selects external OIDC login.
- ClientId identifies the client you registered.
- Authority is that client's actual identity-provider issuer/authority.
- RolePropertyName names the groups claim the provider returns.
- AllowAnonymousUsage=false requires login before conversion as well as before saving notes.

Other identity claims default to `preferred_username`, `sub`, `name`, and `email`.
Override them only if your provider uses different names.
Put this configuration in the target deployment's normal reviewed format, such as Compose.

## Checkpoint 12E - Public access is a real login test

This checkpoint needs your actual server and identity provider; a local image build cannot prove it.

- Complete a real login and callback. A redirect to the identity provider alone is not enough.
- Confirm an admitted ordinary user can save their own note and cannot use management actions.
- Confirm the intended management group has its assigned capabilities.
- Sign out and in after permission changes, so the cookie gets fresh claims.
- Check the intended anonymous-access behavior.
- Check uploads, the recycle bin, health, logs, backups, and persistent data on the target server.
- Complete the company's registration and employee-trial steps when this is company hosting.

You now know what to verify locally and what still needs a real deployment environment.
The [after-class exercises](./step13.md) are optional. Pick one when you feel ready.
